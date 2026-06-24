import streamlit as st
import os
from utils.helper import save_uploaded_file, cleanup_file
from ai.input_processor import process_file_to_transcript
from ai.meeting_agent import analyze_meeting
from ai.transcriber import transcribe_audio
from ai.email_generator import send_email
from database.db import SessionLocal
from database.models import Meeting, ActionItem, FollowUp
from datetime import datetime
from components.ui import setup_ui

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
setup_ui()
st.title("Meeting Dashboard 📊")

# --- KPIs ---
db = SessionLocal()
total_meetings = db.query(Meeting).count()
pending_tasks = db.query(ActionItem).filter(ActionItem.status == 'Pending').count()
positive_meetings = db.query(Meeting).filter(Meeting.sentiment.ilike('%positive%')).count()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Meetings", total_meetings)
col2.metric("Pending Action Items", pending_tasks)
col3.metric("Positive Meetings", positive_meetings)
col4.metric("Deal Stages Tracked", total_meetings)
db.close()

st.divider()

# --- Upload Section ---
with st.sidebar:
    st.header("Upload Meeting")
    customer_name = st.text_input("Customer Name", value="Acme Corp")
    meeting_date_input = st.date_input("Meeting Date", datetime.today())
    uploaded_file = st.file_uploader(
        "Upload recording or transcript", 
        type=['mp4', 'mov', 'mkv', 'mp3', 'wav', 'm4a', 'txt', 'docx']
    )

if uploaded_file is not None:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    
    if file_ext in ['mp3', 'wav', 'm4a']:
        st.audio(uploaded_file)
    elif file_ext in ['mp4', 'mov', 'mkv']:
        st.video(uploaded_file)
        
    if st.button("Process Meeting"):
        with st.spinner("Processing... This may take a few minutes."):
            file_path = save_uploaded_file(uploaded_file)
            
            if file_path:
                try:
                    st.info("Step 1/2: Extracting and Transcribing...")
                    transcript = process_file_to_transcript(file_path, file_ext, transcribe_audio)
                    
                    if transcript.startswith("Error"):
                        raise Exception(transcript)
                        
                    st.info("Step 2/2: Generating Meeting Intelligence...")
                    date_str = meeting_date_input.strftime("%Y-%m-%d")
                    intelligence = analyze_meeting(transcript, customer_name, date_str)
                    
                    if "error" in intelligence:
                        raise Exception(intelligence["error"])
                        
                    # Save to DB
                    st.success("Analysis complete! Saving to database...")
                    db = SessionLocal()
                    
                    new_meeting = Meeting(
                        customer_name=customer_name,
                        meeting_date=meeting_date_input,
                        transcript=transcript,
                        summary=intelligence.get("summary"),
                        mom=intelligence.get("mom"),
                        customer_insights=intelligence.get("customer_insights"),
                        sentiment=intelligence.get("sentiment"),
                        deal_stage=intelligence.get("deal_stage"),
                        probability=str(intelligence.get("probability", ""))
                    )
                    db.add(new_meeting)
                    db.commit()
                    db.refresh(new_meeting)
                    
                    # Add Action Items
                    for task in intelligence.get("action_items", []):
                        if isinstance(task, dict):
                            new_item = ActionItem(
                                meeting_id=new_meeting.id,
                                task=task.get("task", ""),
                                owner=task.get("owner", ""),
                                due_date=task.get("due_date", "")
                            )
                        else:
                            new_item = ActionItem(
                                meeting_id=new_meeting.id,
                                task=str(task)
                            )
                        db.add(new_item)
                        
                    # Add FollowUp Email
                    email_draft = intelligence.get("email_draft", "")
                    new_followup = FollowUp(
                        meeting_id=new_meeting.id,
                        email_subject=f"Follow-up: Meeting with {customer_name}",
                        email_body=email_draft
                    )
                    db.add(new_followup)
                    db.commit()
                    db.close()
                    
                    st.success("Saved successfully!")
                    
                    # Display Results
                    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                        "MoM & Summary", "Insights & Deal", "Action Items", "Sentiment", "Transcript", "Follow-up Email"
                    ])
                    
                    with tab1:
                        st.subheader("Minutes of Meeting")
                        st.markdown(intelligence.get("mom", "N/A"))
                        st.divider()
                        st.subheader("Executive Summary")
                        st.markdown(intelligence.get("summary", "N/A"))
                        
                    with tab2:
                        st.subheader("Customer Insights")
                        st.markdown(intelligence.get("customer_insights", "N/A"))
                        st.divider()
                        st.subheader("Deal Intelligence")
                        st.write(f"**Deal Stage:** {intelligence.get('deal_stage', 'N/A')}")
                        st.write(f"**Closing Probability:** {intelligence.get('probability', 'N/A')}")
                        
                    with tab3:
                        st.subheader("Action Items")
                        items = intelligence.get("action_items", [])
                        if items:
                            for idx, item in enumerate(items):
                                if isinstance(item, dict):
                                    st.write(f"{idx+1}. **{item.get('task')}** - Owner: {item.get('owner')} - Due: {item.get('due_date')}")
                                else:
                                    st.write(f"{idx+1}. {item}")
                        else:
                            st.write("No action items detected.")
                            
                    with tab4:
                        st.subheader("Sentiment")
                        st.write(intelligence.get("sentiment", "N/A"))
                        
                    with tab5:
                        st.text_area("Full Transcript", transcript, height=300)
                        
                    with tab6:
                        st.markdown(email_draft)
                        st.divider()
                        st.subheader("Send Follow-up Email")
                        to_email = st.text_input("Recipient Email Address")
                        if st.button("Send Email"):
                            if to_email:
                                success = send_email(to_email, f"Follow-up: Meeting with {customer_name}", email_draft)
                                if success:
                                    db = SessionLocal()
                                    db.query(FollowUp).filter(FollowUp.meeting_id == new_meeting.id).update({"sent": True})
                                    db.commit()
                                    db.close()
                                    st.success("Email sent successfully!")
                                else:
                                    st.error("Failed to send email. Check your SendGrid configuration.")
                            else:
                                st.warning("Please enter a recipient email address.")
                                
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    cleanup_file(file_path)
else:
    st.info("Please upload a file to begin.")
