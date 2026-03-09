import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def laporan(df):

    df.columns = df.columns.str.strip()

    if "Wilayah" in df.columns:
            df["Wilayah"] = df["Wilayah"].astype(str).str.strip().str.title()


    st.title("📊 Laporan Analisis Data Kegiatan Patroli")
    st.caption("Laporan ini dihasilkan secara otomatis berdasarkan data kegiatan patroli.")

    st.divider()

    # ============================
    # STATISTIK DASAR
    # ============================

    total_kegiatan = len(df)

    if "Jumlah Personel" in df.columns:
        rata_personel = round(df["Jumlah Personel"].mean(), 1)
        max_personel = df["Jumlah Personel"].max()
        min_personel = df["Jumlah Personel"].min()
    else:
        rata_personel = 0
        max_personel = 0
        min_personel = 0

    if "Wilayah" in df.columns:
        wilayah_counts = df["Wilayah"].value_counts()
        wilayah_terbanyak = wilayah_counts.idxmax()
        jumlah_wilayah = wilayah_counts.max()
    else:
        wilayah_terbanyak = "-"
        jumlah_wilayah = 0

    # ============================
    # PERHITUNGAN DURASI UNTUK RINGKASAN
    # ============================

    mean_durasi = 0
    min_durasi = 0
    max_durasi = 0

    if "Durasi" in df.columns:

        df_durasi = df.copy()

        df_durasi["Durasi"] = df_durasi["Durasi"].astype(str)

        df_durasi["Durasi_Menit"] = pd.to_timedelta(
            df_durasi["Durasi"], errors="coerce"
        ).dt.total_seconds() / 60

        df_durasi = df_durasi.dropna(subset=["Durasi_Menit"])

        if len(df_durasi) > 0:
            mean_durasi = round(df_durasi["Durasi_Menit"].mean(), 2)
            min_durasi = round(df_durasi["Durasi_Menit"].min(), 2)
            max_durasi = round(df_durasi["Durasi_Menit"].max(), 2)

    # ============================
    # METRIC UTAMA
    # ============================

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Kegiatan Patroli", total_kegiatan)
    col2.metric("Rata-rata Personel", rata_personel)
    col3.metric("Wilayah Terbanyak", wilayah_terbanyak)

    st.divider()

    # ============================
    # RINGKASAN EKSEKUTIF
    # ============================

    st.header("Ringkasan Eksekutif")

    st.write(f""" Berdasarkan data kegiatan patroli yang tercatat dalam sistem, terdapat **{total_kegiatan} kegiatan patroli** yang telah dilaksanakan. Rata-rata jumlah personel yang terlibat dalam setiap kegiatan patroli adalah **{rata_personel} personel**. Wilayah yang paling sering menjadi lokasi patroli adalah **{wilayah_terbanyak}** dengan total **{jumlah_wilayah} kegiatan patroli**. Selain itu, hasil analisis menunjukkan bahwa rata-rata durasi kegiatan patroli adalah **{mean_durasi} menit**, dengan durasi tercepat **{min_durasi} menit** dan durasi terlama mencapai **{max_durasi} menit**.
    """)

    st.divider()

    # ============================
    # ANALISIS DURASI PATROLI
    # ============================

    if "Durasi" in df.columns:

        df["Durasi"] = df["Durasi"].astype(str)

        df["Durasi_Menit"] = pd.to_timedelta(
            df["Durasi"], errors="coerce"
        ).dt.total_seconds() / 60

        df = df.dropna(subset=["Durasi_Menit"])

        mean_durasi = round(df["Durasi_Menit"].mean(),2)
        median_durasi = round(df["Durasi_Menit"].median(),2)
        min_durasi = round(df["Durasi_Menit"].min(),2)
        max_durasi = round(df["Durasi_Menit"].max(),2)

        st.header("Analisis Durasi Patroli")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rata-rata Durasi", f"{mean_durasi} menit")
        col2.metric("Median Durasi", f"{median_durasi} menit")
        col3.metric("Durasi Minimum", f"{min_durasi} menit")
        col4.metric("Durasi Maksimum", f"{max_durasi} menit")

        st.write(f""" Durasi kegiatan patroli memiliki rata-rata **{mean_durasi} menit** dengan median **{median_durasi} menit**. Durasi patroli tercepat tercatat **{min_durasi} menit** dan durasi terlama mencapai **{max_durasi} menit**.
""")
    st.divider()

    # ============================
    # ANALISIS PERSONEL
    # ============================

    st.header("Analisis Jumlah Personel")

    if max_personel == min_personel:

        st.info(f""" Seluruh kegiatan patroli menggunakan jumlah personel yang sama yaitu **{max_personel} personel** pada setiap kegiatan. Hal ini menunjukkan bahwa komposisi personel dalam kegiatan patroli bersifat konsisten pada seluruh kegiatan yang tercatat.
""")

    else:

        st.write(f""" Jumlah personel yang terlibat dalam kegiatan patroli bervariasi antara **{min_personel} hingga {max_personel} personel** dengan rata-rata **{rata_personel} personel**.
""")

        personel_counts = df["Jumlah Personel"].value_counts().sort_index()

        st.bar_chart(personel_counts)

    st.divider()

    # ============================
    # ANALISIS WILAYAH
    # ============================

    st.header("Analisis Wilayah Patroli")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Grafik Jumlah Patroli per Wilayah")

        if "Wilayah" in df.columns:
            st.bar_chart(wilayah_counts)

    with col2:

        st.subheader("Tabel Distribusi Wilayah")

        wilayah_table = wilayah_counts.reset_index()
        wilayah_table.columns = ["Wilayah", "Jumlah Patroli"]

        st.dataframe(wilayah_table, use_container_width=True)

    st.divider()

    # ============================
    # DISTRIBUSI JENIS PATROLI
    # ============================

    if "Jenis Patroli" in df.columns:

        st.header("Distribusi Jenis Patroli")

        jenis_counts = df["Jenis Patroli"].value_counts()

        fig, ax = plt.subplots()

        ax.pie(
            jenis_counts,
            labels=jenis_counts.index,
            autopct='%1.0f%%',
            startangle=90
        )

        st.pyplot(fig)

# ============================
# INTERPRETASI DATA
# ============================

    st.header("Interpretasi Data")
    st.write(f""" Dari hasil analisis dapat diketahui bahwa kegiatan patroli dilakukan secara rutin dengan rata-rata **{rata_personel} personel** per kegiatan. Wilayah **{wilayah_terbanyak}** tercatat sebagai lokasi dengan frekuensi patroli tertinggi. Distribusi jenis patroli menunjukkan adanya variasi kegiatan yang dilakukan untuk menjaga keamanan wilayah operasional. Durasi patroli bervariasi antara **{min_durasi} hingga {max_durasi} menit**, dengan rata-rata **{mean_durasi} menit** dan median **{median_durasi} menit**. Hal ini mengindikasikan adanya variasi durasi kegiatan yang dipengaruhi oleh jenis patroli, lokasi, dan jumlah personel, sehingga informasi ini dapat digunakan untuk merencanakan kegiatan patroli lebih efektif.
    """)

    st.divider()

# ============================
# KESIMPULAN
# ============================

    st.header("Kesimpulan")
    st.write(f""" Berdasarkan analisis data, tercatat **{total_kegiatan} kegiatan patroli** selama periode pengamatan. Kegiatan patroli dilaksanakan secara rutin dengan jumlah personel yang relatif konsisten, terutama di wilayah **{wilayah_terbanyak}**. Durasi patroli bervariasi antara **{min_durasi} hingga {max_durasi} menit** dengan rata-rata **{mean_durasi} menit**, sehingga informasi ini dapat digunakan untuk merencanakan distribusi personel dan waktu patroli agar kegiatan lebih efektif dan efisien.
    """)