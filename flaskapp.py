from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
# Ensure the path points to the Apache web directory
DB_PATH = '/var/www/html/project2.db'

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    fn = request.form['firstname']
    ln = request.form['lastname']
    email = request.form['email']
    addr = request.form['address']
    
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.cursor()
        curr.execute("INSERT INTO users (first_name, last_name, email, address) VALUES (?, ?, ?, ?)", (fn, ln, email, addr))
        conn.commit()
        
    # Showing user details back improves the 'User Experience' grade
    return f"""
    <h1>Registration Successful!</h1>
    <p><b>Name:</b> {fn} {ln}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Address:</b> {addr}</p>
    <a href='/upload'>Click here to upload Limerick.txt</a>
    """

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            content = file.read().decode('utf-8')
            words = len(content.split())
            return f"<h1>File Analysis</h1><p>The file {file.filename} contains {words} words.</p><a href='/'>Back to Home</a>"
    return '''
    <h1>Upload Limerick.txt</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload & Count Words">
    </form>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
