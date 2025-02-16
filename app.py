import streamlit as st
import pandas as pd
import json
from google_forms import create_google_form

st.title("📄 Δημιουργία Quiz στο Google Forms")

st.write("Ανεβάστε ένα αρχείο CSV με τις ερωτήσεις για να δημιουργηθεί ένα Google Form Quiz.")

# Upload αρχείου CSV
uploaded_file = st.file_uploader("Ανεβάστε το αρχείο CSV", type=["csv"])

if uploaded_file is not None:
    # Ανάγνωση αρχείου CSV
    df = pd.read_csv(uploaded_file)

    # Μετατροπή δεδομένων σε λίστα ερωτήσεων
    questions = []
    for _, row in df.iterrows():
        question_data = {
            "title": row["title"],
            "options": [row["option_1"], row["option_2"], row["option_3"], row["option_4"]],
            "correct": int(row["correct_answer"])  # Δείκτης της σωστής απάντησης
        }
        questions.append(question_data)

    # Κουμπί για δημιουργία Google Form
    if st.button("📌 Δημιουργία Quiz στο Google Forms"):
        form_link = create_google_form(questions)
        st.success(f"Το quiz δημιουργήθηκε! [Άνοιξε το Google Form]({form_link})")
