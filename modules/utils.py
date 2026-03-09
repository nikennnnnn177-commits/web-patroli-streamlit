import pandas as pd
import streamlit as st

def baca_excel(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)

        # hapus kolom kosong
        df = df.dropna(how="all")

        # rapikan nama kolom
        df.columns = df.columns.astype(str).str.strip()

        # ubah kolom jumlah personel menjadi numeric jika ada
        for col in df.columns:
            if "personel" in col.lower():
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df.rename(columns={col: "Jumlah Personel"}, inplace=True)

        return df

    except Exception as e:
        st.error(f"Gagal membaca file Excel: {e}")
        return None