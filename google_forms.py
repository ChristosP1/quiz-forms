import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time  

def create_google_form(questions):
    """
    Δημιουργεί ένα Google Form Quiz από μια λίστα ερωτήσεων.
    """
    # Φόρτωση των credentials από τα Streamlit Secrets
    service_account_info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    # Σύνδεση με το Google Forms API
    service = build("forms", "v1", credentials=credentials)

    # ✅ Step 1: Δημιουργία νέας Google Form με quiz mode ενεργοποιημένο
    form_request = {
        "info": {
            "title": "Quiz",
            "documentTitle": "Quiz",
        },
        "settings": {
            "quizSettings": {
                "isQuiz": True  # ✅ Enable Quiz Mode
            }
        }
    }

    try:
        form = service.forms().create(body=form_request).execute()
    except Exception as e:
        st.error(f"❌ Error creating form: {str(e)}")  # ✅ Show full error message in Streamlit
        raise

    form_id = form["formId"]

    # ✅ Step 2: Προσθήκη ερωτήσεων με grading
    for i, q in enumerate(questions):
        question = {
            "requests": [
                {
                    "createItem": {
                        "item": {
                            "title": q["title"],
                            "questionItem": {
                                "question": {
                                    "required": True,
                                    "grading": {  # ✅ Add grading (assumes 1 point per question)
                                        "pointValue": 1,
                                        "correctAnswers": {
                                            "answers": [{"value": q["options"][q["correct"]]}]  # Correct answer
                                        }
                                    },
                                    "choiceQuestion": {
                                        "type": "RADIO",
                                        "options": [{"value": opt} for opt in q["options"]],
                                        "shuffle": False,
                                    },
                                }
                            },
                        },
                        "location": {"index": i},
                    }
                }
            ]
        }
        service.forms().batchUpdate(formId=form_id, body=question).execute()

    return f"https://docs.google.com/forms/d/{form_id}/edit"
