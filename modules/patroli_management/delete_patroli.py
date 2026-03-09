import streamlit as st

def delete_patroli():

    st.subheader("🗑️ Hapus Data Patroli")

    df = st.session_state.get("df")
    if df is None:
        st.warning("Data belum tersedia")
        return

    # Gunakan nomor urut mulai dari 1 agar konsisten dengan tabel
    index_input = st.number_input(
        "Masukkan nomor baris yang ingin dihapus (No Urut)",
        min_value=1,
        max_value=len(df),
        step=1
    )
    index = index_input - 1  # sesuaikan ke index asli DataFrame

    # Tombol Hapus dan Kembali dalam satu baris
    col1, col2 = st.columns(2)
    hapus_btn = col1.button("🗑️ Hapus Data")
    kembali_btn = col2.button("⬅️ Kembali")

    if hapus_btn:
        df = df.drop(index=index).reset_index(drop=True)
        st.session_state.df = df
        st.success("Data berhasil dihapus")
        st.session_state.halaman_crud = "data_patroli"
        st.rerun()

    if kembali_btn:
        st.session_state.halaman_crud = "data_patroli"
        st.rerun()