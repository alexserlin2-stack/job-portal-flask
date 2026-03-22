from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect to database
conn = sqlite3.connect('jobs.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, job TEXT)")
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post_job():
    title = request.form['title']
    cursor.execute("INSERT INTO jobs (title) VALUES (?)", (title,))
    conn.commit()
    return redirect('/jobs')

@app.route('/jobs')
def view_jobs():
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    return render_template('jobs.html', jobs=jobs)

@app.route('/apply', methods=['POST'])
def apply():
    name = request.form['name']
    job = request.form['job']
    cursor.execute("INSERT INTO applications (name, job) VALUES (?, ?)", (name, job))
    conn.commit()
    return "Application Submitted!"

if __name__ == '__main__':
    app.run(debug=True)