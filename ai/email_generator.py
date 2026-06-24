import google.generativeai as genai
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import GEMINI_API_KEY, SENDGRID_API_KEY, SENDGRID_SENDER_EMAIL

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_email_draft(summary: str, action_items: str) -> str:
    """
    Generates a follow-up email draft using Gemini based on summary and action items.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is missing."
        
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        prompt = f"""
        Draft a professional follow-up email to the meeting participants based on the summary and action items below.
        Keep it concise, polite, and well-structured.
        
        Summary:
        {summary}
        
        Action Items:
        {action_items}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Email generation error: {e}")
        return f"Error generating email: {e}"

def send_email(to_email: str, subject: str, content: str) -> bool:
    """
    Sends an email using SendGrid.
    """
    if not SENDGRID_API_KEY:
        print("Error: SENDGRID_API_KEY is missing.")
        return False
        
    message = Mail(
        from_email=SENDGRID_SENDER_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=content.replace("\n", "<br>")
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent with status code: {response.status_code}")
        return response.status_code in [200, 202]
    except Exception as e:
        print(f"Error sending email via SendGrid: {e}")
        return False
