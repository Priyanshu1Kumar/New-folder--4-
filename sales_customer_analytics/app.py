# ============================================================
# ENTERPRISE SALES & CUSTOMER ANALYTICS PLATFORM
# Final Year Data Analytics Project
# ============================================================

# -------------------- IMPORTS --------------------
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, date

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Enterprise Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL PATHS
# ============================================================

DATA_PATH = "data/sales_data.csv"
REPORTS_PATH = "reports"
os.makedirs(REPORTS_PATH, exist_ok=True)

# ============================================================
# CUSTOM CSS (PROFESSIONAL UI)
# ============================================================

st.markdown("""
<style>

/* -------- Global -------- */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f4f6f9;
}

/* -------- Sidebar -------- */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
    color: white;
}

/* -------- Titles -------- */
.main-title {
    font-size: 32px;
    font-weight: 700;
    color: #0f172a;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 10px;
    color: #1e293b;
}

/* -------- Metric Cards -------- */
.metric-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
}

.metric-label {
    font-size: 14px;
    color: #64748b;
}

.metric-value {
    font-size: 24px;
    font-weight: 700;
    color: #0f172a;
}

/* -------- Status Colors -------- */
.status-good { color: #16a34a; font-weight: 600; }
.status-warning { color: #d97706; font-weight: 600; }
.status-critical { color: #dc2626; font-weight: 600; }

/* -------- Footer -------- */
.footer {
    margin-top: 40px;
    padding: 15px;
    text-align: center;
    font-size: 13px;
    color: #64748b;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR : BRANDING & CONTROLS
# ============================================================

st.sidebar.markdown("## 📊 Enterprise Analytics")
st.sidebar.markdown("### Decision Support System")

st.sidebar.divider()

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()

uploaded_file = st.sidebar.file_uploader(
    "📤 Upload Sales Dataset (CSV)",
    type=["csv"]
)

# ============================================================
# DATA LOADING & CLEANING
# ============================================================

def load_data():
    """
    Loads sales data from CSV or uploaded file,
    cleans it, and derives time features.
    """
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(DATA_PATH)

    # Date handling
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df.dropna(inplace=True)

    # Derived features
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Order_Date"].dt.year

    return df

df = load_data()

# ============================================================
# SIDEBAR : DATA ENTRY (CRUD - CREATE)
# ============================================================

st.sidebar.markdown("### ➕ Add New Sale")

with st.sidebar.form("add_sale_form", clear_on_submit=True):
    order_id = st.number_input("Order ID", step=1)
    order_date = st.date_input("Order Date")
    customer_name = st.text_input("Customer Name")
    product = st.text_input("Product Name")
    category = st.text_input("Category")
    quantity = st.number_input("Quantity", min_value=1)
    revenue = st.number_input("Revenue", min_value=0)

    submitted = st.form_submit_button("Add Sale")

    if submitted:
        new_row = pd.DataFrame([{
            "Order_ID": order_id,
            "Order_Date": order_date,
            "Customer_ID": customer_name[:3].upper(),
            "Customer_Name": customer_name,
            "Product": product,
            "Category": category,
            "Quantity": quantity,
            "Revenue": revenue
        }])

        # Append safely to CSV
        if os.path.exists(DATA_PATH):
            new_row.to_csv(DATA_PATH, mode="a", header=False, index=False)
        else:
            new_row.to_csv(DATA_PATH, index=False)

        st.session_state.data_updated = True
        st.success("✅ Sale added successfully!")


# ============================================================
# SIDEBAR : FILTERS
# ============================================================

st.sidebar.divider()
st.sidebar.markdown("### 🔍 Filters")

categories = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

years = st.sidebar.multiselect(
    "Year",
    options=df["Year"].unique(),
    default=df["Year"].unique()
)

data = df[
    (df["Category"].isin(categories)) &
    (df["Year"].isin(years))
]

# ============================================================
# KPI COMPUTATION
# ============================================================

total_revenue = data["Revenue"].sum()
total_orders = data["Order_ID"].nunique()
total_customers = data["Customer_ID"].nunique()
avg_order_value = round(total_revenue / total_orders, 2) if total_orders else 0

health_score = min(100, int((total_revenue / 100000) * 100))

if health_score >= 80:
    status = "Good"
    status_class = "status-good"
elif health_score >= 50:
    status = "Warning"
    status_class = "status-warning"
else:
    status = "Critical"
    status_class = "status-critical"

# ============================================================
# MAIN TITLE
# ============================================================

st.markdown("<div class='main-title'>📈 Sales & Customer Analytics Platform</div>", unsafe_allow_html=True)
st.caption("Enterprise-grade data analytics and decision support system")

# ============================================================
# KPI DASHBOARD
# ============================================================

k1, k2, k3, k4, k5 = st.columns(5)

def metric_card(col, label, value):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

metric_card(k1, "Total Revenue", f"₹{total_revenue:,}")
metric_card(k2, "Total Orders", total_orders)
metric_card(k3, "Total Customers", total_customers)
metric_card(k4, "Avg Order Value", f"₹{avg_order_value}")
metric_card(k5, "Health Score", f"{health_score}/100")

st.markdown(f"<p class='{status_class}'>Business Status: {status}</p>", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "👥 Customers",
    "📦 Products",
    "📄 Reports",
    "ℹ️ About"
])

# ============================================================
# TAB 1 : DASHBOARD
# ============================================================

with tab1:
    st.markdown("<div class='section-title'>Sales Trend Analysis</div>", unsafe_allow_html=True)

    monthly_sales = data.groupby("Month")["Revenue"].sum()

    fig, ax = plt.subplots()
    ax.plot(monthly_sales.index, monthly_sales.values, marker="o")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.grid(True)
    st.pyplot(fig)

    avg_growth = monthly_sales.pct_change().mean() * 100
    forecast = (
        monthly_sales.iloc[-1] * (1 + avg_growth / 100)
        if len(monthly_sales) > 1 else 0
    )

    st.info(f"📈 Average Growth Rate: {round(avg_growth,2)}%")
    st.success(f"🔮 Forecasted Next Month Revenue: ₹{int(forecast):,}")

# ============================================================
# TAB 2 : CUSTOMER ANALYTICS
# ============================================================

with tab2:
    st.markdown("<div class='section-title'>Customer Segmentation</div>", unsafe_allow_html=True)

    cust_revenue = data.groupby("Customer_Name")["Revenue"].sum()
    segments = pd.qcut(
        cust_revenue,
        q=3,
        labels=["Low Value", "Medium Value", "High Value"]
    )

    seg_df = pd.DataFrame({
        "Customer": cust_revenue.index,
        "Revenue": cust_revenue.values,
        "Segment": segments.values
    })

    st.dataframe(seg_df)

# ============================================================
# TAB 3 : PRODUCT ANALYTICS
# ============================================================

with tab3:
    st.markdown("<div class='section-title'>Product Performance</div>", unsafe_allow_html=True)

    product_perf = data.groupby("Product").agg({
        "Revenue": "sum",
        "Quantity": "sum"
    }).sort_values("Revenue", ascending=False)

    st.dataframe(product_perf)

    fig2, ax2 = plt.subplots()
    product_perf["Revenue"].head(10).plot(kind="bar", ax=ax2)
    ax2.set_ylabel("Revenue")
    st.pyplot(fig2)

# ============================================================
# TAB 4 : REPORTS
# ============================================================

with tab4:
    st.markdown("<div class='section-title'>Generate Reports</div>", unsafe_allow_html=True)

    report_name = f"{REPORTS_PATH}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    data.to_csv(report_name, index=False)

    with open(report_name, "rb") as f:
        st.download_button(
            "⬇️ Download CSV Report",
            f,
            file_name=os.path.basename(report_name)
        )

    st.dataframe(data)

# ============================================================
# TAB 5 : ABOUT
# ============================================================

with tab5:
    st.markdown("""
    ### About This Project

    This **Enterprise Sales & Customer Analytics Platform** is a final-year
    data analytics project designed to transform raw sales data into
    actionable business intelligence.

    **Key Features**
    - Data ingestion & validation
    - KPI monitoring
    - Customer & product analytics
    - Forecasting
    - Reporting
    - Decision support

    **Technology Stack**
    - Python
    - Pandas, NumPy
    - Matplotlib, Seaborn
    - Streamlit
    """)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    © Final Year Project | Sales Analytics Platform
</div>
""", unsafe_allow_html=True)
