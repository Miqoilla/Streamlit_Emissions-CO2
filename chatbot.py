import streamlit as st
import os
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from streamlit_lottie import st_lottie
import requests

# Mendefinisikan fungsi untuk memuat Groq dengan API key
def load_groq(api_key):
    return ChatGroq(groq_api_key=api_key)

# Fungsi untuk memuat animasi Lottie dari URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Mendefinisikan tampilan aplikasi Streamlit
def run():
    st.title("Hai Sobat Mojadiapp 🫰")
    lottie_animation = load_lottieurl("https://lottie.host/dac3b166-9a41-4c33-8c08-cf1088b884f9/DDy8St12vV.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=400)

    # Sidebar untuk memasukkan API key Groq dan kustomisasi
    with st.sidebar:
        st.markdown("## API Key")
        groq_api_key = st.text_input("Masukkan Kunci API Key Anda", key="chatbot_api_key", type="password")
        st.markdown("[Get an Groq API key](https://console.groq.com/keys)")
        
        st.sidebar.markdown("---")

        st.title('Kustomisasi')
        model = st.selectbox('Pilih model', ['gemma-7b-it', 'llama2-70b-4096', 'llama3-70b-8192', 'llama3-8b-8192'])
        panjang_memori_percakapan = st.slider('Panjang memori percakapan:', 1, 10, value=5)

    # Menambahkan animasi Lottie di sidebar
    

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Halo! Mau dibantu apa nih?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Malu bertanya sesat di jalan"):
        # Memastikan API key Groq sudah dimasukkan
        if not groq_api_key:
            st.info("Silakan tambahkan Groq API key Anda untuk melanjutkan.")
            st.stop()

        # Memuat Groq dengan API key yang dimasukkan
        groq_chat = load_groq(api_key=groq_api_key)

        # Membuat atau memuat memori percakapan jika belum ada
        memori = ConversationBufferWindowMemory(k=panjang_memori_percakapan)
        st.session_state.riwayat_chat = st.session_state.riwayat_chat if 'riwayat_chat' in st.session_state else []

        for pesan in st.session_state.riwayat_chat:
            memori.save_context({'input': pesan['manusia']}, {'output': pesan['AI']})

        # Menginisialisasi rantai percakapan dengan Groq
        percakapan = ConversationChain(llm=groq_chat, memory=memori)

        # Mengirimkan pertanyaan dan mendapatkan respons dari Groq
        respons = percakapan(prompt)

        # Menyimpan pesan ke dalam riwayat percakapan
        st.session_state["messages"].append({"role": "user", "content": prompt})
        st.session_state["messages"].append({"role": "assistant", "content": respons['response']})

        # Menampilkan pesan dari Groq
        st.chat_message("assistant").write(respons['response'])

if __name__ == "__main__":
    run()
