import streamlit as st
import requests

st.set_page_config(page_title="Hindu Mythology Agent", layout="centered")
st.image("logo.png", width=200)
st.title("Hindu Mythology Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_response_from_api(query):
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    API_KEY = "AIzaSyDx6l_gHCApauiodFZsaCX9MJL0V3up204"  
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": query}]}]
    }
    try:
        response = requests.post(f"{API_URL}?key={API_KEY}", json=payload, headers=headers)
        response_data = response.json()
        candidates = response_data.get("candidates", [])
        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]
        else:
            return "No valid response content found."
    except Exception as e:
        return f"An error occurred: {e}"
        
st.markdown("### Ask any question about Hindu mythology:")
with st.form(key="query_form"):
    user_query = st.text_input("Your Query", placeholder="E.g., Who is Lord Vishnu?")
    submit_button = st.form_submit_button("Send")

if submit_button and user_query.strip():
    with st.spinner("Thinking..."):
        response = get_response_from_api(user_query)
        st.session_state.messages.append({"user": user_query, "bot": response})

st.markdown("### Chat History:")
for message in st.session_state.messages:
    st.markdown(f"**You:** {message['user']}")
    st.markdown(f"**Agent:** {message['bot']}")
