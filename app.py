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
        "📊 Unit Cost & Profitability Analysis", 
        "📦 Sweden Export Order Cost Report", 
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
        ශ්‍රී ලංකාවේ උසස්ම තත්වයේ අරාබිකා කෝපි බීජ මෙන්ම කුරුඳු සහ ඉඟුරු සාරය එකතු කරමින්, නවීන තාක්ෂණය යටතේ නිෂ්පාදනය කරනු ලබන **දියවන කෝපි ටැබ්ලට් (Soluble Coffee Tablets)** නිෂ්පාදනයේ ප්‍රමුඛයා වන්නේ **Ceylon Coffee Tablet (Pvt) Ltd** අප ආයතනයයි.
        """)
    with col_w2:
        st.info("""
        📌 **ප්‍රධාන වාර්තා ටැබ් දෙක:**
        1. **Unit Cost & Profitability Analysis:** කම්කරු ශ්‍රම පිරිවැය, මාසික නිෂ්පාදන ධාරිතාව, පොදු උපයෝගिता වියදම් (Electricity, Water, Gas, Gloves, Masks) සහ ටැබ්ලට් එකක පිරිවැය ගණනය කිරීමේ නිල ආකෘතිය.
        2. **Sweden Export Order Cost Report:** ස්වීඩන් අපනයන ඇණවුම සඳහා අමුද්‍රව්‍ය පිරිවැය, මුළු පිරිවැය සහ ශුද්ධ ලාභය දැක්වෙන ආකෘතිය.
        """)

# --- SECTION 1: UNIT COST & PROFITABILITY ANALYSIS ---
elif menu_selection == "📊 Unit Cost & Profitability Analysis":
    st.header("Unit Cost & Profitability Analysis")
    st.markdown("Comprehensive Tablet Production & Order Financial Breakdown (Drop it. Dissolve it. Done.)")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Mfg. Cost / Tablet", "LKR 41.95")
    col_m2.metric("Courier Cost / Tablet", "LKR 4.05")
    col_m3.metric("Total Cost / Tablet", "LKR 46.00")
    col_m4.metric("Selling Price / Tablet", "LKR 50.00")

    st.markdown("---")
    st.subheader("1. Labor & Staffing Cost Calculation")
    
    labor_data = [
        {"Component / Operational Detail": "Productivity Rate", "Standard Calculation Basis": "60 Tablets/hr + 7 Productive hrs/day = 420 Tablets/day/person", "Monthly Amount (LKR)": "-", "Cost per Tablet (LKR)": "-"},
        {"Component / Operational Detail": "Monthly Target Capacity", "Standard Calculation Basis": "2 Workers x 400 Tablets x 20 Working Days = 8,000 Tablets", "Monthly Amount (LKR)": "-", "Cost per Tablet (LKR)": "-"},
        {"Component / Operational Detail": "Staff Salaries", "Standard Calculation Basis": "2 Workers x LKR 35,000 / month", "Monthly Amount (LKR)": "70,000.00", "Cost per Tablet (LKR)": "8.75"},
        {"Component / Operational Detail": "Staff Snacks & Allowance", "Standard Calculation Basis": "2 Workers x LKR 150/day x 20 Days", "Monthly Amount (LKR)": "6,000.00", "Cost per Tablet (LKR)": "0.75"},
        {"Component / Operational Detail": "Total Labor Cost (Monthly Basis: 8,000 Tablets)", "Standard Calculation Basis": "Combined Labor Expenses", "Monthly Amount (LKR)": "76,000.00", "Cost per Tablet (LKR)": "9.50"}
    ]
    st.table(pd.DataFrame(labor_data))

    st.subheader("2. Operational Overheads & Consumables")
    overhead_data = [
        {"Cost Center / Expense Item": "Electricity & Rent", "Details / Consumption Rate": "Monthly Overhead allocation", "Monthly Cost (LKR)": "5,000.00", "Cost per Tablet (LKR)": "0.62"},
        {"Cost Center / Expense Item": "Water Usage", "Details / Consumption Rate": "Monthly Utility charge", "Monthly Cost (LKR)": "1,000.00", "Cost per Tablet (LKR)": "0.12"},
        {"Cost Center / Expense Item": "LP Gas Usage", "Details / Consumption Rate": "12.5 kg Gas cylinder allocation (LKR 4,800 / 6)", "Monthly Cost (LKR)": "800.00", "Cost per Tablet (LKR)": "0.10"},
        {"Cost Center / Expense Item": "Fuel & Transport", "Details / Consumption Rate": "Transport & dispatch expenses", "Monthly Cost (LKR)": "5,000.00", "Cost per Tablet (LKR)": "0.62"},
        {"Cost Center / Expense Item": "Safety & Hygiene Consumables", "Details / Consumption Rate": "Gloves (8,960) + Masks (1,600) + Hairnets (4,000) + Sanitizer", "Monthly Cost (LKR)": "16,000.00", "Cost per Tablet (LKR)": "2.00"},
        {"Cost Center / Expense Item": "Total Operational Overheads (Per Tablet)", "Details / Consumption Rate": "Sum of all Overheads", "Monthly Cost (LKR)": "27,800.00", "Cost per Tablet (LKR)": "3.46"}
    ]
    st.table(pd.DataFrame(overhead_data))

    unit_analysis_html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Unit Cost & Profitability Analysis Report</title></head>
<body style="font-family: Arial, sans-serif; padding: 30px; color: #333;">
    <h2 style="color: #5a3825; text-align: center;">CEYLON COFFEE TABLETS (PVT) LTD</h2>
    <h3 style="text-align: center; color: #666;">Unit Cost & Profitability Analysis Report</h3>
    <hr style="border: 1px solid #5a3825;">
    <h4>1. Labor & Staffing Cost Calculation</h4>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
        <tr style="background-color: #5a3825; color: white;"><th style="padding: 8px; border: 1px solid #ddd;">Component</th><th style="padding: 8px; border: 1px solid #ddd;">Basis</th><th style="padding: 8px; border: 1px solid #ddd;">Monthly (LKR)</th><th style="padding: 8px; border: 1px solid #ddd;">Per Tablet (LKR)</th></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;">Staff Salaries</td><td style="padding: 8px; border: 1px solid #ddd;">2 Workers</td><td style="padding: 8px; border: 1px solid #ddd;">70,000.00</td><td style="padding: 8px; border: 1px solid #ddd;">8.75</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;">Staff Snacks & Allowance</td><td style="padding: 8px; border: 1px solid #ddd;">2 Workers x 20 Days</td><td style="padding: 8px; border: 1px solid #ddd;">6,000.00</td><td style="padding: 8px; border: 1px solid #ddd;">0.75</td></tr>
        <tr style="font-weight: bold;"><td style="padding: 8px; border: 1px solid #ddd;">Total Labor Cost</td><td style="padding: 8px; border: 1px solid #ddd;">8,000 Tablets</td><td style="padding: 8px; border: 1px solid #ddd;">76,000.00</td><td style="padding: 8px; border: 1px solid #ddd;">9.50</td></tr>
    </table>
    <h4>2. Operational Overheads & Consumables</h4>
    <table style="width: 100%; border-collapse: collapse;">
        <tr style="background-color: #5a3825; color: white;"><th style="padding: 8px; border: 1px solid #ddd;">Expense Item</th><th style="padding: 8px; border: 1px solid #ddd;">Details</th><th style="padding: 8px; border: 1px solid #ddd;">Monthly (LKR)</th><th style="padding: 8px; border: 1px solid #ddd;">Per Tablet (LKR)</th></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;">Electricity & Rent</td><td style="padding: 8px; border: 1px solid #ddd;">Overhead allocation</td><td style="padding: 8px; border: 1px solid #ddd;">5,000.00</td><td style="padding: 8px; border: 1px solid #ddd;">0.62</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;">Water Usage</td><td style="padding: 8px; border: 1px solid #ddd;">Utility charge</td><td style="padding: 8px; border: 1px solid #ddd;">1,000.00</td><td style="padding: 8px; border: 1px solid #ddd;">0.12</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;">LP Gas Usage</td><td style="padding: 8px; border: 1px solid #ddd;">Gas cylinder allocation</td><td style="padding: 8px; border: 1px solid #ddd;">800.00</td><td style="padding: 8px; border: 1px solid #ddd;">0.10</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;">Fuel & Transport</td><td style="padding: 8px; border: 1px solid #ddd;">Dispatch expenses</td><td style="padding: 8px; border: 1px solid #ddd;">5,000.00</td><td style="padding: 8px; border: 1px solid #ddd;">0.62</td></tr>
        <tr><td style="padding: 8px; border: 1px solid #ddd;">Safety & Hygiene (Gloves, Masks)</td><td style="padding: 8px; border: 1px solid #ddd;">Consumables</td><td style="padding: 8px; border: 1px solid #ddd;">16,000.00</td><td style="padding: 8px; border: 1px solid #ddd;">2.00</td></tr>
        <tr style="font-weight: bold;"><td style="padding: 8px; border: 1px solid #ddd;">Total Operational Overheads</td><td style="padding: 8px; border: 1px solid #ddd;">Per Tablet</td><td style="padding: 8px; border: 1px solid #ddd;">27,800.00</td><td style="padding: 8px; border: 1px solid #ddd;">3.46</td></tr>
    </table>
</body>
</html>"""

    st.download_button(
        label="🖨️ Download Unit Cost Analysis Report (.html for Printing)",
        data=unit_analysis_html.encode('utf-8'),
        file_name=f"Unit_Cost_Analysis_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html"
    )

# --- SECTION 2: SWEDEN EXPORT ORDER COST REPORT ---
elif menu_selection == "📦 Sweden Export Order Cost Report":
    st.header("Case Study: Sweden Export Order Cost Report (QTY: 650 Tablets)")
    st.markdown("ස්වීඩන් අපනයන ඇණවුම සඳහා අමුද්‍රව්‍ය පිරිවැය, ශ්‍රම පිරිවැය, පොදු වියදම් සහ ශුද්ධ ලාභය දැක්වෙන නිල වාර්තාව.")

    sweden_rm_data = [
        {"#": 1, "Raw Material / Cost Component": "Light Roasted Coffee", "Quantity / Weight": "500 g", "Total Cost (LKR)": "8,500.00", "Cost per Tablet (LKR)": "13.08"},
        {"#": 2, "Raw Material / Cost Component": "Dark Roasted Coffee", "Quantity / Weight": "500 g", "Total Cost (LKR)": "7,500.00", "Cost per Tablet (LKR)": "11.54"},
        {"#": 3, "Raw Material / Cost Component": "Ginger Coffee", "Quantity / Weight": "300 g", "Total Cost (LKR)": "1,000.00", "Cost per Tablet (LKR)": "1.54"},
        {"#": 4, "Raw Material / Cost Component": "Cinnamon Powder", "Quantity / Weight": "100 g", "Total Cost (LKR)": "1,800.00", "Cost per Tablet (LKR)": "2.77"},
        {"#": 5, "Raw Material / Cost Component": "Sugar", "Quantity / Weight": "200 g", "Total Cost (LKR)": "44.00", "Cost per Tablet (LKR)": "0.07"},
        {"#": "A", "Raw Material / Cost Component": "Total Raw Material Cost", "Quantity / Weight": "-", "Total Cost (LKR)": "18,844.00", "Cost per Tablet (LKR)": "28.99"},
        {"#": "B", "Raw Material / Cost Component": "Direct Labor Cost (650 x LKR 9.50)", "Quantity / Weight": "-", "Total Cost (LKR)": "6,175.00", "Cost per Tablet (LKR)": "9.50"},
        {"#": "C", "Raw Material / Cost Component": "Operational Overhead & Utilities (650 x LKR 3.46)", "Quantity / Weight": "-", "Total Cost (LKR)": "2,249.00", "Cost per Tablet (LKR)": "3.46"},
        {"#": "-", "Raw Material / Cost Component": "Total Manufacturing Cost (650 Tablets)", "Quantity / Weight": "-", "Total Cost (LKR)": "LKR 27,268.00", "Cost per Tablet (LKR)": "LKR 41.95"},
        {"#": "D", "Raw Material / Cost Component": "Courier, Packaging Box & Wrapping Charges", "Quantity / Weight": "-", "Total Cost (LKR)": "2,632.50", "Cost per Tablet (LKR)": "4.05"},
        {"#": "-", "Raw Material / Cost Component": "TOTAL LANDED COST (Manufacturing + Delivery)", "Quantity / Weight": "-", "Total Cost (LKR)": "LKR 29,900.00", "Cost per Tablet (LKR)": "LKR 46.00"}
    ]
    st.table(pd.DataFrame(sweden_rm_data))

    st.success("""
    ### 🇸🇪 SWEDEN ORDER FINANCIAL SUMMARY (650 TABLETS)
    - **Total Revenue (650 Tablets @ LKR 50.00/ea):** LKR 32,500.00
    - **Total Cost (650 Tablets @ LKR 46.00/ea):** LKR 29,900.00
    
    ### 💰 NET PROFIT: LKR 2,600.00
    *(Margin: 8.00% / LKR 4.00 per tablet)*
    """)

    sweden_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Sweden Export Order Cost Report</title></head>
<body style="font-family: Arial, sans-serif; padding: 30px; color: #333;">
    <h2 style="color: #5a3825; text-align: center;">CEYLON COFFEE TABLETS (PVT) LTD</h2>
    <h3 style="text-align: center; color: #666;">Case Study: Sweden Export Order Cost Report (QTY: 650 Tablets)</h3>
    <hr style="border: 1px solid #5a3825;">
    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
        <tr style="background-color: #5a3825; color: white;">
            <th style="padding: 8px; border: 1px solid #ddd;">#</th>
            <th style="padding: 8px; border: 1px solid #ddd;">Raw Material / Cost Component</th>
            <th style="padding: 8px; border: 1px solid #ddd;">Quantity / Weight</th>
            <th style="padding: 8px; border: 1px solid #ddd;">Total Cost (LKR)</th>
            <th style="padding: 8px; border: 1px solid #ddd;">Cost per Tablet (LKR)</th>
        </tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">1</td><td style="padding: 6px; border: 1px solid #ddd;">Light Roasted Coffee</td><td style="padding: 6px; border: 1px solid #ddd;">500 g</td><td style="padding: 6px; border: 1px solid #ddd;">8,500.00</td><td style="padding: 6px; border: 1px solid #ddd;">13.08</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">2</td><td style="padding: 6px; border: 1px solid #ddd;">Dark Roasted Coffee</td><td style="padding: 6px; border: 1px solid #ddd;">500 g</td><td style="padding: 6px; border: 1px solid #ddd;">7,500.00</td><td style="padding: 6px; border: 1px solid #ddd;">11.54</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">3</td><td style="padding: 6px; border: 1px solid #ddd;">Ginger Coffee</td><td style="padding: 6px; border: 1px solid #ddd;">300 g</td><td style="padding: 6px; border: 1px solid #ddd;">1,000.00</td><td style="padding: 6px; border: 1px solid #ddd;">1.54</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">4</td><td style="padding: 6px; border: 1px solid #ddd;">Cinnamon Powder</td><td style="padding: 6px; border: 1px solid #ddd;">100 g</td><td style="padding: 6px; border: 1px solid #ddd;">1,800.00</td><td style="padding: 6px; border: 1px solid #ddd;">2.77</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">5</td><td style="padding: 6px; border: 1px solid #ddd;">Sugar</td><td style="padding: 6px; border: 1px solid #ddd;">200 g</td><td style="padding: 6px; border: 1px solid #ddd;">44.00</td><td style="padding: 6px; border: 1px solid #ddd;">0.07</td></tr>
        <tr style="font-weight: bold; background-color: #f7f7f7;"><td style="padding: 6px; border: 1px solid #ddd;">A</td><td style="padding: 6px; border: 1px solid #ddd;">Total Raw Material Cost</td><td style="padding: 6px; border: 1px solid #ddd;">-</td><td style="padding: 6px; border: 1px solid #ddd;">18,844.00</td><td style="padding: 6px; border: 1px solid #ddd;">28.99</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">B</td><td style="padding: 6px; border: 1px solid #ddd;">Direct Labor Cost (650 x LKR 9.50)</td><td style="padding: 6px; border: 1px solid #ddd;">-</td><td style="padding: 6px; border: 1px solid #ddd;">6,175.00</td><td style="padding: 6px; border: 1px solid #ddd;">9.50</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">C</td><td style="padding: 6px; border: 1px solid #ddd;">Operational Overhead & Utilities (650 x LKR 3.46)</td><td style="padding: 6px; border: 1px solid #ddd;">-</td><td style="padding: 6px; border: 1px solid #ddd;">2,249.00</td><td style="padding: 6px; border: 1px solid #ddd;">3.46</td></tr>
        <tr style="font-weight: bold; background-color: #eaf2f8;"><td style="padding: 6px; border: 1px solid #ddd;">-</td><td style="padding: 6px; border: 1px solid #ddd;">Total Manufacturing Cost (650 Tablets)</td><td style="padding: 6px; border: 1px solid #ddd;">-</td><td style="padding: 6px; border: 1px solid #ddd;">LKR 27,268.00</td><td style="padding: 6px; border: 1px solid #ddd;">LKR 41.95</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">D</td><td style="padding: 6px; border: 1px solid #ddd;">Courier, Packaging Box & Wrapping Charges</td><td style="padding: 6px; border: 1px solid #ddd;">-</td><td style="padding: 6px; border: 1px solid #ddd;">2,632.50</td><td style="padding: 6px; border: 1px solid #ddd;">4.05</td></tr>
        <tr style="font-weight: bold; background-color: #d4efdf;"><td style="padding: 6px; border: 1px solid #ddd;">-</td><td style="padding: 6px; border: 1px solid #ddd;">TOTAL LANDED COST (Manufacturing + Delivery)</td><td style="padding: 6px; border: 1px solid #ddd;">-</td><td style="padding: 6px; border: 1px solid #ddd;">LKR 29,900.00</td><td style="padding: 6px; border: 1px solid #ddd;">LKR 46.00</td></tr>
    </table>
    <div style="margin-top: 20px; background-color: #27ae60; color: white; padding: 15px; border-radius: 5px;">
        <h3 style="margin: 0 0 10px 0;">SWEDEN ORDER FINANCIAL SUMMARY (650 TABLETS)</h3>
        <p style="margin: 3px 0;">• Total Revenue (650 Tablets @ LKR 50.00/ea): LKR 32,500.00</p>
        <p style="margin: 3px 0;">• Total Cost (650 Tablets @ LKR 46.00/ea): LKR 29,900.00</p>
        <h2 style="margin: 10px 0 0 0; text-align: right;">NET PROFIT: LKR 2,600.00</h2>
        <p style="margin: 2px 0 0 0; font-size: 11px; text-align: right;">(Margin: 8.00% / LKR 4.00 per tablet)</p>
    </div>
</body>
</html>"""

    st.download_button(
        label="🖨️ Download Sweden Export Order Report (.html for Printing)",
        data=sweden_html.encode('utf-8'),
        file_name=f"Sweden_Export_Cost_Report_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html"
    )

# --- SECTION 3: EXPENSES REPORT ---
elif menu_selection == "💸 Expenses Report":
    st.header("Expenses Report & Operational Cost Tracking")
    with st.form("expenses_form"):
        e1, e2 = st.columns(2)
        with e1:
            exp_date = st.date_input("Expense Date", value=datetime.now().date())
            expense_category = st.selectbox("Expense Category", ["Raw Materials", "Safety Gear (Gloves/Masks)", "Ingredients (Sugar)", "Packaging", "Equipment", "Other"])
            custom_item_name = st.text_input("Custom Item Description")
        with e2:
            funded_by = st.selectbox("Funded By", list(USERS.keys()))
            amount_lkr = st.number_input("Total Amount (LKR)", value=5000.0, step=100.0)
            receipt_ref = st.text_input("Reference No")

        if st.form_submit_button("Save Expense Record"):
            st.session_state.expenses_logs.append({
                "Date": str(exp_date),
                "Category": expense_category,
                "Item": custom_item_name if custom_item_name else expense_category,
                "Funded By": funded_by,
                "Amount (LKR)": amount_lkr,
                "Reference": receipt_ref
            })
            st.success("Expense recorded successfully!")

    if st.session_state.expenses_logs:
        st.subheader("Recorded Expenses Ledger")
        for idx, exp in enumerate(st.session_state.expenses_logs):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(f"📅 {exp['Date']} | **{exp['Item']}** | Paid by: `{exp['Funded By']}` | **LKR {exp['Amount (LKR)']:,.2f}**")
            with c2:
                if st.button("Delete", key=f"del_exp_{idx}"):
                    st.session_state.expenses_logs.pop(idx)
                    st.rerun()

# --- SECTION 4: FINANCIAL P&L & PROFIT SHARING ---
elif menu_selection == "📈 Financial P&L & Profit Sharing":
    st.header("Financial P&L, Reinvestment & Directors Profit Sharing (5 Directors)")
    total_revenue = sum([order["Grand Total (LKR)"] for order in st.session_state.orders])
    total_expenses = sum([item["Amount (LKR)"] for item in st.session_state.expenses_logs])
    net_profit = total_revenue - total_expenses

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total Revenue", f"LKR {total_revenue:,.2f}")
    col_m2.metric("Total Expenses", f"LKR {total_expenses:,.2f}")
    col_m3.metric("Net Profit", f"LKR {net_profit:,.2f}")

    reinvest_percentage = st.slider("Company Reinvestment Percentage (%)", 0, 100, 40)
    directors_share_pct = 100 - reinvest_percentage
    reinvest_amount = (net_profit * reinvest_percentage) / 100 if net_profit > 0 else 0
    directors_total_pool = (net_profit * directors_share_pct) / 100 if net_profit > 0 else 0
    per_director_share = directors_total_pool / 5.0 if net_profit > 0 else 0

    st.success(f"🏢 **Reinvested in Company:** LKR {reinvest_amount:,.2f} ({reinvest_percentage}%)")
    st.warning(f"👥 **Directors Total Pool (5 Directors):** LKR {directors_total_pool:,.2f} ({directors_share_pct}%) -> LKR {per_director_share:,.2f} each")

# --- SECTION 5: BATCH PRODUCTION RECORD (BPR MASTER) ---
elif menu_selection == "🏭 Batch Production (BPR)":
    st.header("Batch Production Record (BPR) Master System")
    with st.form("bpr_form"):
        bpr_mfg = st.date_input("Manufacture Date", value=datetime.now().date())
        auto_batch_no = f"CCT{bpr_mfg.strftime('%y%m%d')}"
        bpr_variant = st.selectbox("Product Variant", list(st.session_state.tablet_stock.keys()))
        bpr_target_qty = st.number_input("Tablets Quantity Produced", value=150)
        if st.form_submit_button("Save Batch"):
            st.session_state.bpr_logs.append({"Batch No": auto_batch_no, "Variant": bpr_variant, "Qty": bpr_target_qty})
            st.session_state.tablet_stock[bpr_variant] += bpr_target_qty
            st.success("Batch saved and stock updated!")
    if st.session_state.bpr_logs:
        st.table(pd.DataFrame(st.session_state.bpr_logs))

# --- SECTION 6: STORES & STOCK ---
elif menu_selection == "📦 Stores & Stock":
    st.header("Stores & Stock Management")
    col_st1, col_st2 = st.columns(2)
    with col_st1:
        st.table(pd.DataFrame(list(st.session_state.raw_stock.items()), columns=["Raw Material", "Quantity"]))
    with col_st2:
        st.table(pd.DataFrame(list(st.session_state.tablet_stock.items()), columns=["Variant", "Quantity"]))

# --- SECTION 7: LAB & R&D REPORTS ---
elif menu_selection == "🧪 Lab & R&D Reports":
    st.header("Lab & R&D Quality Control Reports")
    with st.form("rd_form"):
        batch_no = st.text_input("Test Report Ref", value="RND-TR-2025-013")
        if st.form_submit_button("Save Report"):
            st.session_state.rd_logs.append({"Batch No": batch_no})
            st.success("Saved!")
    if st.session_state.rd_logs:
        st.table(pd.DataFrame(st.session_state.rd_logs))

# --- SECTION 8: DEALERS DIRECTORY ---
elif menu_selection == "🤝 Dealers Directory":
    st.header("Dealers Directory")
    if st.session_state.user_role == "Admin":
        with st.form("dealer_form"):
            d_name = st.text_input("Dealer Name")
            if st.form_submit_button("Save"):
                st.session_state.dealers_logs.append({"Dealer Name": d_name})
                st.success("Saved!")
    else:
        st.error("Admin only.")

# --- SECTION 9: LETTERS & MEMOS ---
elif menu_selection == "✉️ Letters & Memos":
    st.header("Letters & Memos")
    with st.form("letter_form"):
        subj = st.text_input("Subject")
        if st.form_submit_button("Save"):
            st.session_state.letters_logs.append({"Subject": subj})
            st.success("Saved!")

# --- SECTION 10: INVOICE GENERATOR ---
elif menu_selection == "📄 Invoice Generator":
    st.header("Invoice Generator")
    inv_no = st.text_input("Invoice No", value="CCT-00012")
    cust = st.text_input("Customer Name")
    with st.form("cart"):
        var = st.selectbox("Variant", list(st.session_state.tablet_stock.keys()))
        qty = st.number_input("Qty", value=10)
        if st.form_submit_button("Add"):
            st.session_state.invoice_cart.append({"Variant": var, "Qty": qty, "Total": qty * st.session_state.retail_price})
            st.success("Added!")
    if st.session_state.invoice_cart:
        st.table(pd.DataFrame(st.session_state.invoice_cart))
        if st.button("Generate Invoice"):
            st.session_state.orders.append({"Invoice No": inv_no, "Customer": cust, "Grand Total (LKR)": sum([i['Total'] for i in st.session_state.invoice_cart])})
            st.success("Generated!")

# --- SECTION 11: DIRECTORS DASHBOARD ---
elif menu_selection == "📋 Directors Dashboard":
    st.header("Directors' Central Dashboard")
    cat = st.selectbox("Category", ["Expenses Report", "Unit Cost Analysis", "Sweden Export Report", "Batch Production", "Lab Reports", "Invoices"])
    if cat == "Expenses Report" and st.session_state.expenses_logs:
        st.dataframe(pd.DataFrame(st.session_state.expenses_logs))
    elif cat == "Unit Cost Analysis":
        st.info("Check the 'Unit Cost & Profitability Analysis' tab for complete breakdowns and print view.")
    elif cat == "Sweden Export Report":
        st.info("Check the 'Sweden Export Order Cost Report' tab for the complete case study and print view.")
    elif cat == "Invoices" and st.session_state.orders:
        st.dataframe(pd.DataFrame(st.session_state.orders))
    else:
        st.info("No records found in this category.")
