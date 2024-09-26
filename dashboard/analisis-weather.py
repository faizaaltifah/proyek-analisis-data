import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import geopandas as gpd
import requests
import zipfile
import os
import gdown

st.title('# **Analyzing Weather Data in Dongsi Subdistrict** :sun_with_face::cloud:')
st.write('---------------------------------------------------')

file_id = "1mz9sEtVa9udxzHcOkDGKreS68M0XTdjU"
download_url = f"https://drive.google.com/uc?id={file_id}"

output_zip = "gis_osm_pois_free_1.zip"
gdown.download(download_url, output_zip, quiet=False)

with zipfile.ZipFile(output_zip, 'r') as zip_ref:
    zip_ref.extractall("gis_osm_pois_free_1")
shp_file = None
for root, dirs, files in os.walk("gis_osm_pois_free_1"):
    for file in files:
        if file.endswith(".shp"):
            shp_file = os.path.join(root, file)
            break

if shp_file:
    gdf = gpd.read_file(shp_file)

    fig, ax = plt.subplots()
    gdf.plot(column='fclass', cmap='Set3', edgecolor='black', ax=ax)

    plt.title("Map by Places Types")
    st.pyplot(fig)
    st.write("These are a plots of places types in Beijing."
             " Most of the area are dominated by residential, forest, farmland, park, industrial, grass, commercial, orchard, scrub and retail"
             " ")
    freq = gdf['fclass'].value_counts().reset_index()
    freq_col = ['Places Types', 'Frequency']
    top10 = freq.head(10)
    st.write("Top 10 Places Types")
    st.table(top10)

else:
    st.error("No shapefile found in the zip archive.")

def many_dist(new_file):
    df = pd.read_csv("https://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/PM2.5%20All%20Data.csv")
    average_pm25 = df.groupby('District')['PM2.5'].mean().reset_index()
    average_pm25 = average_pm25.sort_values(by='PM2.5', ascending=False)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='PM2.5', y='District', data=average_pm25, palette='viridis')
    plt.title('Average PM2.5 per District in Beijing', fontsize=15)
    plt.xlabel('PM2.5 Average', fontsize=12)
    plt.ylabel('Distrik', fontsize=12)
    plt.grid(axis='x')
    plt.tight_layout()
    plt.show()

    st.pyplot(plt)

new_files = "https://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/PM2.5%20All%20Data.csv"
st.title("Average PM2.5 per District")
many_dist(new_files)

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
    df = pd.read_csv("https://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/updated%20dongsi%20data.csv")
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
corr_analysis2(csv_file)

def cluster_bin(csv_file):
    df = pd.read_csv("https://raw.githubusercontent.com/faizaaltifah/proyek-analisis-data/refs/heads/main/dashboard/updated%20dongsi%20data.csv")
    plt.figure(figsize=(10, 6))
    df['bin'] = pd.cut(df['PRES'], bins=3, labels=['Low', 'Medium', 'High'])
    df['bin'].value_counts().plot(kind='bar')
    plt.title('Distribution of Pressure')
    plt.xlabel('Pressure')
    plt.ylabel('Frequency')
    plt.show()
    st.pyplot(plt)

st.title("Distribution of Pressure:anchor:")
cluster_bin(csv_file)