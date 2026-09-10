import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. Page Configuration Settings
st.set_page_config(page_title="Statistical Inference Dashboard", layout="wide")

st.title("📊 E-Commerce Competitor Price Optimization & Statistical Inference Engine")
st.markdown("An interactive statistical workspace environment designed to test marketplace data distribution shifts.")

# 2. Control Parameter Board
st.sidebar.header("🔬 Statistical Calibration Panel")
alpha_level = st.sidebar.select_slider("Select Significance Threshold (Alpha)", options=[0.01, 0.05, 0.10], value=0.05)
undercut_rate = st.sidebar.slider("Market Undercut Strategy (%)", min_value=0.0, max_value=30.0, value=10.0, step=1.0) / 100

# 3. Core Database Matrix Setup
st.subheader("📋 Core Marketplace Data Ledger")
data = {
    'Product_Name': ['Wireless Headphones', 'Mechanical Keyboard', 'Gaming Mouse', '4K Monitor', 'USB-C Hub', 'Webcam 1080p', 'Laptop Stand', 'Bluetooth Speaker'],
    'Competitor_Price_A': [89.99, 120.00, 45.50, 299.99, 25.00, 69.99, 35.00, 55.00],
    'Competitor_Price_B': [95.00, 115.00, 49.99, 310.00, 22.50, 74.99, 32.00, 59.99],
    'Your_Target_Cost': [40.00, 50.00, 18.00, 150.00, 8.00, 30.00, 12.00, 22.00]
}
df = pd.DataFrame(data)

# Real-time calculations based on interactive slider configurations
df['Average_Market_Price'] = (df['Competitor_Price_A'] + df['Competitor_Price_B']) / 2
df['Your_Suggested_Retail_Price'] = df['Average_Market_Price'] * (1 - undercut_rate)
df['Projected_Profit_Margin_USD'] = df['Your_Suggested_Retail_Price'] - df['Your_Target_Cost']

# Render Dynamic Formatted Data Frame Layout
st.dataframe(df.style.format({
    'Competitor_Price_A': '${:.2f}', 'Competitor_Price_B': '${:.2f}',
    'Average_Market_Price': '${:.2f}', 'Your_Suggested_Retail_Price': '${:.2f}',
    'Projected_Profit_Margin_USD': '${:.2f}', 'Your_Target_Cost': '${:.2f}'
}), use_container_width=True)

# 4. Distribution Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Sample Size Population (N)", len(df))
with col2:
    st.metric("Avg Projected Profit Margin", f"${df['Projected_Profit_Margin_USD'].mean():.2f}")
with col3:
    st.metric("Standard Error Variance", f"${df['Projected_Profit_Margin_USD'].std():.2f}")

# 5. Hypothesis Testing Calculation Frame
st.subheader("🔬 Paired-Sample Student's T-Test Evaluation")
t_stat, p_value = stats.ttest_rel(df['Competitor_Price_A'], df['Competitor_Price_B'])

st.markdown(f"**Calculated T-Statistic Value:** `{t_stat:.4f}`")
st.markdown(f"**Calculated Significance Value (P-Value):** `{p_value:.4f}`")

if p_value < alpha_level:
    st.success(f"👉 **Decision: Reject H0** (P-Value < {alpha_level}). Statistically significant pricing variance verified between competitors!")
else:
    st.warning(f"👉 **Decision: Fail to Reject H0** (P-Value ≥ {alpha_level}). Pricing differences between competitor systems are statistically negligible.")

# 6. Dual Visualization Pipeline Execution
st.subheader("📉 Analytics Layout & Variance Visualization")
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1 (Left)
sns.barplot(x='Product_Name', y='Projected_Profit_Margin_USD', data=df, palette='Blues_r', hue='Product_Name', legend=False, ax=axes[0])
axes[0].bar_label(axes[0].containers[0], fmt='$%.2f', padding=4, weight='bold', size=8)
axes[0].set_title('Calculated Unit Profit Margin Projections', weight='bold', size=11)
axes[0].set_xticklabels(df['Product_Name'], rotation=25, ha='right', size=8)

# Subplot 2 (Right)
melted_df = df.melt(id_vars=['Product_Name'], value_vars=['Competitor_Price_A', 'Competitor_Price_B'], var_name='Competitor', value_name='Price')
sns.boxplot(x='Competitor', y='Price', data=melted_df, palette='Set2', hue='Competitor', legend=False, ax=axes[1])
axes[1].set_title('Competitor Base Retail Price Spreads', weight='bold', size=11)

plt.tight_layout()
st.pyplot(fig)
