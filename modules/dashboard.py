import streamlit as st
import pandas as pd

def dashboard():

    st.title("📊 Dashboard Sistem Analisis Data Patroli")

    uploaded_file = st.file_uploader(
        "Upload Data Excel Patroli", type=["xlsx"]
    )

    # =========================
    # JIKA FILE DIUPLOAD
    # =========================
    if uploaded_file is not None:

        df = pd.read_excel(uploaded_file, header=3)
        df.columns = df.columns.str.strip()
        df = df.dropna(how="all")
        df = df.fillna(method="ffill")

        # SIMPAN DATA KE SESSION
        st.session_state.df = df
        st.session_state.data_patroli = df

    # =========================
    # JIKA FILE TIDAK DIUPLOAD TAPI SUDAH ADA DI SESSION
    # =========================
    if "df" in st.session_state and st.session_state.df is not None:

        df = st.session_state.df

        # =========================
        # HITUNG TOTAL DAN RINGKASAN
        # =========================
        total_patroli = len(df)

        total_personel = 0
        if "Jumlah Personel" in df.columns:
            df["Jumlah Personel"] = pd.to_numeric(
                df["Jumlah Personel"], errors="coerce"
            )
            total_personel = df["Jumlah Personel"].sum()

        rata_harian = 0
        if "Tanggal Patroli" in df.columns:
            df["Tanggal Patroli"] = pd.to_datetime(
                df["Tanggal Patroli"], errors="coerce"
            )
            jumlah_hari = df["Tanggal Patroli"].nunique()
            if jumlah_hari > 0:
                rata_harian = round(total_patroli / jumlah_hari, 2)

        total_wilayah = 0
        if "Wilayah" in df.columns:
            total_wilayah = df["Wilayah"].nunique()

        # =========================
        # STYLE CARD
        # =========================
        st.markdown("""
        <style>
        .card{padding:25px;border-radius:12px;color:white;text-align:center;font-weight:bold;}
        .blue{background:#3b82f6;}
        .darkblue{background:#1e3a8a;}
        .green{background:#10b981;}
        .orange{background:#f59e0b;}
        .card-title{font-size:18px;}
        .card-value{font-size:34px;margin-top:10px;}
        .welcome{background:#f3f4f6;padding:30px;border-radius:10px;text-align:center;font-size:22px;color:#666;margin-top:30px;margin-bottom:30px;}
        </style>
        """, unsafe_allow_html=True)

        # =========================
        # CARD DASHBOARD
        # =========================
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="card blue">
            <div class="card-title">Total Patroli</div>
            <div class="card-value">{total_patroli}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card darkblue">
            <div class="card-title">Total Personel</div>
            <div class="card-value">{int(total_personel)}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card green">
            <div class="card-title">Rata-rata Per Hari</div>
            <div class="card-value">{rata_harian}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="card orange">
            <div class="card-title">Total Wilayah</div>
            <div class="card-value">{total_wilayah}</div>
            </div>
            """, unsafe_allow_html=True)

        # =========================
        # WELCOME
        # =========================
        st.markdown("""
        <div class="welcome">
        Selamat Datang di Sistem Analisis Data Patroli Ditsamapta
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # PREVIEW DATA
        # =========================
        st.subheader("Preview Data Patroli")
        st.dataframe(df, use_container_width=True)

    # =========================
    # JIKA FILE TIDAK DIUPLOAD DAN BELUM ADA SESSION
    # =========================
    else:
        st.info("Silakan upload file Excel terlebih dahulu.")