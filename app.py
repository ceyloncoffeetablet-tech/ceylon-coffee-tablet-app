import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Ceylon Coffee Tablets - Management Portal", layout="wide")

# Session State Initialization
if 'retail_price' not in st.session_state:
    st.session_state.retail_price = 50.00
if 'trade_price' not in st.session_state:
    st.session_state.trade_price = 42.00
if 'mfg_cost' not in st.session_state:
    st.session_state.mfg_cost = 41.95
if 'courier_cost' not in st.session_state:
    st.session_state.courier_cost = 4.05
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'rd_logs' not in st.session_state:
    st.session_state.rd_logs = []

st.title("Ceylon Coffee Tablets (Pvt) Ltd - Enterprise System")
st.markdown("*Drop it. Dissolve it. Done. | Corporate Management Portal*")

# Navigation Tabs
tabs = st.tabs([
    "📊 Cost & Profit Analysis", 
    "🧪 Lab / R&D Reports", 
    "🏷️ Retail Pricing & Orders", 
    "📦 Trade Pricing & Orders", 
    "📄 Invoices & All Records"
])

# --- TAB 1: COST & PROFIT ANALYSIS ---
with tabs[0]:
    st.header("Tablet Production Cost & Profit Structure Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cost Inputs")
        st.session_state.mfg_cost = st.number_input("Manufacturing Cost per Tablet (LKR)", value=float(st.session_state.mfg_cost), step=0.05)
        st.session_state.courier_cost = st.number_input("Courier & Packing Cost per Tablet (LKR)", value=float(st.session_state.courier_cost), step=0.05)
        total_cost = st.session_state.mfg_cost + st.session_state.courier_cost
        st.info(f"**Total Landed Cost / Tablet:** LKR {total_cost:.2f}")

    with col2:
        st.subheader("Selling Price Inputs")
        st.session_state.retail_price = st.number_input("Retail Selling Price / Tablet (LKR)", value=float(st.session_state.retail_price), step=0.50)
        st.session_state.trade_price = st.number_input("Trade Selling Price / Tablet (LKR)", value=float(st.session_state.trade_price), step=0.50)

    st.markdown("---")
    st.subheader("Profit Margins Calculation")
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        retail_profit = st.session_state.retail_price - total_cost
        retail_margin = (retail_profit / st.session_state.retail_price) * 100 if st.session_state.retail_price > 0 else 0
        st.success(f"**Retail Profit per Tablet:** LKR {retail_profit:.2f} \n\n **Profit Margin:** {retail_margin:.2f}%")
        
    with p_col2:
        trade_profit = st.session_state.trade_price - total_cost
        trade_margin = (trade_profit / st.session_state.trade_price) * 100 if st.session_state.trade_price > 0 else 0
        st.warning(f"**Trade Profit per Tablet:** LKR {trade_profit:.2f} \n\n **Profit Margin:** {trade_margin:.2f}%")

# --- TAB 2: LAB / R&D REPORTS ---
with tabs[1]:
    st.header("Lab & R&D Quality Control Reports (RM-LOG & BPR-QC Master)")
    
    with st.form("rd_form"):
        st.subheader("1. Batch & Raw Material Details")
        col1, col2, col3 = st.columns(3)
        with col1:
            batch_no = st.text_input("Batch Number (e.g., CCT260930B)")
            variant = st.selectbox("Product Variant", ["Black Coffee", "Ginger Coffee", "Cinnamon Coffee"])
        with col2:
            mfg_date = st.date_input("Manufacture Date")
            coffee_wt = st.number_input("Green/Roasted Coffee Weight (kg)", value=5.0)
        with col3:
            roast_level = st.selectbox("Roast Profile Level", ["Medium", "Medium-Dark", "Dark"])
            grind_size = st.selectbox("Grind Size Profile", ["Fine Powder", "Extra Fine"])

        st.subheader("2. Quality & Parameter Checks (Standard: Moisture < 4.0%)")
        c1, c2 = st.columns(2)
        with c1:
            moisture = st.number_input("Observed Moisture Level (%)", value=3.5, step=0.1)
            aroma_check = st.selectbox("Aroma & Color Inspection", ["Pass", "Fail"])
        with c2:
            dissolve_time = st.number_input("Average Dissolve Time (sec at 100°C)", value=45)
            qc_status = st.selectbox("Batch Acceptance Status", ["APPROVED FOR RELEASE", "REJECTED / HOLD"])

        submitted_rd = st.form_submit_button("Save R&D / Lab Report")
        if submitted_rd and batch_no:
            st.session_state.rd_logs.append({
                "Batch No": batch_no,
                "Variant": variant,
                "Date": str(mfg_date),
                "Moisture": f"{moisture}%",
                "Dissolve Time": f"{dissolve_time} sec",
                "Status": qc_status
            })
            st.success("Lab & R&D Report Saved Successfully!")

    if st.session_state.rd_logs:
        st.subheader("Saved R&D Logs History")
        st.table(st.session_state.rd_logs)

# --- TAB 3: RETAIL PRICING & ORDERS ---
with tabs[2]:
    st.header("Retail Orders & Pricing Management")
    st.write(f"Current Retail Price: **LKR {st.session_state.retail_price} per tablet**")
    
    with st.form("retail_order_form"):
        cust_name = st.text_input("Customer Name")
        cust_phone = st.text_input("Phone Number")
        r_variant = st.selectbox("Select Variant", ["Black Coffee", "Ginger Coffee", "Cinnamon Coffee"], key="r_var")
        r_qty = st.number_input("Quantity (Tablets)", min_value=1, value=10, key="r_qty")
        
        r_submit = st.form_submit_button("Create Retail Order")
        if r_submit and cust_name:
            total_amt = r_qty * st.session_state.retail_price
            st.session_state.orders.append({
                "Reference": f"CCT-R-{len(st.session_state.orders)+101}",
                "Customer": cust_name,
                "Phone": cust_phone,
                "Type": "Retail",
                "Variant": r_variant,
                "Qty": r_qty,
                "Unit Price": st.session_state.retail_price,
                "Total Amount": total_amt,
                "Date/Time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("Retail Order Created Successfully!")

# --- TAB 4: TRADE PRICING & ORDERS ---
with tabs[3]:
    st.header("Trade / Bulk Orders & Pricing Management")
    st.write(f"Current Trade Price: **LKR {st.session_state.trade_price} per tablet**")
    
    with st.form("trade_order_form"):
        t_cust = st.text_input("Business / Partner Name")
        t_phone = st.text_input("Business Phone")
        t_variant = st.selectbox("Select Variant", ["Black Coffee", "Ginger Coffee", "Cinnamon Coffee"], key="t_var")
        t_qty = st.number_input("Bulk Quantity (Tablets)", min_value=100, value=500, key="t_qty")
        
        t_submit = st.form_submit_button("Create Trade Order")
        if t_submit and t_cust:
            total_amt = t_qty * st.session_state.trade_price
            st.session_state.orders.append({
                "Reference": f"CCT-T-{len(st.session_state.orders)+101}",
                "Customer": t_cust,
                "Phone": t_phone,
                "Type": "Trade",
                "Variant": t_variant,
                "Qty": t_qty,
                "Unit Price": st.session_state.trade_price,
                "Total Amount": total_amt,
                "Date/Time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("Trade Order Created Successfully!")

# --- TAB 5: INVOICES & ALL RECORDS ---
with tabs[4]:
    st.header("Invoices & All Order Records")
    
    if st.session_state.orders:
        st.table(st.session_state.orders)
        
        if st.button("Print / Export Report View"):
            st.info("Use your browser's Print function (Ctrl+P / Cmd+P) to save these records as PDF/Invoice.")
    else:
        st.info("No orders or invoices recorded yet.")
