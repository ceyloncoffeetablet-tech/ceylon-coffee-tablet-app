import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Ceylon Coffee Tablets Portal", layout="wide")

st.title("Ceylon Coffee Tablets (Pvt) Ltd - Management System")

# Session state for prices and orders
if 'retail_price' not in st.session_state:
    st.session_state.retail_price = 50.00  # සිල්ලර මිල[span_0](start_span)[span_0](end_span)
if 'trade_price' not in st.session_state:
    st.session_state.trade_price = 42.00   # තොග මිල
if 'orders' not in st.session_state:
    st.session_state.orders = []

manufacturing_cost = 41.95  # නිෂ්පාදන වියදම[span_1](start_span)[span_1](end_span)
courier_cost = 4.05         # කුරියර් වියදම[span_2](start_span)[span_2](end_span)
total_cost = manufacturing_cost + courier_cost

menu = st.sidebar.selectbox("Navigation (මෙනුව)", ["Dashboard & Pricing", "Retail Page", "Trade Page", "Reports & Printing"])

if menu == "Dashboard & Pricing":
    st.header("விலە සංස්කරණය සහ ලාභ විශ්ලේෂණය (Price & Profit Config)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.retail_price = st.number_input("Retail Price (සිල්ලර මිල - LKR)", value=float(st.session_state.retail_price), step=0.50)
    with col2:
        st.session_state.trade_price = st.number_input("Trade Price (තොග මිල - LKR)", value=float(st.session_state.trade_price), step=0.50)
    
    st.markdown("---")
    st.subheader("කොස්ට් සහ ලාභ ප්‍රතිශතය (Cost & Profit Margin)")
    st.write(f"**නිෂ්පාදන වියදම:** LKR {manufacturing_cost}[span_3](start_span)[span_3](end_span)")
    st.write(f"**කුරියර් වියදම:** LKR {courier_cost}[span_4](start_span)[span_4](end_span)")
    st.write(f"**මුළු වියදම (Total Cost / Tablet):** LKR {total_cost:.2f}[span_5](start_span)[span_5](end_span)")
    
    c1, c2 = st.columns(2)
    with c1:
        retail_profit = st.session_state.retail_price - total_cost
        retail_margin = (retail_profit / st.session_state.retail_price) * 100 if st.session_state.retail_price > 0 else 0
        st.info(f"**Retail Profit:** LKR {retail_profit:.2f} ({retail_margin:.2f}%)")
        
    with c2:
        trade_profit = st.session_state.trade_price - total_cost
        trade_margin = (trade_profit / st.session_state.trade_price) * 100 if st.session_state.trade_price > 0 else 0
        st.success(f"**Trade Profit:** LKR {trade_profit:.2f} ({trade_margin:.2f}%)")

elif menu == "Retail Page":
    st.header("Retail Orders & Pricing Page (සිල්ලර ඇණවුම්)")
    st.write(f"වෙළඳපොළ සිල්ලර මිල: **LKR {st.session_state.retail_price} per tablet**")
    
    with st.form("retail_form"):
        customer = st.text_input("Customer Name (පාරිභෝගිකයාගේ නම)")
        qty = st.number_input("Quantity (ප්‍රමාණය)", min_value=1, value=10)
        submitted = st.form_submit_button("Place Retail Order")
        if submitted and customer:
            total = qty * st.session_state.retail_price
            st.session_state.orders.append({
                "customer": customer,
                "type": "Retail",
                "qty": qty,
                "price": st.session_state.retail_price,
                "total": total,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("Retail Order Placed Successfully!")

elif menu == "Trade Page":
    st.header("Trade / Bulk Orders & Pricing Page (තොග ඇණවුම්)")
    st.write(f"වෙළඳපොළ තොග මිල: **LKR {st.session_state.trade_price} per tablet**")
    
    with st.form("trade_form"):
        customer = st.text_input("Business / Buyer Name (ව්‍යාපාරයේ නම)")
        qty = st.number_input("Quantity (තොග ප්‍රමාණය)", min_value=1, value=100)
        submitted = st.form_submit_button("Place Trade Order")
        if submitted and customer:
            total = qty * st.session_state.trade_price
            st.session_state.orders.append({
                "customer": customer,
                "type": "Trade",
                "qty": qty,
                "price": st.session_state.trade_price,
                "total": total,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("Trade Order Placed Successfully!")

elif menu == "Reports & Printing":
    st.header("All Orders & Financial Reports (සියලුම වාර්තා)")
    if st.session_state.orders:
        st.table(st.session_state.orders)
        if st.button("Print / Refresh Report"):
            st.rerun()
    else:
        st.info("No orders recorded yet. (තවම ඇණවුම් වාර්තා වී නැත)")
