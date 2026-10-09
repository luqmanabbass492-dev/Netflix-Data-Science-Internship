import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Netflix Data Dashboard", page_icon="🎬", layout="wide")

# Title
st.title("🎬 Netflix Data Science Dashboard")
st.markdown("### Auspify Data Science Internship Project")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_cleaned.csv')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
content_type = st.sidebar.multiselect(
    "Select Content Type:",
    options=df['type'].unique(),
    default=df['type'].unique()
)

filtered_df = df[df['type'].isin(content_type)]

# ============ SECTION 1: OVERVIEW ============
st.header("📊 Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Titles", f"{len(filtered_df):,}")
col2.metric("Movies", f"{(filtered_df['type']=='Movie').sum():,}")
col3.metric("TV Shows", f"{(filtered_df['type']=='TV Show').sum():,}")
col4.metric("Countries", f"{filtered_df['country'].nunique():,}")

st.markdown("---")

# ============ SECTION 2: MOVIES VS TV SHOWS ============
st.header("🎭 Movies vs TV Shows")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    type_counts = filtered_df['type'].value_counts()
    ax.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%',
           colors=['#FF6B6B', '#4ECDC4'], startangle=90)
    ax.set_title('Content Type Distribution')
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(x='type', data=filtered_df, palette='Set2', ax=ax)
    ax.set_title('Movies vs TV Shows Count')
    ax.set_xlabel('Type')
    ax.set_ylabel('Count')
    st.pyplot(fig)

st.markdown("---")

# ============ SECTION 3: TOP COUNTRIES ============
st.header("🌍 Top 10 Countries")

top_countries = filtered_df['country'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis', ax=ax)
ax.set_title('Top 10 Countries with Most Content', fontsize=14, fontweight='bold')
ax.set_xlabel('Number of Titles')
st.pyplot(fig)

st.markdown("---")

# ============ SECTION 4: CONTENT TREND ============
st.header("📈 Content Release Trend")

yearly = filtered_df['release_year'].value_counts().sort_index()
yearly = yearly[yearly.index >= 2000]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(yearly.index, yearly.values, marker='o', color='crimson', linewidth=2)
ax.set_title('Content Release Trend (2000-2021)', fontsize=14, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Titles')
ax.grid(True, alpha=0.3)
st.pyplot(fig)

st.markdown("---")

# ============ SECTION 5: TOP GENRES ============
st.header("🎬 Top 10 Genres")

top_genres = filtered_df['listed_in'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_genres.values, y=top_genres.index, palette='magma', ax=ax)
ax.set_title('Top 10 Genres on Netflix', fontsize=14, fontweight='bold')
ax.set_xlabel('Number of Titles')
st.pyplot(fig)

st.markdown("---")

# ============ SECTION 6: RATINGS ============
st.header("⭐ Ratings Distribution")

rating_counts = filtered_df['rating'].value_counts().head(8)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=rating_counts.index, y=rating_counts.values, palette='pastel', ax=ax)
ax.set_title('Content Ratings Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Rating')
ax.set_ylabel('Count')
plt.xticks(rotation=45)
st.pyplot(fig)

st.markdown("---")

# ============ SECTION 7: KEY INSIGHTS ============
st.header("📌 Key Business Insights")

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
    **📊 Content Statistics:**
    - Total Titles: {len(filtered_df):,}
    - Top Country: {filtered_df['country'].value_counts().index[0]}
    - Top Genre: {filtered_df['listed_in'].value_counts().index[0]}
    - Top Rating: {filtered_df['rating'].value_counts().index[0]}
    """)

with col2:
    st.success(f"""
    **📈 Trends:**
    - Latest Release: {filtered_df['release_year'].max()}
    - Earliest Release: {filtered_df['release_year'].min()}
    - Peak Year: {filtered_df['release_year'].value_counts().idxmax()}
    - Avg Release Year: {int(filtered_df['release_year'].mean())}
    """)

st.markdown("---")
st.markdown("**Made with ❤️ by Luqman Abbas | Auspify Data Science Internship**")