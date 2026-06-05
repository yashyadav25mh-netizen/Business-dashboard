import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

st.set_page_config(
    page_title="Business Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Performance Dashboard")
st.markdown("**Managing Digital Transformation** | IFHE Hyderabad")
st.markdown("---")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/sanjayfuloria/business-dashboard/main/sales_data.csv"
    return pd.read_csv(url)

df = load_data()

st.sidebar.header("Filters")
months = st.sidebar.multiselect(
    "Select Months",
    options=df["Month"].tolist(),
    default=df["Month"].tolist()
)
df_filtered = df[df["Month"].isin(months)]

st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales",       f"Rs. {df_filtered['Sales'].sum():,.0f}")
col2.metric("Total Expenses",    f"Rs. {df_filtered['Expenses'].sum():,.0f}")
col3.metric("Total Profit",      f"Rs. {df_filtered['Profit'].sum():,.0f}")
col4.metric("Avg Profit Margin", f"{(df_filtered['Profit']/df_filtered['Sales']*100).mean():.1f}%")

st.markdown("---")
st.subheader("Charts")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Monthly Sales**")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.bar(df_filtered["Month"], df_filtered["Sales"], color="steelblue", alpha=0.85)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x/1000:.0f}K"))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig1)

with col_b:
    st.markdown("**Profit Trend**")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(df_filtered["Month"], df_filtered["Profit"], color="green", marker="o", linewidth=2)
    ax2.fill_between(range(len(df_filtered)), df_filtered["Profit"], alpha=0.2, color="green")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x/1000:.0f}K"))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig2)

col_c, col_d = st.columns(2)

with col_c:
    st.markdown("**Sales vs Expenses**")
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    x = range(len(df_filtered["Month"]))
    ax3.bar([i - 0.2 for i in x], df_filtered["Sales"],    0.4, label="Sales",    color="steelblue")
    ax3.bar([i + 0.2 for i in x], df_filtered["Expenses"], 0.4, label="Expenses", color="tomato")
    ax3.set_xticks(list(x))
    ax3.set_xticklabels(df_filtered["Month"], rotation=45)
    ax3.legend()
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x/1000:.0f}K"))
    plt.tight_layout()
    st.pyplot(fig3)

with col_d:
    st.markdown("**Profit Margin %**")
    df_filtered = df_filtered.copy()
    df_filtered["Margin"] = (df_filtered["Profit"] / df_filtered["Sales"] * 100).round(1)
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    ax4.plot(df_filtered["Month"], df_filtered["Margin"], color="darkorange", marker="s", linewidth=2)
    ax4.set_ylabel("Margin (%)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig4)

st.markdown("---")

with st.expander("View Raw Data"):
    st.dataframe(df_filtered, use_container_width=True)

st.caption("Built with Streamlit | Data loaded from GitHub | IFHE Hyderabad — Managing Digital Transformation")
