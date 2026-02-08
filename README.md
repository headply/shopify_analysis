# Shopify Sales Dashboard

A professional, interactive **Shopify Sales Performance Dashboard** for a fictional Beauty & Skincare e-commerce store. Built with **Streamlit**, **Plotly**, and **Pandas**, the dashboard is designed to be screenshot-ready, client-facing, and easy to understand by non-technical business owners.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-blueviolet)

---

## Table of Contents

- [Features](#features)
- [Key Insights from the Data](#key-insights-from-the-data)
- [Dataset](#dataset)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Dashboard Tabs](#dashboard-tabs)
- [Exploratory Notebook](#exploratory-notebook)
- [Tech Stack](#tech-stack)
- [License](#license)

---

## Features

| Area | Details |
|------|---------|
| **KPI Cards** | Total Revenue, Total Orders, Avg Order Value, Best-Selling Product, Unique Customers — with 30-day trend deltas |
| **Sales Trends** | Revenue over time (area chart), Orders per month (bar chart), Day × Hour heatmap, Order status breakdown |
| **Product Performance** | Top 10 products by revenue (bar), Revenue by category (donut) |
| **Customers & Payments** | Top 10 countries by revenue, Payment method split (donut) |
| **Discounts & Value** | Most popular discount codes, Average Order Value trend over time |
| **Sidebar Filters** | Date range picker, Product category, Country, Order status — all with an "All" option for quick reset |

---

## Key Insights from the Data

The generated dataset simulates **65,000 orders** over **18 months** (Jul 2024 – Dec 2025). Running the analysis notebook and dashboard reveals several noteworthy patterns:

### Revenue & Orders

| Metric | Value |
|--------|-------|
| **Total Revenue** | ~$2.69 M |
| **Average Order Value** | $41.40 |
| **Median Order Value** | $31.98 |
| **Peak Revenue Month** | December 2024 ($232 K, 5,621 orders) |
| **Lowest Revenue Month** | June 2025 ($99 K, 2,457 orders) |

### Seasonality

Revenue and order volume follow clear seasonal trends driven by the data generator's built-in multipliers:

- **Black Friday / Cyber Monday** (late November) and **December holiday shopping** produce the strongest spikes — up to **2.5×** normal volume.
- **Valentine's Day** (Feb 7–14) and **Mother's Day** (early May) create secondary peaks ideal for beauty product promotions.
- **June** is the quietest month, presenting an opportunity for flash sales or loyalty campaigns.
- **Fridays** are the busiest day of the week for orders.

### Product & Category Breakdown

| Category | Revenue Share |
|----------|--------------|
| Skincare | 33.5% |
| Makeup | 23.8% |
| Haircare | 16.9% |
| Fragrance | 16.1% |
| Bath & Body | 9.7% |

**Top 5 products by revenue:**
1. Retinol Night Cream — $167 K
2. Floral Eau de Parfum — $143 K
3. Eyeshadow Palette – Neutral — $141 K
4. Hydrating Face Serum — $137 K
5. Hyaluronic Acid Moisturizer — $125 K

### Customer Geography

The United States dominates at **42.4%** of revenue, followed by the United Kingdom (12.2%), Canada (10.2%), Australia (6.9%), and Germany (5.2%). The store serves customers across **15 countries**.

### Payments & Discounts

- **Credit Card** is the most popular payment method (39.8%), followed by PayPal (24.7%) and Shopify Payments (20.6%).
- About **53%** of orders use a discount code. Eight codes are available (e.g., `WELCOME10`, `VIP25`, `BEAUTY20`), with usage spread fairly evenly — each code is used roughly 4,200–4,400 times.
- **71.9%** of orders are delivered; returns and cancellations account for about 5% and 3%, respectively.

---

## Dataset

The included data generator (`generate_data.py`) creates **65,000 realistic Shopify-style orders** spanning **18 months** (Jul 2024 – Dec 2025) for a beauty and skincare niche store.

- **Seasonal patterns**: Black Friday, Christmas, Valentine's Day, Mother's Day, back-to-school, and summer lull
- **31 products** across 5 categories (Skincare, Makeup, Haircare, Bath & Body, Fragrance)
- **15 customer countries** weighted by market size (US-heavy)
- **6 payment methods**, **4 shipping tiers**, and **8 discount codes**
- 16 columns that mirror a real Shopify CSV export:

| Column | Description |
|--------|-------------|
| `order_id` | Unique order identifier (e.g., `#SB1001`) |
| `order_date` | Timestamp of the order |
| `product_name` | Name of the product purchased |
| `product_category` | Category (Skincare, Makeup, etc.) |
| `sku` | Auto-generated SKU |
| `quantity` | Units ordered (1–5) |
| `unit_price` | Price per unit |
| `discount_code` | Discount code applied, if any |
| `discount_amount` | Dollar amount discounted |
| `total_price` | Final order total after discount |
| `customer_id` | Customer identifier |
| `customer_country` | Customer's country |
| `payment_method` | Payment method used |
| `shipping_method` | Shipping tier selected |
| `shipping_cost` | Shipping fee charged |
| `order_status` | Delivered, Shipped, Processing, Returned, Cancelled, or Refunded |

> **Note:** The CSV is git-ignored. It is generated automatically on first dashboard launch, or you can run `python generate_data.py` manually.

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/headply/shopify_analysis.git
cd shopify_analysis

# 2. Create a virtual environment (recommended)
python -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the dataset (optional — the dashboard auto-generates it)
python generate_data.py

# 5. Launch the dashboard
streamlit run app.py
```

The dashboard will open at **http://localhost:8501**.

---

## Project Structure

```
shopify_analysis/
├── app.py                 # Streamlit dashboard application
├── generate_data.py       # Synthetic data generation script (65K orders)
├── create_notebook.py     # Helper to regenerate analysis.ipynb
├── analysis.ipynb         # Jupyter notebook for exploratory data analysis
├── requirements.txt       # Python dependencies
├── assets/
│   └── favicon.png        # Browser tab icon
├── data/
│   └── shopify_orders.csv # Generated dataset (git-ignored, created by generate_data.py)
└── README.md
```

---

## Dashboard Tabs

The dashboard is organized into four tabs, each focusing on a different aspect of the business:

### 1. Sales Trends

- **Revenue Over Time** — area chart showing monthly revenue with spline interpolation
- **Orders Per Month** — bar chart of order volume
- **Day × Hour Heatmap** — identifies peak shopping windows (useful for ad scheduling)
- **Order Status Breakdown** — horizontal bar chart of Delivered, Shipped, Processing, Returned, Cancelled, and Refunded orders

### 2. Products

- **Top 10 Products by Revenue** — horizontal bar chart highlighting the best sellers
- **Revenue by Category** — donut chart showing category share (Skincare leads at ~34%)

### 3. Customers & Payments

- **Top 10 Countries by Revenue** — bar chart of geographic revenue distribution
- **Revenue by Payment Method** — donut chart of payment preferences

### 4. Discounts & Value

- **Most Popular Discount Codes** — bar chart of code usage frequency
- **Average Order Value Over Time** — line chart tracking AOV trends month-over-month

All charts are interactive (hover, zoom, pan) thanks to Plotly, and all respond to the sidebar filters in real time.

---

## Exploratory Notebook

The companion Jupyter notebook (`analysis.ipynb`) provides a step-by-step exploratory analysis of the dataset covering:

- Dataset overview and summary statistics
- Revenue and order trends over time
- Top products and category breakdowns
- Geographic revenue distribution
- Order status distribution
- Discount code popularity

```bash
# Make sure the dataset exists first
python generate_data.py

# Open the notebook
jupyter notebook analysis.ipynb
```

You can regenerate the notebook from scratch using:

```bash
python create_notebook.py
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| **[Streamlit](https://streamlit.io/)** | Interactive web application framework |
| **[Plotly](https://plotly.com/python/)** | Rich, interactive charts and visualizations |
| **[Pandas](https://pandas.pydata.org/)** | Data manipulation and analysis |
| **[NumPy](https://numpy.org/)** | Numerical operations |
| **[nbformat](https://nbformat.readthedocs.io/)** | Jupyter notebook creation |

---

## License

This project is provided as a portfolio demo. Feel free to use and adapt it.