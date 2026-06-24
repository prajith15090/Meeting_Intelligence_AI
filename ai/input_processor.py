import os
import uuid
import tempfile
import docx
from moviepy import VideoFileClip

def extract_audio_from_video(video_path: str) -> str:
    """
    Extracts audio from a video file and saves it as a .wav file.
    Returns the path to the extracted .wav file.
    """
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}_extracted.wav")
        audio.write_audiofile(audio_path, codec='pcm_s16le', logger=None)
        return audio_path
    except Exception as e:
        return f"Error extracting audio: {str(e)}"

def read_text_file(file_path: str) -> str:
    """Reads a .txt file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading text file: {str(e)}"

def read_docx_file(file_path: str) -> str:
    """Reads a .docx file."""
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f"Error reading docx file: {str(e)}"

def process_file_to_transcript(file_path: str, file_extension: str, transcriber_func) -> str:
    """
    Master function to handle any file type.
    - Video: extracts audio, then transcribes
    - Audio: transcribes directly
    - Text/Docx: reads text directly
    """
    file_extension = file_extension.lower().replace('.', '')
    
    if file_extension in ['mp4', 'mov', 'mkv']:
        audio_path = extract_audio_from_video(file_path)
        if audio_path.startswith("Error"):
            return audio_path
        transcript = transcriber_func(audio_path)
        # Cleanup extracted audio
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
        except:
            pass
        return transcript
        
    elif file_extension in ['mp3', 'wav', 'm4a']:
        return transcriber_func(file_path)
        
    elif file_extension == 'txt':
        return read_text_file(file_path)
        
    elif file_extension == 'docx':
        return read_docx_file(file_path)
        
    else:
        return f"Error: Unsupported file type '{file_extension}'"
