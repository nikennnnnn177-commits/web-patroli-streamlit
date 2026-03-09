import streamlit as st
import pandas as pd

def create_patroli():

    st.subheader("➕ Tambah Data Patroli")

    df = st.session_state.get("df")
    if df is None:
        st.warning("Data belum tersedia")
        return

    # List jam untuk dropdown
    jam_list = [f"{h:02d}:00" for h in range(0, 24)]

    with st.form("form_tambah"):

        no = st.number_input("No", min_value=1, step=1)
        tanggal = st.date_input("Tanggal Patroli")
        wilayah = st.text_input("Wilayah")
        personel = st.number_input("Jumlah Personel", min_value=0)

        # Dropdown untuk memilih jam mulai & selesai
        jam_mulai = st.selectbox("Jam Mulai", options=jam_list, index=8)  # default 08:00
        jam_selesai = st.selectbox("Jam Selesai", options=jam_list, index=10)  # default 10:00

        # Hitung durasi otomatis
        durasi = (int(jam_selesai.split(":")[0]) - int(jam_mulai.split(":")[0])) % 24
        st.text(f"Durasi Patroli: {durasi} jam")

        # Gabungkan jam mulai & selesai menjadi satu string untuk kolom Excel
        jam_shift = f"{jam_mulai} - {jam_selesai}"

        # Kolom tambahan sesuai Excel
        jenis_kegiatan = st.text_input("Jenis Kegiatan")
        model_patroli = st.text_input("Model Patroli")
        objek_patroli = st.text_input("Objek Patroli")
        kategori_lokasi = st.text_input("Kategori Lokasi")
        standar_personel = st.text_input("Standar Personel")
        kategori_kerawanan = st.text_input("Kategori Kerawanan")

        # Tombol Simpan & Kembali
        col1, col2 = st.columns(2)
        simpan = col1.form_submit_button("💾 Simpan")
        kembali = col2.form_submit_button("⬅️ Kembali")

        if simpan:
            if wilayah.strip() == "":
                st.warning("Wilayah tidak boleh kosong")
                return

            # Isi kolom yang sudah ada di Excel, termasuk Jam/Shift
            data_baru = {
                "No": no,
                "Tanggal Patroli": pd.Timestamp(tanggal),
                "Wilayah": wilayah,
                "Jumlah Personel": personel,
                "Jam/Shift": jam_shift,  # gunakan satu kolom Excel
                "Durasi": durasi,
                "Jenis Kegiatan": jenis_kegiatan,
                "Model Patroli": model_patroli,
                "Objek Patroli": objek_patroli,
                "Kategori Lokasi": kategori_lokasi,
                "Standar Personel": standar_personel,
                "Kategori Kerawanan": kategori_kerawanan
            }

            # Tambahkan ke DataFrame
            df_baru = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)
            st.session_state.df = df_baru.reset_index(drop=True)

            st.success("Data berhasil ditambahkan")
            st.session_state.halaman_crud = "data_patroli"
            st.rerun()

        if kembali:
            st.session_state.halaman_crud = "data_patroli"
            st.rerun()