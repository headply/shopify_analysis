"""
Generate a realistic Shopify-style dataset for a fictional online beauty store.
Produces 50,000–80,000 orders over 18 months with seasonal patterns.
"""

import csv
import os
import random
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SEED = 42
random.seed(SEED)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "shopify_orders.csv")
NUM_ORDERS = 65_000
START_DATE = datetime(2024, 7, 1)
END_DATE = datetime(2025, 12, 31)  # ~18 months

# Niche: Beauty & Skincare
PRODUCTS = {
    "Skincare": [
        ("Hydrating Face Serum", 34.99),
        ("Vitamin C Brightening Cream", 28.99),
        ("Retinol Night Cream", 42.99),
        ("Gentle Foaming Cleanser", 18.99),
        ("SPF 50 Daily Sunscreen", 24.99),
        ("Hyaluronic Acid Moisturizer", 31.99),
        ("Niacinamide Pore Minimizer", 26.99),
        ("Exfoliating Toner", 19.99),
    ],
    "Makeup": [
        ("Matte Liquid Lipstick", 16.99),
        ("Full Coverage Foundation", 32.99),
        ("Volumizing Mascara", 14.99),
        ("Eyeshadow Palette - Neutral", 38.99),
        ("Cream Blush Stick", 22.99),
        ("Setting Spray", 18.99),
        ("Brow Defining Pencil", 12.99),
        ("Concealer Wand", 15.99),
    ],
    "Haircare": [
        ("Argan Oil Shampoo", 21.99),
        ("Deep Repair Conditioner", 21.99),
        ("Leave-In Hair Treatment", 27.99),
        ("Heat Protectant Spray", 16.99),
        ("Scalp Detox Scrub", 24.99),
        ("Keratin Smoothing Mask", 29.99),
    ],
    "Bath & Body": [
        ("Shea Butter Body Lotion", 19.99),
        ("Coconut Milk Body Wash", 14.99),
        ("Exfoliating Body Scrub", 22.99),
        ("Rose Petal Bath Bombs (Set of 4)", 18.99),
        ("Hand & Nail Cream", 12.99),
    ],
    "Fragrance": [
        ("Floral Eau de Parfum", 54.99),
        ("Citrus Eau de Toilette", 44.99),
        ("Vanilla Musk Body Mist", 24.99),
        ("Woody Amber Perfume Oil", 39.99),
    ],
}

COUNTRIES = [
    ("United States", 0.42),
    ("United Kingdom", 0.12),
    ("Canada", 0.10),
    ("Australia", 0.07),
    ("Germany", 0.05),
    ("France", 0.04),
    ("Netherlands", 0.03),
    ("India", 0.03),
    ("Brazil", 0.03),
    ("Japan", 0.02),
    ("Mexico", 0.02),
    ("South Korea", 0.02),
    ("Italy", 0.02),
    ("Spain", 0.015),
    ("Sweden", 0.005),
]

PAYMENT_METHODS = [
    ("Credit Card", 0.40),
    ("PayPal", 0.25),
    ("Shopify Payments", 0.20),
    ("Apple Pay", 0.08),
    ("Google Pay", 0.05),
    ("Klarna", 0.02),
]

ORDER_STATUSES = [
    ("Delivered", 0.72),
    ("Shipped", 0.12),
    ("Processing", 0.06),
    ("Returned", 0.05),
    ("Cancelled", 0.03),
    ("Refunded", 0.02),
]

DISCOUNT_CODES = [
    None, None, None, None, None, None, None,  # ~70% no discount
    "WELCOME10", "SUMMER15", "BEAUTY20", "VIP25", "FLASH10",
    "HOLIDAY15", "NEWYEAR20", "BDAY10",
]

SHIPPING_METHODS = [
    ("Standard Shipping", 0.50),
    ("Express Shipping", 0.30),
    ("Free Shipping", 0.15),
    ("Overnight Shipping", 0.05),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def weighted_choice(items_with_weights):
    items, weights = zip(*items_with_weights)
    return random.choices(items, weights=weights, k=1)[0]


def seasonal_multiplier(dt: datetime) -> float:
    """Return a multiplier that simulates realistic e-commerce seasonality."""
    month = dt.month
    day = dt.day
    # Black Friday / Cyber Monday window (late Nov)
    if month == 11 and day >= 20:
        return 2.5
    # December holiday shopping
    if month == 12 and day <= 24:
        return 2.2
    # Valentine's week
    if month == 2 and 7 <= day <= 14:
        return 1.6
    # Mother's Day bump (early May)
    if month == 5 and day <= 14:
        return 1.5
    # Back-to-school (Aug-Sep)
    if month in (8, 9):
        return 1.2
    # January & July sales
    if month in (1, 7):
        return 1.15
    # Summer lull
    if month == 6:
        return 0.85
    return 1.0


def random_date(start: datetime, end: datetime) -> datetime:
    """Pick a random datetime between start and end, biased by seasonality."""
    delta = (end - start).days
    # Keep trying until we accept (rejection sampling with seasonality)
    while True:
        day_offset = random.randint(0, delta)
        dt = start + timedelta(days=day_offset)
        mult = seasonal_multiplier(dt)
        if random.random() < mult / 2.6:  # 2.6 is max multiplier
            hour = random.choices(
                range(24),
                weights=[1,1,1,1,1,2,3,4,6,8,9,10,10,9,8,7,7,8,9,10,9,7,4,2],
                k=1,
            )[0]
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            return dt.replace(hour=hour, minute=minute, second=second)


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def generate_dataset():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    flat_products = []
    for cat, prods in PRODUCTS.items():
        for name, price in prods:
            flat_products.append((cat, name, price))

    # Category popularity weights
    cat_weights = {
        "Skincare": 0.30,
        "Makeup": 0.28,
        "Haircare": 0.18,
        "Bath & Body": 0.14,
        "Fragrance": 0.10,
    }
    product_weights = [cat_weights[p[0]] / sum(1 for x in flat_products if x[0] == p[0]) for p in flat_products]

    fieldnames = [
        "order_id",
        "order_date",
        "product_name",
        "product_category",
        "sku",
        "quantity",
        "unit_price",
        "discount_code",
        "discount_amount",
        "total_price",
        "customer_id",
        "customer_country",
        "payment_method",
        "shipping_method",
        "shipping_cost",
        "order_status",
    ]

    customer_pool_size = int(NUM_ORDERS * 0.55)  # ~55% unique customers, ~45% repeat rate

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, NUM_ORDERS + 1):
            cat, product_name, unit_price = random.choices(flat_products, weights=product_weights, k=1)[0]
            quantity = random.choices([1, 2, 3, 4, 5], weights=[55, 25, 12, 5, 3], k=1)[0]

            discount_code = random.choice(DISCOUNT_CODES)
            if discount_code:
                pct = int("".join(c for c in discount_code if c.isdigit()))
                discount_amount = round(unit_price * quantity * pct / 100, 2)
            else:
                discount_amount = 0.00

            total_price = round(unit_price * quantity - discount_amount, 2)

            shipping_method = weighted_choice(SHIPPING_METHODS)
            if shipping_method == "Free Shipping":
                shipping_cost = 0.00
            elif shipping_method == "Standard Shipping":
                shipping_cost = round(random.uniform(3.99, 6.99), 2)
            elif shipping_method == "Express Shipping":
                shipping_cost = round(random.uniform(9.99, 14.99), 2)
            else:
                shipping_cost = round(random.uniform(19.99, 29.99), 2)

            sku_prefix = cat[:3].upper()
            sku = f"{sku_prefix}-{product_name.split()[0][:4].upper()}-{random.randint(100,999)}"

            writer.writerow({
                "order_id": f"#SB{1000 + i}",
                "order_date": random_date(START_DATE, END_DATE).strftime("%Y-%m-%d %H:%M:%S"),
                "product_name": product_name,
                "product_category": cat,
                "sku": sku,
                "quantity": quantity,
                "unit_price": f"{unit_price:.2f}",
                "discount_code": discount_code if discount_code else "",
                "discount_amount": f"{discount_amount:.2f}",
                "total_price": f"{total_price:.2f}",
                "customer_id": f"CUST-{random.randint(1, customer_pool_size):06d}",
                "customer_country": weighted_choice(COUNTRIES),
                "payment_method": weighted_choice(PAYMENT_METHODS),
                "shipping_method": shipping_method,
                "shipping_cost": f"{shipping_cost:.2f}",
                "order_status": weighted_choice(ORDER_STATUSES),
            })

    print(f"Generated {NUM_ORDERS:,} orders → {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_dataset()
