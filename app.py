import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Claude Chat", page_icon="🤖", layout="centered")
st.title("Claude Chat")

client = OpenAI(
    api_key=st.secrets["ANTHROPIC_API_KEY"],
    base_url="https://litellm.dhhmena.com/"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Message Claude..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="claude-sonnet-4-6",
            messages=st.session_state.messages,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full_response += delta
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
