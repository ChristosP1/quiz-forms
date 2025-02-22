import streamlit as st
import pandas as pd
import json
from google_forms import create_google_form, get_form_responses
import clipboard

st.title("📄 Δημιουργία Quiz στο Google Forms")

st.write("Ανεβάστε ένα αρχείο CSV με τις ερωτήσεις για να δημιουργηθεί ένα Google Form Quiz.")

# Upload αρχείου CSV
uploaded_file = st.file_uploader("Ανεβάστε το αρχείο CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="utf-8").fillna("")

    questions = []
    for _, row in df.iterrows():
        try:
            correct_index = int(row["correct_answer"])  
        except ValueError:
            correct_index = 0  

        question_data = {
            "title": row["title"].strip(),
            "options": [row["option_1"].strip(), row["option_2"].strip(), row["option_3"].strip(), row["option_4"].strip()],
            "correct": correct_index
        }
        questions.append(question_data)
    
    st.write("🔍 Processed Questions:")
    st.json(questions)

    # ✅ Button to Create Quiz
    if st.button("📌 Δημιουργία Quiz στο Google Forms"):
        form_link = create_google_form(questions)
        st.success(f"Το quiz δημιουργήθηκε! [Άνοιξε το Google Form]({form_link})")
        with st.button("📋", key="copy"):
            clipboard.copy(f"form_link")

        # ✅ Show a button to fetch responses
        form_id = form_link.split("/")[-2]  # Extract form ID from link
        if st.button("📥 Λήψη Αποτελεσμάτων"):
            responses = get_form_responses(form_id)
            st.json(responses)  # Show responses as JSON
