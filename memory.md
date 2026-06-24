# Sales Meeting Intelligence App - Simple Explanation

Welcome to the simple guide for the **Sales Meeting Intelligence** project! This document explains what this project is and how it works in plain, non-technical language.

---

## 🎯 What is this project?

Imagine having a super-smart assistant who sits in on your sales meetings, takes perfect notes, writes a quick summary, creates a to-do list, figures out if the client was happy, and even drafts a follow-up email for you. 

That is exactly what this app does! You just give it an audio recording of your meeting, and it does all the hard work of organizing the information.

---

## 🧩 How does it work? (The Project Pieces)

The project is divided into a few main folders and files. Here is what each part does:

### 1. The Screen You See (`app.py` & the `pages/` folder)
*   **The Main Menu (`app.py`)**: This is the welcome screen of the app. It greets you and shows you where to go.
*   **Dashboard (`pages/dashboard.py`)**: This is where the action happens. You can upload your meeting's audio file here, and the app will start processing it.
*   **History (`pages/history.py`)**: Think of this as your library. You can go here to look back at the notes and summaries from any past meeting.

### 2. The "Brain" of the App (the `ai/` folder)
This folder contains all the smart artificial intelligence (AI) workers. When you upload an audio file, these workers get busy:
*   **Transcriber**: It "listens" to the audio recording and types out every single word that was spoken (like a court reporter).
*   **Summarizer**: It reads the long transcript and writes a short, easy-to-read summary of the whole meeting.
*   **Action Items**: It scans the text to figure out what promises were made or what needs to be done next (e.g., "Send John the pricing sheet by Friday").
*   **Sentiment**: It tries to understand the "mood" of the meeting. Was the client excited? Frustrated? Neutral?
*   **Email Generator**: It takes all the meeting notes and automatically writes a polite follow-up email that you can just copy, paste, and send to the client.

### 3. The Secure Filing Cabinet (the `database/` folder)
After the "Brain" does all its work, the app needs to save that information so it isn't lost. This folder manages the connection to a safe database (like a digital filing cabinet) where all your past meeting notes, summaries, and action items are permanently stored.

### 4. Extra Helpful Tools (the `utils/` folder)
*   **PDF Generator**: If you want to save or share a beautiful, formatted report of the meeting, this tool takes all the text and packages it into a nice PDF document for you to download.
*   **Helper**: A small collection of behind-the-scenes tools that help the app run smoothly.

### 5. The Setup Instructions (`config.py` & `requirements.txt`)
*   **The Keys (`config.py`)**: To use the smart AI and the secure filing cabinet, the app needs special passwords and keys. This file securely holds those keys.
*   **The Shopping List (`requirements.txt`)**: This is a list of all the extra software building blocks the app needs to work properly (kind of like the ingredients needed for a recipe).

---

## 🚀 Summary of the Flow:
1. **You** upload a meeting audio file on the **Dashboard**.
2. The **Transcriber** writes down everything said.
3. The **Summarizer, Action Items, and Sentiment** tools analyze the text.
4. The **Email Generator** drafts a message for your client.
5. Everything is safely saved in the **Database**.
6. You can review everything or download a **PDF** report at any time!

---

## 🏃‍♂️ How to Run the App

If you want to start the app yourself, follow these simple steps:

1. **Open your computer's terminal** (or command prompt) and go to the project folder (`Meeting_Intelligence_AI`).
2. **Activate the environment**: This makes sure the app uses its own specific tools. Run this command:
   * On Windows: `.venv\Scripts\activate`
   * On Mac/Linux: `source .venv/bin/activate`
3. **Install the required tools** (if you haven't already):
   `pip install -r requirements.txt`
4. **Set up your secret keys**: Make sure your `.env` file exists and has the correct passwords for the database and AI services.
5. **Launch the app!**: Run this final command to open the app in your web browser:
   `streamlit run app.py`
