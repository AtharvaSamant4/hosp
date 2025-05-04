from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)


# Function to connect to the database
def connect_db():
    return sqlite3.connect('hospital.db')

# Function to initialize the database and create the table if it doesn't exist
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        age INTEGER,
                        disease TEXT,
                        admission_date TEXT,
                        phone TEXT)''') 
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# View all patients
@app.route('/patients')
def view_patients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template('view_patients.html', patients=patients)

# Add patient
@app.route('/add', methods=['GET', 'POST'])
def add_patient():

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']
        phone = request.form['phone']  

        if not name or not age or not disease or not phone:
            return redirect(url_for('add_patient'))

        admission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, age, disease, admission_date, phone) VALUES (?, ?, ?, ?, ?)",
                       (name, age, disease, admission_date, phone))
        conn.commit()
        conn.close()

       
        return redirect(url_for('view_patients'))

    return render_template('add_patient.html')

# Edit patient
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']
        phone = request.form['phone']  

        if not name or not age or not disease or not phone:
            
            return redirect(url_for('edit_patient', id=id))

        cursor.execute("UPDATE patients SET name = ?, age = ?, disease = ?, phone = ? WHERE id = ?",
                       (name, age, disease, phone, id))
        conn.commit()
        conn.close()

        return redirect(url_for('view_patients'))

    cursor.execute("SELECT * FROM patients WHERE id = ?", (id,))
    patient = cursor.fetchone()
    conn.close()
    return render_template('edit_patient.html', patient=patient)

# Delete patient
@app.route('/delete/<int:id>')
def delete_patient(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id = ?", (id,))
    conn.commit()
    conn.close()

   
    return redirect(url_for('view_patients'))

# Search patient
@app.route('/search', methods=['POST'])
def search_patient():
    search_query = request.form['search']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM patients WHERE name=?", (search_query,))
    patients = cursor.fetchall()
    conn.close()
    return render_template('view_patients.html', patients=patients)

# Initialize the database
init_db()

if __name__ == '__main__':
    app.run(debug=True)
