import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Ceylon Coffee Tablets - Enterprise Portal", layout="wide")

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
    "📊 Cost Analysis", 
    "🧪 Lab & R&D Reports", 
    "🏷️ Retail Price & Orders", 
    "📦 Trade Price & Orders", 
    "📄 Professional Invoice", 
    "📋 All Records"
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

# --- TAB 3: RETAIL PRICE & ORDERS ---
with tabs[2]:
    st.header("Retail Pricing & Orders Management")
    st.write(f"Current Retail Price: **LKR {st.session_state.retail_price} per tablet**")
    with st.form("retail_order_form"):
        cust_name = st.text_input("Customer Name")
        cust_phone = st.text_input("Phone Number")
        cust_address = st.text_input("Customer Delivery Address")
        r_variant = st.selectbox("Select Variant", ["Black Coffee", "Ginger Coffee", "Cinnamon Coffee"], key="r_var")
        r_qty = st.number_input("Quantity (Tablets)", min_value=1, value=10, key="r_qty")
        
        r_submit = st.form_submit_button("Create Retail Order")
        if r_submit and cust_name:
            total_amt = r_qty * st.session_state.retail_price
            st.session_state.orders.append({
                "Reference": f"CCT-R-{len(st.session_state.orders)+101}",
                "Customer": cust_name,
                "Phone": cust_phone,
                "Address": cust_address,
                "Type": "Retail",
                "Variant": r_variant,
                "Qty": r_qty,
                "Unit Price": st.session_state.retail_price,
                "Total Amount": total_amt,
                "Date/Time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("Retail Order Saved Successfully!")

# --- TAB 4: TRADE PRICE & ORDERS ---
with tabs[3]:
    st.header("Trade / Bulk Pricing & Orders Management")
    st.write(f"Current Trade Price: **LKR {st.session_state.trade_price} per tablet**")
    with st.form("trade_order_form"):
        t_cust = st.text_input("Business / Partner Name")
        t_phone = st.text_input("Business Phone")
        t_address = st.text_input("Business / Warehouse Address")
        t_variant = st.selectbox("Select Variant", ["Black Coffee", "Ginger Coffee", "Cinnamon Coffee"], key="t_var")
        t_qty = st.number_input("Bulk Quantity (Tablets)", min_value=100, value=500, key="t_qty")
        
        t_submit = st.form_submit_button("Create Trade Order")
        if t_submit and t_cust:
            total_amt = t_qty * st.session_state.trade_price
            st.session_state.orders.append({
                "Reference": f"CCT-T-{len(st.session_state.orders)+101}",
                "Customer": t_cust,
                "Phone": t_phone,
                "Address": t_address,
                "Type": "Trade",
                "Variant": t_variant,
                "Qty": t_qty,
                "Unit Price": st.session_state.trade_price,
                "Total Amount": total_amt,
                "Date/Time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("Trade Order Saved Successfully!")

# --- TAB 5: PROFESSIONAL INVOICE GENERATOR (MATCHING EXACT IMAGE STRUCTURE) ---
with tabs[4]:
    st.header("Professional Invoice Generator (Official Layout)")
    
    with st.form("invoice_form"):
        inv_no = st.text_input("Invoice Number", value="CET 0010")
        i_name = st.text_input("Customer Name (Deliver To)", value="D.F.R perera")
        i_address = st.text_area("Delivery Address", value="49/2/2 Thekkawatta road\nThannakumbura\nKandy")
        
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            i_variant = st.selectbox("Item Description / Variant", [
                "Black Coffee (Light Roast) - 15 Tablets Pack", 
                "Black Coffee (Dark Roast) - 15 Tablets Pack", 
                "Cinnamon Coffee 15 Tablets Pack", 
                "Ginger Coffee 15 Tablets Pack"
            ])
            unit_p = st.number_input("Unit Price (LKR)", value=975.00, step=5.00)
        with col_i2:
            i_qty = st.number_input("Quantity (QTY)", min_value=1, value=1)
            
        generate_btn = st.form_submit_button("Generate Official Invoice")

    if generate_btn:
        total_price = i_qty * unit_p
        
        # Render Invoice HTML matching the exact structure from the image
        invoice_html = f"""
        <div style="border: 2px solid #5a3825; padding: 25px; border-radius: 8px; font-family: Arial, sans-serif; background-color: #ffffff; color: #000000;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #5a3825; padding-bottom: 15px;">
                <div>
                    <h2 style="margin: 0; color: #5a3825; font-size: 22px;">CEYLON COFFEE TABLETS (PVT) LTD</h2>
                    <p style="margin: 3px 0; font-size: 12px; color: #555;">No 173, Hepana, Pilimathalawa<br>TP: +94 76 367 6856</p>
                </div>
                <div style="text-align: right;">
                    <h1 style="margin: 0; color: #5a3825; font-size: 26px; letter-spacing: 2px;">INVOICE</h1>
                    <p style="margin: 5px 0; font-size: 13px;"><b>Invoice No:</b> {inv_no}<br><b>Date:</b> {datetime.now().strftime('%d %b, %Y')}</p>
                </div>
            </div>
            
            <div style="display: flex; justify-content: space-between; margin-top: 20px; gap: 20px;">
                <div style="flex: 1; border: 1px solid #c8b198; padding: 12px; border-radius: 5px; background-color: #fdfbf7;">
                    <p style="margin: 0 0 5px 0; font-size: 11px; color: #8c6239; font-weight: bold;">DELIVER TO</p>
                    <p style="margin: 0; font-size: 13px; line-height: 1.4;"><b>{i_name}</b><br>{i_address.replace(chr(10), '<br>')}</p>
                </div>
                <div style="flex: 1; border: 1px solid #bce8f1; padding: 12px; border-radius: 5px; background-color: #f4f8fb;">
                    <p style="margin: 0 0 5px 0; font-size: 11px; color: #31708f; font-weight: bold;">BANK DETAILS FOR PAYMENT</p>
                    <p style="margin: 0; font-size: 12px; line-height: 1.4;"><b>Account Name:</b> CEYLON COFFEE TABLET (PVT) LTD<br><b>Account Number:</b> 141010054345<br><b>Bank:</b> Hatton National Bank (HNB)<br><b>Branch:</b> Pilimathalawa</p>
                </div>
            </div>
            
            <table style="width: 100%; margin-top: 25px; border-collapse: collapse;">
                <thead>
                    <tr style="background-color: #5a3825; color: #ffffff; font-size: 13px;">
                        <th style="padding: 10px; text-align: center; width: 10%;">SUB</th>
                        <th style="padding: 10px; text-align: left; width: 50%;">ITEM DESCRIPTION</th>
                        <th style="padding: 10px; text-align: center; width: 10%;">QTY</th>
                        <th style="padding: 10px; text-align: right; width: 15%;">UNIT PRICE (LKR)</th>
                        <th style="padding: 10px; text-align: right; width: 15%;">TOTAL (LKR)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid #ddd; font-size: 13px;">
                        <td style="padding: 10px; text-align: center;">01</td>
                        <td style="padding: 10px;">{i_variant}</td>
                        <td style="padding: 10px; text-align: center;">{i_qty}</td>
                        <td style="padding: 10px; text-align: right;">{unit_p:.2f}</td>
                        <td style="padding: 10px; text-align: right;">{total_price:.2f}</td>
                    </tr>
                </tbody>
            </table>
            
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-top: 20px;">
                <div style="border: 1px dashed #b5835a; padding: 8px 12px; border-radius: 4px; font-size: 12px; color: #5a3825; background-color: #faf4ed;">
                    Note: + Delivery Fee
                </div>
                <div style="border: 2px solid #5a3825; padding: 12px 25px; border-radius: 6px; text-align: right; background-color: #fff;">
                    <p style="margin: 0; font-size: 11px; color: #666; font-weight: bold;">TOTAL AMOUNT</p>
                    <h2 style="margin: 5px 0 0 0; color: #5a3825; font-size: 22px;">{total_price:,.2f} LKR</h2>
                </div>
            </div>
            
            <div style="margin-top: 35px; border: 1px solid #e0d0c0; background-color: #faf6f0; padding: 12px; text-align: center; border-radius: 5px;">
                <p style="margin: 0; color: #5a3825; font-weight: bold; font-size: 14px;">Thank you for your Order!</p>
                <p style="margin: 3px 0 0 0; font-size: 11px; color: #666;">Ceylon Coffee Tablets (Pvt) Ltd — Quality Sri Lankan Specialty Coffee Products</p>
            </div>
        </div>
        """
        st.markdown(invoice_html, unsafe_allow_html=True)
        st.info("💡 **ඉන්වොයිසිය PDF ලෙස ලබාගැනීමට:** බ්‍රවුසර් එකේ `Ctrl+P` (Windows) හෝ `Cmd+P` (Mac) ඔබා 'Save as PDF' තෝරාගන්න.")

# --- TAB 6: ALL RECORDS ---
with tabs[5]:
    st.header("All Stored Orders & Invoices History")
    if st.session_state.orders:
        st.table(st.session_state.orders)
        if st.button("Clear All Records"):
            st.session_state.orders = []
            st.rerun()
    else:
        st.info("No records found.")
