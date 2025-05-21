import streamlit as st
import pandas as pd
import requests
import io
import json

st.title("🎮 Snake Game Dashboard")

# 🔗 روابط الملفات
csv_url = 'https://drive.google.com/uc?export=download&id=1aoUmTcS3oWizYEglhbHlwlmMyXXtdemP'
json_url = 'https://drive.google.com/uc?export=download&id=1pXaFbMJ4CGyM8QMYN9qkgVutIAJpx3Cz'

@st.cache_data
def load_data():
    csv_response = requests.get(csv_url)
    df_csv = pd.read_csv(io.StringIO(csv_response.text))

    json_response = requests.get(json_url)
    ngrams_list = json.loads(json_response.text)
    df_ngrams = pd.DataFrame(ngrams_list)

    df = pd.concat([df_csv, df_ngrams], axis=1)
    return df

df = load_data()

st.subheader("📊 Merged Data Preview")
st.dataframe(df)
