import streamlit as st
import pandas as pd

def update_patroli():

    st.subheader("✏️ Update Data Patroli")

    df = st.session_state.get("df")
    if df is None:
        st.warning("Data belum tersedia")
        return

    # Gunakan nomor urut mulai dari 1 agar sesuai tabel
    index_input = st.number_input(
        "Masukkan nomor baris yang ingin diubah (No Urut)",
        min_value=1,
        max_value=len(df),
        step=1
    )
    index = index_input - 1  # sesuaikan ke index asli DataFrame

    data_lama = df.loc[index]

    # =========================
    # Semua kolom sesuai create
    # =========================
    tanggal = st.date_input("Tanggal Patroli", data_lama["Tanggal Patroli"])
    jam_shift = st.text_input("Jam / Shift", data_lama.get("Jam/Shift", ""))
    durasi = st.text_input("Durasi Patroli", data_lama.get("Durasi", ""))
    jenis_kegiatan = st.text_input("Jenis Kegiatan", data_lama.get("Jenis Kegiatan", ""))
    model_patroli = st.text_input("Model Patroli", data_lama.get("Model Patroli", ""))
    objek_patroli = st.text_input("Objek Patroli", data_lama.get("Objek Patroli", ""))
    kategori_lokasi = st.text_input("Kategori Lokasi", data_lama.get("Kategori Lokasi", ""))
    standar_personel = st.number_input("Standar Personel", value=int(data_lama.get("Standar Personel", 0)))
    kategori_kerawanan = st.text_input("Kategori Kerawanan", data_lama.get("Kategori Kerawanan", ""))
    wilayah = st.text_input("Wilayah", data_lama["Wilayah"])
    personel = st.number_input("Jumlah Personel", value=int(data_lama["Jumlah Personel"]))

    # Tombol Update dan Kembali
    col1, col2 = st.columns(2)
    update_btn = col1.button("💾 Update Data")
    kembali_btn = col2.button("⬅️ Kembali")

    if update_btn:
        # Update semua kolom
        df.loc[index, "Tanggal Patroli"] = pd.Timestamp(tanggal)
        df.loc[index, "Jam/Shift"] = jam_shift
        df.loc[index, "Durasi"] = durasi
        df.loc[index, "Jenis Kegiatan"] = jenis_kegiatan
        df.loc[index, "Model Patroli"] = model_patroli
        df.loc[index, "Objek Patroli"] = objek_patroli
        df.loc[index, "Kategori Lokasi"] = kategori_lokasi
        df.loc[index, "Standar Personel"] = standar_personel
        df.loc[index, "Kategori Kerawanan"] = kategori_kerawanan
        df.loc[index, "Wilayah"] = wilayah
        df.loc[index, "Jumlah Personel"] = personel

        st.session_state.df = df.reset_index(drop=True)
        st.success("Data berhasil diupdate")
        st.session_state.halaman_crud = "data_patroli"
        st.rerun()

    if kembali_btn:
        st.session_state.halaman_crud = "data_patroli"
        st.rerun()