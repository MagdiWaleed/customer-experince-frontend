import streamlit as st
import requests

st.set_page_config(page_title="Customer Chat", layout="wide")
st.title("🗨️ Customer Support Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "token" not in st.session_state:
    st.warning("⚠️ You are not signed in. Please sign in first.")
else:
    chat_container = st.container()
    for msg in st.session_state.messages:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        st.chat_message(role).markdown(content)

    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        placeholder = st.empty()
        with st.spinner("🤖 Thinking..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/chat/",
                    json={
                        "token": st.session_state.token,
                        "message": prompt
                    },
                    timeout=60
                )
                if response.status_code == 200:
                    bot_answer = response.json().get("message", "No response from server.")
                else:
                    bot_answer = f"⚠️ Server error: {response.status_code}"
            except requests.exceptions.ConnectionError:
                bot_answer = "⚠️ Could not connect to backend. Make sure the Flask app is running."
            except Exception as e:
                bot_answer = f"⚠️ Unexpected error: {e}"

        placeholder.chat_message("assistant").markdown(bot_answer)
        st.session_state.messages.append({"role": "assistant", "content": bot_answer})
