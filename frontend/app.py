import streamlit as st
import requests
import time

st.set_page_config(
    page_title="🩺 AI Medi Prescriptor",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inject custom dark CSS with animations
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #e0e0e0;
    }
    .stApp {
        background: linear-gradient(145deg, #1f1f1f, #181818);
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        animation: fadeIn 1s ease-in-out;
    }

    h1 {
        color: #ff4b4b;
        text-align: center;
        padding: 10px;
        font-size: 2.5rem;
    }

    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }

    .css-1cpxqw2 {
        background-color: #1e1e1e;
    }

    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5em 1.5em;
        transition: all 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #e63b3b;
        transform: scale(1.05);
    }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea {
        background-color: #2c2c2c;
        color: white;
        border-radius: 8px;
    }

    .stNumberInput>div>div>input {
        background-color: #2c2c2c;
        color: white;
        border-radius: 8px;
    }

    .css-1offfwp {
        background-color: #2a2a2a !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("AI Medi Prescriptor")

# Input Form
with st.form(key='med_form'):
    age = st.number_input("👶 Enter your age", min_value=0, max_value=120, step=1)
    symptoms = st.text_input("📝 Enter symptoms (e.g., fever, pain, cold)")
    prescription = st.text_area("💊 Enter prescribed drugs", height=150)
    submit_button = st.form_submit_button(label='🔍 Analyze Prescription')

# Backend call
if submit_button:
    if not prescription or not symptoms:
        st.warning("⚠ Please fill in all fields.")
    else:
        with st.spinner("🧪 Analyzing your prescription..."):
            try:
                time.sleep(1.5)  # Simulate delay
                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={
                        "age": age,
                        "prescription": prescription,
                        "symptoms": symptoms
                    }
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success("✅ Analysis Complete")

                    st.subheader("🔍 Extracted Drugs")
                    st.write(result["extracted_drugs"])

                    st.subheader("⚠ Interaction Warnings")
                    if result["interaction_warnings"]:
                        for warning in result["interaction_warnings"]:
                            st.error(f"⚠ {warning}")
                    else:
                        st.info("✅ No major drug interactions found.")

                    st.subheader("💊 Safe Dosage Recommendations")
                    for drug, dosage in result["safe_dosage"].items():
                        st.write(f"🧪 {drug}: {dosage}")

                    st.subheader("🔄 Alternative Suggestions")
                    for drug, alternatives in result["alternative_suggestions"].items():
                        st.write(f"🔁 {drug} alternatives: {', '.join(alternatives)}")
                else:
                    st.error("❌ Something went wrong. Backend error.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Failed to connect to backend: {e}")

# Footer
st.markdown("""
    <footer style="text-align: center; margin-top: 20px; color: #888;">
        <p>Made with ❤️ by GENie-AI-us</p>
        <p>© 2025 AI Medi Prescriptor</p>

    </footer>
""", unsafe_allow_html=True)