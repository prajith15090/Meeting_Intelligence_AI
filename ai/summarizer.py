import google.generativeai as genai
from config import GEMINI_API_KEY

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_summary(transcript: str) -> str:
    """
    Generates a concise summary of the meeting transcript using Gemini.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is missing."
        
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        prompt = f"""
        Please provide a comprehensive but concise summary of the following meeting transcript.
        Highlight the main topics discussed, key decisions made, and overall flow.
        
        Transcript:
        {transcript}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Summarization error: {e}")
        return f"Error during summarization: {e}"
