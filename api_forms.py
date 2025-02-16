from google.oauth2 import service_account
from googleapiclient.discovery import build

# Φόρτωση credentials από το αρχείο JSON
SCOPES = ["https://www.googleapis.com/auth/forms.body"]
SERVICE_ACCOUNT_FILE = "credentials.json"  # Τοποθέτησε εδώ το αρχείο σου

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("forms", "v1", credentials=credentials)

# Δημιουργία νέας Google Form
form_request = {
    "info": {
        "title": "Πολιτισμός - Quiz",
        "documentTitle": "Πολιτισμός Quiz",
    }
}

# Κλήση API για δημιουργία φόρμας
form = service.forms().create(body=form_request).execute()
form_id = form["formId"]
print(f"Η φόρμα δημιουργήθηκε: https://docs.google.com/forms/d/{form_id}/edit")

# Ερωτήσεις Quiz
questions = [
    {
        "title": "Σύμφωνα με την ελληνική μυθολογία, δύο θεοί του Ολύμπου διεκδίκησαν την προστασία της πόλεως των Αθηνών. Ποιοι ήταν αυτοί;",
        "options": ["Η Αθηνά και η Δήμητρα", "Η Αθηνά και ο Ποσειδών", "Η Αθηνά και ο Άρης", "Η Αθηνά και η Αφροδίτη"],
        "correct": 1,
    },
    {
        "title": "Σύμφωνα με τη μυθολογία των αρχαίων Ελλήνων, οι μόνοι άνθρωποι που σώθηκαν από τον μεγάλο κατακλυσμό ήταν:",
        "options": ["Ο Ζευς και ο Ποσειδώνας", "Ο Περσεύς και η Ανδρομέδα", "Ο Πάρης και η Ελένη", "Ο Δευκαλίων και η Πύρρα"],
        "correct": 3,
    },
]

# Προσθήκη ερωτήσεων στο Google Form
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

print(f"Το quiz δημιουργήθηκε επιτυχώς! Δες το εδώ: https://docs.google.com/forms/d/{form_id}/edit")
