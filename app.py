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

# Session State Initialization for Editable Unit Cost & Sweden Case Study
if 'workers_count' not in st.session_state:
    st.session_state.workers_count = 2
if 'worker_salary' not in st.session_state:
    st.session_state.worker_salary = 35000.0
if 'worker_allowance' not in st.session_state:
    st.session_state.worker_allowance = 150.0
if 'working_days' not in st.session_state:
    st.session_state.working_days = 20
if 'daily_target_per_worker' not in st.session_state:
    st.session_state.daily_target_per_worker = 400

if 'elec_rent' not in st.session_state:
    st.session_state.elec_rent = 5000.0
if 'water_cost' not in st.session_state:
    st.session_state.water_cost = 1000.0
if 'gas_cost' not in st.session_state:
    st.session_state.gas_cost = 800.0
if 'transport_cost' not in st.session_state:
    st.session_state.transport_cost = 5000.0
if 'safety_consumables' not in st.session_state:
    st.session_state.safety_consumables = 16000.0

if 'sweden_qty' not in st.session_state:
    st.session_state.sweden_qty = 650
if 'sweden_selling_price' not in st.session_state:
    st.session_state.sweden_selling_price = 50.00
if 'light_coffee_cost' not in st.session_state:
    st.session_state.light_coffee_cost = 8500.0
if 'dark_coffee_cost' not in st.session_state:
    st.session_state.dark_coffee_cost = 7500.0
if 'ginger_coffee_cost' not in st.session_state:
    st.session_state.ginger_coffee_cost = 1000.0
if 'cinnamon_cost' not in st.session_state:
    st.session_state.cinnamon_cost = 1800.0
if 'sugar_cost' not in st.session_state:
    st.session_state.sugar_cost = 44.0
if 'courier_packaging_cost' not in st.session_state:
    st.session_state.courier_packaging_cost = 2632.50

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
    st.info("📌 සියලුම කොස්ට් සහ මිල ගණන් දැන් ඔබට අවශ්‍ය පරිදි **Edit** කර ස්වයංක්‍රීය ගණනය කිරීම් ලබාගත හැක.")

# --- SECTION 1: EDITABLE UNIT COST & PROFITABILITY ANALYSIS ---
elif menu_selection == "📊 Unit Cost & Profitability Analysis":
    st.header("Unit Cost & Profitability Analysis (Editable)")
    st.markdown("කම්කරු ශ්‍රම පිරිවැය, වැටුප් සහ පොදු උපයෝගීතා වියදම් වෙනස් කර ක්ෂණික ප්‍රතිඵල ලබාගන්න.")

    with st.form("unit_cost_edit_form"):
        st.subheader("⚙️ 1. Labor & Staffing Cost Inputs")
        c1, c2, c3 = st.columns(3)
        with c1:
            workers_count = st.number_input("Number of Workers", value=st.session_state.workers_count, step=1)
            worker_salary = st.number_input("Monthly Salary per Worker (LKR)", value=st.session_state.worker_salary, step=1000.0)
        with c2:
            worker_allowance = st.number_input("Daily Snacks/Allowance per Worker (LKR)", value=st.session_state.worker_allowance, step=50.0)
            working_days = st.number_input("Working Days per Month", value=st.session_state.working_days, step=1)
        with c3:
            daily_target_per_worker = st.number_input("Daily Tablets per Worker", value=st.session_state.daily_target_per_worker, step=10)

        st.subheader("⚙️ 2. Operational Overheads & Consumables Inputs")
        o1, o2, o3 = st.columns(3)
        with o1:
            elec_rent = st.number_input("Electricity & Rent (Monthly LKR)", value=st.session_state.elec_rent, step=500.0)
            water_cost = st.number_input("Water Usage (Monthly LKR)", value=st.session_state.water_cost, step=100.0)
        with o2:
            gas_cost = st.number_input("LP Gas Usage (Monthly LKR)", value=st.session_state.gas_cost, step=100.0)
            transport_cost = st.number_input("Fuel & Transport (Monthly LKR)", value=st.session_state.transport_cost, step=500.0)
        with o3:
            safety_consumables = st.number_input("Safety & Hygiene (Gloves/Masks/Hairnets LKR)", value=st.session_state.safety_consumables, step=1000.0)

        save_unit_costs = st.form_submit_button("Update & Recalculate Unit Costs")
        if save_unit_costs:
            st.session_state.workers_count = workers_count
            st.session_state.worker_salary = worker_salary
            st.session_state.worker_allowance = worker_allowance
            st.session_state.working_days = working_days
            st.session_state.daily_target_per_worker = daily_target_per_worker
            
            st.session_state.elec_rent = elec_rent
            st.session_state.water_cost = water_cost
            st.session_state.gas_cost = gas_cost
            st.session_state.transport_cost = transport_cost
            st.session_state.safety_consumables = safety_consumables
            st.success("Unit cost parameters updated successfully!")

    # Calculations
    monthly_target_capacity = st.session_state.workers_count * st.session_state.daily_target_per_worker * st.session_state.working_days
    total_salaries = st.session_state.workers_count * st.session_state.worker_salary
    total_allowance = st.session_state.workers_count * st.session_state.worker_allowance * st.session_state.working_days
    total_labor_cost = total_salaries + total_allowance
    cost_per_tablet_labor = total_labor_cost / monthly_target_capacity if monthly_target_capacity > 0 else 0

    total_overheads = st.session_state.elec_rent + st.session_state.water_cost + st.session_state.gas_cost + st.session_state.transport_cost + st.session_state.safety_consumables
    cost_per_tablet_overhead = total_overheads / monthly_target_capacity if monthly_target_capacity > 0 else 0

    st.markdown("---")
    st.subheader("📋 Calculated Results Summary")
    r1, r2, r3 = st.columns(3)
    r1.metric("Monthly Target Capacity", f"{monthly_target_capacity:,} Tablets")
    r2.metric("Labor Cost / Tablet", f"LKR {cost_per_tablet_labor:.2f}")
    r3.metric("Overhead Cost / Tablet", f"LKR {cost_per_tablet_overhead:.2f}")

# --- SECTION 2: EDITABLE SWEDEN EXPORT ORDER COST REPORT ---
elif menu_selection == "📦 Sweden Export Order Cost Report":
    st.header("Case Study: Sweden Export Order Cost Report (Editable)")
    st.markdown("අපනයන ඇණවුම් ප්‍රමාණය, අමුද්‍රව්‍ය මිල සහ ඩිලිවරි වියදම් වෙනස් කර ලාභය ගණනය කරන්න.")

    with st.form("sweden_edit_form"):
        s1, s2 = st.columns(2)
        with s1:
            sweden_qty = st.number_input("Order Quantity (Tablets)", value=st.session_state.sweden_qty, step=10)
            sweden_selling_price = st.number_input("Selling Price per Tablet (LKR)", value=st.session_state.sweden_selling_price, step=0.50)
            light_coffee_cost = st.number_input("Light Roasted Coffee Total Cost (LKR)", value=st.session_state.light_coffee_cost, step=100.0)
            dark_coffee_cost = st.number_input("Dark Roasted Coffee Total Cost (LKR)", value=st.session_state.dark_coffee_cost, step=100.0)
        with s2:
            ginger_coffee_cost = st.number_input("Ginger Coffee Total Cost (LKR)", value=st.session_state.ginger_coffee_cost, step=100.0)
            cinnamon_cost = st.number_input("Cinnamon Powder Total Cost (LKR)", value=st.session_state.cinnamon_cost, step=100.0)
            sugar_cost = st.number_input("Sugar Total Cost (LKR)", value=st.session_state.sugar_cost, step=10.0)
            courier_packaging_cost = st.number_input("Courier & Packaging Charges (LKR)", value=st.session_state.courier_packaging_cost, step=100.0)

        save_sweden = st.form_submit_button("Update & Calculate Sweden Order")
        if save_sweden:
            st.session_state.sweden_qty = sweden_qty
            st.session_state.sweden_selling_price = sweden_selling_price
            st.session_state.light_coffee_cost = light_coffee_cost
            st.session_state.dark_coffee_cost = dark_coffee_cost
            st.session_state.ginger_coffee_cost = ginger_coffee_cost
            st.session_state.cinnamon_cost = cinnamon_cost
            st.session_state.sugar_cost = sugar_cost
            st.session_state.courier_packaging_cost = courier_packaging_cost
            st.success("Sweden Export Order parameters updated successfully!")

    # Sweden Calculations
    total_rm_cost = (st.session_state.light_coffee_cost + 
                     st.session_state.dark_coffee_cost + 
                     st.session_state.ginger_coffee_cost + 
                     st.session_state.cinnamon_cost + 
                     st.session_state.sugar_cost)
    
    # Assume proportional labor & overhead from previous tab or standard rate (e.g. 9.50 + 3.46 = 12.96 per tablet)
    total_labor_order = st.session_state.sweden_qty * 9.50
    total_overhead_order = st.session_state.sweden_qty * 3.46
    total_mfg_cost = total_rm_cost + total_labor_order + total_overhead_order
    total_landed_cost = total_mfg_cost + st.session_state.courier_packaging_cost
    
    cost_per_tablet_landed = total_landed_cost / st.session_state.sweden_qty if st.session_state.sweden_qty > 0 else 0
    total_revenue = st.session_state.sweden_qty * st.session_state.sweden_selling_price
    net_profit_sweden = total_revenue - total_landed_cost
    profit_per_tablet = net_profit_sweden / st.session_state.sweden_qty if st.session_state.sweden_qty > 0 else 0

    st.markdown("---")
    st.subheader("🇸🇪 Sweden Order Financial Summary")
    sw1, sw2, sw3 = st.columns(3)
    sw1.metric("Total Revenue", f"LKR {total_revenue:,.2f}")
    sw2.metric("Total Landed Cost", f"LKR {total_landed_cost:,.2f}")
    sw3.metric("Net Profit", f"LKR {net_profit_sweden:,.2f}", f"LKR {profit_per_tablet:.2f} / tablet")

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
            st.session_state.invoice_cart.append({"Variant": var, "Qty": qty, "Total": qty * 50.0})
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
        st.info("Check the 'Unit Cost & Profitability Analysis' tab for complete breakdowns and live edits.")
    elif cat == "Sweden Export Report":
        st.info("Check the 'Sweden Export Order Cost Report' tab for live case study edits.")
    elif cat == "Invoices" and st.session_state.orders:
        st.dataframe(pd.DataFrame(st.session_state.orders))
    else:
        st.info("No records found in this category.")
