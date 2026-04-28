import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model
model = joblib.load("models/demand_model.pkl")

st.set_page_config(page_title="Demand Forecasting System", layout="wide")

# -------------------------------
# HEADER
# -------------------------------
st.title("📦 Demand Forecasting System")
st.markdown("Predict product demand and get smart business insights")

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("🎛️ Select Features")

category = st.sidebar.selectbox("Category", ["Electronics", "Clothing", "Groceries", "Toys", "Furniture"])
region = st.sidebar.selectbox("Region", ["North", "South", "East", "West"])
weather = st.sidebar.selectbox("Weather Condition", ["Sunny", "Rainy", "Snowy"])
season = st.sidebar.selectbox("Seasonality", ["Winter", "Summer", "Monsoon"])

price = st.sidebar.slider("Price", 10.0, 200.0, 50.0)
discount = st.sidebar.slider("Discount (%)", 0, 50, 10)

# ✅ Updated (Yes/No instead of 0/1)
promotion_input = st.sidebar.selectbox("Promotion", ["No", "Yes"])
promotion = 1 if promotion_input == "Yes" else 0

competitor_price = st.sidebar.slider("Competitor Price", 10.0, 200.0, 60.0)
inventory = st.sidebar.slider("Inventory Level", 0, 500, 100)

epidemic_input = st.sidebar.selectbox("Epidemic", ["No", "Yes"])
epidemic = 1 if epidemic_input == "Yes" else 0

# -------------------------------
# FEATURE ENGINEERING
# -------------------------------
day = 15
dayofweek = 2
is_weekend = 0

price_diff = price - competitor_price
price_ratio = price / (competitor_price + 1)
stock_coverage = inventory / (inventory + 1)
promo_discount = promotion * discount
promo_season = promotion * (1 if season == "Winter" else 0)
bad_weather = 1 if weather == "Snowy" else 0
epidemic_impact = epidemic * promotion
log_inventory = np.log1p(inventory)

input_df = pd.DataFrame({
    'Category': [category],
    'Region': [region],
    'Weather Condition': [weather],
    'Seasonality': [season],
    'Inventory Level': [inventory],
    'Price': [price],
    'Discount': [discount],
    'Promotion': [promotion],
    'Competitor Pricing': [competitor_price],
    'Epidemic': [epidemic],
    'Year': [2022],
    'Month': [1],
    'Day': [day],
    'DayOfWeek': [dayofweek],
    'IsWeekend': [is_weekend],
    'Price_Diff': [price_diff],
    'Price_Ratio': [price_ratio],
    'Stock_Coverage': [stock_coverage],
    'Promo_Discount': [promo_discount],
    'Promo_Season': [promo_season],
    'Bad_Weather': [bad_weather],
    'Epidemic_Impact': [epidemic_impact],
    'Log_Inventory': [log_inventory]
})

# -------------------------------
# USER GUIDE
# -------------------------------
st.subheader("📘 How to Use")
st.info("""
1. Select product and market details from the sidebar  
2. Adjust price, discount, and inventory  
3. Click **Predict Demand**  
4. View predicted demand and business insights  
""")

# -------------------------------
# PREDICTION
# -------------------------------
if st.button("🔮 Predict Demand"):

    prediction = model.predict(input_df)[0]

    st.subheader("📊 Prediction Result")
    st.success(f"Estimated Demand: {int(prediction)} units")

    # -------------------------------
    # BUSINESS INSIGHTS (IMPROVED)
    # -------------------------------
    st.subheader("💡 Business Insights")

    insights = []

    if price > competitor_price:
        insights.append("⚠️ Your price is higher than competitors → demand may decrease")

    if price < competitor_price:
        insights.append("✅ Competitive pricing → demand advantage")

    if promotion == 1:
        insights.append("🎯 Promotion active → demand likely to increase")

    if promotion == 0:
        insights.append("ℹ️ No promotion → consider marketing campaigns")

    if discount > 20:
        insights.append("💰 High discount → strong demand boost")

    if discount == 0:
        insights.append("⚠️ No discount → lower attractiveness")

    if category == "Groceries":
        insights.append("🛒 Groceries typically have high demand")

    if category == "Furniture":
        insights.append("🪑 Furniture has slower demand cycle")

    if epidemic == 1:
        insights.append("🦠 Epidemic impact → demand pattern may fluctuate")

    if weather == "Snowy":
        insights.append("❄️ Bad weather may impact customer movement")

    if inventory < 50:
        insights.append("⚠️ Low inventory → risk of stockout")

    if inventory > 300:
        insights.append("📦 High inventory → potential overstock risk")

    # Default fallback
    if len(insights) == 0:
        insights.append("✅ Stable conditions → demand likely normal")

    for i in insights:
        st.write(i)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("👨‍💻 Prepared by **Dharmesh Parmar**")