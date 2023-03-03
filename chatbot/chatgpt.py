import streamlit as st
from streamlit_chat import message

import openai
from auth import auth0,auth1

# Streamlit App
st.set_page_config(
    page_title="人工智能对话",
    page_icon="👺"
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'sk' not in st.session_state:
    st.session_state['sk'] = ""

def authkey():
    st.session_state['sk'] = ""
    cdkey = st.session_state.cdkey
    (sk,days,expireTime) = auth0(cdkey)
    print(sk)
    if sk.startswith("sk-") and auth1(sk):
        st.session_state['sk'] = sk
        st.success('CDKey检测通过', icon="✅")
        return
    st.session_state.cdkey = ""
    st.error('CDKey检测失败，请在左侧栏输入', icon="🚨")



with st.sidebar:
    st.text_input('CDKey', '',key="cdkey", placeholder="请输入你的CDKey")
    st.button("确认",on_click=authkey)

# openAI code
def openai_create(prompt):
    print(prompt)
    openai.api_key = st.session_state['sk']

    messages = []
    MAX_LEN = 3096
    now_len = len(prompt)
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        if now_len>MAX_LEN:break
        now_len += (len(st.session_state['past'][i])+len(st.session_state["generated"][i]))
        messages.append({"role": "assistant", "content": st.session_state["generated"][i]})
        messages.append({"role": "user", "content": st.session_state['past'][i]})
    messages = messages[::-1]
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=MAX_LEN,
        stream=True,
        temperature=0.9,
        presence_penalty=0.6,
        frequency_penalty=0
    ) #.choices[0].text.strip()

    ct = st.container()
    with ct:
        now = str(len(st.session_state['generated']))
        message(prompt, is_user=True, key=now + '_test_user')
        # mess = message(response, key=now)
        res = ""
        percent_complete = 0
        prog = st.progress(percent_complete)
        for r in response:
            if "content" in r.choices[0].delta:
                res += r.choices[0].delta.content
            percent_complete+=1
            if percent_complete>100:percent_complete=100
            prog.progress(percent_complete, text=res)

        prog.progress(100, text=res)
    return res

def chatgpt_clone(input):
    output = openai_create(input)
    return output
            

def chatit():
    if 'sk' not in st.session_state or len(st.session_state['sk'])<1:
        st.error('CDKey检测失败，请在左侧栏输入', icon="🚨")
        return
    user_input = st.session_state.input
    print("chatit",user_input)
    st.session_state["input"] = ""
    ctCnt=2
    st.header("人工智能对话")

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            ctCnt+=2

    if len(user_input)>0:
        output = chatgpt_clone(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    hideCt(ctCnt)

    message(user_input, is_user=True, key=str(len(st.session_state['generated'])) + '_user')
    message(output, key=str(len(st.session_state['generated'])))


def hideCt(ctCnt):
    css_msg_container = f'''
        <style>
            [data-testid="stVerticalBlock"] div:nth-of-type({ctCnt})
            [data-testid="stVerticalBlock"] {{display: none}}
        </style>
        '''
    st.markdown(css_msg_container,unsafe_allow_html=True)
    
if len(st.session_state['generated'])==0:
    st.header("人工智能对话")
elif len(st.session_state.input)>0:
    st.header("人工智能对话")
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

# st.text_area('用一句简短的话描述您的问题', on_change=chatit, key='input',placeholder="用一句简短的话描述您的问题",label_visibility="collapsed")
st.text_area('用一句简短的话描述您的问题', key='input', placeholder="用一句简短的话描述您的问题",label_visibility="collapsed")
st.button('发送',key="input2", on_click=chatit)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
# hide_streamlit_style = """
#             <style>
#             footer {visibility: hidden;}
#             </style>
#             """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

