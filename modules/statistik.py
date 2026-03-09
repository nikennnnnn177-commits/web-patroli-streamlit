import streamlit as st
import pandas as pd
import plotly.express as px


def statistik(df):

    # ================= STYLE CARD =================
    st.markdown("""
    <style>
    .card{
        background: linear-gradient(135deg,#1e3c72,#2a5298);
        padding:20px;
        border-radius:10px;
        color:white;
        text-align:center;
        box-shadow:0px 4px 10px rgba(0,0,0,0.2);
    }

    .card h3{
        margin:0;
        font-size:20px;
    }

    .card h1{
        margin:5px;
        font-size:32px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Statistik Deskriptif Kegiatan Patroli")
    st.markdown("---")

    # ================= FORMAT DATA =================
    df["Tanggal Patroli"] = pd.to_datetime(df["Tanggal Patroli"])

    total_patroli = len(df)
    jumlah_wilayah = df["Wilayah"].nunique()
    jenis_patroli = df["Jenis Kegiatan"].nunique()

    # ================= CARD STATISTIK =================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
        <h3>Total Patroli</h3>
        <h1>{total_patroli}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
        <h3>Jumlah Wilayah</h3>
        <h1>{jumlah_wilayah}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
        <h3>Jenis Patroli</h3>
        <h1>{jenis_patroli}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ================= KONVERSI DURASI KE MENIT =================
    def convert_to_minutes(t):
        if pd.isnull(t):
            return None
        try:
            return t.hour * 60 + t.minute + t.second / 60
        except:
            return None

    df["Durasi_Menit"] = df["Durasi"].apply(convert_to_minutes)
    df = df.dropna(subset=["Durasi_Menit"])

    # ================= HITUNG STATISTIK DURASI =================
    mean_durasi = df["Durasi_Menit"].mean()
    median_durasi = df["Durasi_Menit"].median()
    min_durasi = df["Durasi_Menit"].min()
    max_durasi = df["Durasi_Menit"].max()
    std_durasi = df["Durasi_Menit"].std()

    # ================= STATISTIK DURASI =================
    col_stat, col_hist = st.columns(2)

    with col_stat:

        st.subheader("Statistik Durasi Patroli")

        st.metric("Mean Durasi Patroli (Menit)", f"{mean_durasi:.2f}")
        st.metric("Median Durasi Patroli (Menit)", f"{median_durasi:.2f}")
        st.metric("Minimum Durasi Patroli (Menit)", f"{min_durasi:.0f}")
        st.metric("Maksimum Durasi Patroli (Menit)", f"{max_durasi:.0f}")
        st.metric("Standar Deviasi Durasi (Menit)", f"{std_durasi:.2f}")

        st.markdown("---")

    with col_hist:

        st.subheader("Distribusi Durasi Patroli")

        fig_hist = px.histogram(
            df,
            x="Durasi_Menit",
            nbins=10
        )

        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown("---")

    # ================= BOXPLOT DURASI =================
    st.subheader("Boxplot Durasi Patroli")

    fig_box = px.box(
        df,
        y="Durasi_Menit",
        title="Distribusi Durasi Patroli"
    )

    fig_box.update_layout(
        yaxis_title="Durasi Patroli (Menit)"
    )

    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # ================= GRAFIK BARIS 1 =================
    col4, col5 = st.columns(2)

    # ===== Distribusi Patroli Per Wilayah =====
    with col4:

        st.subheader("Distribusi Patroli Per Wilayah")

        wilayah = df["Wilayah"].value_counts().reset_index()
        wilayah.columns = ["Wilayah", "Jumlah"]

        fig_bar = px.bar(
            wilayah,
            x="Wilayah",
            y="Jumlah",
            color="Wilayah",
            text_auto=True
        )

        fig_bar.update_layout(
            xaxis_title="Wilayah",
            yaxis_title="Jumlah Patroli",
            showlegend=False
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # ===== Distribusi Jenis Patroli =====
    with col5:

        st.subheader("Distribusi Jenis Patroli")

        jenis = df["Jenis Kegiatan"].value_counts()

        top5 = jenis.head(5)
        lainnya = jenis.iloc[5:].sum()

        if lainnya > 0:
            jenis_final = top5.copy()
            jenis_final["Lainnya"] = lainnya
        else:
            jenis_final = top5

        fig_pie = px.pie(
            values=jenis_final.values,
            names=jenis_final.index,
            hole=0.45
        )

        fig_pie.update_layout(
            legend_title="Jenis Patroli"
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # ================= DISTRIBUSI BERDASARKAN HARI =================
    st.subheader("Distribusi Patroli Berdasarkan Hari")

    df["Hari"] = df["Tanggal Patroli"].dt.day_name()

    urutan_hari = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    hari = df["Hari"].value_counts().reindex(urutan_hari).fillna(0).reset_index()
    hari.columns = ["Hari", "Jumlah"]

    fig_hari = px.bar(
        hari,
        x="Hari",
        y="Jumlah",
        color="Hari",
        text_auto=True
    )

    fig_hari.update_layout(
        xaxis_title="Hari",
        yaxis_title="Jumlah Patroli",
        showlegend=False
    )

    st.plotly_chart(fig_hari, use_container_width=True)