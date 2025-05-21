import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json

st.title("📊 Game Analytics Dashboard - Snake Game")

# ✅ تحميل البيانات كاملة
df = pd.read_csv("data.csv")

# ✅ حذف عمود movements فقط من العرض (مش من الملف)
if "movements" in df.columns:
    df_preview = df.drop(columns=["movements"])
else:
    df_preview = df.copy()

# ✅ تحميل ملف الأنماط الثلاثية
with open("ngrams.json", "r") as f:
    all_ngrams = json.load(f)

# ✅ عرض البيانات (بدون movements)
st.header("🧾 Player Sessions Data")
st.dataframe(df_preview, height=600)

# ✅ تحليل التجمعات (لو فيه clustering)
if "cluster_label" in df.columns:
    st.header("🧠 Player Clusters by Performance")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x="duration_sec",
        y="applesEaten",
        hue="cluster_label",
        palette="coolwarm",
        s=100,
        ax=ax
    )
    plt.xlabel("Session Duration (seconds)")
    plt.ylabel("Apples Eaten")
    plt.title("Player Clustering (K-Means)")
    st.pyplot(fig)

# ✅ ملخص الأداء
st.header("🎯 Player Performance")
failed_counts = df["failed"].value_counts()
st.write(f"✅ Successful players: {failed_counts.get(0, 0)}")
st.write(f"❌ Failed players: {failed_counts.get(1, 0)}")

# ✅ أنماط الحركات الثلاثية
st.header("🔁 Top 10 Most Frequent 3-Move Patterns")
counter = Counter([tuple(x) for x in all_ngrams])
most_common = counter.most_common(10)
for pattern, count in most_common:
    st.write(" → ".join(pattern), f"| Occurrences: {count}")

# ✅ التوصيات بناءً على التحليل
st.header("💡 Design Recommendations")
failure_rate = df["failed"].mean() * 100
avg_apples_fail = df[df["failed"] == 1]["applesEaten"].mean()
avg_duration_fail = df[df["failed"] == 1]["duration_sec"].mean()
avg_apples_success = df[df["failed"] == 0]["applesEaten"].mean()
avg_duration_success = df[df["failed"] == 0]["duration_sec"].mean()

if failure_rate > 50:
    st.write(f"🔴 {failure_rate:.1f}% of players failed. Consider adding a tutorial early in the game.")
if avg_duration_fail < 20:
    st.write(f"⏱️ Failed players lasted only {avg_duration_fail:.1f} seconds. Consider slowing down game start.")
if avg_apples_fail < 5:
    st.write(f"🍏 Failed players collected only {avg_apples_fail:.1f} apples. Try placing apples closer at the beginning.")
if avg_apples_success > 15 and avg_duration_success > 60:
    st.write(f"🏆 High performers ate {avg_apples_success:.1f} apples in {avg_duration_success:.1f} seconds. Add bonus levels or speed challenges.")
