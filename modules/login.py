import streamlit as st

def halaman_login():

    # ================= SESSION =================
    if "login" not in st.session_state:
        st.session_state.login = False

    if "users" not in st.session_state:
        st.session_state.users = {
            "admin": "123"
        }

    # ================= DETEKSI PAGE =================
    query = st.query_params
    page = query.get("page", "login")

    # ================= STYLE =================
    st.markdown("""
        <style>

        /* hide sidebar & header */
        [data-testid="stSidebar"] {display:none;}
        header {visibility:hidden;}
        footer {visibility:hidden;}

        /* background */
        .stApp{
            background: linear-gradient(135deg,#4e73df,#224abe);
        }

        /* title */
        .login-title{
            font-size:22px;
            font-weight:bold;
            margin-bottom:5px;
            text-align:center;
            color:white;
        }

        .login-subtitle{
            font-size:14px;
            color:white;
            margin-bottom:25px;
            text-align:center;
        }

        /* link */
        .link{
            margin-top:15px;
            font-size:14px;
            text-align:center;
        }

        .link a{
            color:#ffd166;
            text-decoration:none;
            font-weight:bold;
        }

        .link a:hover{
            text-decoration:underline;
        }

        /* button */
        div.stButton > button{
            background:#f6a821;
            color:white;
            font-weight:bold;
            border-radius:6px;
            width:100%;
            height:42px;
            border:none;
        }

        div.stButton > button:hover{
            background:#e69500;
        }

        /* input field */
        .stTextInput input{
            background-color:white;
            color:black;
            border-radius:8px;
            border:1px solid #dcdcdc;
            padding:10px;
        }

        .stTextInput input:focus{
            border:1px solid #4e73df;
            box-shadow:0 0 5px rgba(78,115,223,0.5);
        }

        /* password field fix */
        div[data-baseweb="input"]{
            background-color:white !important;
            border-radius:8px;
        }

        div[data-baseweb="input"] input{
            background-color:white !important;
            color:black !important;
        }

        /* icon mata */
        div[data-baseweb="input"] button{
            background-color:white !important;
            border:none;
        }

        div[data-baseweb="input"] button svg{
            stroke:black !important;
            fill:black !important;
        }

        </style>
    """, unsafe_allow_html=True)

    # ================= CENTER CARD =================
    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        # ===== LOGO =====
        st.markdown("""
        <div style="text-align:center; font-size:60px; margin-bottom:10px;">
        🛡️
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="login-title">Sistem Evaluasi Kegiatan<br>Patroli Ditsamapta</div>',
            unsafe_allow_html=True
        )

        # ================= LOGIN =================
        if page == "login":

            st.markdown(
                '<div class="login-subtitle">Masukkan username dan password untuk masuk</div>',
                unsafe_allow_html=True
            )

            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")

            if st.button("Login"):

                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.login = True
                    st.success("Login berhasil!")
                    st.rerun()
                else:
                    st.error("Username atau password salah")

            st.markdown(
                '<div class="link">Belum punya akun? <a href="?page=register" target="_self">Daftar</a></div>',
                unsafe_allow_html=True
            )

        # ================= REGISTER =================
        elif page == "register":

            st.markdown(
                '<div class="login-subtitle">Buat akun baru</div>',
                unsafe_allow_html=True
            )

            new_user = st.text_input("👤 Username Baru")
            new_pass = st.text_input("🔒 Password Baru", type="password")

            if st.button("Register"):

                if new_user in st.session_state.users:
                    st.warning("Username sudah ada!")

                elif new_user == "" or new_pass == "":
                    st.warning("Username dan password wajib diisi!")

                else:
                    st.session_state.users[new_user] = new_pass
                    st.success("Registrasi berhasil! Silakan login.")

            st.markdown(
                '<div class="link">Sudah punya akun? <a href="?page=login" target="_self">Login</a></div>',
                unsafe_allow_html=True
            )