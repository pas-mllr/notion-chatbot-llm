# import time
# import streamlit as st
# from utils import load_chain
#
#
# # Configure streamlit page
# st.set_page_config(
#     page_title="Your Notion Chatbot",
# )
#
# # Initialize LLM chain
# # llm = OpenAI(client=OpenAI, streaming=True, callbacks=[StreamlitCallbackHandler(message_placeholder)])
# #
# chain = load_chain()
#
#
# # def load_chain():
# #     """Logic for loading the chain you want to use should go here."""
# #     llm = OpenAI(temperature=0)
# #     chain = ConversationChain(llm=llm)
# #     return chain
#
#
# # chain = load_chain()
# # # Initialize LLM chain in session_state
# # if 'chain' not in st.session_state:
# #     st.session_state['chain']= load_chain()
#
# # Initialize chat history
# if 'messages' not in st.session_state:
#     # Start with first message from assistant
#     st.session_state['messages'] = [{"role": "assistant",
#                                   "content": "Hi human! I am pyAtlas's smart AI. How can I help you today?"}]
#
# # Display chat messages from history on app rerun
# # Custom avatar for the assistant, default avatar for user
# for message in st.session_state.messages:
#     if message["role"] == 'assistant':
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
#     else:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
#
# # Chat logic
# if query := st.chat_input("Ask me anything"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": query})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(query)
#
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         # Send user's question to our chain
#         result = chain({"question": query})
#         # result = chain.run(input=query)
#         # result = st.session_state['chain']({"question": query})
#         response = result['answer']
#         full_response = ""
#
#         # Simulate stream of response with milliseconds delay
#         for chunk in response.split():
#             full_response += chunk + " "
#             time.sleep(0.05)
#             # Add a blinking cursor to simulate typing
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#
#     # Add assistant message to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})
# **app.py**
# import time
# import streamlit as st
# from utils import load_chain
# # Custom image for the app icon and the assistant's avatar
# company_logo = 'https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2F136a64bb-3927-46ca-9295-8d2b747b2135%2F998243a1-0e63-4627-90e7-8dd46c28ed00%2Ficon.png?id=2ba2b19f-f03c-4107-be2a-93ff45e8b54d&table=collection&spaceId=136a64bb-3927-46ca-9295-8d2b747b2135&width=60&userId=6b9d30c5-7481-4495-b40c-8213ae426d4f&cache=v2'
# # Configure Streamlit page
# st.set_page_config(
#     page_title="Your Notion Chatbot",
#     page_icon=company_logo
# )
# # Initialize LLM chain
# chain = load_chain()
# # Initialize chat history
# if 'messages' not in st.session_state:
#     # Start with first message from assistant
#     st.session_state['messages'] = [{"role": "assistant",
#                                   "content": "Hi human! I am pyAtlas's smart AI. How can I help you today?"}]
# # Display chat messages from history on app rerun
# # Custom avatar for the assistant, default avatar for user
# for message in st.session_state.messages:
#     if message["role"] == 'assistant':
#         with st.chat_message(message["role"], avatar=company_logo):
#             st.markdown(message["content"])
#     else:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
# # Chat logic
# if query := st.chat_input("Ask me anything"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": query})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(query)
#     with st.chat_message("assistant", avatar=company_logo):
#         message_placeholder = st.empty()
#         # Send user's question to our chain
#         # result = chain({"question": query})
#         result = "Sorry. I'm still learning"
#         # response = result['answer']
#         response = result
#         full_response = ""
#         # Simulate stream of response with milliseconds delay
#         for chunk in response.split():
#             full_response += chunk + " "
#             time.sleep(0.05)
#             # Add a blinking cursor to simulate typing
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#     # Add assistant message to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})
from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})