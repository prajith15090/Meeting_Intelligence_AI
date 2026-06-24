import google.generativeai as genai
from config import GEMINI_API_KEY, USER_NAME, COMPANY_NAME
import json
import time

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def analyze_meeting(transcript: str, customer_name: str, meeting_date: str) -> dict:
    """
    Sends the transcript to Gemini API and generates all required intelligence in a single JSON call.
    Handles temporary 429 rate limit errors with automatic exponential backoff retry.
    """
    if not GEMINI_API_KEY:
        return {"error": "GEMINI_API_KEY is missing."}
        
    max_retries = 4
    base_delay = 5  # seconds
    
    prompt = f"""
    You are a highly advanced Sales Meeting Intelligence Agent.
    Analyze the following meeting transcript and generate a comprehensive intelligence report.
    
    Meeting Details:
    - Customer Name: {customer_name}
    - Meeting Date: {meeting_date}

    Respond ONLY with a valid JSON object matching the following structure exactly. Do not include markdown formatting or backticks around the JSON.
    {{
        "summary": "Detailed summary including Executive Summary, Discussion Points, and Key Decisions",
        "mom": "Minutes of Meeting including Meeting Title, Date and Time, Participants, Agenda, Discussion Summary, Decisions Taken, Action Items, Owners, Due Dates, Next Meeting Date",
        "customer_insights": "Customer insights including Customer Pain Points, Requirements, Risks, and Opportunities",
        "sentiment": "Positive, Neutral, or Negative (just the word)",
        "deal_stage": "The current deal stage based on the conversation (e.g., Discovery, Proposal, Negotiation, Closed Won, Closed Lost)",
        "probability": "Closing probability percentage (e.g., '75%')",
        "action_items": [
            {{
                "task": "Description of the task",
                "owner": "Name of the person responsible",
                "due_date": "Deadline or timeframe if mentioned, else 'TBD'"
            }}
        ],
        "email_draft": "A professional follow-up email draft based on the discussion. Sign off the email using the following name and company: Best regards, {USER_NAME}, {COMPANY_NAME}."
    }}

    Transcript:
    {transcript}
    """
    
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # We request JSON response to ensure structured output
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                ),
            )
            
            try:
                result = json.loads(response.text)
                return result
            except json.JSONDecodeError as e:
                print(f"JSON Parse Error: {e}")
                return {"error": "Failed to parse JSON response from Gemini."}
                
        except Exception as e:
            error_str = str(e)
            print(f"Meeting analysis attempt {attempt + 1} failed: {error_str}")
            
            # Detect 429 rate limit or quota exceeded errors
            is_rate_limit = any(keyword in error_str.lower() for keyword in ["429", "quota", "exhausted", "rate limit", "rate_limit"])
            
            if is_rate_limit and attempt < max_retries - 1:
                # Exponential backoff: 5s, 10s, 20s
                delay = base_delay * (2 ** attempt)
                print(f"Rate limit / Quota exceeded. Waiting {delay} seconds before retrying...")
                time.sleep(delay)
                continue
            else:
                return {"error": f"Gemini API Error: {error_str}"}
