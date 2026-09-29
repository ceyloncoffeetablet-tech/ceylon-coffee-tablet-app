import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Ceylon Coffee Tablets - Enterprise Portal", layout="wide")

# --- USER AUTHENTICATION & DIRECTORS ACCESS CONTROL ---
USERS = {
    "Krishan Damith": {"pin": "admin123", "role": "Admin"},
    "Shehan Maduranga": {"pin": "shehan2026", "role": "Director"},
    "Kanishka Dulanjana": {"pin": "kanishka2026", "role": "Director"},
    "Chanuka Vinod": {"pin": "chanuka2026", "role": "Director"},
    "Pasindu Sachintha": {"pin": "pasindu2026", "role": "Director"}
}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""

# Session State Initialization for Business Data
if 'retail_price' not in st.session_state:
    st.session_state.retail_price = 50.00
if 'trade_price' not in st.session_state:
    st.session_state.trade_price = 42.00
if 'mfg_cost' not in st.session_state:
    st.session_state.mfg_cost = 41.95
if 'courier_cost' not in st.session_state:
    st.session_state.courier_cost = 4.05
if 'prices_locked' not in st.session_state:
    st.session_state.prices_locked = False

if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'rd_logs' not in st.session_state:
    st.session_state.rd_logs = []
if 'rm_logs' not in st.session_state:
    st.session_state.rm_logs = []
if 'invoice_cart' not in st.session_state:
    st.session_state.invoice_cart = []

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #5a3825;'>Ceylon Coffee Tablets (Pvt) Ltd</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Corporate Management Portal — Secure Directors Login</p>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        with st.form("login_form"):
            selected_user = st.selectbox("Select Director / User", list(USERS.keys()))
            entered_pin = st.text_input("Enter Passcode / PIN", type="password")
            login_btn = st.form_submit_button("Secure Login")
            
            if login_btn:
                if USERS[selected_user]["pin"] == entered_pin:
                    st.session_state.logged_in = True
                    st.session_state.current_user = selected_user
                    st.session_state.user_role = USERS[selected_user]["role"]
                    st.success(f"Welcome, {selected_user} ({st.session_state.user_role})!")
                    st.rerun()
                else:
                    st.error("Invalid Passcode! Please check your credentials.")
    st.stop()

# --- SIDEBAR USER & LOCK STATUS ---
st.sidebar.title("System Status")
st.sidebar.write(f"👤 **User:** {st.session_state.current_user}")
st.sidebar.write(f"🛡️ **Role:** {st.session_state.user_role}")

if st.session_state.prices_locked:
    st.sidebar.error("🔒 Cost & Pricing Structure is **LOCKED**")
else:
    st.sidebar.success("🔓 Cost & Pricing Structure is **UNLOCKED**")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.user_role = ""
    st.rerun()

st.title("Ceylon Coffee Tablets (Pvt) Ltd - Enterprise System")
st.markdown("*Drop it. Dissolve it. Done. | Corporate Management Portal*")

# Navigation Tabs
tabs = st.tabs([
    "📊 Cost & Pricing (Secure)", 
    "🧪 Lab & R&D Reports", 
    "📦 Raw Materials (RM-LOG)", 
    "📄 Professional Invoice Generator", 
    "📋 Directors & All Records"
])

# --- TAB 1: COST & PROFIT ANALYSIS & LOCK CONTROL ---
with tabs[0]:
    st.header("Tablet Production Cost & Profit Structure Analysis")
    
    if st.session_state.prices_locked:
        st.warning("🔒 **මෙම මිල ගණන් සහ නිෂ්පාදන පිරිවැය මේ වන විට ADMIN විසින් Lock කර ඇත.** වෙනස් කිරීම් සිදුකිරීමට අවශ්‍ය නම් Admin (ක්‍රිශන් දමිත්) අතින් එය Unlock කළ යුතුය.")
    else:
        st.info("🔓 පද්ධතිය දැනට Unlock කර ඇත. Admin කෙනෙකුට අවශ්‍ය වෙනස්කම් සිදු කර අවසානයේ එය Lock කළ හැක.")

    # Admin Lock/Unlock Controls
    if st.session_state.user_role == "Admin":
        col_lk1, col_lk2 = st.columns(2)
        with col_lk1:
            if not st.session_state.prices_locked:
                if st.button("🔒 Lock Costs & Prices Now"):
                    st.session_state.prices_locked = True
                    st.success("Costs and Prices have been securely locked!")
                    st.rerun()
        with col_lk2:
            if st.session_state.prices_locked:
                if st.button("🔓 Unlock Costs & Prices (Admin Only)"):
                    st.session_state.prices_locked = False
                    st.success("Costs and Prices have been unlocked for editing.")
                    st.rerun()
    else:
        st.markdown("*සටහන: මිල ගණන් සහ පිරිවැය වෙනස් කිරීමේ හෝ Lock/Unlock කිරීමේ බලය ඇත්තේ ඇඩ්මින් (ක්‍රිශන් දමිත්) වෙත පමණි.*")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cost Inputs")
        # Disable inputs if locked or if user is not Admin
        is_disabled = st.session_state.prices_locked or (st.session_state.user_role != "Admin")
        
        mfg_input = st.number_input("Manufacturing Cost per Tablet (LKR)", value=float(st.session_state.mfg_cost), step=0.05, disabled=is_disabled)
        courier_input = st.number_input("Courier & Packing Cost per Tablet (LKR)", value=float(st.session_state.courier_cost), step=0.05, disabled=is_disabled)
        
        if not is_disabled:
            st.session_state.mfg_cost = mfg_input
            st.session_state.courier_cost = courier_input

        total_cost = st.session_state.mfg_cost + st.session_state.courier_cost
        st.info(f"**Total Landed Cost / Tablet:** LKR {total_cost:.2f}")

    with col2:
        st.subheader("Selling Price Inputs")
        retail_input = st.number_input("Retail Selling Price / Tablet (LKR)", value=float(st.session_state.retail_price), step=0.50, disabled=is_disabled)
        trade_input = st.number_input("Trade Selling Price / Tablet (LKR)", value=float(st.session_state.trade_price), step=0.50, disabled=is_disabled)
        
        if not is_disabled:
            st.session_state.retail_price = retail_input
            st.session_state.trade_price = trade_input

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

    cost_data = pd.DataFrame([{
        "Manufacturing Cost": st.session_state.mfg_cost,
        "Courier Cost": st.session_state.courier_cost,
        "Total Landed Cost": total_cost,
        "Retail Price": st.session_state.retail_price,
        "Trade Price": st.session_state.trade_price,
        "Status": "LOCKED" if st.session_state.prices_locked else "UNLOCKED"
    }])
    st.download_button("📥 Download Cost Analysis Report (CSV)", cost_data.to_csv(index=False).encode('utf-8'), "cost_analysis.csv", "text/csv")

# --- TAB 2: LAB / R&D REPORTS ---
with tabs[1]:
    st.header("Lab & R&D Quality Control Reports (BPR-QC Master)")
    st.markdown("පරීක්ෂණ වාර්තා සඳහා අවශ්‍ය ඡායාරූප (Photos) උඩුගත කර වාර්තාව සුරකින්න.")

    with st.form("rd_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            batch_no = st.text_input("Batch Number (e.g., CCT-2026-001)")
            variant = st.selectbox("Product Variant", ["Black Coffee (Light Roast)", "Black Coffee (Dark Roast)", "Cinnamon Coffee", "Ginger Coffee"])
        with col2:
            mfg_date = st.date_input("Manufacture Date")
            coffee_wt = st.number_input("Coffee Weight (kg)", value=5.0)
        with col3:
            moisture = st.number_input("Moisture Level (%) [Standard < 4.0%]", value=3.5, step=0.1)
            qc_status = st.selectbox("Batch Status", ["APPROVED FOR RELEASE", "REJECTED / HOLD"])

        uploaded_photo = st.file_uploader("Attach Lab Test / Report Photo", type=["png", "jpg", "jpeg"])

        submitted_rd = st.form_submit_button("Save R&D Report")
        if submitted_rd and batch_no:
            photo_name = uploaded_photo.name if uploaded_photo else "No Photo"
            st.session_state.rd_logs.append({
                "Batch No": batch_no,
                "Variant": variant,
                "Date": str(mfg_date),
                "Coffee Weight (kg)": coffee_wt,
                "Moisture": f"{moisture}%",
                "Status": qc_status,
                "Attached Photo": photo_name,
                "Recorded By": st.session_state.current_user
            })
            st.success("R&D Report Saved Successfully with Photo!")

    if st.session_state.rd_logs:
        st.subheader("Saved R&D Logs")
        rd_df = pd.DataFrame(st.session_state.rd_logs)
        st.table(rd_df)
        st.download_button("📥 Download R&D Reports (CSV)", rd_df.to_csv(index=False).encode('utf-8'), "rd_logs_report.csv", "text/csv")

# --- TAB 3: RAW MATERIALS (RM-LOG) ---
with tabs[2]:
    st.header("Raw Materials Inventory & Sourcing Management (RM-LOG)")
    with st.form("rm_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            rm_name = st.selectbox("Raw Material Item", ["Green Coffee Beans (Arabica)", "Ginger Extract Powder", "Cinnamon Extract Powder", "Tableting Excipients / Binders", "Packaging Foils"])
            supplier = st.text_input("Supplier / Source Name (e.g., Kandy Agro Exports)")
        with c2:
            purch_date = st.date_input("Purchase Date")
            expiry_date = st.date_input("Expiry Date")
        with c3:
            rm_qty = st.number_input("Quantity Purchased (kg / units)", value=25.0)
            total_cost_rm = st.number_input("Total Cost (LKR)", value=45000.0)

        submitted_rm = st.form_submit_button("Add Raw Material Record")
        if submitted_rm and supplier:
            st.session_state.rm_logs.append({
                "Date": str(purch_date),
                "Item": rm_name,
                "Supplier / Source": supplier,
                "Quantity": rm_qty,
                "Total Cost (LKR)": total_cost_rm,
                "Expiry Date": str(expiry_date),
                "Recorded By": st.session_state.current_user
            })
            st.success("Raw Material Record Saved Successfully!")

    if st.session_state.rm_logs:
        st.subheader("Raw Materials Stock & Sourcing Log")
        rm_df = pd.DataFrame(st.session_state.rm_logs)
        st.table(rm_df)
        st.download_button("📥 Download Raw Materials Report (CSV)", rm_df.to_csv(index=False).encode('utf-8'), "raw_materials_report.csv", "text/csv")

# --- TAB 4: PROFESSIONAL INVOICE GENERATOR ---
with tabs[3]:
    st.header("Official Invoice Generator (Tablets Quantity-wise)")
    st.markdown("ඉන්වොයිස් අංකය **CCT-** යටතේ ඇතුළත් කර, බහු කෝපි වර්ග එකින් එක කාර්ට් එකට එකතු කරගත හැක.")

    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        inv_no = st.text_input("Invoice Number", value="CCT-00012")
        cust_name = st.text_input("Customer Name (Deliver To)", value="")
        cust_phone = st.text_input("Telephone Number", value="")
    with col_inf2:
        pricing_type = st.selectbox("Pricing Category", ["Retail Price", "Trade Price"])
        cust_address = st.text_area("Delivery Address", value="")

    st.markdown("---")
    st.subheader("Add Coffee Variant & Tablet Quantity")
    
    with st.form("add_cart_form"):
        c_var = st.selectbox("Select Coffee Variant", [
            "Black Coffee (Light Roast)", 
            "Black Coffee (Dark Roast)", 
            "Cinnamon Coffee", 
            "Ginger Coffee"
        ])
        c_tablets_qty = st.number_input("Tablets Quantity (ටැබ්ලට් ගණන)", min_value=1, value=10)
        add_btn = st.form_submit_button("Add Item to Invoice Cart")
        
        if add_btn:
            unit_price = st.session_state.retail_price if pricing_type == "Retail Price" else st.session_state.trade_price
            st.session_state.invoice_cart.append({
                "Variant": c_var,
                "Qty": c_tablets_qty,
                "Unit Price": unit_price,
                "Total": c_tablets_qty * unit_price
            })
            st.success(f"Added {c_tablets_qty} tablets of {c_var} to invoice cart!")

    if st.session_state.invoice_cart:
        st.subheader("Current Invoice Items List")
        cart_df = pd.DataFrame(st.session_state.invoice_cart)
        st.table(cart_df)
        
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("Clear Cart"):
                st.session_state.invoice_cart = []
                st.rerun()
        with c_btn2:
            generate_final = st.button("Generate & Save Official Invoice")

        if generate_final:
            grand_total = sum([item["Total"] for item in st.session_state.invoice_cart])
            total_tablets_count = sum([item["Qty"] for item in st.session_state.invoice_cart])
            
            st.session_state.orders.append({
                "Invoice No": inv_no,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Customer": cust_name if cust_name else "Guest Customer",
                "Phone": cust_phone,
                "Address": cust_address,
                "Type": pricing_type,
                "Total Tablets": total_tablets_count,
                "Grand Total (LKR)": grand_total,
                "Cart Details": st.session_state.invoice_cart.copy(),
                "Issued By": st.session_state.current_user
            })
            
            st.success("Invoice generated and saved successfully!")

        if st.session_state.orders:
            latest_order = st.session_state.orders[-1]
            
            cart_rows_html = ""
            for idx, cart_item in enumerate(latest_order["Cart Details"], 1):
                cart_rows_html += f"""
                    <tr style="border-bottom: 1px solid #ddd; font-size: 13px;">
                        <td style="padding: 10px; text-align: center;">{idx:02d}</td>
                        <td style="padding: 10px;">{cart_item['Variant']} ({cart_item['Qty']} Tablets)</td>
                        <td style="padding: 10px; text-align: center;">{cart_item['Qty']}</td>
                        <td style="padding: 10px; text-align: right;">{cart_item['Unit Price']:,.2f}</td>
                        <td style="padding: 10px; text-align: right;">{cart_item['Total']:,.2f}</td>
                    </tr>
                """

            formatted_address = latest_order["Address"].replace(chr(10), '<br>') if latest_order["Address"] else "No Address Provided"
            
            invoice_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Invoice {latest_order['Invoice No']}</title></head>
<body style="font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">
<div style="max-width: 800px; margin: auto; border: 2px solid #5a3825; padding: 25px; border-radius: 8px; background-color: #ffffff; color: #000000;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #5a3825; padding-bottom: 15px;">
        <div>
            <h2 style="margin: 0; color: #5a3825; font-size: 22px;">CEYLON COFFEE TABLETS (PVT) LTD</h2>
            <p style="margin: 3px 0; font-size: 12px; color: #555;">No 173, Hepana, Pilimathalawa<br>TP: +94 76 367 6856</p>
        </div>
        <div style="text-align: right;">
            <h1 style="margin: 0; color: #5a3825; font-size: 26px; letter-spacing: 2px;">INVOICE</h1>
            <p style="margin: 5px 0; font-size: 13px;"><b>Invoice No:</b> {latest_order['Invoice No']}<br><b>Date:</b> {latest_order['Date']}</p>
        </div>
    </div>
    
    <div style="display: flex; justify-content: space-between; margin-top: 20px; gap: 20px;">
        <div style="flex: 1; border: 1px solid #c8b198; padding: 12px; border-radius: 5px; background-color: #fdfbf7;">
            <p style="margin: 0 0 5px 0; font-size: 11px; color: #8c6239; font-weight: bold;">DELIVER TO</p>
            <p style="margin: 0; font-size: 13px; line-height: 1.4;"><b>{latest_order['Customer']}</b><br>{formatted_address}<br>TP: {latest_order['Phone']}</p>
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
            {cart_rows_html}
        </tbody>
    </table>
    
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-top: 20px;">
        <div style="border: 1px dashed #b5835a; padding: 8px 12px; border-radius: 4px; font-size: 12px; color: #5a3825; background-color: #faf4ed;">
            Note: + Delivery Fee | Category: {latest_order['Type']}<br>Issued By: {latest_order.get('Issued By', 'Admin')}
        </div>
        <div style="border: 2px solid #5a3825; padding: 12px 25px; border-radius: 6px; text-align: right; background-color: #fff;">
            <p style="margin: 0; font-size: 11px; color: #666; font-weight: bold;">TOTAL AMOUNT</p>
            <h2 style="margin: 5px 0 0 0; color: #5a3825; font-size: 22px;">{latest_order['Grand Total (LKR)']:,.2f} LKR</h2>
        </div>
    </div>
    
    <div style="margin-top: 35px; border: 1px solid #e0d0c0; background-color: #faf6f0; padding: 12px; text-align: center; border-radius: 5px;">
        <p style="margin: 0; color: #5a3825; font-weight: bold; font-size: 14px;">Thank you for your Order!</p>
        <p style="margin: 3px 0 0 0; font-size: 11px; color: #666;">Ceylon Coffee Tablets (Pvt) Ltd — Quality Sri Lankan Specialty Coffee Products</p>
    </div>
</div>
</body>
</html>"""
            
            st.markdown("---")
            st.download_button(
                label="📥 Download Official Invoice as HTML File (.html)",
                data=invoice_html.encode('utf-8'),
                file_name=f"{latest_order['Invoice No'].replace('/', '_')}.html",
                mime="text/html"
            )
            
            st.info("💡 **PDF ලෙස ලබා ගැනීමට:** ඉහත ඩවුන්ලෝඩ් කරගත් HTML ගොනුව ඔබගේ බ්‍රව්සරයෙන් විවෘත කර, **`Ctrl + P`** ඔබා **'Save as PDF'** තෝරාගෙන PDF එකක් ලෙස සේව් කරගන්න.")

# --- TAB 5: DIRECTORS & ALL RECORDS ---
with tabs[4]:
    st.header("Directors' Management Report & All Orders History")
    st.markdown("මාසිකව සහ දිනපතා නිකුත් කළ ටැබ්ලට් ප්‍රමාණයන් සහ ඇණවුම් වාර්තා මෙහි දැක්වේ.")

    if st.session_state.orders:
        total_orders_count = len(st.session_state.orders)
        total_tablets_dispatched = sum([order["Total Tablets"] for order in st.session_state.orders])
        total_revenue = sum([order["Grand Total (LKR)"] for order in st.session_state.orders])

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Orders Dispatched", total_orders_count)
        m2.metric("Total Tablets Dispatched", total_tablets_dispatched)
        m3.metric("Total Revenue (LKR)", f"LKR {total_revenue:,.2f}")

        st.markdown("---")
        st.subheader("Orders Ledger")
        
        display_orders = []
        for ord_item in st.session_state.orders:
            display_orders.append({
                "Invoice No": ord_item["Invoice No"],
                "Date/Time": ord_item["Date"],
                "Customer": ord_item["Customer"],
                "Type": ord_item["Type"],
                "Total Tablets": ord_item["Total Tablets"],
                "Grand Total (LKR)": f"{ord_item['Grand Total (LKR)']:,.2f}",
                "Issued By": ord_item.get("Issued By", "N/A")
            })
        orders_df = pd.DataFrame(display_orders)
        st.table(orders_df)
        
        st.download_button("📥 Download All Orders History Report (CSV)", orders_df.to_csv(index=False).encode('utf-8'), "all_orders_report.csv", "text/csv")

        if st.session_state.user_role == "Admin":
            if st.button("Clear All Orders History"):
                st.session_state.orders = []
                st.rerun()
    else:
        st.info("No orders recorded yet. දත්ත ඇතුළත් කළ පසු මෙහි වාර්තා දිස්වේ.")
