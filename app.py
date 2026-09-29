import streamlit as st
from datetime import datetime
import pandas as pd

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
if 'rm_logs' not in st.session_state:
    st.session_state.rm_logs = []
if 'current_cart' not in st.session_state:
    st.session_state.current_cart = []

st.title("Ceylon Coffee Tablets (Pvt) Ltd - Enterprise System")
st.markdown("*Drop it. Dissolve it. Done. | Corporate Management Portal*")

# Navigation Tabs
tabs = st.tabs([
    "📊 Cost Analysis", 
    "🧪 Lab & R&D Reports", 
    "📦 Raw Materials (RM-LOG)", 
    "📄 Invoice & Order Generator", 
    "📋 Directors & All Records"
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
    st.header("Lab & R&D Quality Control Reports (BPR-QC Master)")
    with st.form("rd_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            batch_no = st.text_input("Batch Number (e.g., CCT260930B)")
            variant = st.selectbox("Product Variant", ["Black Coffee (Light Roast)", "Black Coffee (Dark Roast)", "Cinnamon Coffee", "Ginger Coffee"])
        with col2:
            mfg_date = st.date_input("Manufacture Date")
            coffee_wt = st.number_input("Coffee Weight (kg)", value=5.0)
        with col3:
            moisture = st.number_input("Moisture Level (%) [Standard < 4.0%]", value=3.5, step=0.1)
            qc_status = st.selectbox("Batch Status", ["APPROVED FOR RELEASE", "REJECTED / HOLD"])

        submitted_rd = st.form_submit_button("Save R&D Report")
        if submitted_rd and batch_no:
            st.session_state.rd_logs.append({
                "Batch No": batch_no,
                "Variant": variant,
                "Date": str(mfg_date),
                "Moisture": f"{moisture}%",
                "Status": qc_status
            })
            st.success("R&D Report Saved Successfully!")

    if st.session_state.rd_logs:
        st.subheader("Saved R&D Logs")
        st.table(st.session_state.rd_logs)

# --- TAB 3: RAW MATERIALS (RM-LOG) ---
with tabs[2]:
    st.header("Raw Materials Inventory & Sourcing Management (RM-LOG)")
    st.markdown("Track raw material sources, supplier details, purchase costs, quantities, and expiry periods.")
    
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
                "Expiry Date": str(expiry_date)
            })
            st.success("Raw Material Record Saved Successfully!")

    if st.session_state.rm_logs:
        st.subheader("Raw Materials Stock & Sourcing Log")
        st.table(st.session_state.rm_logs)

# --- TAB 4: PROFESSIONAL INVOICE & ORDER GENERATOR ---
with tabs[3]:
    st.header("Multi-Item Invoice & Order Generator")
    st.markdown("Select pricing type (Retail or Trade), add multiple variants, enter customer details, and generate official invoices.")

    with st.form("customer_details_form"):
        st.subheader("1. Customer & Pricing Setup")
        c_name = st.text_input("Customer / Business Name", value="D.F.R perera")
        c_phone = st.text_input("Telephone Number", value="+94 77 123 4567")
        c_address = st.text_area("Delivery Address", value="49/2/2 Thekkawatta road\nThannakumbura\nKandy")
        pricing_type = st.selectbox("Select Pricing Category", ["Retail Price", "Trade Price"])
        save_cust_info = st.form_submit_button("Lock Customer Details")
        if save_cust_info:
            st.success("Customer details locked for current invoice!")

    st.markdown("---")
    st.subheader("2. Add Tablet Variants to Invoice Cart")
    with st.form("add_item_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            item_variant = st.selectbox("Select Tablet Variant", [
                "Black Coffee (Light Roast) - 15 Tablets Pack", 
                "Black Coffee (Dark Roast) - 15 Tablets Pack", 
                "Cinnamon Coffee 15 Tablets Pack", 
                "Ginger Coffee 15 Tablets Pack"
            ])
        with col_b:
            item_qty = st.number_input("Quantity (Packs / Units)", min_value=1, value=1)
            
        add_to_cart_btn = st.form_submit_button("Add Item to Cart")
        if add_to_cart_btn:
            unit_price = st.session_state.retail_price if pricing_type == "Retail Price" else st.session_state.trade_price
            st.session_state.current_cart.append({
                "Variant": item_variant,
                "Qty": item_qty,
                "Unit Price": unit_price,
                "Total": item_qty * unit_price
            })
            st.success(f"Added {item_variant} ({item_qty} units) to cart!")

    if st.session_state.current_cart:
        st.subheader("Current Cart Items")
        cart_df = pd.DataFrame(st.session_state.current_cart)
        st.table(cart_df)
        
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("Clear Cart"):
                st.session_state.current_cart = []
                st.rerun()
        with col_act2:
            finalize_order = st.button("Generate Official Invoice & Save Order")

        if finalize_order:
            grand_total = sum([item["Total"] for item in st.session_state.current_cart])
            total_tablets_count = sum([item["Qty"] for item in st.session_state.current_cart])
            
            invoice_no = f"CET {len(st.session_state.orders)+1010}"
            
            # Save to global orders history for Directors
            st.session_state.orders.append({
                "Invoice No": invoice_no,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Customer": c_name,
                "Phone": c_phone,
                "Address": c_address,
                "Type": pricing_type,
                "Items Count": len(st.session_state.current_cart),
                "Total Tablets": total_tablets_count,
                "Grand Total (LKR)": grand_total,
                "Cart Details": st.session_state.current_cart.copy()
            })
            
            st.success("Order finalized and saved to records successfully!")

            # Render Official Printable Invoice Layout matching user requirement
            cart_rows_html = ""
            for idx, cart_item in enumerate(st.session_state.current_cart, 1):
                cart_rows_html += f"""
                    <tr style="border-bottom: 1px solid #ddd; font-size: 13px;">
                        <td style="padding: 10px; text-align: center;">{idx:02d}</td>
                        <td style="padding: 10px;">{cart_item['Variant']} ({pricing_type})</td>
                        <td style="padding: 10px; text-align: center;">{cart_item['Qty']}</td>
                        <td style="padding: 10px; text-align: right;">{cart_item['Unit Price']:,.2f}</td>
                        <td style="padding: 10px; text-align: right;">{cart_item['Total']:,.2f}</td>
                    </tr>
                """

            invoice_html = f"""
            <div style="border: 2px solid #5a3825; padding: 25px; border-radius: 8px; font-family: Arial, sans-serif; background-color: #ffffff; color: #000000; margin-top: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #5a3825; padding-bottom: 15px;">
                    <div>
                        <h2 style="margin: 0; color: #5a3825; font-size: 22px;">CEYLON COFFEE TABLETS (PVT) LTD</h2>
                        <p style="margin: 3px 0; font-size: 12px; color: #555;">No 173, Hepana, Pilimathalawa<br>TP: +94 76 367 6856</p>
                    </div>
                    <div style="text-align: right;">
                        <h1 style="margin: 0; color: #5a3825; font-size: 26px; letter-spacing: 2px;">INVOICE</h1>
                        <p style="margin: 5px 0; font-size: 13px;"><b>Invoice No:</b> {invoice_no}<br><b>Date:</b> {datetime.now().strftime('%d b, %Y')}</p>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-top: 20px; gap: 20px;">
                    <div style="flex: 1; border: 1px solid #c8b198; padding: 12px; border-radius: 5px; background-color: #fdfbf7;">
                        <p style="margin: 0 0 5px 0; font-size: 11px; color: #8c6239; font-weight: bold;">DELIVER TO</p>
                        <p style="margin: 0; font-size: 13px; line-height: 1.4;"><b>{c_name}</b><br>{c_address.replace(chr(10), '<br>')}<br>TP: {c_phone}</p>
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
                        Note: + Delivery Fee | Category: {pricing_type}
                    </div>
                    <div style="border: 2px solid #5a3825; padding: 12px 25px; border-radius: 6px; text-align: right; background-color: #fff;">
                        <p style="margin: 0; font-size: 11px; color: #666; font-weight: bold;">TOTAL AMOUNT</p>
                        <h2 style="margin: 5px 0 0 0; color: #5a3825; font-size: 22px;">{grand_total:,.2f} LKR</h2>
                    </div>
                </div>
                
                <div style="margin-top: 35px; border: 1px solid #e0d0c0; background-color: #faf6f0; padding: 12px; text-align: center; border-radius: 5px;">
                    <p style="margin: 0; color: #5a3825; font-weight: bold; font-size: 14px;">Thank you for your Order!</p>
                    <p style="margin: 3px 0 0 0; font-size: 11px; color: #666;">Ceylon Coffee Tablets (Pvt) Ltd — Quality Sri Lankan Specialty Coffee Products</p>
                </div>
            </div>
            """
            st.markdown(invoice_html, unsafe_allow_html=True)
            st.info("💡 **මෙම ඉන්වොයිසිය PDF ලෙස ලබාගැනීමට:** බ්‍රවුසර් එකේ `Ctrl+P` (Windows) හෝ `Cmd+P` (Mac) ඔබා 'Save as PDF' තෝරාගන්න.")

# --- TAB 5: DIRECTORS & ALL RECORDS ---
with tabs[4]:
    st.header("Directors' Management Report & All Orders History")
    st.markdown("Monthly and overall summary of dispatches, orders, total tablet quantities sold, and revenue for corporate directors.")

    if st.session_state.orders:
        # Calculate summary metrics
        total_orders_count = len(st.session_state.orders)
        total_tablets_dispatched = sum([order["Total Tablets"] for order in st.session_state.orders])
        total_revenue = sum([order["Grand Total (LKR)"] for order in st.session_state.orders])

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Orders Dispatched", total_orders_count)
        m2.metric("Total Tablets Sold", total_tablets_dispatched)
        m3.metric("Total Revenue (LKR)", f"LKR {total_revenue:,.2f}")

        st.markdown("---")
        st.subheader("Detailed Orders Ledger")
        
        # Display simplified table for directors
        display_orders = []
        for ord_item in st.session_state.orders:
            display_orders.append({
                "Invoice No": ord_item["Invoice No"],
                "Date/Time": ord_item["Date"],
                "Customer": ord_item["Customer"],
                "Type": ord_item["Type"],
                "Total Tablets": ord_item["Total Tablets"],
                "Grand Total (LKR)": f"{ord_item['Grand Total (LKR)']:,.2f}"
            })
        st.table(display_orders)

        if st.button("Clear All Orders History"):
            st.session_state.orders = []
            st.rerun()
    else:
        st.info("No orders recorded yet. Generate invoices from the 'Invoice & Order Generator' tab to populate this dashboard.")
