import streamlit as st
import pandas as pd
from database.db import SessionLocal
from database.models import Meeting, ActionItem, FollowUp
from utils.pdf_generator import create_pdf_report
from utils.docx_generator import create_docx_report
import os
import tempfile
from components.ui import setup_ui

st.set_page_config(page_title="History", page_icon="🕒", layout="wide")
setup_ui()
st.title("Meeting History 🕒")

def get_meetings():
    db = SessionLocal()
    try:
        meetings = db.query(Meeting).order_by(Meeting.meeting_date.desc()).all()
        return meetings
    finally:
        db.close()

meetings = get_meetings()

if not meetings:
    st.info("No meetings found in the database. Process a meeting in the Dashboard first.")
else:
    df = pd.DataFrame([{
        "ID": m.id,
        "Customer": m.customer_name,
        "Date": m.meeting_date.strftime("%Y-%m-%d"),
        "Deal Stage": m.deal_stage,
        "Sentiment": m.sentiment[:50] + "..." if m.sentiment else ""
    } for m in meetings])
    
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    st.subheader("Meeting Details")
    selected_id = st.selectbox("Select a meeting ID to view details", options=[m.id for m in meetings])
    selected_meeting = next((m for m in meetings if m.id == selected_id), None)
    
    if selected_meeting:
        st.write(f"### {selected_meeting.customer_name} ({selected_meeting.meeting_date.strftime('%Y-%m-%d')})")
        
        db = SessionLocal()
        action_items = db.query(ActionItem).filter(ActionItem.meeting_id == selected_meeting.id).all()
        followups = db.query(FollowUp).filter(FollowUp.meeting_id == selected_meeting.id).all()
        db.close()
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["MoM & Summary", "Insights & Deal", "Action Items", "Transcript", "Follow-up Emails"])
        
        with tab1:
            st.subheader("Minutes of Meeting")
            st.markdown(selected_meeting.mom or "N/A")
            st.divider()
            st.subheader("Executive Summary")
            st.markdown(selected_meeting.summary or "N/A")
            
        with tab2:
            st.subheader("Customer Insights")
            st.markdown(selected_meeting.customer_insights or "N/A")
            st.divider()
            st.write(f"**Deal Stage:** {selected_meeting.deal_stage or 'N/A'}")
            st.write(f"**Probability:** {selected_meeting.probability or 'N/A'}")
            st.write(f"**Sentiment:** {selected_meeting.sentiment or 'N/A'}")
            
        with tab3:
            if action_items:
                for idx, item in enumerate(action_items):
                    st.write(f"{idx+1}. **{item.task}** - Owner: {item.owner} - Due: {item.due_date} ({item.status})")
            else:
                st.write("No action items.")
                
        with tab4:
            st.text_area("Full Transcript", selected_meeting.transcript, height=300)
            
        with tab5:
            if followups:
                for fu in followups:
                    st.write(f"**Subject:** {fu.email_subject}")
                    st.write(f"**Sent:** {fu.sent}")
                    st.text_area("Body", fu.email_body, height=150, key=f"email_{fu.id}")
            else:
                st.write("No follow-ups recorded.")
                
        st.divider()
        
        # Prepare data for report generation
        report_data = {
            "customer_name": selected_meeting.customer_name,
            "meeting_date": selected_meeting.meeting_date.strftime('%Y-%m-%d'),
            "summary": selected_meeting.summary,
            "mom": selected_meeting.mom,
            "customer_insights": selected_meeting.customer_insights,
            "sentiment": selected_meeting.sentiment,
            "deal_stage": selected_meeting.deal_stage,
            "probability": selected_meeting.probability,
            "action_items": [{"task": ai.task, "owner": ai.owner, "due_date": ai.due_date} for ai in action_items]
        }
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate PDF Report"):
                temp_dir = tempfile.gettempdir()
                pdf_path = os.path.join(temp_dir, f"report_{selected_meeting.id}.pdf")
                try:
                    create_pdf_report(report_data, pdf_path)
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download PDF",
                            data=f,
                            file_name=f"Meeting_Report_{selected_meeting.customer_name.replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"Error generating PDF: {e}")
                    
        with col2:
            if st.button("Generate DOCX Report"):
                temp_dir = tempfile.gettempdir()
                docx_path = os.path.join(temp_dir, f"report_{selected_meeting.id}.docx")
                try:
                    create_docx_report(report_data, docx_path)
                    with open(docx_path, "rb") as f:
                        st.download_button(
                            label="Download DOCX",
                            data=f,
                            file_name=f"Meeting_Report_{selected_meeting.customer_name.replace(' ', '_')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                except Exception as e:
                    st.error(f"Error generating DOCX: {e}")
