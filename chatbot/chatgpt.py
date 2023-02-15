import streamlit as st
from streamlit_chat import message

import openai
openai.api_key = st.secrets['api_key']

# openAI code
def openai_create(prompt):

    response = openai.Completion.create(
    # model="text-davinci-003",
    model="text-babbage-001",
    prompt=prompt,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )

    return response.choices[0].text


def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    print(s)
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history

# @st.cache_data
def reflush(history_input):
    if st.session_state['generated']:
        # for i in range(len(st.session_state['generated'])-1, -1, -1):
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            

def get_text():
    input_text = st.text_input("You: ", key="input", on_change=chatit)
    return input_text 


# Streamlit App
st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

history_input = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def chatit():
    st.header("人工智能对话")
    user_input = st.session_state.input
    print(user_input)
    if user_input:
        output = chatgpt_clone(user_input, history_input)
        history_input.append([user_input, output])
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output[0])

    if st.session_state['generated']:
        # for i in range(len(st.session_state['generated'])-1, -1, -1):
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))


if len(st.session_state['generated'])==0:
    st.header("人工智能对话")

st.text_area('用一句简短的话描述您的问题', on_change=chatit, key='input')

my_slot1 = st.empty()
