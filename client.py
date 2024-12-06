import streamlit as st
import requests

# Set the FastAPI endpoint URL
api_url = "https://language-translate-by-gemma2-9b-it-2.onrender.com/chain"

# Streamlit UI
st.title("Language Translation App")
st.write("Translate text into your chosen language.")

# Dropdown for language selection
language = st.selectbox("Select the target language:", ["French", "Spanish", "German", "Italian", "Hindi"])

# Text input for the text to translate
text_to_translate = st.text_area("Enter the text to translate:")

# Submit button
if st.button("Translate"):
    # Make a request to the FastAPI backend
    if text_to_translate.strip():
        payload = {
            "language": language,
            "text": text_to_translate
        }

        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success("Translation:")
                st.write(result["output"])  # Display translated text
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text to translate.")
