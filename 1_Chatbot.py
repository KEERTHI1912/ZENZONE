import streamlit as st
from streamlit_chat import message
from PIL import Image
import llama
import pandas as pd 
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space


st.set_page_config(page_title="ZenZone", page_icon=":robot:")
page_bg = f"""
<style>
[data-testid="stSidebar"] {{
background-color:#69BFD6;

}}

[data-testid="stToolbar"] {{
background-color:#FCFCFC;

}}
</style>
"""
st.markdown(page_bg,unsafe_allow_html=True)

# Sidebar contents
with st.sidebar:

    image = Image.open('Capture.PNG')
    st.image(image, width=280)

    st.markdown("<h1 style='text-align: left; color: black'> About </h1>", unsafe_allow_html= True)
    st.markdown("""
    <p style='text-align: left; color: black;'> Welcome to ZenZone, your friendly mental health chatbot and safespace! Whether you're feeling down, anxious, or stressed, 
    Our empathetic friend is here to help you navigate through your emotions and provide you with the guidance you need to feel better.
    With ZenZone, you can talk about your mental health concerns in a comfortable way, 
    using Tagalog and English slangs.  So don't hesitate to chat with ZenZone anytime, anywhere! </p>
    """, unsafe_allow_html=True)
    
    add_vertical_space(5)
    st.markdown("<p style='color:purple;'> Made with 💚 by Golden Trio </p>", unsafe_allow_html=True)


count = 1
def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Say something to get started!"}]

st.title("Welcome To ZENZONE!💬")
st.write("Get your mood analyzed [here](https://brain-clip.vercel.app/).")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Say something to get started!"}]

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])

    user_prompt = a.text_input(
        label="Your message:",
        placeholder="Type something...",
        label_visibility="collapsed",
        key="input"
    )

    b.form_submit_button("Send", use_container_width=True )

for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user",key=count)
    count += 1
if user_prompt:
    #print('user_prompt: ', user_prompt)

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    message(user_prompt, is_user=True,key=count)
    count+=1
    response = llama.get_response(
        user_prompt)  # get response from llama2 API (in our case from Workflow we created before)

    msg = {"role": "assistant", "content": response}

    #print('st.session_state.messages: ', st.session_state.messages)

    st.session_state.messages.append(msg)

    #print('msg.content: ', msg["content"])

    message(msg["content"])

if len(st.session_state.messages) > 1:
    st.button('Clear Chat', on_click=clear_chat)