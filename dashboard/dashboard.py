import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

st.title("Analisis jumlah User Rental Bike")
st.subheader("Analisis jumlah user reantal bike berdasarkan keadaan lingkungan")
@st.cache_data
def all_data():
    main_df = pd.read_csv('./dashboard/main_data.csv', parse_dates=['dteday'])
    main_df.rename(columns={
        "cnt":"Total_Customer",
        "atemp":"Temperature",
        "casual":"Unregistered",
        "hum":"Humidity"
    },inplace=True)
    return main_df

main_df = all_data()
min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
filter_df = main_df[
    (main_df["dteday"] >= pd.to_datetime(start_date)) & 
    (main_df["dteday"] <= pd.to_datetime(end_date))
]

#Kelembapan

bins= [0, 0.2 ,0.4, 0.6, 0.8, 1]
labels=['0-0.2', '0.21-0.4', '0.41-0.6', '0.61-0.8', '0.81-1.0']
filter_df['Humidity_range'] = pd.cut(filter_df['Humidity'], bins=bins, labels=labels)

groupedhum_df = filter_df.groupby('Humidity_range')['Total_Customer'].sum().reset_index()

fig_kelembapan, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="Total_Customer",
    x="Humidity_range",
    data=groupedhum_df,
    estimator=sum,
    ax=ax
)
ax.set_title('Jumlah Customer Berdasarkan Rentang Kelembapan')
ax.set_xlabel('Rentang Kelembapan setelah di normalisasi')
ax.set_ylabel('Jumlah Pengunjung (Dalam Jutaan)')

#Windspeed
bins= [0, 0.2 ,0.4, 0.6, 0.8, 1]
labels=['0-0.2', '0.21-0.4', '0.41-0.6', '0.61-0.8', '0.81-1.0']
filter_df['Windspeed_range'] = pd.cut(filter_df['windspeed'], bins=bins, labels=labels)

groupedwind_df = filter_df.groupby('Windspeed_range')['Total_Customer'].sum().reset_index()

fig_windspeed, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="Total_Customer",
    x="Windspeed_range",
    data=groupedwind_df,
    estimator=sum
)
ax.set_title('Jumlah Customer Berdasarkan kecepatan angin')
ax.set_xlabel('Kecepatan angin setelah normalisasi')
ax.set_ylabel('Jumlah Pengunjung (Dalam Jutaan)')

#Suhu
bins= [0, 0.2 ,0.4, 0.6, 0.8, 1]
labels=['0-0.2', '0.21-0.4', '0.41-0.6', '0.61-0.8', '0.81-1.0']
filter_df['Temperature_range'] = pd.cut(filter_df['Temperature'], bins=bins, labels=labels)

groupedtemp_df = filter_df.groupby('Temperature_range')['Total_Customer'].sum().reset_index()

fig_suhu, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="Total_Customer",
    x="Temperature_range",
    data=groupedtemp_df,
    estimator=sum
)
ax.set_title('Jumlah Customer Berdasarkan Rentang Suhu')
ax.set_xlabel('Rentang suhu setelah di normalisasi')
ax.set_ylabel('Jumlah Pengunjung (Dalam Jutaan)')
#Cuaca
fig_cuaca, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="Total_Customer",
    x="weathersit",
    data=filter_df,
    estimator=sum
)

weather_labels = {0: "Cerah", 1: "Berawan", 2: "Gerimis", 3: "Hujan Lebat"}

ax.set_title('Jumlah Customer Berdasarkan Cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Pengunjung (Dalam Jutaan)')
ax.set_xticklabels(list(weather_labels.values()))


option = st.selectbox("Pilih Grafik User berdasarkan keadaan", ["Kelembapan", "Suhu", "Windspeed","Cuaca"])

if option == "Kelembapan":
    st.pyplot(fig_kelembapan)
elif option == "Suhu":
    st.pyplot(fig_suhu)
elif option == "Windspeed":
    st.pyplot(fig_windspeed)
elif option == "Cuaca":
    st.pyplot(fig_cuaca)

st.subheader("Analisis jumlah user reantal bike berdasarkan Waktu")
#Jam
fig_hour, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="Total_Customer",
    x="hr",
    data=filter_df,
    estimator=sum
)

ax.set_title('Jumlah Customer Berdasarkan Waktu')
ax.set_xlabel('Time (Hour)')
ax.set_ylabel('Jumlah Pengunjung (Dalam Jutaan)')

#Hari Kerja
fig_days, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="Total_Customer",
    x="workingday",
    data=filter_df,
    estimator=sum
)
days_label = {0: "Bukan Hari Kerja", 1: "Hari Kerja"}
ax.set_title('Jumlah Customer Berdasarkan Waktu')
ax.set_xlabel('Hari')
ax.set_ylabel('Jumlah Pengunjung (Dalam Jutaan)')
ax.set_xticklabels(list(days_label.values()))

option_2 = st.selectbox("Pilih Grafik User berdasarkan ", ["Jam", "Hari kerja",])
if option_2 == "Jam":
    st.pyplot(fig_hour)
elif option_2 == "Hari kerja":
    st.pyplot(fig_days)

st.subheader("Analisis jumlah user reantal bike berdasarkan Jenis user")

Total_Unregistered = filter_df["Unregistered"].sum()
total_registered = filter_df["registered"].sum()
labels = ["Unregistered", "Registered"]
sizes = [Total_Unregistered, total_registered]
colors = ["lightblue", "orange"]

fig_user, ax = plt.subplots(figsize=(6, 6))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, shadow=True)

ax.set_title("Perbandingan Pelanggan Unregistered vs Registered")
st.pyplot(fig_user)

