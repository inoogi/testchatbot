from openai import OpenAI
import openai
import streamlit as st
import time

assistant_id = 'asst_yWGysjcUdjex88NauUKul9Bb'

with st.sidebar:
    st.link_button("더 좋은 컨텐츠를 위해 후원하기", "https://toss.me/kimfl")

    iframe_html = """<iframe src="https://ads-partners.coupang.com/widgets.html?id=763755&template=banner&trackingCode=AF6327453&subId=&width=300&height=250" width="300" height="250" frameborder="0" scrolling="no" referrerpolicy="unsafe-url" browsingtopics></iframe>"""
    st.markdown(iframe_html, unsafe_allow_html=True)
    st.info("이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.")
    
    openai_api_key = st.text_input("OpenAI API KEY", type="password", value="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")
    thread_id = st.text_input("Thread ID", value='thread_R3qOC2SlUvnTWkYUZ3TS2LvH')
    thread_make_btn = st.button("Create a new thread")

    if thread_make_btn:
        client = openai.OpenAI(api_key=openai_api_key)  # 클라이언트 객체 생성
        thread = client.beta.threads.create()
        thread_id = thread.id
        st.subheader(f"{thread_id}", divider="rainbow")
        st.info("새로운 스레드가 생성되었습니다.")

st.title("My ChatBot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "선생님한테 무엇이든 물어보세요~"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input()

if prompt:
    client = openai.OpenAI(api_key=openai_api_key)  # 클라이언트 객체 생성
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=prompt)
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)
    assistant_content = thread_messages.data[0].content[0].text.value
    st.session_state.messages.append({"role": "assistant", "content": assistant_content})
    st.chat_message("assistant").write(assistant_content)