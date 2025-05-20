import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json

# عنوان رئيسي للواجهة
st.title("📊 Game Analytics Dashboard - Snake Game")

# تحميل البيانات
df = pd.read_csv("data.csv")
with open("ngrams.json", "r") as f:
    all_ngrams = json.load(f)

# عرض جدول الجلسات
st.header("🧾 Player Sessions Data")
st.dataframe(df, height=600)

# عرض الكتل (Clusters) إذا متوفرة
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

# أداء اللاعبين (ناجح × فاشل)
st.header("🎯 Player Performance")
failed_counts = df["failed"].value_counts()
st.write(f"✅ Successful players: {failed_counts.get(0, 0)}")
st.write(f"❌ Failed players: {failed_counts.get(1, 0)}")

# عرض أنماط الحركة الأكثر تكرارًا
st.header("🔁 Top 10 Most Frequent 3-Move Patterns")
counter = Counter([tuple(x) for x in all_ngrams])
most_common = counter.most_common(10)
for pattern, count in most_common:
    st.write(" → ".join(pattern), f" | Occurrences: {count}")

# التوصيات الذكية بناء على التحليل
st.header("💡 Design Recommendations")
failure_rate = df["failed"].mean() * 100
avg_apples_fail = df[df["failed"] == 1]["applesEaten"].mean()
avg_duration_fail = df[df["failed"] == 1]["duration_sec"].mean()
avg_apples_success = df[df["failed"] == 0]["applesEaten"].mean()
avg_duration_success = df[df["failed"] == 0]["duration_sec"].mean()

if failure_rate > 50:
    st.write(f"🔴 {failure_rate:.1f}% of players failed. Consider adding a tutorial in the early game.")
if avg_duration_fail < 20:
    st.write(f"⏱️ Failed players lasted only {avg_duration_fail:.1f} seconds on average. Consider slowing down game start.")
if avg_apples_fail < 5:
    st.write(f"🍏 Players who failed collected only {avg_apples_fail:.1f} apples. Try placing apples closer or more frequently.")
if avg_apples_success > 15 and avg_duration_success > 60:
    st.write(f"🏆 Skilled players played long sessions with {avg_apples_success:.1f} apples. Consider adding advanced challenges or bonus levels.")
