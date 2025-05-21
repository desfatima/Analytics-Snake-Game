import streamlit as st
import pandas as pd
import requests
import io
import json

st.set_page_config(page_title="Snake Game Dashboard", layout="wide")
st.title("🎮 Snake Game Dashboard")

# 🔗 روابط ملفات Google Drive (تأكدي إنهم عامّين: Anyone with the link)
csv_url = 'https://drive.google.com/uc?export=download&id=1aoUmTcS3oWizYEglhbHlwlmMyXXtdemP'
json_url = 'https://drive.google.com/uc?export=download&id=1pXaFbMJ4CGyM8QMYN9qkgVutIAJpx3Cz'

@st.cache_data
def load_data():
    # تحميل ملف CSV من Google Drive
    csv_response = requests.get(csv_url)
    df_csv = pd.read_csv(io.StringIO(csv_response.text))

    # تحميل ملف JSON من Google Drive
    json_response = requests.get(json_url)
    ngrams_data = json.loads(json_response.text)
    df_ngrams = pd.DataFrame(ngrams_data, columns=["ngram_1", "ngram_2", "ngram_3"])

    # تأكيد تطابق الطول
    min_len = min(len(df_csv), len(df_ngrams))
    df_csv = df_csv.iloc[:min_len].reset_index(drop=True)
    df_ngrams = df_ngrams.iloc[:min_len].reset_index(drop=True)

    # دمج البيانات
    df = pd.concat([df_csv, df_ngrams], axis=1)
    return df

df = load_data()

# عرض البيانات
st.subheader("📊 Merged Game Sessions with N-grams")
st.dataframe(df, use_container_width=True)
