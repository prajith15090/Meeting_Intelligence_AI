import os
import uuid
import tempfile
import streamlit as st

def save_uploaded_file(uploaded_file) -> str:
    """
    Saves an uploaded file to a temporary directory and returns the path.
    """
    try:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{uploaded_file.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return ""

def cleanup_file(file_path: str):
    """
    Removes the temporary file.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error cleaning up file: {e}")
