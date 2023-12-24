import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Ubah style seaborn
sns.set(style='dark')

# Menyiapkan data df_day
df_day = pd.read_csv("datasets/day.csv")

# Mengubah angka menjadi keterangan
df_day['mnth'] = df_day['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

df_day['season'] = df_day['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

df_day['weekday'] = df_day['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})

df_day['weathersit'] = df_day['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Membuat komponen filter berdasarkan tanggal
min_date = pd.to_datetime(df_day['dteday']).dt.date.min()
max_date = pd.to_datetime(df_day['dteday']).dt.date.max()


# Membuat judul dashboard
st.header('Bike Sharing Dashboard 🚲')

# Sidebar Dashboard (Information)
# Membuat judul sidebar
st.sidebar.title("Bike Sharing Dashboard")

# Mengambil start_date & end_date dari date_input
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value= min_date,
    max_value= max_date,
    value=[min_date, max_date]
)

# Menampilkan fungsi dari dashboard
st.sidebar.title("About")
st.sidebar.info("The dashboard provides visualisation of bike rental data, including information on seasonality, temperature, humidity, and other factors.")


st.sidebar.title("Dataset Bike Sharing")
# Menampilkan dataset asli
if st.sidebar.checkbox("Show Dataset"):
    st.subheader("Raw Data")
    st.write(df_day)

# Menampilkan summary statistics dari dataset
if st.sidebar.checkbox("Show Summary Statistics"):
    st.subheader("Summary Statistics")
    st.write(df_day.describe())

# Menampilkan sumber dataset
st.sidebar.markdown("[Download Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)")


# Membuat isi dashboard
main_df = df_day[(df_day['dteday'] >= str(start_date)) & 
                (df_day['dteday'] <= str(end_date))]


# Membuat jumlah penyewaan harian berdasarkan casual, registered, dan total users
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_casual_rent_df = main_df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value= daily_rent_casual)

with col2:
    daily_registered_rent_df = main_df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()

    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value= daily_rent_registered)

with col3:
    daily_rent_df = main_df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    
    daily_rent_total = daily_rent_df['cnt'].sum()
    st.metric('Total User', value= daily_rent_total)


# Membuat jumlah penyewaan bulanan
st.subheader('Monthly Rentals')
ordered_mnths = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]

monthly_rent_df = main_df.groupby(by='mnth').agg({
        'cnt': 'sum'
    })
monthly_rent_df = monthly_rent_df.reindex(ordered_mnths, fill_value=0)
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['cnt'],
    marker='o', 
    linewidth=5,
    color='tab:blue'
)

for index, row in enumerate(monthly_rent_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=15)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)


# Membuat jumlah penyewaan berdasarkan musim pada casual dan registered users
st.subheader('Seasonly Rentals')

season_rent_df = main_df.groupby(by='season')[['registered', 'casual']].sum().reset_index()

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='tab:blue',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='tab:orange',
    ax=ax
)

for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=15)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=15)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)


# Membuah jumlah penyewaan berdasarkan kondisi cuaca
st.subheader('Weatherly Rentals')

weather_rent_df = main_df.groupby(by='weathersit').agg({
        'cnt': 'sum'
    })

fig, ax = plt.subplots(figsize=(16, 8))

colors=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['cnt'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_rent_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=15)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)


# Membuat jumlah penyewaan berdasarkan weekday, working dan holiday
st.subheader('Weekday, Workingday, and Holiday Rentals')

weekday_rent_df = main_df.groupby(by='weekday').agg({
        'cnt': 'sum'
    }).reset_index()

workingday_rent_df = main_df.groupby(by='workingday').agg({
        'cnt': 'sum'
    }).reset_index()

holiday_rent_df = main_df.groupby(by='holiday').agg({
        'cnt': 'sum'
    }).reset_index()

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,10))

colors1=["tab:blue", "tab:orange"]
colors2=["tab:blue", "tab:orange"]
colors3=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

# Berdasarkan workingday
sns.barplot(
    x='workingday',
    y='cnt',
    data=workingday_rent_df,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(workingday_rent_df['cnt']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=15)

axes[0].set_title('Number of Rents based on Working Day')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Berdasarkan holiday
sns.barplot(
    x='holiday',
    y='cnt',
    data=holiday_rent_df,
    palette=colors2,
    ax=axes[1]
)

for index, row in enumerate(holiday_rent_df['cnt']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=15)

axes[1].set_title('Number of Rents based on Holiday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Berdasarkan weekday
sns.barplot(
    x='weekday',
    y='cnt',
    data=weekday_rent_df,
    palette=colors3,
    ax=axes[2]
)

for index, row in enumerate(weekday_rent_df['cnt']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=15)

axes[2].set_title('Number of Rents based on Weekday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright (c) Gede Satyamahinsa Prastita Uttama 2023')