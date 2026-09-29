from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# ගතිකව වෙනස් කළ හැකි මිල සහ කොස්ට් දත්ත (Database එකක් ලෙස ක්‍රියා කරයි)
SYSTEM_CONFIG = {
    "retail_price": 50.00,  # සිල්ලර මිල[span_0](start_span)[span_0](end_span)
    "trade_price": 42.00,   # තොග මිල
    "manufacturing_cost": 41.95, # ටැබ්ලට් එකක නිෂ්පාදන වියදම[span_1](start_span)[span_1](end_span)
    "courier_cost": 4.05    # කුරියර් ගාස්තුව[span_2](start_span)[span_2](end_span)
}

# ඇණවුම් සහ දත්ත ගබඩා කිරීම සඳහා ලැයිස්තුවක්
ORDERS_DB = []

# HTML Layout සහ Design එක (Print සහ Download කරගත හැකි වන පරිදි)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ceylon Coffee Tablets - Management Portal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; color: #333; }
        h1, h2 { color: #2c3e50; }
        .card { background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
        .btn { background: #27ae60; color: white; padding: 8px 15px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn-print { background: #2980b9; margin-top: 10px; }
        .nav-links a { margin-right: 15px; text-decoration: none; font-weight: bold; color: #2980b9; }
        @media print { .no-print { display: none; } }
    </style>
</head>
<body>
    <h1>Ceylon Coffee Tablets (Pvt) Ltd - Management System</h1>
    <div class="nav-links no-print">
        <a href="/">Home / Dashboard</a>
        <a href="/retail">Retail Page</a>
        <a href="/trade">Trade Page</a>
        <a href="/reports">Reports & Printing</a>
    </div>
    <hr class="no-print">

    {% if page == 'home' %}
    <div class="card">
        <h2>விலە සංස්කරණය (Price Configuration)</h2>
        <form method="POST" action="/update_prices">
            <label>Retail Price (සිල්ලර මිල - LKR):</label><br>
            <input type="number" step="0.01" name="retail" value="{{ config.retail_price }}" required><br><br>
            
            <label>Trade Price (තොග මිල - LKR):</label><br>
            <input type="number" step="0.01" name="trade" value="{{ config.trade_price }}" required><br><br>
            
            <button type="submit" class="btn">Update Prices</button>
        </form>
    </div>

    <div class="card">
        <h2>ලාභය සහ කොස්ට් ගණනය කිරීම (Profit & Cost Analysis)</h2>
        <p><b>නිෂ්පාදන වියදම (Manufacturing Cost):</b> LKR {{ config.manufacturing_cost }}[span_3](start_span)[span_3](end_span)</p>
        <p><b>කුරියර් වියදම (Courier Cost):</b> LKR {{ config.courier_cost }}[span_4](start_span)[span_4](end_span)</p>
        <p><b>මුළු වියදම (Total Cost / Tablet):</b> LKR {{ "%.2f"|format(config.manufacturing_cost + config.courier_cost) }}[span_5](start_span)[span_5](end_span)</p>
        <hr>
        <h3>Retail Profit Margin:</h3>
        <p>Selling Price: LKR {{ config.retail_price }} | Net Profit per unit: LKR {{ "%.2f"|format(config.retail_price - (config.manufacturing_cost + config.courier_cost)) }} 
        ({{ "%.2f"|format(((config.retail_price - (config.manufacturing_cost + config.courier_cost)) / config.retail_price) * 100) }}%)</p>
        
        <h3>Trade Profit Margin:</h3>
        <p>Selling Price: LKR {{ config.trade_price }} | Net Profit per unit: LKR {{ "%.2f"|format(config.trade_price - (config.manufacturing_cost + config.courier_cost)) }} 
        ({{ "%.2f"|format(((config.trade_price - (config.manufacturing_cost + config.courier_cost)) / config.trade_price) * 100) }}%)</p>
    </div>
    {% endif %}

    {% if page == 'retail' %}
    <div class="card">
        <h2>Retail Orders & Pricing Page (සිල්ලර ඇණවුම්)</h2>
        <p>වෙළඳපොළ සිල්ලර මිල: <b>LKR {{ config.retail_price }} per tablet</b></p>
        <form method="POST" action="/add_order">
            <input type="hidden" name="order_type" value="Retail">
            <label>Customer Name:</label><br><input type="text" name="customer" required><br><br>
            <label>Quantity (ප්‍රමාණය):</label><br><input type="number" name="qty" required><br><br>
            <button type="submit" class="btn">Place Retail Order</button>
        </form>
    </div>
    {% endif %}

    {% if page == 'trade' %}
    <div class="card">
        <h2>Trade / Bulk Orders & Pricing Page (තොග ඇණවුම්)</h2>
        <p>වෙළඳපොළ තොග මිල: <b>LKR {{ config.trade_price }} per tablet</b></p>
        <form method="POST" action="/add_order">
            <input type="hidden" name="order_type" value="Trade">
            <label>Business / Buyer Name:</label><br><input type="text" name="customer" required><br><br>
            <label>Quantity (තොග ප්‍රමාණය):</label><br><input type="number" name="qty" required><br><br>
            <button type="submit" class="btn">Place Trade Order</button>
        </form>
    </div>
    {% endif %}

    {% if page == 'reports' %}
    <div class="card">
        <h2>All Orders & Financial Reports (සියලුම වාර්තා සහ ඉන්වොයිස්)</h2>
        <button onclick="window.print();" class="btn btn-print no-print">Print / Save as PDF</button>
        <table>
            <tr>
                <th>Order ID</th>
                <th>Customer Name</th>
                <th>Type</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Total Amount</th>
                <th>Date & Time</th>
            </tr>
            {% for o in orders %}
            <tr>
                <td>#CCT-{{ loop.index0 + 1001 }}</td>
                <td>{{ o.customer }}</td>
                <td>{{ o.type }}</td>
                <td>{{ o.qty }}</td>
                <td>LKR {{ o.price }}</td>
                <td>LKR {{ o.total }}</td>
                <td>{{ o.date }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, page='home', config=SYSTEM_CONFIG)

@app.route('/retail')
def retail_page():
    return render_template_string(HTML_TEMPLATE, page='retail', config=SYSTEM_CONFIG)

@app.route('/trade')
def trade_page():
    return render_template_string(HTML_TEMPLATE, page='trade', config=SYSTEM_CONFIG)

@app.route('/reports')
def reports_page():
    return render_template_string(HTML_TEMPLATE, page='reports', config=SYSTEM_CONFIG, orders=ORDERS_DB)

@app.route('/update_prices', methods=['POST'])
def update_prices():
    SYSTEM_CONFIG['retail_price'] = float(request.form['retail'])
    SYSTEM_CONFIG['trade_price'] = float(request.form['trade'])
    return redirect(url_for('home'))

@app.route('/add_order', methods=['POST'])
def add_order():
    o_type = request.form['order_type']
    qty = int(request.form['qty'])
    unit_price = SYSTEM_CONFIG['retail_price'] if o_type == 'Retail' else SYSTEM_CONFIG['trade_price']
    total = qty * unit_price
    
    order_data = {
        "customer": request.form['customer'],
        "type": o_type,
        "qty": qty,
        "price": unit_price,
        "total": total,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    ORDERS_DB.append(order_data)
    return redirect(url_for('reports_page'))

if __name__ == '__main__':
    app.run(debug=True)
