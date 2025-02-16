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
            "title": "Quiz"
        }
    }
    form = service.forms().create(body=form_request).execute()
    form_id = form["formId"]
    
    quiz_update_request = {
        "requests": [
            {
                "updateSettings": {
                    "settings": {
                        "quizSettings": {
                            "isQuiz": True  # ✅ Enable quiz mode
                        }
                    },
                    "updateMask": "quizSettings.isQuiz"
                }
            }
        ]
    }
    service.forms().batchUpdate(formId=form_id, body=quiz_update_request).execute()

    # ✅ Step 2: Προσθήκη ερωτήσεων με grading
    requests = []
    for i, q in enumerate(questions):
        question_request = {
            "createItem": {
                "item": {
                    "title": q["title"],
                    "questionItem": {
                        "question": {
                            "required": True,
                            "grading": {  # ✅ Add grading
                                "pointValue": 1,
                                "correctAnswers": {
                                    "answers": [{"value": q["options"][q["correct"]]}]
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
        requests.append(question_request)

    # ✅ Step 4: Send all questions in a single batch update
    service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()

    return f"https://docs.google.com/forms/d/{form_id}/edit"


def get_form_responses(form_id):
    """
    Retrieves responses from a Google Form.
    """
    service_account_info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    service = build("forms", "v1", credentials=credentials)

    # ✅ Fetch responses
    response = service.forms().responses().list(formId=form_id).execute()

    return response.get("responses", [])

