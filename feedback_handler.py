import json
from datetime import datetime
import os

FEEDBACK_FILE = "feedback.json"

def submit_feedback(user_id: str, course_title: str, rating: float, comment: str = ""):
    feedback_data = {
        "user_id": user_id,
        "course": course_title,
        "rating": rating,
        "comment": comment,
        "timestamp": str(datetime.now())
    }

    # If file doesn't exist, create it
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Check for duplicates
    with open(FEEDBACK_FILE, "r+", encoding="utf-8") as f:
        existing = json.load(f)
        for entry in existing:
            if entry["user_id"] == user_id and entry["course"] == course_title:
                return {
                    "status": "error",
                    "message": f"Feedback for '{course_title}' by user '{user_id}' already exists."
                }

        # Append new feedback
        existing.append(feedback_data)
        f.seek(0)
        json.dump(existing, f, indent=2)

    return {
        "status": "success",
        "message": "Feedback submitted.",
        "feedback": feedback_data
    }
