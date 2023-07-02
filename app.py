import openai
import streamlit as st

st.title("pwitter")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def setAvatar(role):
    if role == "user":
        return "./images/user.png"
    if role == "assistant":
        return "./images/pretty.jpg"
    else:
        return None
    
system_prompt = f"""
あなたはユーザーの発言に対してとにかく kawaii 感じで褒める行動を取ってください。
あなたはユーザーの発言を受取る度に新しい架空の人格を形成し、毎回違った名前、口調、その他年齢等の情報を設定してからその設定に則って行動してください。
"""

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-0613"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

for message in st.session_state.messages:
    if message["role"] == "system":
        continue    
    with st.chat_message(message["role"], avatar=setAvatar(message["role"])):
        st.markdown(message["content"])

if prompt := st.chat_input("何か入力してちょうだい(/・ω・)/"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=setAvatar("user")):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=setAvatar("assistant")):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})