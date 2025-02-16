import json
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_google_form(questions):
    """
    Δημιουργεί ένα Google Form Quiz από μια λίστα ερωτήσεων.
    """
    # Φόρτωση των credentials από τα Streamlit Secrets
    service_account_info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    # Σύνδεση με το Google Forms API
    service = build("forms", "v1", credentials=credentials)

    # Δημιουργία νέας Google Form
    form_request = {
    "info": {
        "title": "Quiz",
        "documentTitle": "Quiz",
    },
    "settings": {
        "quizSettings": {
            "isQuiz": True,  # Converts form into a quiz
            "showReleasedScore": "ALWAYS",  # Show results immediately after submission
            }
        }
    }


    form = service.forms().create(body=form_request).execute()
    form_id = form["formId"]

    # Προσθήκη ερωτήσεων
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
