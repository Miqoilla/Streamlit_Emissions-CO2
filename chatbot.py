import streamlit as st
import os
import requests
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# Coba import paket yang mungkin tidak tersedia
try:
    from groq import Groq
    from langchain_groq import ChatGroq
    from streamlit_lottie import st_lottie
except ImportError as e:
    st.error(f"Error importing required package: {e}")
    st.stop()

def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_animation = load_lottieurl("https://lottie.host/dac3b166-9a41-4c33-8c08-cf1088b884f9/DDy8St12vV.json")

def run():
    st.title("Hai Sobat Mojadiapp")
    
    groq_api_key = os.environ.get('GROQ_API_KEY')
    if not groq_api_key:
        st.error("Variabel lingkungan GROQ_API_KEY tidak diatur.")
        return

    if lottie_animation:
        st_lottie(lottie_animation, height=450, key="chatbot")

    st.write("Saya adalah Chatbot, asisten virtual Anda yang ramah dan siap membantu dengan cepat. Apakah Anda memiliki pertanyaan, butuh informasi, atau ingin sekadar mengobrol? Mari kita mulai percakapan yang seru ini!")

    st.sidebar.title('Kustomisasi')
    model = st.sidebar.selectbox('Pilih model', ['gemma-7b-it', 'llama2-70b-4096', 'llama3-70b-8192', 'llama3-8b-8192'])
    panjang_memori_percakapan = st.sidebar.slider('Panjang memori percakapan:', 1, 10, value=5)

    memori = ConversationBufferWindowMemory(k=panjang_memori_percakapan)
    st.session_state.riwayat_chat = st.session_state.riwayat_chat if 'riwayat_chat' in st.session_state else []

    for pesan in st.session_state.riwayat_chat:
        memori.save_context({'input': pesan['manusia']}, {'output': pesan['AI']})

    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model)
    percakapan = ConversationChain(llm=groq_chat, memory=memori)

    pertanyaan_pengguna = st.text_input("Ajukan pertanyaan:")
    if pertanyaan_pengguna:
        respons = percakapan(pertanyaan_pengguna)
        pesan = {'manusia': pertanyaan_pengguna, 'AI': respons['response']}
        st.session_state.riwayat_chat.append(pesan)
        st.write("Chatbot:", respons['response'])

if __name__ == "__main__":
    run()
