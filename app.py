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

# Session State Initialization for Business Data & Empty Stock
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

# Empty Stock Ledger Initialization (Starts at 0)
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
        
        උණුසුම් ජලයට හෝ කිරිවලට පහසුවෙන් දියවන මෙම ටැබ්ලට් එකක ප්‍රමිතිය, නැවුම් බව සහ සුවඳ රැකගනිමින් දේශීය හා විදේශීය වෙළඳපොළ (උදා: ස්වීඩනය වැනි රටවල්) වෙත උසස්ම මට්ටමින් නිෂ්පාදන බෙදා හැරීම අපගේ අරමුණයි.
        """)
    with col_w2:
        st.info("""
        📌 **පද්ධතියේ ප්‍රධාන විශේෂාංග:**
        - **PDF / Image අප්‌ලෝඩ් කර ස්කෑන් කිරීම:** ඔබේ පැරණි ලැබ් වාර්තා හෝ ලිපි PDF/Image ලෙස අප්‌ලෝඩ් කළ විට ඒවා ස්වයංක්‍රීයව හඳුනාගෙන ඩෑෂ්බෝඩ් එකට ඇතුළත් වේ.
        - **ස්ටොක් කළමනාකරණය (Stores & Stock):** අමුද්‍රව්‍ය සහ නිමි ටැබ්ලට් ශේෂයන් ස්වයංක්‍රීයව යාවත්කාලීන වීම.
        - **ඩිරෙක්ටර්ස් ඩෑෂ්බෝඩ් (Directors Dashboard):** සියලුම වාර්තා ෆිල්ටර් කර ප්‍රින්ට් අවුට් ලබාගැනීම.
        
        👉 **කරුණාකර වම්පස ඇති මෙනුව (Sidebar Menu) භාවිතා කර ඔබට අවශ්‍ය අංශය වෙත පිවිසෙන්න.**
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

    cost_data = pd.DataFrame([{
        "Manufacturing Cost": st.session_state.mfg_cost,
        "Courier Cost": st.session_state.courier_cost,
        "Total Landed Cost": total_cost,
        "Retail Price": st.session_state.retail_price,
        "Trade Price": st.session_state.trade_price,
        "Status": "LOCKED" if st.session_state.prices_locked else "UNLOCKED"
    }])
    
    if st.session_state.user_role == "Admin":
        st.download_button("📥 Download Cost Analysis Report (CSV)", cost_data.to_csv(index=False).encode('utf-8'), "cost_analysis.csv", "text/csv")
    else:
        st.info("🔒 ඩවුන්ලෝඩ් කරගැනීමේ අවසරය ඇත්තේ ඇඩ්මින් වෙත පමණි.")

# --- SECTION 2: BATCH PRODUCTION RECORD (BPR MASTER) ---
elif menu_selection == "🏭 Batch Production (BPR)":
    st.header("Batch Production Record (BPR) Master System")
    st.markdown("නිෂ්පාදන දිනය (Mfg Date) ඇතුළත් කළ විට බැච් අංකය (`CCTYYMMDD`) සහ කල් ඉකුත්වීමේ දිනය (මාස 8කින්) ස්වයංක්‍රීයව ජනනය වේ.")

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
            dissolve_sec = st.number_input("Dissolve Time (seconds) [Target: 20-30s]", value=25)
        with c_test3:
            visual_check = st.selectbox("Visual Check Status", ["OK (Pass)", "Defect / Discolour / Delay"])
        with c_test4:
            tested_qty = st.number_input("Tablets Tested Qty", value=5)

        st.subheader("3. Drying, Packaging & Yield Summary")
        d1, d2 = st.columns(2)
        with d1:
            drying_method = st.selectbox("Drying Method", ["Cabinet (20-30m)", "Air Dry"])
            moisture_content = st.number_input("Moisture Content (%) [Target < 3%]", value=2.5, step=0.1)
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
            
            raw_used_kg = (bpr_target_qty * 2.0) / 1000.0
            if "Green Coffee Beans (Arabica)" in st.session_state.raw_stock:
                st.session_state.raw_stock["Green Coffee Beans (Arabica)"] = max(0.0, st.session_state.raw_stock["Green Coffee Beans (Arabica)"] - raw_used_kg)

            st.success(f"Batch {auto_batch_no} saved successfully! Tablet stock updated and raw materials deducted.")

    if st.session_state.bpr_logs:
        st.subheader("Saved Batch Production Records (BPR Master)")
        bpr_df = pd.DataFrame(st.session_state.bpr_logs)
        st.table(bpr_df)
        if st.session_state.user_role == "Admin":
            st.download_button("📥 Download BPR Logs (CSV)", bpr_df.to_csv(index=False).encode('utf-8'), "bpr_master_logs.csv", "text/csv")

# --- SECTION 3: STORES & STOCK ---
elif menu_selection == "📦 Stores & Stock":
    st.header("Stores & Stock Management (Raw Materials & Tablets)")
    st.markdown("අමුද්‍රව්‍ය ස්ටොක් සහ නිම කළ ටැබ්ලට් ස්ටොක් ශේෂයන් මෙහි දැක්වේ.")

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

# --- SECTION 4: LAB & R&D REPORTS (PDF / IMAGE SCAN & UPLOAD) ---
elif menu_selection == "🧪 Lab & R&D Reports":
    st.header("Lab & R&D Quality Control Reports (PDF / Image Scanner)")
    st.markdown("ඔබගේ ලැබ් වාර්තා (PDF හෝ පින්තූර) මෙහි අප්‌ලෝඩ් කරන්න. පද්ධතිය මඟින් ඒවා ස්වයංක්‍රීයව හඳුනාගෙන සුරකිනු ඇත.")

    # File Uploader outside form for reliable handling
    uploaded_lab_file = st.file_uploader("Upload Lab Report (PDF / PNG / JPG)", type=["png", "jpg", "jpeg", "pdf"], key="lab_file_uploader")

    default_batch = "CCT260929"
    if uploaded_lab_file is not None:
        # Auto-extract batch number from uploaded file name if possible
        fname_clean = uploaded_lab_file.name.rsplit('.', 1)[0]
        if "CCT" in fname_clean.upper():
            default_batch = fname_clean.upper()
        else:
            default_batch = f"CCT-{fname_clean[:10]}"
        st.success(f"📄 File '{uploaded_lab_file.name}' attached successfully! Details auto-filled below.")

    with st.form("rd_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            batch_no = st.text_input("Batch Number", value=default_batch)
            variant = st.selectbox("Product Variant", ["Black Coffee (Light Roast)", "Black Coffee (Dark Roast)", "Cinnamon Coffee", "Ginger Coffee"])
        with col2:
            mfg_date = st.date_input("Manufacture Date")
            coffee_wt = st.number_input("Coffee Weight (kg)", value=5.0)
        with col3:
            moisture = st.number_input("Moisture Level (%) [Standard < 4.0%]", value=3.5, step=0.1)
            qc_status = st.selectbox("Batch Status", ["APPROVED FOR RELEASE", "REJECTED / HOLD"])

        submitted_rd = st.form_submit_button("Save R&D Report")
        if submitted_rd:
            file_name = uploaded_lab_file.name if uploaded_lab_file is not None else "No File Attached"
            st.session_state.rd_logs.append({
                "Batch No": batch_no,
                "Variant": variant,
                "Date": str(mfg_date),
                "Coffee Weight (kg)": coffee_wt,
                "Moisture": f"{moisture}%",
                "Status": qc_status,
                "Attached File": file_name,
                "Recorded By": st.session_state.current_user
            })
            st.success(f"✅ Lab & R&D Report for Batch {batch_no} saved successfully with file: {file_name}!")

    if st.session_state.rd_logs:
        st.subheader("Saved Lab & R&D Logs")
        rd_df = pd.DataFrame(st.session_state.rd_logs)
        st.table(rd_df)
        if st.session_state.user_role == "Admin":
            st.download_button("📥 Download R&D Reports (CSV)", rd_df.to_csv(index=False).encode('utf-8'), "rd_logs_report.csv", "text/csv")

# --- SECTION 5: DEALERS DIRECTORY ---
elif menu_selection == "🤝 Dealers Directory":
    st.header("Local & Foreign Dealers Directory (Secure Confidential)")
    
    if st.session_state.user_role == "Admin":
        st.markdown("දේශීය සහ විදේශීය ඩීලර්වරුන්ගේ (උදා: Sweden ඩීලර්) විස්තර ආරක්ෂිතව ඇතුළත් කර සුරකින්න.")
        
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
                st.success("Dealer record saved securely!")

        if st.session_state.dealers_logs:
            st.subheader("Saved Dealers Directory")
            dealers_df = pd.DataFrame(st.session_state.dealers_logs)
            st.table(dealers_df)
            st.download_button("📥 Download Dealers Directory (CSV)", dealers_df.to_csv(index=False).encode('utf-8'), "dealers_directory.csv", "text/csv")
        else:
            st.info("No dealers registered yet.")
    else:
        st.error("🔒 රහස්‍යභාවය සුරක්ෂිත කිරීම සඳහා ඩීලර්ස් නාමාවලිය බැලීමේ සහ ඇතුළත් කිරීමේ පූර්ණ අවසරය ඇත්තේ ඇඩ්මින් වෙත පමණි.")

# --- SECTION 6: LETTERS & MEMOS (PDF / IMAGE SCAN & UPLOAD) ---
elif menu_selection == "✉️ Letters & Memos":
    st.header("Official Letters, Inbound/Outbound Memos & Documents")
    st.markdown("ලිපි හෝ මීමොවන්ගේ PDF හෝ පින්තූර (Images) මෙහි අප්‌ලෝඩ් කරන්න.")

    uploaded_letter_file = st.file_uploader("Upload Letter Document (PDF / PNG / JPG)", type=["png", "jpg", "jpeg", "pdf"], key="letter_file_uploader")

    default_subject = "General Corporate Notice"
    if uploaded_letter_file is not None:
        fname_clean = uploaded_letter_file.name.rsplit('.', 1)[0]
        default_subject = fname_clean.replace("_", " ").title()
        st.success(f"📄 Document '{uploaded_letter_file.name}' attached successfully!")

    with st.form("letter_form"):
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            doc_type = st.selectbox("Document Type", ["Inbound Letter (ලැබුණු ලිපිය)", "Outbound Memo (යැවූ ලිපිය/මීමොව)", "Corporate Notice"])
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
            st.success(f"✅ Official Document '{subject_title}' saved successfully with file: {file_name}!")

    if st.session_state.letters_logs:
        st.subheader("Registered Letters & Memos History")
        letters_df = pd.DataFrame(st.session_state.letters_logs)
        st.table(letters_df)
        if st.session_state.user_role == "Admin":
            st.download_button("📥 Download Letters Report (CSV)", letters_df.to_csv(index=False).encode('utf-8'), "letters_memos_report.csv", "text/csv")

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
            
            st.success("Invoice generated, stock updated, and saved successfully!")

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
            if st.session_state.user_role == "Admin":
                st.download_button(
                    label="📥 Download Official Invoice as HTML File (.html)",
                    data=invoice_html.encode('utf-8'),
                    file_name=f"{latest_order['Invoice No'].replace('/', '_')}.html",
                    mime="text/html"
                )
            else:
                st.info("🔒 ඩවුන්ලෝඩ් කරගැනීමේ අවසරය ඇත්තේ ඇඩ්මින් වෙත පමණි.")

# --- SECTION 8: DIRECTORS DASHBOARD ---
elif menu_selection == "📋 Directors Dashboard":
    st.header("Directors' Central Records & Master Dashboard")
    st.markdown("සියලුම අංශවල (Batch Production, Lab Reports, Raw Materials, Letters, Invoices) වාර්තා මෙහි එකතු වී ඇත. ඔබට අවශ්‍ය වාර්තා වර්ගය සහ දිනය තෝරා **ප්‍රින්ට් අවුට් (Print) සඳහා ඩවුන්ලෝඩ්** කරගත හැක.")

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
            bpr_df = pd.DataFrame(st.session_state.bpr_logs)
            
            use_date_filter = st.checkbox("Filter by Manufacture Date")
            if use_date_filter and "Mfg Date" in bpr_df.columns:
                unique_dates = list(bpr_df["Mfg Date"].unique())
                selected_date = st.selectbox("Select Date", unique_dates)
                bpr_df = bpr_df[bpr_df["Mfg Date"] == selected_date]
            
            st.dataframe(bpr_df, use_container_width=True)
            
            csv_data = bpr_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="🖨️ Download / Print BPR Report (CSV for Manual Files)",
                data=csv_data,
                file_name=f"BPR_Master_Report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No Batch Production records found yet.")

    elif report_category == "Lab & R&D Reports":
        st.subheader("🧪 Lab & R&D Quality Control Records")
        if st.session_state.rd_logs:
            rd_df = pd.DataFrame(st.session_state.rd_logs)
            
            use_date_filter = st.checkbox("Filter by Report Date")
            if use_date_filter and "Date" in rd_df.columns:
                unique_dates = list(rd_df["Date"].unique())
                selected_date = st.selectbox("Select Date", unique_dates)
                rd_df = rd_df[rd_df["Date"] == selected_date]
            
            st.dataframe(rd_df, use_container_width=True)
            
            csv_data = rd_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="🖨️ Download / Print Lab Reports (CSV for Manual Files)",
                data=csv_data,
                file_name=f"Lab_Reports_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No Lab & R&D records found yet.")

    elif report_category == "Raw Materials (RM-LOG)":
        st.subheader("📦 Raw Materials Sourcing & Purchase Logs")
        if st.session_state.rm_logs:
            rm_df = pd.DataFrame(st.session_state.rm_logs)
            
            use_date_filter = st.checkbox("Filter by Purchase Date")
            if use_date_filter and "Date" in rm_df.columns:
                unique_dates = list(rm_df["Date"].unique())
                selected_date = st.selectbox("Select Date", unique_dates)
                rm_df = rm_df[rm_df["Date"] == selected_date]
            
            st.dataframe(rm_df, use_container_width=True)
            
            csv_data = rm_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="🖨️ Download / Print Raw Materials Report (CSV for Manual Files)",
                data=csv_data,
                file_name=f"Raw_Materials_Logs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No Raw Materials records found yet.")

    elif report_category == "Official Letters & Memos":
        st.subheader("✉️ Official Letters & Memos Records")
        if st.session_state.letters_logs:
            letters_df = pd.DataFrame(st.session_state.letters_logs)
            
            use_date_filter = st.checkbox("Filter by Document Date")
            if use_date_filter and "Date" in letters_df.columns:
                unique_dates = list(letters_df["Date"].unique())
                selected_date = st.selectbox("Select Date", unique_dates)
                letters_df = letters_df[letters_df["Date"] == selected_date]
            
            st.dataframe(letters_df, use_container_width=True)
            
            csv_data = letters_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="🖨️ Download / Print Letters Report (CSV for Manual Files)",
                data=csv_data,
                file_name=f"Letters_Memos_Report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
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
            st.dataframe(orders_df, use_container_width=True)
            
            csv_data = orders_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="🖨️ Download / Print Invoices History (CSV for Manual Files)",
                data=csv_data,
                file_name=f"Invoices_Dispatched_Orders_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            if st.session_state.user_role == "Admin":
                if st.button("Clear All Orders History"):
                    st.session_state.orders = []
                    st.rerun()
        else:
            st.info("No invoices or orders recorded yet.")
