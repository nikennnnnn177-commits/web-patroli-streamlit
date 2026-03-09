import streamlit as st
import pandas as pd

from modules.login import halaman_login
from modules.utils import baca_excel
from modules.dashboard import dashboard
from modules.data_patroli import data_patroli
from modules.patroli_management.create_patroli import create_patroli
from modules.patroli_management.update_patroli import update_patroli
from modules.patroli_management.delete_patroli import delete_patroli
from modules.statistik import statistik
from modules.laporan import laporan

# ================= CONFIG PAGE =================
st.set_page_config(
    page_title="Sistem Analisis Data Patroli",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= SIDEBAR STYLE =================
st.markdown("""
<style>

/* Sidebar background */
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#1e3c72,#2f5fb3);
}

/* Sidebar text */
[data-testid="stSidebar"] label{
    color:white;
    font-weight:500;
}

/* Menu radio text */
[data-testid="stSidebar"] .stRadio label{
    color:white;
}

/* Divider */
.sidebar-divider{
    border-top:1px solid rgba(255,255,255,0.3);
    margin-top:20px;
    margin-bottom:10px;
}

/* Logout posisi bawah */
.logout-bottom{
    position: fixed;
    bottom: 20px;
    left: 20px;
    width: 200px;
}

</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "login" not in st.session_state:
    st.session_state.login = False

if "df" not in st.session_state:
    st.session_state.df = None

if "halaman_crud" not in st.session_state:
    st.session_state.halaman_crud = None

# ================= LOGIN PAGE =================
if not st.session_state.login:
    halaman_login()

# ================= MAIN SYSTEM =================
else:

    # ================= SIDEBAR =================
    st.sidebar.title("🚔 MENU SISTEM")

    menu = st.sidebar.radio(
        "Navigasi",
        [
            "📊 Dashboard",
            "📂 Data Patroli",
            "📈 Statistik Deskriptif",
            "📑 Laporan"
        ]
    )

    # ================= AMBIL DATA =================
    df = st.session_state.df

    # ================= CEK HALAMAN CRUD =================
    if st.session_state.halaman_crud == "create":
        create_patroli()
        st.stop()

    elif st.session_state.halaman_crud == "update":
        update_patroli()
        st.stop()

    elif st.session_state.halaman_crud == "delete":
        delete_patroli()
        st.stop()

    # ================= MENU =================
    if menu == "📊 Dashboard":
        st.session_state.halaman_crud = None
        dashboard()

    elif menu == "📂 Data Patroli":
        st.session_state.halaman_crud = None
        if df is not None:
            data_patroli()
        else:
            st.warning("Silakan import Excel terlebih dahulu dari Dashboard")

    elif menu == "📈 Statistik Deskriptif":
        if df is not None:
            statistik(df)
        else:
            st.warning("Silakan import Excel terlebih dahulu")

    elif menu == "📑 Laporan":
        if df is not None:
            laporan(df)
        else:
            st.warning("Silakan import Excel terlebih dahulu")

    # ================= DIVIDER =================
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # ================= LOGOUT =================
    st.sidebar.markdown('<div class="logout-bottom">', unsafe_allow_html=True)

    if st.sidebar.button("⏻ Logout"):
        st.session_state.login = False
        st.session_state.halaman_crud = None
        st.rerun()

    st.sidebar.markdown('</div>', unsafe_allow_html=True)