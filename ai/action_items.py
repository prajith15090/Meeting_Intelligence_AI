import google.generativeai as genai
from config import GEMINI_API_KEY

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def extract_action_items(transcript: str) -> str:
    """
    Extracts action items from the meeting transcript using Gemini.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is missing."
        
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        prompt = f"""
        Extract a list of actionable items from the following meeting transcript.
        Format them as a clear, bulleted list. Identify who is responsible if mentioned.
        
        Transcript:
        {transcript}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Action item extraction error: {e}")
        return f"Error extracting action items: {e}"
