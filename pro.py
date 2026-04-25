# AI-Powered Email Classification and Insights System

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import altair as alt

st.set_page_config(
    page_title="AI-Powered Email Sorting System",
    page_icon="📧",
    layout="wide"
)

engine = create_engine("sqlite:///emails.db")

@st.cache_data
def load_emails():
    try:
        df = pd.read_sql("SELECT * FROM emails", engine)
        return df
    except:
        return pd.DataFrame(columns=["subject", "sender", "category", "body", "date"])


keywords = {
    "Customer Support": ["help", "issue", "password", "login", "reset"],
    "Sales Inquiry": ["price", "quote", "offer", "purchase", "discount"],
    "Complaint": ["complaint", "bad", "poor", "unhappy", "refund"]
}

def classify_with_confidence(subject, body):
    text = (subject + " " + body).lower()
    scores = {}
    for category, words in keywords.items():
        match_count = sum(word in text for word in words)
        scores[category] = (match_count / len(words)) * 100  # %
    best_category = max(scores, key=scores.get)
    return best_category, scores[best_category]


def fetch_dummy_emails():
    test_emails = [
        ("Need help with account", "Hello, I need help with my login."),
        ("Request for price", "Could you send me your latest price list?"),
        ("Complaint about service", "I am unhappy with the last order."),
        ("Just saying hi", "This is a test email.")
    ]

    all_data = []
    for subject, body in test_emails:
        category, _ = classify_with_confidence(subject, body)  # Don't save confidence
        all_data.append({
            "subject": subject,
            "sender": "dummy_account@gmail.com",
            "category": category,
            "body": body,
            "date": datetime.now()
        })
    pd.DataFrame(all_data).to_sql("emails", engine, if_exists="append", index=False)

st.title("📧 AI-Powered Email Sorting System")
st.markdown("Automatically categorize incoming emails into **Customer Support**, **Sales Inquiry**, and **Complaint** with insights from confidence scores (calculated live).")

# Sidebar Controls
st.sidebar.header("Controls")
if st.sidebar.button("Fetch New Emails"):
    fetch_dummy_emails()
    st.sidebar.success("Fetched, classified, and saved new emails!")

category_filter = st.sidebar.selectbox(
    "Filter by Category",
    options=["All", "Customer Support", "Sales Inquiry", "Complaint"]
)

df = load_emails()

if category_filter != "All" and not df.empty:
    df = df[df["category"] == category_filter]

if df.empty:
    st.warning("No emails found. Click **Fetch New Emails** to start.")
else:
    # Calculate confidence dynamically
    df["confidence"] = df.apply(
        lambda row: classify_with_confidence(row["subject"], row["body"])[1],
        axis=1
    )

    st.subheader("📋 Email Table")
    st.dataframe(df)

    # Insights - Category Distribution
    st.subheader("📊 Category Distribution")
    chart = alt.Chart(df).mark_bar().encode(
        x='category',
        y='count()',
        color='category'
    )
    st.altair_chart(chart, use_container_width=True)

    # Insights - Confidence Scores Over Time
    st.subheader("📈 Confidence Scores Over Time")
    line_chart = alt.Chart(df).mark_line(point=True).encode(
        x='date:T',
        y='confidence:Q',
        color='category'
    )
    st.altair_chart(line_chart, use_container_width=True)

    # Insights after the confidence graph
    st.subheader("💡 Insights from Email Classification")

    avg_conf_per_cat = df.groupby("category")["confidence"].mean()
    top_cat = avg_conf_per_cat.idxmax()
    top_conf = avg_conf_per_cat.max()

    most_freq_cat = df["category"].value_counts().idxmax()
    most_freq_count = df["category"].value_counts().max()

    st.markdown(f"✅ **Highest Average Confidence:** `{top_cat}` ({top_conf:.2f}%)")
    st.markdown(f"📨 **Most Frequent Category:** `{most_freq_cat}` ({most_freq_count} emails)")

    if df["confidence"].iloc[-1] > df["confidence"].iloc[0]:
        st.markdown("📈 Confidence scores are **increasing over time**.")
    else:
        st.markdown("📉 Confidence scores are **decreasing or stable**.")


st.markdown("---")
st.caption("Prototype by Jagrati Sharma — AI-Powered Email Sorting Demo")
