#Import library
import streamlit as st
import pandas as pd
import plotly.express as px

#Load dataset
df = pd.read_csv("dashboard/main_data.csv")

#Konversi format tanggal agar hanya menampilkan tahun, bulan, tanggal
df["dteday"] = pd.to_datetime(df["dteday"]).dt.strftime('%Y-%m-%d')
#Mapping untuk mengubah kode musim & cuaca menjadi string
season_mapping = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
weather_mapping = {1: "Clear", 2: "Mist", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"}
weekday_mapping = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}

df["season"] = df["season"].map(season_mapping)
df["weathersit"] = df["weathersit"].map(weather_mapping)
df["weekday"] = df["weekday"].map(weekday_mapping)

#Tampilan dashboard
st.set_page_config(page_title="🚴‍♂️ Bike Sharing Data Analysis", layout="wide")
st.title("🚴‍♂️ Bike Sharing Data Analysis")
st.markdown("Analisis tren penggunaan sepeda berdasarkan musim, kondisi cuaca, dan faktor lainnya")

#Sidebar untuk filter
with st.sidebar:
    st.header("🔍 Filter Data")
    #filter rentang tanggal
    min_date, max_date = df["dteday"].min(), df["dteday"].max()
    date_range = st.date_input("Pilih rentang tanggal", [pd.to_datetime(min_date), pd.to_datetime(max_date)], 
                               min_value=pd.to_datetime(min_date), max_value=pd.to_datetime(max_date))
    #filter musim & cuaca
    season_filter = st.multiselect("Musim", df["season"].unique(), default=df["season"].unique())
    weather_filter = st.multiselect("Kondisi cuaca", df["weathersit"].unique(), default=df["weathersit"].unique())

#Filter dataset berdasarkan pilihan pengguna
filtered_df = df[(df["dteday"] >= date_range[0].strftime('%Y-%m-%d')) & (df["dteday"] <= date_range[1].strftime('%Y-%m-%d'))]
filtered_df = filtered_df[(filtered_df["season"].isin(season_filter)) & (filtered_df["weathersit"].isin(weather_filter))]

#Menampilkan total & rata-rata pengguna
total_users = filtered_df["cnt"].sum()
average_users = filtered_df["cnt"].mean()

col1, col2 = st.columns(2)
with col1:
    st.metric("📊 Total pengguna sepeda", f"{total_users:,}")
with col2:
    st.metric("📈 Rata-rata pengguna harian", f"{average_users:.2f}")

#Menampilkan data yang difilter
st.subheader("📋 Data yang difilter")
hidden_cols = ["yr", "holiday"]

st.data_editor(
    filtered_df, 
    hide_index=True,  
    column_config={col: None for col in hidden_cols}  
)

#Jika tidak ada data setelah filter
if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang tersedia untuk filter yang dipilih. Silakan pilih opsi lain!")
else:
    #Pengaruh musim terhadap pengguna sepeda
    st.subheader("🌤️ Pengaruh musim terhadap penggunaan sepeda")
    fig_season = px.box(filtered_df, x="season", y="cnt", color="season",
                         title="Distribusi pengguna sepeda berdasarkan musim",
                         labels={"season": "Musim", "cnt": "Jumlah pengguna"})
    st.plotly_chart(fig_season, use_container_width=True)
    #Pengaruh cuaca terhadap pengguna sepeda
    st.subheader("🌦️ Pengaruh kondisi cuaca terhadap penggunaan sepeda")
    fig_weather = px.box(filtered_df, x="weathersit", y="cnt", color="weathersit",
                          title="Pengaruh kondisi cuaca terhadap penggunaan sepeda",
                          labels={"weathersit": "Kondisi cuaca", "cnt": "Jumlah pengguna"})
    st.plotly_chart(fig_weather, use_container_width=True)
    #Tren penggunaan sepeda
    st.subheader("📅 Tren penggunaan sepeda sepanjang tahun")
    fig_trend = px.line(filtered_df, x="dteday", y="cnt", 
                         title="Tren penggunaan sepeda berdasarkan waktu",
                         labels={"dteday": "Tanggal", "cnt": "Jumlah pengguna"},
                         template="plotly_white")
    st.plotly_chart(fig_trend, use_container_width=True)
    #Distribusi penggunaan sepeda berdasarkan hari
    st.subheader("📆 Penggunaan sepeda berdasarkan hari dalam seminggu")
    weekday_order = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    weekday_avg = filtered_df.groupby("weekday")["cnt"].mean().reindex(weekday_order).reset_index()
    fig_weekday = px.bar(weekday_avg, x="weekday", y="cnt", 
                         title="Rata-rata pengguna sepeda berdasarkan hari",
                         labels={"weekday": "Hari", "cnt": "Jumlah pengguna"},
                         color="weekday",
                         category_orders={"weekday": weekday_order},
                         color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_weekday, use_container_width=True)
    #Hubungan suhu dan pengguna sepeda
    st.subheader("🌡️ Hubungan suhu dan jumlah pengguna sepeda")
    fig_temp = px.scatter(filtered_df, x="temp", y="cnt", color="cnt",
                           title="Pengaruh suhu terhadap jumlah pengguna",
                           labels={"temp": "Suhu", "cnt": "Jumlah pengguna"},
                           trendline="ols")
    st.plotly_chart(fig_temp, use_container_width=True)
    #Pola pengguna sepeda berdasarkan jam
    st.subheader("⏰ Pola penggunaan sepeda berdasarkan jam dalam sehari")
    hour_df = pd.read_csv("data/hour.csv")
    hour_df["hr"] = hour_df["hr"].astype(str) + ":00"
    fig_hour = px.line(hour_df.groupby("hr")["cnt"].mean().reset_index(), x="hr", y="cnt",
                        title="Rata-rata pengguna sepeda berdasarkan jam",
                        labels={"hr": "Jam", "cnt": "Jumlah pengguna"},
                        template="plotly_white")
    st.plotly_chart(fig_hour, use_container_width=True)