import streamlit as st
from streamlit_chat import message

from common.config import config
from core.openai_api import Chatbot

chatbot = Chatbot()
streamlit_config = config.streamlit


def setup():
    st.set_page_config(page_title="Conversation Partner", layout="centered")
    st.title("Conversation Partner")

    if "generated" not in st.session_state:
        st.session_state["generated"] = []
        st.session_state.generated.append(streamlit_config.start_message)

    if "past" not in st.session_state:
        st.session_state["past"] = []


def get_text():
    input_text = st.text_input(
        "", placeholder=streamlit_config.placeholder_message, key="input"
    )
    return input_text


def main():
    user_input = get_text()

    if user_input:
        response = chatbot.ask(user_input)

        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    # Display messages
    message(st.session_state["generated"][0], key=str(0))

    if st.session_state["past"]:
        for i in range(len(st.session_state["past"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i + 1], key=str(i + 1))


if __name__ == "__main__":
    setup()
    main()
