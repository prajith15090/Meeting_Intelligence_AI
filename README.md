# Meeting Intelligence AI 🎙️

Welcome to **Meeting Intelligence AI**! This is a smart AI assistant app designed to sit in on your meetings, take notes, analyze customer sentiment, draft follow-up emails, and generate professional reports.

You upload a meeting audio or video recording, and the app takes care of the rest.

---

## ✨ Features

- **Automatic Transcription**: Listens to meeting recordings (supporting Tamil/English mix) and transcribes them using Whisper.
- **AI-Powered Meeting Insights**: Automatically generates:
  - Executive Summaries
  - Detailed Minutes of Meeting (MoM)
  - Customer Sentiment analysis
  - Deal Stage & probability tracking
- **Follow-up Email Generator**: Automatically drafts a personalized email to send to the client.
- **Interactive Dashboard**: A clean interface with KPI metrics showing total meetings and pending tasks.
- **Meeting History**: A library to view, look up, and manage past meetings.
- **Export Reports**: Generate and download professional PDF or Word (DOCX) reports.

---

## 🛠️ Project Structure (How it Works)

- **`app.py`**: The landing welcome screen.
- **`pages/`**:
  - `dashboard.py`: Where you upload and process new recordings.
  - `history.py`: Where you browse past meetings and download reports.
- **`ai/`**: The intelligence engine handling speech-to-text, summarization, action items, and emails.
- **`components/`**: Handles the custom "The Yellow Network" branding and dark theme UI layout.
- **`database/`**: Configures connection to a PostgreSQL database to safely save your meeting files.
- **`utils/`**: Helper files to compile transcripts and construct PDF/Word documents.

---

## 🚀 Setup and Installation

Follow these quick steps to get the app running locally on your machine:

### 1. Clone the Project
Open your terminal and make sure you are in the project folder.

### 2. Set Up a Virtual Environment
Create and activate a python environment to keep libraries organized:

**On Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install all the required software ingredients:
```bash
pip install -r requirements.txt
```

### 4. Configure Environmental Variables (`.env`)
Create a file named `.env` in the root folder of the project, and add your API keys:
```env
NEON_DATABASE_URL="your-postgresql-neon-database-url"
GEMINI_API_KEY="your-gemini-api-key"
SEND_GRID_EMAIL="your-sendgrid-api-key"
SENDGRID_SENDER_EMAIL="your-sender-email@example.com"
USER_NAME="Your Name"
COMPANY_NAME="The Yellow Network"
```

### 5. Initialize the Database
Before running the app for the first time, run this script to set up the database tables:
```bash
python setup_db.py
```

### 6. Run the App!
Start the Streamlit interface:
```bash
streamlit run app.py
```
This will automatically open the app in your default web browser at `http://localhost:8501`.