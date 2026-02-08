# Shopify Sales Dashboard

A professional, interactive **Shopify Sales Performance Dashboard** for a fictional Beauty & Skincare e-commerce store. Built with **Streamlit**, **Plotly**, and **Pandas**, this dashboard is designed to be screenshot-ready, client-facing, and easy to understand by non-technical business owners.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-blueviolet)

---

## Features

| Area | Details |
|------|---------|
| **KPI Cards** | Total Revenue, Total Orders, AOV, Best-Selling Product, Unique Customers |
| **Sales Trends** | Revenue over time (area chart), Orders per month (bar chart) |
| **Product Breakdown** | Top 10 products by revenue, Revenue by category (donut chart) |
| **Geography & Payments** | Top 10 countries by revenue, Payment method split |
| **Customer Timing** | Day x Hour heatmap, Order status distribution |
| **Discounts & Value** | Popular discount codes, AOV trend line |
| **Sidebar Filters** | Date range, Product category, Country, Order status |

---

## Dataset

The included data generator (`generate_data.py`) creates **65,000 realistic Shopify-style orders** spanning **18 months** (Jul 2024 to Dec 2025) for a beauty and skincare niche store.

- Seasonal spikes around Black Friday, Christmas, Valentine's Day, and Mother's Day
- 31 products across 5 categories (Skincare, Makeup, Haircare, Bath & Body, Fragrance)
- 15 customer countries, 6 payment methods, and 8 discount codes
- Columns mirror a real Shopify CSV export

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

# 4. Generate the dataset
python generate_data.py

# 5. Launch the dashboard
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

---

## Project Structure

```
shopify_analysis/
├── app.py                 # Streamlit dashboard application
├── generate_data.py       # Data generation script
├── create_notebook.py     # Script to create the analysis notebook
├── analysis.ipynb         # Jupyter notebook for exploratory analysis
├── requirements.txt       # Python dependencies
├── assets/
│   └── favicon.png        # Browser tab icon
├── data/
│   └── shopify_orders.csv # Generated dataset (created by generate_data.py)
└── README.md
```

---

## Exploratory Notebook

Open `analysis.ipynb` in Jupyter for a step-by-step exploratory analysis of the dataset.

```bash
jupyter notebook analysis.ipynb
```

---

## Tech Stack

- **[Streamlit](https://streamlit.io/)** for the interactive web application
- **[Plotly](https://plotly.com/python/)** for rich, interactive charts
- **[Pandas](https://pandas.pydata.org/)** for data manipulation and analysis
- **[NumPy](https://numpy.org/)** for numerical operations

---

## License

This project is provided as a portfolio demo. Feel free to use and adapt it.