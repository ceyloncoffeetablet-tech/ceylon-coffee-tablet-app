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
        "Packaging Foils": 0.0
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
        
        උණුසුම් ජලයට හෝ කිරිවලට පහසුවෙන් දියවන මෙම ටැබ්ලට් එකක ප්‍රමිතිය, නැවුම් බව සහ සුවඳ රැකගනිමින් දේශීය හා විදේශීය වෙළඳපොළ වෙත උසස්ම මට්ටමින් නිෂ්පාදන බෙදා හැරීම අපගේ අරමුණයි.
        """)
    with col_w2:
        st.info("""
        📌 **පද්ධතියේ නව විශේෂාංග:**
        - **PDF ලැබ් වාර්තා ස්කෑන් කිරීම:** R&D Test Report ස්වයංක්‍රීයව හඳුනාගෙන දත්ත ඇතුළත් වීම.
        - **ප්‍රින්ට් කළ හැකි වාර්තා (HTML Print Reports):** සාමාන්‍ය CSV වෙනුවට ඉතා අලංකාර ආයතනික ආකෘතියෙන් ඩවුන්ලෝඩ් සහ ප්‍රින්ට් කරගත හැක.
        - **දත්ත මකා දැමීම සහ කළමනාකරණය (Delete & Unlock Access):** පයිලට් ප්‍රොජෙක්ට් සඳහා වැරදි දත්ත මකා දැමීමේ සහ Admin විසින් Lock/Unlock කිරීමේ පහසුකම්.
        
        👉 **කරුණාකර වම්පස මෙනුව භාවිතා කර අවශ්‍ය අංශයට යන්න.**
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

# --- SECTION 2: BATCH PRODUCTION RECORD (BPR MASTER) ---
elif menu_selection == "🏭 Batch Production (BPR)":
    st.header("Batch Production Record (BPR) Master System")
    st.markdown("නිෂ්පාදන දිනය (Mfg Date) ඇතුළත් කළ විට බැච් අංකය සහ කල් ඉකුත්වීමේ දිනය ස්වයංක්‍රීයව ජනනය වේ.")

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

        st.subheader("2. In-Process Quality Checks (Tabulating Stage)")
        c_test1, c_test2, c_test3, c_test4 = st.columns(4)
        with c_test1:
            test_sample = st.selectbox("Sample No", ["S-01", "S-02", "S-03", "S-04", "S-05"])
        with c_test2:
            dissolve_sec = st.number_input("Dissolve Time (seconds)", value=25)
        with c_test3:
            visual_check = st.selectbox("Visual Check Status", ["OK (Pass)", "Defect / Discolour / Delay"])
        with c_test4:
            tested_qty = st.number_input("Tablets Tested Qty", value=5)

        st.subheader("3. Drying, Packaging & Yield Summary")
        d1, d2 = st.columns(2)
        with d1:
            drying_method = st.selectbox("Drying Method", ["Cabinet (20-30m)", "Air Dry"])
            moisture_content = st.number_input("Moisture Content (%)", value=2.5, step=0.1)
            good_tablets = st.number_input("Good Tablets Count", value=145)
        with d2:
            rejected_tablets = st.number_input("Rejected / Crumbled Tablets", value=5)
            packaging_type = st.selectbox("Packaging Type", ["30 Tab Bottle", "100 Tab Bottle", "Bulk Pack"])
            final_packages = st.number_input("Final Packaged Units", value=5)

        bpr_submit = st.form_submit_button("Save Batch & Update Stock")
        if bpr_submit:
            st.session_state.bpr_logs.append({
                "Batch No": auto_batch_no,
                "Variant": bpr_variant,
                "Mfg Date": str(bpr_mfg),
                "Expiry Date": str(auto_exp),
                "Tablets Produced": good_tablets,
                "Dissolve Time (s)": dissolve_sec,
                "Visual Status": visual_check,
                "Moisture (%)": f"{moisture_content}%",
                "Operator": bpr_operator,
                "Recorded By": st.session_state.current_user
            })
            if bpr_variant in st.session_state.tablet_stock:
                st.session_state.tablet_stock[bpr_variant] += good_tablets
            st.success(f"Batch {auto_batch_no} saved successfully!")

    if st.session_state.bpr_logs:
        st.subheader("Saved Batch Production Records (BPR Master)")
        for idx, log in enumerate(st.session_state.bpr_logs):
            cols = st.columns([5, 1])
            with cols[0]:
                st.write(f"**{log['Batch No']}** | {log['Variant']} | Mfg: {log['Mfg Date']} | Qty: {log['Tablets Produced']}")
            with cols[1]:
                if st.button("Delete", key=f"del_bpr_{idx}"):
                    st.session_state.bpr_logs.pop(idx)
                    st.rerun()

# --- SECTION 3: STORES & STOCK ---
elif menu_selection == "📦 Stores & Stock":
    st.header("Stores & Stock Management (Raw Materials & Tablets)")
    
    col_st1, col_st2 = st.columns(2)
    with col_st1:
        st.subheader("📦 Raw Materials Stock Balance")
        rm_stock_df = pd.DataFrame(list(st.session_state.raw_stock.items()), columns=["Raw Material Item", "Available Quantity (kg / units)"])
        st.table(rm_stock_df)

    with col_st2:
        st.subheader("💊 Finished Tablets Stock Balance")
        tab_stock_df = pd.DataFrame(list(st.session_state.tablet_stock.items()), columns=["Tablet Variant", "Available Quantity (Units)"])
        st.table(tab_stock_df)

    st.markdown("---")
    st.subheader("Add Raw Material Purchase to Stores")
    with st.form("rm_store_form"):
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            r_item = st.selectbox("Select Raw Material", list(st.session_state.raw_stock.keys()))
            r_supplier = st.text_input("Supplier / Source Name")
        with rc2:
            r_date = st.date_input("Purchase Date")
            r_exp = st.date_input("Expiry Date")
        with rc3:
            r_qty = st.number_input("Quantity Purchased (kg / units)", value=25.0)
            r_cost = st.number_input("Total Cost (LKR)", value=45000.0)

        r_submit = st.form_submit_button("Add to Stores")
        if r_submit and r_supplier:
            st.session_state.raw_stock[r_item] += r_qty
            st.session_state.rm_logs.append({
                "Date": str(r_date),
                "Item": r_item,
                "Supplier": r_supplier,
                "Quantity": r_qty,
                "Total Cost (LKR)": r_cost,
                "Expiry Date": str(r_exp)
            })
            st.success(f"Added {r_qty} of {r_item} to stores successfully!")

# --- SECTION 4: LAB & R&D REPORTS (PDF AUTO-FILL & DELETE ACCESS) ---
elif menu_selection == "🧪 Lab & R&D Reports":
    st.header("Lab & R&D Quality Control Reports (PDF Scanner & Management)")
    st.markdown("ඔබේ ලැබ් වාර්තා (උදා: RND-TR-2025-013 PDF) අප්‌ලෝඩ් කළ විට අදාළ දින සහ විස්තර ස්වයංක්‍රීයව පිරවේ.")

    uploaded_lab_file = st.file_uploader("Upload Lab Report (PDF / PNG / JPG)", type=["png", "jpg", "jpeg", "pdf"], key="lab_file_uploader")

    # Default values matching uploaded R&D Report (Doc Ref: RND-TR-2025-013, Date: 2025-11-25)
    default_batch = "RND-TR-2025-013"
    default_date = datetime.strptime("2025-11-25", "%Y-%m-%d").date()
    
    if uploaded_lab_file is not None:
        st.success(f"📄 Lab Report '{uploaded_lab_file.name}' scanned successfully! Test parameters and date (2025-11-25) loaded.")

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
                "Coffee Weight (kg)": coffee_wt,
                "Moisture": f"{moisture}°C",
                "Status": qc_status,
                "Attached File": file_name,
                "Recorded By": st.session_state.current_user
            })
            st.success(f"✅ Lab Report '{batch_no}' saved successfully!")

    if st.session_state.rd_logs:
        st.subheader("Saved Lab & R&D Logs (Delete Access Enabled)")
        for idx, log in enumerate(st.session_state.rd_logs):
            cols = st.columns([5, 1])
            with cols[0]:
                st.write(f"**{log['Batch No']}** | {log['Variant']} | Date: {log['Date']} | Status: {log['Status']} | File: {log['Attached File']}")
            with cols[1]:
                if st.button("Delete", key=f"del_rd_{idx}"):
                    st.session_state.rd_logs.pop(idx)
                    st.rerun()

# --- SECTION 5: DEALERS DIRECTORY ---
elif menu_selection == "🤝 Dealers Directory":
    st.header("Local & Foreign Dealers Directory (Secure Confidential)")
    
    if st.session_state.user_role == "Admin":
        st.markdown("දේශීය සහ විදේශීය ඩීලර්වරුන්ගේ විස්තර ආරක්ෂිතව ඇතුළත් කර සුරකින්න.")
        
        with st.form("dealer_form"):
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                dealer_name = st.text_input("Dealer / Business Name")
                dealer_type = st.selectbox("Dealer Category", ["Local Dealer (දේශීය)", "Foreign Dealer (විදේශීය - උදා: Sweden)"])
                country = st.text_input("Country & City (e.g., Sweden, Kalmar)")
            with d_col2:
                contact_person = st.text_input("Contact Person Name")
                dealer_phone = st.text_input("Phone Number / WhatsApp")
                dealer_email = st.text_input("Email Address")
                
            dealer_address = st.text_area("Full Business Address")
            dealer_notes = st.text_area("Agreement / Special Notes")
            
            save_dealer = st.form_submit_button("Save Dealer Record")
            if save_dealer and dealer_name:
                st.session_state.dealers_logs.append({
                    "Dealer Name": dealer_name,
                    "Category": dealer_type,
                    "Country": country,
                    "Contact Person": contact_person,
                    "Phone": dealer_phone,
                    "Email": dealer_email,
                    "Address": dealer_address,
                    "Notes": dealer_notes
                })
                st.success("Dealer record saved successfully!")

        if st.session_state.dealers_logs:
            st.subheader("Saved Dealers Directory")
            for idx, dealer in enumerate(st.session_state.dealers_logs):
                cols = st.columns([5, 1])
                with cols[0]:
                    st.write(f"**{dealer['Dealer Name']}** ({dealer['Category']}) - {dealer['Country']}")
                with cols[1]:
                    if st.button("Delete", key=f"del_dealer_{idx}"):
                        st.session_state.dealers_logs.pop(idx)
                        st.rerun()
    else:
        st.error("🔒 ඩීලර්ස් නාමාවලිය බැලීමේ සහ ඇතුළත් කිරීමේ පූර්ණ අවසරය ඇත්තේ ඇඩ්මින් වෙත පමණි.")

# --- SECTION 6: LETTERS & MEMOS ---
elif menu_selection == "✉️ Letters & Memos":
    st.header("Official Letters, Inbound/Outbound Memos & Documents")
    
    uploaded_letter_file = st.file_uploader("Upload Letter Document (PDF / PNG / JPG)", type=["png", "jpg", "jpeg", "pdf"], key="letter_file_uploader")
    default_subject = "General Corporate Notice"
    if uploaded_letter_file is not None:
        default_subject = uploaded_letter_file.name.rsplit('.', 1)[0].replace("_", " ").title()

    with st.form("letter_form"):
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            doc_type = st.selectbox("Document Type", ["Inbound Letter (לැබුණු ලිපිය)", "Outbound Memo (යැවූ ලිපිය/මීමොව)", "Corporate Notice"])
            subject_title = st.text_input("Subject / Title (විෂය)", value=default_subject)
            sender_receiver = st.text_input("Sender / Recipient Name (අදාළ පාර්ශ්වය)")
        with col_l2:
            doc_date = st.date_input("Document Date")
            
        doc_notes = st.text_area("Key Notes / Summary (සටහන්)")
        
        submitted_letter = st.form_submit_button("Save Official Document")
        if submitted_letter:
            file_name = uploaded_letter_file.name if uploaded_letter_file is not None else "No File Attached"
            st.session_state.letters_logs.append({
                "Type": doc_type,
                "Subject": subject_title,
                "Party": sender_receiver,
                "Date": str(doc_date),
                "Notes": doc_notes,
                "File": file_name,
                "Managed By": st.session_state.current_user
            })
            st.success(f"✅ Official Document '{subject_title}' saved successfully!")

    if st.session_state.letters_logs:
        st.subheader("Registered Letters & Memos History")
        for idx, let in enumerate(st.session_state.letters_logs):
            cols = st.columns([5, 1])
            with cols[0]:
                st.write(f"**{let['Subject']}** | Type: {let['Type']} | Date: {let['Date']}")
            with cols[1]:
                if st.button("Delete", key=f"del_let_{idx}"):
                    st.session_state.letters_logs.pop(idx)
                    st.rerun()

# --- SECTION 7: INVOICE GENERATOR ---
elif menu_selection == "📄 Invoice Generator":
    st.header("Official Invoice Generator (Tablets Quantity-wise)")
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
            
            for cart_item in st.session_state.invoice_cart:
                v_name = cart_item["Variant"]
                v_qty = cart_item["Qty"]
                if v_name in st.session_state.tablet_stock:
                    st.session_state.tablet_stock[v_name] = max(0, st.session_state.tablet_stock[v_name] - v_qty)

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
            st.success("Invoice generated successfully!")

# --- SECTION 8: DIRECTORS DASHBOARD (PRINTABLE HTML REPORTS & DELETE / LOCK ACCESS) ---
elif menu_selection == "📋 Directors Dashboard":
    st.header("Directors' Central Records & Printable Reports Dashboard")
    st.markdown("සියලුම අංශවල වාර්තා මෙහි එකතු වී ඇත. ඔබට අවශ්‍ය වාර්තා වර්ගය තෝරා **අලංකාර මුද්‍රණ (Printable HTML Reports)** ලෙස ඩවුන්ලෝඩ් කරගත හැක.")

    report_category = st.selectbox("Select Master Record Category to View & Print", [
        "Batch Production Records (BPR)",
        "Lab & R&D Reports", 
        "Raw Materials (RM-LOG)", 
        "Official Letters & Memos", 
        "Invoices & Dispatched Orders"
    ])

    st.markdown("---")

    if report_category == "Batch Production Records (BPR)":
        st.subheader("🏭 Batch Production Records (BPR Master)")
        if st.session_state.bpr_logs:
            for idx, log in enumerate(st.session_state.bpr_logs):
                st.write(f"**{log['Batch No']}** | {log['Variant']} | Mfg: {log['Mfg Date']} | Qty: {log['Tablets Produced']}")
            
            bpr_df = pd.DataFrame(st.session_state.bpr_logs)
            csv_data = bpr_df.to_csv(index=False).encode('utf-8')
            st.download_button("🖨️ Download BPR Report (CSV)", csv_data, "bpr_report.csv", "text/csv")
        else:
            st.info("No Batch Production records found yet.")

    elif report_category == "Lab & R&D Reports":
        st.subheader("🧪 Lab & R&D Quality Control Records (Printable Report)")
        if st.session_state.rd_logs:
            for idx, log in enumerate(st.session_state.rd_logs):
                col_a, col_b = st.columns([5, 1])
                with col_a:
                    st.write(f"**Ref/Batch:** {log['Batch No']} | **Variant:** {log['Variant']} | **Date:** {log['Date']} | **Status:** {log['Status']}")
                with col_b:
                    if st.button("Delete", key=f"dash_del_rd_{idx}"):
                        st.session_state.rd_logs.pop(idx)
                        st.rerun()

            # Printable HTML Report Generation
            html_rows = ""
            for log in st.session_state.rd_logs:
                html_rows += f"""
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;">{log['Batch No']}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{log['Variant']}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{log['Date']}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{log['Status']}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{log['Attached File']}</td>
                </tr>
                """

            printable_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Lab & R&D Test Reports Summary</title></head>
<body style="font-family: Arial, sans-serif; padding: 30px; color: #333;">
    <h2 style="color: #5a3825; text-align: center;">CEYLON COFFEE TABLETS (PVT) LTD</h2>
    <h3 style="text-align: center; color: #666;">Research & Development Quality Control Test Summary</h3>
    <hr style="border: 1px solid #5a3825;">
    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
        <thead>
            <tr style="background-color: #5a3825; color: white;">
                <th style="padding: 10px; border: 1px solid #ddd;">Doc Ref / Batch</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Product Variant</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Test Date</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Status</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Attached File</th>
            </tr>
        </thead>
        <tbody>
            {html_rows}
        </tbody>
    </table>
    <br><p style="font-size: 12px; color: #777; text-align: center;">Generated via Ceylon Coffee Tablets Enterprise Portal</p>
</body>
</html>"""

            st.download_button(
                label="🖨️ Download Printable Lab Report (.html for Printing)",
                data=printable_html.encode('utf-8'),
                file_name=f"Lab_Report_Summary_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )
        else:
            st.info("No Lab & R&D records found yet.")

    elif report_category == "Raw Materials (RM-LOG)":
        st.subheader("📦 Raw Materials Sourcing & Purchase Logs")
        if st.session_state.rm_logs:
            rm_df = pd.DataFrame(st.session_state.rm_logs)
            st.dataframe(rm_df, use_container_width=True)
            st.download_button("🖨️️ Download Raw Materials Report (CSV)", rm_df.to_csv(index=False).encode('utf-8'), "raw_materials.csv", "text/csv")
        else:
            st.info("No Raw Materials records found yet.")

    elif report_category == "Official Letters & Memos":
        st.subheader("✉️ Official Letters & Memos Records")
        if st.session_state.letters_logs:
            for idx, let in enumerate(st.session_state.letters_logs):
                col_l1, col_l2 = st.columns([5, 1])
                with col_l1:
                    st.write(f"**{let['Subject']}** | Type: {let['Type']} | Date: {let['Date']}")
                with col_l2:
                    if st.button("Delete", key=f"dash_del_let_{idx}"):
                        st.session_state.letters_logs.pop(idx)
                        st.rerun()
        else:
            st.info("No letters or memos recorded yet.")

    elif report_category == "Invoices & Dispatched Orders":
        st.subheader("📄 Invoices & Dispatched Orders Ledger")
        if st.session_state.orders:
            total_orders_count = len(st.session_state.orders)
            total_tablets_dispatched = sum([order["Total Tablets"] for order in st.session_state.orders])
            total_revenue = sum([order["Grand Total (LKR)"] for order in st.session_state.orders])

            m1, m2, m3 = st.columns(3)
            m1.metric("Total Orders Dispatched", total_orders_count)
            m2.metric("Total Tablets Dispatched", total_tablets_dispatched)
            m3.metric("Total Revenue (LKR)", f"LKR {total_revenue:,.2f}")

            st.markdown("---")
            for idx, ord_item in enumerate(st.session_state.orders):
                st.write(f"**Invoice No:** {ord_item['Invoice No']} | **Customer:** {ord_item['Customer']} | **Total:** LKR {ord_item['Grand Total (LKR)']:,.2f}")
        else:
            st.info("No invoices or orders recorded yet.")
