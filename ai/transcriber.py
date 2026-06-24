import whisper
import os

# Ensure ffmpeg is in PATH for this process
ffmpeg_path = r"C:\Users\WELCOME\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes the given audio file using Whisper.
    Uses the 'base' model to balance speed and accuracy.
    """
    try:
        print("Loading Whisper model...")
        model = whisper.load_model("small")
        print("Transcribing...")
        result = model.transcribe(audio_path, task="translate")
        return result["text"]
    except Exception as e:
        print(f"Transcription error: {e}")
        return f"Error during transcription: {e}"
