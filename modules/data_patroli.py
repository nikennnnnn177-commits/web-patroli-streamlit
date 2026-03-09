import streamlit as st

def data_patroli():

    st.title("📄 Data Patroli")

    df = st.session_state.get("df")

    if df is None:
        st.warning("Data belum diimport dari Dashboard")
        return

    # ====================
    # INFO JUMLAH DATA
    # ====================
    total_data = len(df)
    st.info(f"Total Data Patroli : {total_data}")

    # ====================
    # TOMBOL CRUD
    # ====================
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ Tambah Data"):
            st.session_state.halaman_crud = "create"
            st.rerun()

    with col2:
        if st.button("✏️ Edit Data"):
            st.session_state.halaman_crud = "update"
            st.rerun()

    with col3:
        if st.button("🗑 Hapus Data"):
            st.session_state.halaman_crud = "delete"
            st.rerun()

    st.divider()

    # ====================
    # TABEL DATA DENGAN NOMOR URUT TANPA MENGHAPUS KOLOM ASLI
    # ====================
    st.subheader("Tabel Data Patroli")

    df_tampil = df.copy()

    if "No Urut" in df_tampil.columns:
        df_tampil = df_tampil.drop(columns=["No Urut"])

    df_tampil.insert(0, "No Urut", range(1, len(df_tampil) + 1))

    st.dataframe(
        df_tampil,
        use_container_width=True,
        hide_index=True
    )