import streamlit as st
import chatbot
import eda
import model

# Masukkan path file gambar logo Anda di sini
LOGO_FILE = "logo1.png"

# Tampilkan logo dengan tautan ke App Gallery
st.logo(LOGO_FILE, link="https://mojadiapp.com/", icon_image=LOGO_FILE)

# Setel konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Emission CO2",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("---")
# Judul untuk sidebar
st.sidebar.title('Main Menu') 

# Pilihan halaman
navigation = st.sidebar.selectbox('Pilih Halaman : ', ('Insight Analysis', 'predictions', 'Chatbot'))

# Tambahkan garis pembatas di antara judul dan pilihan halaman
st.sidebar.markdown("---")

# Tampilkan halaman terkait berdasarkan pilihan navigasi
if navigation == 'Insight Analysis':
    eda.run()
elif navigation == 'predictions':
    model.run()
elif navigation == 'Chatbot':
    chatbot.run()