from flask import Flask, request, jsonify, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key

# Create and initialize the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    if 'username' in session:
        return f"Welcome, {session['username']}! This is the main page."
    else:
        return "Welcome to the Login and Register website. You are not logged in."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Login failed. Please check your credentials."

    return """
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
    """

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        newUsername = data.get('newUsername')
        newPassword = data.get('newPassword')

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (newUsername, newPassword))
        conn.commit()
        conn.close()

        return "Registration successful! You can now <a href='/login'>login</a>."

    return """
    <form method="POST">
        <label for="newUsername">Username:</label>
        <input type="text" id="newUsername" name="newUsername" required><br>
        <label for="newPassword">Password:</label>
        <input type="password" id="newPassword" name="newPassword" required><br>
        <button type="submit">Register</button>
    </form>
    """
@app.route('/show_users')
def show_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    if users:
        user_list = "<ul>"
        for user in users:
            user_list += f"<li>ID: {user[0]}, Username: {user[1]}, Password: {user[2]}</li>"
        user_list += "</ul>"
        return f"All Users:<br>{user_list}"
    else:
        return "No users found in the database."

if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

