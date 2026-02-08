"""
Shopify Sales Performance Dashboard
====================================
A professional, interactive sales analytics dashboard for a beauty & skincare
e‑commerce store.  Built with Streamlit + Plotly.
"""

import os
import subprocess
import sys

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Shopify Sales Dashboard",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0');

/* ---------- root variables ---------- */
:root {
    --bg: #f4f1ee;
    --card-bg: #ffffff;
    --primary: #c06078;
    --primary-light: #f8e8ec;
    --text: #2e2e2e;
    --text-muted: #777777;
    --border: #e8e2dd;
    --shadow: 0 2px 12px rgba(0,0,0,0.06);
    --radius: 12px;
}

/* ---------- global ---------- */
html, body, [class*="stApp"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--primary) !important;
}
/* Clean sidebar selectbox and radio styling */
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: var(--text) !important;
}

/* ---------- KPI cards ---------- */
div[data-testid="stMetric"] {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 22px;
    box-shadow: var(--shadow);
}
div[data-testid="stMetric"] label {
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    white-space: nowrap;
    overflow: visible !important;
    text-overflow: unset !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-weight: 700 !important;
    font-size: 1.35rem !important;
    white-space: nowrap;
    overflow: visible !important;
    text-overflow: unset !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
}

/* ---------- chart containers ---------- */
div[data-testid="stPlotlyChart"] {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 10px;
    box-shadow: var(--shadow);
}

/* ---------- headings ---------- */
.dashboard-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 2px;
}
.dashboard-subtitle {
    font-size: 0.95rem;
    color: var(--text-muted);
    margin-bottom: 24px;
}
.section-header {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
    margin: 0 0 4px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-desc {
    font-size: 0.88rem;
    color: var(--text-muted);
    margin: 0 0 18px 0;
    line-height: 1.4;
}

/* ---------- segment card ---------- */
.segment-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 28px 24px 18px 24px;
    box-shadow: var(--shadow);
    margin-bottom: 24px;
}

/* material icon helper */
.mi {
    font-family: 'Material Symbols Rounded';
    font-size: 20px;
    vertical-align: middle;
    color: var(--primary);
}

/* ---------- misc ---------- */
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 18px 0;
}

/* Hide default Streamlit footer & menu, but keep sidebar toggle visible */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: transparent !important;
    backdrop-filter: none !important;
}
header[data-testid="stHeader"] .stAppDeployButton,
header[data-testid="stHeader"] [data-testid="stStatusWidget"] {
    visibility: hidden;
}

/* ---------- tab styling ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500;
    font-size: 0.88rem;
    padding: 8px 20px;
    border-radius: 8px 8px 0 0;
}
/* Material icons before each tab label */
.stTabs [data-baseweb="tab"] p::before {
    font-family: 'Material Symbols Rounded';
    margin-right: 6px;
    vertical-align: middle;
    font-size: 18px;
    color: var(--primary);
}
.stTabs [data-baseweb="tab"]:nth-child(1) p::before {
    content: 'trending_up';
}
.stTabs [data-baseweb="tab"]:nth-child(2) p::before {
    content: 'inventory_2';
}
.stTabs [data-baseweb="tab"]:nth-child(3) p::before {
    content: 'groups';
}
.stTabs [data-baseweb="tab"]:nth-child(4) p::before {
    content: 'sell';
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "shopify_orders.csv")


@st.cache_data(show_spinner="Loading order data …")
def load_data() -> pd.DataFrame:
    if not os.path.exists(DATA_PATH):
        subprocess.check_call([sys.executable, "generate_data.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    df["unit_price"] = df["unit_price"].astype(float)
    df["total_price"] = df["total_price"].astype(float)
    df["discount_amount"] = df["discount_amount"].astype(float)
    df["shipping_cost"] = df["shipping_cost"].astype(float)
    df["order_month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    df["order_weekday"] = df["order_date"].dt.day_name()
    df["order_hour"] = df["order_date"].dt.hour
    return df


df_raw = load_data()

# ---------------------------------------------------------------------------
# Color palette (beauty / rose‑gold theme)
# ---------------------------------------------------------------------------
PALETTE = [
    "#c06078", "#e8a0b0", "#7c9885", "#d4a574",
    "#8facc0", "#c9b8d9", "#e6c88a", "#9cb3a0",
    "#d98a94", "#a0c4d8",
]
COLORSCALE = "RdPu"

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<h2 style="margin-top:0"><span class="mi">filter_alt</span> Filters</h2>',
        unsafe_allow_html=True,
    )

    # --- Date range ---
    min_date = df_raw["order_date"].min().date()
    max_date = df_raw["order_date"].max().date()
    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.markdown("")

    # --- Product category (selectbox with "All" option) ---
    all_categories = sorted(df_raw["product_category"].unique())
    cat_options = ["All Categories"] + all_categories
    cat_choice = st.selectbox("Product Category", cat_options, index=0)
    selected_cats = all_categories if cat_choice == "All Categories" else [cat_choice]

    # --- Country (selectbox with "All" option) ---
    all_countries = sorted(df_raw["customer_country"].unique())
    country_options = ["All Countries"] + all_countries
    country_choice = st.selectbox("Country", country_options, index=0)
    selected_countries = all_countries if country_choice == "All Countries" else [country_choice]

    # --- Order status (selectbox with "All" option) ---
    all_statuses = sorted(df_raw["order_status"].unique())
    status_options = ["All Statuses"] + all_statuses
    status_choice = st.selectbox("Order Status", status_options, index=0)
    selected_statuses = all_statuses if status_choice == "All Statuses" else [status_choice]

    st.markdown("---")
    st.caption("Shopify Sales Dashboard  ·  Demo")

# ---------------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------------
if len(date_range) == 2:
    start_dt, end_dt = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_dt, end_dt = pd.Timestamp(min_date), pd.Timestamp(max_date)

df = df_raw[
    (df_raw["order_date"] >= start_dt)
    & (df_raw["order_date"] <= end_dt + pd.Timedelta(days=1))
    & (df_raw["product_category"].isin(selected_cats))
    & (df_raw["customer_country"].isin(selected_countries))
    & (df_raw["order_status"].isin(selected_statuses))
].copy()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="dashboard-title">'
    '<span class="mi">storefront</span>  Shopify Sales Dashboard'
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="dashboard-subtitle">Beauty &amp; Skincare Store  ·  Performance overview of sales data</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------------------
total_revenue = df["total_price"].sum()
total_orders = len(df)
avg_order_value = df["total_price"].mean() if total_orders else 0
best_product = df.groupby("product_name")["total_price"].sum().idxmax() if total_orders else "—"
total_customers = df["customer_id"].nunique() if total_orders else 0

# Simple delta: compare last 30 days vs prior 30 days in filtered set
last_30 = df[df["order_date"] >= df["order_date"].max() - pd.Timedelta(days=30)]
prev_30 = df[
    (df["order_date"] >= df["order_date"].max() - pd.Timedelta(days=60))
    & (df["order_date"] < df["order_date"].max() - pd.Timedelta(days=30))
]
rev_delta = None
if len(prev_30) and prev_30["total_price"].sum():
    rev_delta = f"{(last_30['total_price'].sum() / prev_30['total_price'].sum() - 1) * 100:+.1f}%"

orders_delta = None
if len(prev_30):
    orders_delta = f"{(len(last_30) / len(prev_30) - 1) * 100:+.1f}%"

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Revenue", f"${total_revenue:,.0f}", delta=rev_delta)
k2.metric("Total Orders", f"{total_orders:,}", delta=orders_delta)
k3.metric("Avg Order Value", f"${avg_order_value:,.2f}")
k4.metric("Best‑Selling Product", best_product)
k5.metric("Unique Customers", f"{total_customers:,}")

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Helper: consistent chart layout
# ---------------------------------------------------------------------------

def _layout(fig, height=400, **kwargs):
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Inter, sans-serif", size=12, color="#2e2e2e"),
        height=height,
        margin=dict(l=40, r=20, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
        **kwargs,
    )
    return fig


# ===========================================================================
# TABBED DASHBOARD SEGMENTS
# ===========================================================================
tab_sales, tab_products, tab_customers, tab_discounts = st.tabs([
    "Sales Trends",
    "Products",
    "Customers & Payments",
    "Discounts & Value",
])

# ---------------------------------------------------------------------------
# TAB 1: Sales Trends
# ---------------------------------------------------------------------------
with tab_sales:
    st.markdown(
        '<div class="section-header">'
        '<span class="mi">trending_up</span> Sales Performance'
        '</div>'
        '<div class="section-desc">'
        'Track revenue growth and order volume over time to identify trends and seasonality.'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    # Revenue over time (area chart)
    with c1:
        rev_monthly = (
            df.groupby("order_month")["total_price"]
            .sum()
            .reset_index()
            .rename(columns={"order_month": "Month", "total_price": "Revenue"})
        )
        fig1 = px.area(
            rev_monthly, x="Month", y="Revenue",
            title="Revenue Over Time",
            color_discrete_sequence=[PALETTE[0]],
        )
        fig1.update_traces(line_shape="spline", fill="tozeroy", fillcolor="rgba(192,96,120,0.12)")
        _layout(fig1)
        st.plotly_chart(fig1, use_container_width=True)

    # Orders per month (bar chart)
    with c2:
        orders_monthly = (
            df.groupby("order_month")["order_id"]
            .count()
            .reset_index()
            .rename(columns={"order_month": "Month", "order_id": "Orders"})
        )
        fig2 = px.bar(
            orders_monthly, x="Month", y="Orders",
            title="Orders Per Month",
            color_discrete_sequence=[PALETTE[2]],
        )
        _layout(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # --- When Customers Buy (heatmap + order status) ---
    st.markdown(
        '<div class="section-header">'
        '<span class="mi">schedule</span> When Customers Buy'
        '</div>'
        '<div class="section-desc">'
        'Identify peak shopping hours and days to optimize marketing and staffing.'
        '</div>',
        unsafe_allow_html=True,
    )

    c7, c8 = st.columns(2)

    # Day × Hour heatmap
    with c7:
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heatmap_data = (
            df.groupby(["order_weekday", "order_hour"])["order_id"]
            .count()
            .reset_index()
            .rename(columns={"order_weekday": "Day", "order_hour": "Hour", "order_id": "Orders"})
        )
        heatmap_pivot = heatmap_data.pivot(index="Day", columns="Hour", values="Orders").fillna(0)
        heatmap_pivot = heatmap_pivot.reindex(day_order)

        fig7 = go.Figure(
            data=go.Heatmap(
                z=heatmap_pivot.values,
                x=[f"{h}:00" for h in heatmap_pivot.columns],
                y=heatmap_pivot.index,
                colorscale="RdPu",
                hoverongaps=False,
            )
        )
        fig7.update_layout(title="Orders by Day & Hour")
        _layout(fig7, height=380)
        st.plotly_chart(fig7, use_container_width=True)

    # Order status breakdown (bar)
    with c8:
        status_counts = (
            df["order_status"]
            .value_counts()
            .reset_index()
            .rename(columns={"order_status": "Status", "count": "Orders"})
        )
        fig8 = px.bar(
            status_counts, x="Orders", y="Status", orientation="h",
            title="Orders by Status",
            color="Status",
            color_discrete_sequence=PALETTE,
        )
        fig8.update_layout(showlegend=False)
        _layout(fig8, height=380)
        st.plotly_chart(fig8, use_container_width=True)


# ---------------------------------------------------------------------------
# TAB 2: Products
# ---------------------------------------------------------------------------
with tab_products:
    st.markdown(
        '<div class="section-header">'
        '<span class="mi">category</span> Product Performance'
        '</div>'
        '<div class="section-desc">'
        'Discover top-selling products and see how revenue distributes across categories.'
        '</div>',
        unsafe_allow_html=True,
    )

    c3, c4 = st.columns(2)

    # Top 10 products by revenue (horizontal bar)
    with c3:
        top10 = (
            df.groupby("product_name")["total_price"]
            .sum()
            .nlargest(10)
            .sort_values()
            .reset_index()
            .rename(columns={"product_name": "Product", "total_price": "Revenue"})
        )
        fig3 = px.bar(
            top10, x="Revenue", y="Product", orientation="h",
            title="Top 10 Products by Revenue",
            color_discrete_sequence=[PALETTE[0]],
        )
        _layout(fig3, height=420)
        st.plotly_chart(fig3, use_container_width=True)

    # Revenue by category (donut)
    with c4:
        cat_rev = (
            df.groupby("product_category")["total_price"]
            .sum()
            .reset_index()
            .rename(columns={"product_category": "Category", "total_price": "Revenue"})
            .sort_values("Revenue", ascending=False)
        )
        fig4 = px.pie(
            cat_rev, names="Category", values="Revenue",
            title="Revenue by Category",
            color_discrete_sequence=PALETTE,
            hole=0.45,
        )
        fig4.update_traces(textinfo="percent+label", textposition="outside")
        _layout(fig4, height=420)
        st.plotly_chart(fig4, use_container_width=True)


# ---------------------------------------------------------------------------
# TAB 3: Customers & Payments
# ---------------------------------------------------------------------------
with tab_customers:
    st.markdown(
        '<div class="section-header">'
        '<span class="mi">public</span> Customer Geography'
        '</div>'
        '<div class="section-desc">'
        'Understand where your customers are located and which payment methods they prefer.'
        '</div>',
        unsafe_allow_html=True,
    )

    c5, c6 = st.columns(2)

    # Revenue by country (bar chart)
    with c5:
        country_rev = (
            df.groupby("customer_country")["total_price"]
            .sum()
            .nlargest(10)
            .sort_values()
            .reset_index()
            .rename(columns={"customer_country": "Country", "total_price": "Revenue"})
        )
        fig5 = px.bar(
            country_rev, x="Revenue", y="Country", orientation="h",
            title="Top 10 Countries by Revenue",
            color_discrete_sequence=[PALETTE[4]],
        )
        _layout(fig5, height=400)
        st.plotly_chart(fig5, use_container_width=True)

    # Payment method breakdown (pie)
    with c6:
        pay_rev = (
            df.groupby("payment_method")["total_price"]
            .sum()
            .reset_index()
            .rename(columns={"payment_method": "Method", "total_price": "Revenue"})
            .sort_values("Revenue", ascending=False)
        )
        fig6 = px.pie(
            pay_rev, names="Method", values="Revenue",
            title="Revenue by Payment Method",
            color_discrete_sequence=PALETTE,
            hole=0.45,
        )
        fig6.update_traces(textinfo="percent+label", textposition="outside")
        _layout(fig6, height=400)
        st.plotly_chart(fig6, use_container_width=True)


# ---------------------------------------------------------------------------
# TAB 4: Discounts & Value Trends
# ---------------------------------------------------------------------------
with tab_discounts:
    st.markdown(
        '<div class="section-header">'
        '<span class="mi">local_offer</span> Discounts &amp; Order Value'
        '</div>'
        '<div class="section-desc">'
        'Monitor discount code usage and track how the average order value evolves over time.'
        '</div>',
        unsafe_allow_html=True,
    )

    c9, c10 = st.columns(2)

    # Discount code usage (bar)
    with c9:
        disc_df = df[df["discount_code"] != ""].copy()
        if len(disc_df):
            disc_counts = (
                disc_df["discount_code"]
                .value_counts()
                .reset_index()
                .rename(columns={"discount_code": "Code", "count": "Times Used"})
            )
            fig9 = px.bar(
                disc_counts, x="Times Used", y="Code", orientation="h",
                title="Most Popular Discount Codes",
                color_discrete_sequence=[PALETTE[3]],
            )
            _layout(fig9, height=380)
            st.plotly_chart(fig9, use_container_width=True)
        else:
            st.info("No discount codes used in the selected period.")

    # Average order value trend (line)
    with c10:
        aov_monthly = (
            df.groupby("order_month")["total_price"]
            .mean()
            .reset_index()
            .rename(columns={"order_month": "Month", "total_price": "AOV"})
        )
        fig10 = px.line(
            aov_monthly, x="Month", y="AOV",
            title="Average Order Value Over Time",
            color_discrete_sequence=[PALETTE[5]],
            markers=True,
        )
        fig10.update_traces(line_shape="spline")
        _layout(fig10, height=380)
        st.plotly_chart(fig10, use_container_width=True)
