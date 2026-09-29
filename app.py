import streamlit as st
from datetime import datetime, timedelta
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

# Session State Initialization
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
if 'bpr_logs' not in st.session_state:
    st.session_state.bpr_logs = []
if 'dealers_logs' not in st.session_state:
    st.session_state.dealers_logs = []
if 'letters_logs' not in st.session_state:
    st.session_state.letters_logs = []
if 'invoice_cart' not in st.session_state:
    st.session_state.invoice_cart = []
if 'expenses_logs' not in st.session_state:
    st.session_state.expenses_logs = []

if 'tablet_stock' not in st.session_state:
    st.session_state.tablet_stock = {
        "Black Coffee (Light Roast)": 0,
        "Black Coffee (Dark Roast)": 0,
        "Cinnamon Coffee": 0,
        "Ginger Coffee": 0
    }

if 'raw_stock' not in st.session_state:
    st.session_state.raw_stock = {
        "Green Coffee Beans (Arabica)": 0.0,
        "Ginger Extract Powder": 0.0,
        "Cinnamon Extract Powder": 0.0,
        "Tableting Excipients / Binders": 0.0,
        "Packaging Foils": 0.0,
        "Gloves": 0.0,
        "Masks": 0.0,
        "Sugar / Sweetener": 0.0
    }

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

# --- SIDEBAR NAVIGATION MENU ---
st.sidebar.title("Ceylon Coffee Portal")
st.sidebar.write(f"👤 **User:** {st.session_state.current_user}")
st.sidebar.write(f"🛡️ **Role:** {st.session_state.user_role}")
st.sidebar.markdown("---")

st.sidebar.subheader("Navigation Menu")
menu_selection = st.sidebar.radio(
    "Select Section", 
    [
        "🏠 Welcome & Overview", 
        "📊 Cost & Pricing", 
        "💸 Expenses Report", 
        "📈 Financial P&L & Profit Sharing", 
        "🏭 Batch Production (BPR)", 
        "📦 Stores & Stock", 
        "🧪 Lab & R&D Reports", 
        "🤝 Dealers Directory", 
        "✉️ Letters & Memos", 
        "📄 Invoice Generator", 
        "📋 Directors Dashboard"
    ]
)

st.sidebar.markdown("---")
if st.session_state.prices_locked:
    st.sidebar.error("🔒 Cost & Pricing is **LOCKED**")
else:
    st.sidebar.success("🔓 Cost & Pricing is **UNLOCKED**")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.user_role = ""
    st.rerun()

# --- SECTION 0: WELCOME & OVERVIEW ---
if menu_selection == "🏠 Welcome & Overview":
    st.title("Ceylon Coffee Tablets (Pvt) Ltd")
    st.markdown("### *Drop it. Dissolve it. Done. | Premium Sri Lankan Specialty Coffee Innovation*")
    st.markdown("---")
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("""
        ### අපගේ සංකල්පය සහ නිෂ්පාදනය
        ශ්‍රී ලංකාවේ උසස්ම තත්වයේ අරාබිකා (Arabica) කෝපි බීජ මෙන්ම කුරුඳු (Cinnamon) සහ ඉඟුරු (Ginger) සාරය එකතු කරමින්, නවීන තාක්ෂණය යටතේ නිෂ්පාදනය කරනු ලබන **දියවන කෝපි ටැබ්ලට් (Soluble Coffee Tablets)** නිෂ්පාදනයේ ප්‍රමුඛයා වන්නේ **Ceylon Coffee Tablet (Pvt) Ltd** අප ආයතනයයි.
        """)
    with col_w2:
        st.info("""
        📌 **නව අංගයන් සහ විශේෂාංග:**
        - **Expenses Report (වියදම් වාර්තාව):** රෝ මැටීරියල්ස් (Coffee, Ginger, Cinnamon), Gloves, Masks, Sugar සහ වෙනත් උපකරණ මිලදී ගැනීම් සඳහා වන වියදම් වාර්තාගත කිරීම.
        - **Financial P&L & Profit Sharing:** මුළු ආදායම, නිෂ්පාදන වියදම්, ශුද්ධ ලාභය (Net Profit), සමාගමේ වැඩිදියුණුවට නැවත ආයෝජනය (Reinvestment) සහ අධ්‍යක්ෂවරුන් 5 දෙනා අතර ලාභ බෙදීයාම.
        - **ඩිරෙක්ටර්ස් ඩෑෂ්බෝඩ් (Directors Dashboard):** සියලුම වාර්තා මුද්‍රණය කිරීමට සහ ඩවුන්ලෝඩ් කර ගැනීමට ඇති හැකියාව.
        """)

# --- SECTION 1: COST & PROFIT ANALYSIS ---
elif menu_selection == "📊 Cost & Pricing":
    st.header("Tablet Production Cost & Profit Structure Analysis")
    
    if st.session_state.prices_locked:
        st.warning("🔒 **මෙම මිල ගණන් සහ නිෂ්පාදන පිරිවැය මේ වන විට ADMIN විසින් Lock කර ඇත.**")
    else:
        st.info("🔓 පද්ධතිය දැනට Unlock කර ඇත.")

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

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cost Inputs")
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

# --- SECTION 2: EXPENSES REPORT ---
elif menu_selection == "💸 Expenses Report":
    st.header("Expenses Report & Operational Cost Tracking")
    st.markdown("අධ්‍යක්ෂවරුන් විසින් දරනු ලබන වියදම් (රෝ මැටීරියල්ස්, Gloves, Masks, Sugar සහ අනෙකුත් උපකරණ මිලදී ගැනීම්) මෙහි ඇතුළත් කර වාර්තා කරගත හැක.")

    with st.form("expenses_form"):
        e1, e2 = st.columns(2)
        with e1:
            exp_date = st.date_input("Expense Date", value=datetime.now().date())
            expense_category = st.selectbox("Expense Category", [
                "Raw Materials - Coffee Beans (Arabica)",
                "Raw Materials - Ginger Extract",
                "Raw Materials - Cinnamon Extract",
                "Safety Gear - Gloves",
                "Safety Gear - Masks",
                "Ingredients - Sugar / Sweetener",
                "Packaging Foils & Bottles",
                "Equipment & Machinery",
                "Other / Miscellaneous Expenses"
            ])
            custom_item_name = st.text_input("Custom Item / Description (අවශ්‍ය නම් වෙනත් අයිතමයක් නම් කරන්න)")
        with e2:
            funded_by = st.selectbox("Funded / Paid By (Director Name)", list(USERS.keys()))
            amount_lkr = st.number_input("Total Expense Amount (LKR)", value=5000.0, step=100.0)
            receipt_ref = st.text_input("Receipt / Invoice Reference No")

        submit_exp = st.form_submit_button("Save Expense Record")
        if submit_exp:
            item_desc = custom_item_name if custom_item_name else expense_category
            st.session_state.expenses_logs.append({
                "Date": str(exp_date),
                "Category": expense_category,
                "Item Description": item_desc,
                "Funded By": funded_by,
                "Amount (LKR)": amount_lkr,
                "Reference": receipt_ref
            })
            st.success(f"Expense of LKR {amount_lkr:,.2f} for '{item_desc}' funded by {funded_by} saved successfully!")

    if st.session_state.expenses_logs:
        st.subheader("Recorded Expenses Ledger")
        total_exp_sum = sum([item["Amount (LKR)"] for item in st.session_state.expenses_logs])
        st.metric("Total Accumulated Expenses", f"LKR {total_exp_sum:,.2f}")
        
        for idx, exp in enumerate(st.session_state.expenses_logs):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"📅 {exp['Date']} | **{exp['Item Description']}** | Paid by: `{exp['Funded By']}` | **LKR {exp['Amount (LKR)']:,.2f}** (Ref: {exp['Reference']})")
            with c2:
                if st.button("Delete", key=f"del_exp_{idx}"):
                    st.session_state.expenses_logs.pop(idx)
                    st.rerun()

        exp_df = pd.DataFrame(st.session_state.expenses_logs)
        st.download_button("🖨️ Download Expenses Report (CSV)", exp_df.to_csv(index=False).encode('utf-8'), "expenses_report.csv", "text/csv")
    else:
        st.info("No expense records found yet.")

# --- SECTION 3: FINANCIAL P&L & PROFIT SHARING ---
elif menu_selection == "📈 Financial P&L & Profit Sharing":
    st.header("Financial P&L, Reinvestment & Directors Profit Sharing (5 Directors)")
    st.markdown("සමාගමේ සමස්ත ආදායම, වියදම් සහ ශුද්ධ ලාභය ගණනය කර, ඉන් ප්‍රතිශතයක් සමාගම ඉදිරියට ගෙනයාමට නැවත ආයෝජනය (Reinvestment) කර, ඉතිරිය අධ්‍යක්ෂවරුන් 5 දෙනා අතර බෙදී යන ආකාරය මෙහි දැක්වේ.")

    total_revenue = sum([order["Grand Total (LKR)"] for order in st.session_state.orders])
    total_expenses = sum([item["Amount (LKR)"] for item in st.session_state.expenses_logs])
    net_profit = total_revenue - total_expenses

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total Revenue (IN)", f"LKR {total_revenue:,.2f}")
    col_m2.metric("Total Expenses (OUT)", f"LKR {total_expenses:,.2f}")
    col_m3.metric("Net Profit / Loss", f"LKR {net_profit:,.2f}")

    st.markdown("---")
    st.subheader("Profit Allocation & Reinvestment Settings")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        reinvest_percentage = st.slider("Company Reinvestment Percentage (%) [සමාගම වෙනුවෙන් රඳවා ගන්නා ප්‍රතිශතය]", 0, 100, 40)
    with col_s2:
        directors_share_pct = 100 - reinvest_percentage
        st.info(f"**Directors Total Share Percentage:** {directors_share_pct}% (Divided equally among 5 Directors)")

    reinvest_amount = (net_profit * reinvest_percentage) / 100 if net_profit > 0 else 0
    directors_total_pool = (net_profit * directors_share_pct) / 100 if net_profit > 0 else 0
    per_director_share = directors_total_pool / 5.0 if net_profit > 0 else 0

    st.markdown("---")
    st.subheader("Profit Distribution Summary (5 Directors)")
    
    p1, p2 = st.columns(2)
    with p1:
        st.success(f"🏢 **Reinvested into Company Growth:** LKR {reinvest_amount:,.2f} ({reinvest_percentage}%)")
    with p2:
        st.warning(f"👥 **Total Directors Pool:** LKR {directors_total_pool:,.2f} ({directors_share_pct}%)")

    st.markdown("### Directors Share Breakdown (5 Directors)")
    directors_list = ["Krishan Damith", "Shehan Maduranga", "Kanishka Dulanjana", "Chanuka Vinod", "Pasindu Sachintha"]
    
    dir_rows = []
    for d in directors_list:
        dir_rows.append({
            "Director Name": d,
            "Share Percentage": f"{directors_share_pct / 5.0:.1f}%",
            "Allocated Amount (LKR)": f"LKR {per_director_share:,.2f}"
        })
    
    dir_df = pd.DataFrame(dir_rows)
    st.table(dir_df)

    pnl_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Financial P&L and Profit Sharing Report</title></head>
<body style="font-family: Arial, sans-serif; padding: 30px; color: #333;">
    <h2 style="color: #5a3825; text-align: center;">CEYLON COFFEE TABLETS (PVT) LTD</h2>
    <h3 style="text-align: center; color: #666;">Financial Profit & Loss and Directors Profit Sharing Report</h3>
    <hr style="border: 1px solid #5a3825;">
    <p><b>Total Revenue:</b> LKR {total_revenue:,.2f}</p>
    <p><b>Total Expenses:</b> LKR {total_expenses:,.2f}</p>
    <p><b>Net Profit:</b> LKR {net_profit:,.2f}</p>
    <p><b>Reinvested in Company ({reinvest_percentage}%):</b> LKR {reinvest_amount:,.2f}</p>
    <p><b>Directors Total Pool ({directors_share_pct}%):</b> LKR {directors_total_pool:,.2f}</p>
    <p><b>Per Director Share (5 Directors):</b> LKR {per_director_share:,.2f} each</p>
    <br><p style="font-size: 12px; color: #777; text-align: center;">Generated via Ceylon Coffee Tablets Enterprise Portal</p>
</body>
</html>"""

    st.download_button(
        label="🖨️ Download P&L & Profit Sharing Report (.html for Printing)",
        data=pnl_html.encode('utf-8'),
        file_name=f"Financial_PNL_Report_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html"
    )

# --- SECTION 4: BATCH PRODUCTION RECORD (BPR MASTER) ---
elif menu_selection == "🏭 Batch Production (BPR)":
    st.header("Batch Production Record (BPR) Master System")
    with st.form("bpr_form"):
        st.subheader("1. Batch Identification & Metadata (Auto Generated)")
        b1, b2, b3 = st.columns(3)
        with b1:
            bpr_mfg = st.date_input("Manufacture Date", value=datetime.now().date())
            auto_batch_no = f"CCT{bpr_mfg.strftime('%y%m%d')}"
            st.text_input("Auto Batch Number", value=auto_batch_no, disabled=True)
        with b2:
            auto_exp = bpr_mfg + timedelta(days=240)
            st.text_input("Auto Expiry Date (+8 Months)", value=str(auto_exp), disabled=True)
            bpr_variant = st.selectbox("Product Variant", ["Black Coffee (Light Roast)", "Black Coffee (Dark Roast)", "Cinnamon Coffee", "Ginger Coffee"])
        with b3:
            bpr_target_qty = st.number_input("Target Tablets Quantity Produced", value=150)
            bpr_operator = st.text_input("Operator / Technician Name")

        bpr_submit = st.form_submit_button("Save Batch & Update Stock")
        if bpr_submit:
            st.session_state.bpr_logs.append({
                "Batch No": auto_batch_no,
                "Variant": bpr_variant,
                "Mfg Date": str(bpr_mfg),
                "Expiry Date": str(auto_exp),
                "Tablets Produced": bpr_target_qty,
                "Operator": bpr_operator
            })
            if bpr_variant in st.session_state.tablet_stock:
                st.session_state.tablet_stock[bpr_variant] += bpr_target_qty
            st.success(f"Batch {auto_batch_no} saved successfully!")

    if st.session_state.bpr_logs:
        st.subheader("Saved Batch Production Records")
        for idx, log in enumerate(st.session_state.bpr_logs):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"**{log['Batch No']}** | {log['Variant']} | Qty: {log['Tablets Produced']}")
            with c2:
                if st.button("Delete", key=f"del_bpr_{idx}"):
                    st.session_state.bpr_logs.pop(idx)
                    st.rerun()

# --- SECTION 5: STORES & STOCK ---
elif menu_selection == "📦 Stores & Stock":
    st.header("Stores & Stock Management (Raw Materials & Tablets)")
    col_st1, col_st2 = st.columns(2)
    with col_st1:
        st.subheader("📦 Raw Materials Stock Balance")
        rm_stock_df = pd.DataFrame(list(st.session_state.raw_stock.items()), columns=["Raw Material Item", "Available Quantity"])
        st.table(rm_stock_df)
    with col_st2:
        st.subheader("💊 Finished Tablets Stock Balance")
        tab_stock_df = pd.DataFrame(list(st.session_state.tablet_stock.items()), columns=["Tablet Variant", "Available Quantity"])
        st.table(tab_stock_df)

# --- SECTION 6: LAB & R&D REPORTS ---
elif menu_selection == "🧪 Lab & R&D Reports":
    st.header("Lab & R&D Quality Control Reports (PDF Scanner & Management)")
    uploaded_lab_file = st.file_uploader("Upload Lab Report (PDF / PNG / JPG)", type=["png", "jpg", "jpeg", "pdf"], key="lab_file_uploader")

    default_batch = "RND-TR-2025-013"
    default_date = datetime.strptime("2025-11-25", "%Y-%m-%d").date()

    with st.form("rd_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            batch_no = st.text_input("Test Report Ref / Batch No", value=default_batch)
            variant = st.selectbox("Product Variant", ["Black Coffee (Light Roast)", "Black Coffee (Dark Roast)", "Cinnamon Coffee", "Ginger Coffee"])
        with col2:
            mfg_date = st.date_input("Test Date", value=default_date)
            coffee_wt = st.number_input("Coffee Weight / Base (g)", value=10.0)
        with col3:
            moisture = st.number_input("Moisture / Thermal Level", value=100.0, step=1.0)
            qc_status = st.selectbox("Batch Status", ["Completed / Verified", "APPROVED FOR RELEASE", "REJECTED / HOLD"])

        submitted_rd = st.form_submit_button("Save R&D Report")
        if submitted_rd:
            file_name = uploaded_lab_file.name if uploaded_lab_file is not None else "RND-TR-2025-013.pdf"
            st.session_state.rd_logs.append({
                "Batch No": batch_no,
                "Variant": variant,
                "Date": str(mfg_date),
                "Status": qc_status,
                "Attached File": file_name
            })
            st.success(f"✅ Lab Report '{batch_no}' saved successfully!")

    if st.session_state.rd_logs:
        st.subheader("Saved Lab & R&D Logs")
        for idx, log in enumerate(st.session_state.rd_logs):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"**{log['Batch No']}** | {log['Variant']} | Date: {log['Date']} | Status: {log['Status']}")
            with c2:
                if st.button("Delete", key=f"del_rd_{idx}"):
                    st.session_state.rd_logs.pop(idx)
                    st.rerun()

# --- SECTION 7: DEALERS DIRECTORY ---
elif menu_selection == "🤝 Dealers Directory":
    st.header("Local & Foreign Dealers Directory")
    if st.session_state.user_role == "Admin":
        with st.form("dealer_form"):
            dealer_name = st.text_input("Dealer / Business Name")
            country = st.text_input("Country & City (e.g., Sweden, Kalmar)")
            save_dealer = st.form_submit_button("Save Dealer Record")
            if save_dealer and dealer_name:
                st.session_state.dealers_logs.append({"Dealer Name": dealer_name, "Country": country})
                st.success("Dealer saved successfully!")
        if st.session_state.dealers_logs:
            for idx, d in enumerate(st.session_state.dealers_logs):
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.write(f"**{d['Dealer Name']}** ({d['Country']})")
                with c2:
                    if st.button("Delete", key=f"del_dlr_{idx}"):
                        st.session_state.dealers_logs.pop(idx)
                        st.rerun()
    else:
        st.error("🔒 Admin access required.")

# --- SECTION 8: LETTERS & MEMOS ---
elif menu_selection == "✉️ Letters & Memos":
    st.header("Official Letters & Memos")
    with st.form("letter_form"):
        subject_title = st.text_input("Subject / Title")
        submitted_letter = st.form_submit_button("Save Document")
        if submitted_letter and subject_title:
            st.session_state.letters_logs.append({"Subject": subject_title})
            st.success("Document saved!")
    if st.session_state.letters_logs:
        for idx, l in enumerate(st.session_state.letters_logs):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"**{l['Subject']}**")
            with c2:
                if st.button("Delete", key=f"del_let_{idx}"):
                    st.session_state.letters_logs.pop(idx)
                    st.rerun()

# --- SECTION 9: INVOICE GENERATOR ---
elif menu_selection == "📄 Invoice Generator":
    st.header("Official Invoice Generator")
    inv_no = st.text_input("Invoice Number", value="CCT-00012")
    cust_name = st.text_input("Customer Name")
    with st.form("add_cart_form"):
        c_var = st.selectbox("Coffee Variant", list(st.session_state.tablet_stock.keys()))
        c_qty = st.number_input("Quantity", min_value=1, value=10)
        if st.form_submit_button("Add to Cart"):
            st.session_state.invoice_cart.append({"Variant": c_var, "Qty": c_qty, "Total": c_qty * st.session_state.retail_price})
            st.success("Added to cart!")
    if st.session_state.invoice_cart:
        st.table(pd.DataFrame(st.session_state.invoice_cart))
        if st.button("Generate & Save Invoice"):
            st.session_state.orders.append({
                "Invoice No": inv_no,
                "Customer": cust_name,
                "Total Tablets": sum([i['Qty'] for i in st.session_state.invoice_cart]),
                "Grand Total (LKR)": sum([i['Total'] for i in st.session_state.invoice_cart])
            })
            st.success("Invoice generated and saved!")

# --- SECTION 10: DIRECTORS DASHBOARD ---
elif menu_selection == "📋 Directors Dashboard":
    st.header("Directors' Central Records & Master Dashboard")
    report_category = st.selectbox("Select Category", [
        "Expenses Report",
        "Financial P&L & Profit Sharing",
        "Batch Production Records (BPR)",
        "Lab & R&D Reports", 
        "Raw Materials (RM-LOG)", 
        "Official Letters & Memos", 
        "Invoices & Dispatched Orders"
    ])
    st.markdown("---")
    if report_category == "Expenses Report":
        if st.session_state.expenses_logs:
            st.dataframe(pd.DataFrame(st.session_state.expenses_logs), use_container_width=True)
        else:
            st.info("No expenses found.")
    elif report_category == "Financial P&L & Profit Sharing":
        st.info("Check the 'Financial P&L & Profit Sharing' tab for complete breakdowns and printable reports.")
    elif report_category == "Lab & R&D Reports":
        if st.session_state.rd_logs:
            st.dataframe(pd.DataFrame(st.session_state.rd_logs), use_container_width=True)
        else:
            st.info("No lab reports found.")
    elif report_category == "Invoices & Dispatched Orders":
        if st.session_state.orders:
            st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True)
        else:
            st.info("No orders found.")
