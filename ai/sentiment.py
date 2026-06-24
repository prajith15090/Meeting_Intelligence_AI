import google.generativeai as genai
from config import GEMINI_API_KEY

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def analyze_sentiment(transcript: str) -> str:
    """
    Analyzes the overall sentiment of the meeting using Gemini.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is missing."
        
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        prompt = f"""
        Analyze the overall sentiment of the following meeting transcript.
        Is it Positive, Negative, or Neutral? Briefly explain why in one or two sentences.
        
        Transcript:
        {transcript}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return f"Error analyzing sentiment: {e}"
