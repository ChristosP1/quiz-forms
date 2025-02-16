import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests 
import time 

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxAcDeJ7Pnj5KTzzmqOsW524DQ37c9JgeD7sNJFotGOKlotWnug2Sdp2gp_j10XVD6_/exec"


def create_google_form(questions):
    """
    Δημιουργεί ένα Google Form Quiz από μια λίστα ερωτήσεων.
    """
    service_account_info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    service = build("forms", "v1", credentials=credentials)

    # Δημιουργία νέας Google Form
    form_request = {
        "info": {
            "title": "Quiz",
            "documentTitle": "Quiz",
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

    time.sleep(10)  # ✅ Increase delay before calling the API

    # ✅ Send request properly with formId in the URL
    response = requests.get(APPS_SCRIPT_URL, params={"formId": form_id})

    # Check if it worked
    if response.status_code == 200:
        print("✅ Quiz mode enabled successfully!")
    else:
        print(f"❌ Failed to enable quiz mode: {response.text}")

    return f"https://docs.google.com/forms/d/{form_id}/edit"