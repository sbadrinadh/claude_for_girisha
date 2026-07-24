import streamlit as st
import anthropic

st.set_page_config(page_title="Claude Chat", page_icon="🤖", layout="centered")
st.title("Claude Chat")

client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"],
    base_url="https://litellm.dhhmena.com",
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

        try:
            with client.messages.stream(
                model="claude-sonnet-4-6",
                max_tokens=8096,
                messages=st.session_state.messages,
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {type(e).__name__}: {e}")
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": full_response})
