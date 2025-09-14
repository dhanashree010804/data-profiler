import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Profiling Tool", layout="wide")

st.title("📊 Mini Data Profiling Tool")
st.write("Upload a CSV file to get instant profiling: missing values, duplicates, and stats.")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Load CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Preview of Data")
    st.dataframe(df.head())

    # Dataset Info
    st.subheader("📏 Dataset Overview")
    st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    st.write("**Columns:**", list(df.columns))

    # Missing values
    st.subheader("🚨 Missing Values")
    st.write(df.isnull().sum())

    # Duplicates
    st.subheader("📌 Duplicate Rows")
    st.write(f"Total Duplicates: {df.duplicated().sum()}")

    # Summary stats
    st.subheader("📈 Summary Statistics")
    st.write(df.describe(include="all").T)

    # Correlation heatmap
    st.subheader("📊 Correlation Heatmap (Numerical Features)")
    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="Blues", ax=ax)
        st.pyplot(fig)
    else:
        st.write("No numerical columns found.")

    # Column-wise distribution
    st.subheader("📊 Column Distributions")
    col = st.selectbox("Select a column", df.columns)
    fig, ax = plt.subplots(figsize=(6, 4))
    if pd.api.types.is_numeric_dtype(df[col]):
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
    else:
        df[col].value_counts().head(10).plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.success("✅ Data profiling completed!")
else:
    st.info("Please upload a CSV file to begin profiling.")
