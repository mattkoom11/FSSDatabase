from flask import Flask, render_template, request, send_file
import sqlite3
import pandas as pd
import io

app = Flask(__name__)

def query_clients(
    name='', plan2025='', plan2024='', type_='',
    contact_from='', contact_to='',
    sort_by='client_name', sort_dir='asc'
):
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    query = """
    SELECT client_name, phone_number, plan_2025, plan_2024, type, contact_date, address
    FROM clients
    WHERE client_name IS NOT NULL AND TRIM(client_name) != ''
    """
    params = []

    if name:
        query += " AND client_name LIKE ?"
        params.append(f"%{name}%")
    if plan2025:
        query += " AND plan_2025 LIKE ?"
        params.append(f"%{plan2025}%")
    if plan2024:
        query += " AND plan_2024 LIKE ?"
        params.append(f"%{plan2024}%")
    if type_:
        query += " AND type LIKE ?"
        params.append(f"%{type_}%")
    if contact_from:
        query += " AND contact_date >= ?"
        params.append(contact_from)
    if contact_to:
        query += " AND contact_date <= ?"
        params.append(contact_to)

    # Add sorting
    allowed_columns = ['client_name', 'phone_number', 'plan_2025', 'plan_2024', 'type', 'contact_date', 'address']
    if sort_by in allowed_columns:
        query += f" ORDER BY {sort_by} {'DESC' if sort_dir == 'desc' else 'ASC'}"

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    filters = {
        'name': request.values.get('name', ''),
        'plan2025': request.values.get('plan2025', ''),
        'plan2024': request.values.get('plan2024', ''),
        'type_': request.values.get('type', ''),
        'contact_from': request.values.get('contact_from', ''),
        'contact_to': request.values.get('contact_to', ''),
    }

    sort_by = request.values.get('sort_by', 'client_name')
    sort_dir = request.values.get('sort_dir', 'asc')

    clients = query_clients(**filters, sort_by=sort_by, sort_dir=sort_dir)

    return render_template('index.html', clients=clients, sort_by=sort_by, sort_dir=sort_dir, **filters)

@app.route('/download', methods=['POST'])
def download():
    filters = {
        'name': request.form.get('name', ''),
        'plan2025': request.form.get('plan2025', ''),
        'plan2024': request.form.get('plan2024', ''),
        'type_': request.form.get('type', ''),
        'contact_from': request.form.get('contact_from', ''),
        'contact_to': request.form.get('contact_to', ''),
    }

    clients = query_clients(**filters)

    df = pd.DataFrame(clients, columns=[
        'Name', 'Phone', '2025 Plan', '2024 Plan', 'Type', 'Contact Date', 'Address'
    ])

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(
        io.BytesIO(buffer.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='clients_export.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
