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
    df = pd.read_csv(uploaded_file, encoding="utf-8").fillna("")

    # Μετατροπή δεδομένων σε λίστα ερωτήσεων
    questions = []
    for _, row in df.iterrows():
        try:
            correct_index = int(row["correct_answer"])  # Ensure valid integer
        except ValueError:
            correct_index = 0  # Default to first option if invalid

        question_data = {
            "title": row["title"].strip(),  # Remove trailing spaces
            "options": [row["option_1"].strip(), row["option_2"].strip(), row["option_3"].strip(), row["option_4"].strip()],
            "correct": correct_index
        }
        questions.append(question_data)
    
    # Debugging: Show processed questions
    # st.write("🔍 Processed Questions:")
    # st.json(questions)

    # Κουμπί για δημιουργία Google Form
    if st.button("📌 Δημιουργία Quiz στο Google Forms"):
        form_link = create_google_form(questions)
        st.success(f"Το quiz δημιουργήθηκε! [Άνοιξε το Google Form]({form_link})")
