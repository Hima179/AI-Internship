UAI Quiz App
============

Description:
A Tkinter-based desktop application developed for Universal AI University (UAI). It administers a quiz from `questions.json`, features an interactive question navigator, tracks correct/wrong/expired answers, tracks time to completion, and exports the final user performance data.

Requirements:
- Python 3.10 or higher
- Pillow (for image processing)

Installation:
1. Open a terminal/command prompt.
2. Navigate to this directory (UAI_Quiz_App).
3. Install dependencies by running:
   pip install Pillow

Running the App:
1. Make sure `assets/uai_logo.png` and `questions.json` exist.
2. Run the application:
   python main.py

Logs:
All quiz sessions are logged and saved automatically to `results/session_log.json` when options are selected or time expires.
