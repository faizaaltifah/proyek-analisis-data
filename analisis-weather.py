import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import geopandas as gpd
import requests
import zipfile
import os

st.title('# **Analyzing Weather Data in Dongsi Subdistrict** :sun_with_face::cloud:')
st.write('---------------------------------------------------')

url = "https://drive.google.com/uc?id=1LS4yFaH1b4thO0rb7cbakklGEWGnwvID"

try:
    r = requests.get(url)
    r.raise_for_status()
    with open("gadm41_CHN_1.zip", "wb") as f:
        f.write(r.content)

    with zipfile.ZipFile("gadm41_CHN_1.zip", "r") as zip_ref:
        zip_ref.extractall("data") 

    shp_file = [f for f in os.listdir("data") if f.endswith(".shp")][0]
    shp_path = os.path.join("data", shp_file)

    gdf = gpd.read_file(shp_path)

    beijing = gdf[gdf['NAME_1']=='Beijing']
    if beijing.empty:
        st.error("No data")
    else:
        fig, ax = plt.subplots()
        beijing.plot(ax=ax)
        plt.savefig('beijingmap.png')
        st.title("Beijing Map:earth_asia:")
        st.image("beijingmap.png", caption="Beijing Map", use_column_width=True)


except requests.exceptions.RequestException as e:
    st.error(f"Error downloading file: {e}")
except zipfile.BadZipFile:
    st.error("Downloaded file is not a valid zip file.")
except Exception as e:
    st.error(f"An error occurred: {e}")

#shpfile_path = r"https://github.com/faizaaltifah/proyek-analisis-data/blob/main/data/gadm41_CHN_1.shp"

def plot_pm25(csv_file):
    df = pd.read_csv("https://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/updated%20dongsi%20data.csv")
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.set_index('datetime', inplace=True)
    if 'PM2.5' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['PM2.5'], label='PM2.5', color='blue')
        plt.title('PM2.5 Over Time')
        plt.xlabel('Time')
        plt.ylabel('Concentration')
        plt.xticks(rotation=45)
        plt.legend()

        st.pyplot(plt)
    else:
         st.error("No data")

csv_file = "https://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/updated%20dongsi%20data.csv"
st.title('PM2.5 Data Visualization:dash:')
plot_pm25(csv_file)

def plot_pm10(csv_file):
    df = pd.read_csv("https://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/updated%20dongsi%20data.csv")
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.set_index('datetime', inplace=True)
    if 'PM10' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['PM10'], label='PM10', color='green')
        plt.title('PM10 Over Time')
        plt.xlabel('Time')
        plt.ylabel('Concentration')
        plt.xticks(rotation=45)
        plt.legend()

        st.pyplot(plt)
    else:
         st.error("No data")

st.title('PM10 Data Visualization:fog:')
plot_pm10(csv_file)

def avg_temp(csv_file):
    df = pd.read_csv("https://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/updated%20dongsi%20data.csv")
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.set_index('datetime', inplace=True)
    if 'TEMP' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['TEMP'], label=('Temperature'), color='magenta')
        plt.title('Dongsi Average Temperature')
        plt.xlabel('Time')
        plt.ylabel('Temperature')
        plt.xticks(rotation=45)
        plt.legend()

        st.pyplot(plt)
    else:
        st.error('No data')

st.title('Average Temperature Data Visualization:chart_with_upwards_trend:')
avg_temp(csv_file)

def corr_analysis(csv_file):
    df = pd.read_csv("https://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/updated%20dongsi%20data.csv")
    if 'PM2.5' and 'PM10' in df.columns:
        x = 'PM2.5'
        y = 'PM10'

        plt.figure(figsize=(10, 6))
        plt.scatter(df[x], df[y], color='green')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f'{x} vs {y}')
        plt.show()

        st.pyplot(plt)
    else:
        st.error("No data")

st.title("PM2.5 vs PM10")
corr_analysis(csv_file)

def corr_analysis2(csv_file):
    df = pd.read_csv("uhttps://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/updated%20dongsi%20data.csv")
    if 'TEMP' and 'PRES' in df.columns:
        x = 'TEMP'
        y = 'PRES'

        plt.figure(figsize=(10, 6))
        plt.scatter(df[x], df[y], color='#8A2BE2')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f'{x} vs {y}')
        plt.show()

        st.pyplot(plt)
    else:
        st.error("No data")

st.title("Temperature vs Pressure")
corr_analysis(csv_file)

def cluster_bin(csv_file):
    df = pd.read_csv("https://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/updated%20dongsi%20data.csv")
    plt.figure(figsize=(10, 6))
    df['bin'] = pd.cut(df['PRES'], bins=3, labels=['low', 'medium', 'high'])
    df['bin'].value_counts().plot(kind='bar')
    plt.title('Distribution of Pressure')
    plt.xlabel('Pressure')
    plt.ylabel('Frequency')
    plt.show()
    st.pyplot(plt)

st.title("Distribution of Pressure:anchor:")
cluster_bin(csv_file)