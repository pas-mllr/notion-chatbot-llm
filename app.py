import time
import streamlit as st
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from streamlit_chat import message
from utils import load_chain
import openai


# Configure streamlit page
st.set_page_config(
    page_title="Your Notion Chatbot",
)

# Initialize LLM chain
# llm = OpenAI(client=OpenAI, streaming=True, callbacks=[StreamlitCallbackHandler(message_placeholder)])
#
chain = load_chain()


# def load_chain():
#     """Logic for loading the chain you want to use should go here."""
#     llm = OpenAI(temperature=0)
#     chain = ConversationChain(llm=llm)
#     return chain


chain = load_chain()
# # Initialize LLM chain in session_state
# if 'chain' not in st.session_state:
#     st.session_state['chain']= load_chain()

# Initialize chat history
if 'messages' not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant", 
                                  "content": "Hi human! I am pyAtlas's smart AI. How can I help you today?"}]

# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat logic
if query := st.chat_input("Ask me anything"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # Send user's question to our chain
        # result = chain({"question": query})
        result = chain.run(input=query)
        # result = st.session_state['chain']({"question": query})
        response = result['answer']
        full_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})