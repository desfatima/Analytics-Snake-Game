import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json

st.set_page_config(page_title="Snake Game Dashboard", layout="wide")
st.title("🎮 Game Analytics Dashboard - Snake Game")

# 🔄 تحميل البيانات من Google Drive
csv_url = 'https://drive.google.com/uc?export=download&id=1aoUmTcS3oWizYEglhbHlwlmMyXXtdemP'
json_url = 'https://drive.google.com/uc?export=download&id=1pXaFbMJ4CGyM8QMYN9qkgVutIAJpx3Cz'

@st.cache_data
def load_data():
    df = pd.read_csv(csv_url)
    all_ngrams = json.loads(pd.read_json(json_url).to_json(orient="values"))
    return df, all_ngrams

df, all_ngrams = load_data()

# 📊 بيانات الجلسات
st.header("📋 Player Sessions Data")
st.dataframe(df, use_container_width=True)

# 🎯 عرض التجمعات (Clusters)
if "cluster_label" in df.columns:
    st.header("📍 Player Clusters by Performance")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x="duration_sec", y="applesEaten", hue="cluster_label", palette="coolwarm", s=100, ax=ax)
    ax.set_xlabel("Session Duration (seconds)")
    ax.set_ylabel("Apples Eaten")
    ax.set_title("Clusters Based on Duration & Apples")
    plt.tight_layout()
    st.pyplot(fig)

# 📈 تحليل الأداء
st.header("📉 Player Performance Summary")
failed_counts = df['failed'].value_counts()
col1, col2 = st.columns(2)
with col1:
    st.metric("✅ Good performance", failed_counts.get(0, 0))
with col2:
    st.metric("❌ Failed performance", failed_counts.get(1, 0))

# 🔁 تحليل الأنماط المتكررة
st.header("🔁 Top 10 Most Frequent 3-Move Patterns")
counter = Counter([tuple(x) for x in all_ngrams])
most_common = counter.most_common(10)
for i, (pattern, count) in enumerate(most_common, 1):
    st.write(f"{i}. {' → '.join(pattern)} | Occurrences: {count}")

# 💡 توصيات تصميمية
st.header("💡 Design Recommendations")
failure_rate = df["failed"].mean() * 100
avg_apples_fail = df[df["failed"] == 1]["applesEaten"].mean()
avg_duration_fail = df[df["failed"] == 1]["duration_sec"].mean()
avg_apples_success = df[df["failed"] == 0]["applesEaten"].mean()
avg_duration_success = df[df["failed"] == 0]["duration_sec"].mean()

st.markdown("---")

if failure_rate > 50:
    st.warning(f"🔴 **{failure_rate:.1f}%** of players failed. Consider adding a tutorial in the early game.")

if avg_duration_fail < 20:
    st.info(f"⏱️ Failed players lasted only **{avg_duration_fail:.1f} sec** on average. Consider slowing down the game start.")

if avg_apples_fail < 5:
    st.info(f"🍏 Failed players collected only **{avg_apples_fail:.1f} apples**. Try placing apples closer or more frequently.")

if avg_apples_success > 15 and avg_duration_success > 60:
    st.success(f"🏆 Skilled players average **{avg_apples_success:.1f} apples** and **{avg_duration_success:.1f} sec**. Consider bonus levels or advanced challenges.")
