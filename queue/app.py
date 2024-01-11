from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import sqlite3
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Khởi tạo cơ sở dữ liệu SQLite
conn = sqlite3.connect('queue.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER,
        status TEXT
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    # Lấy danh sách vé đang đợi xử lý và đã xử lý
    conn = sqlite3.connect('queue.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM queue WHERE status = "waiting" ORDER BY timestamp')
    waiting_tickets = cursor.fetchall()

    cursor.execute('SELECT * FROM queue WHERE status = "processing" ORDER BY timestamp DESC')
    processing_tickets = cursor.fetchone()[0]

    cursor.execute('SELECT * FROM queue WHERE status = "processed" ORDER BY timestamp DESC')
    processed_tickets = cursor.fetchall()

    conn.close()

    return render_template('index.html', waiting_tickets=waiting_tickets, processing_tickets=processing_tickets, processed_tickets=processed_tickets)

@app.route('/enqueue', methods=['POST'])
def enqueue():
    # Thêm vé mới vào danh sách đợi
    conn = sqlite3.connect('queue.db')
    cursor = conn.cursor()

    timestamp = int(time.time())
    cursor.execute('INSERT INTO queue (timestamp, status) VALUES (?, ?)', (timestamp, 'waiting'))
    conn.commit()

    # Lấy id của vé mới thêm để tạo QR code
    cursor.execute('SELECT id FROM queue WHERE timestamp = ?', (timestamp,))
    ticket_id = cursor.fetchone()[0]

    conn.close()

    return redirect(url_for('index'))

@app.route('/pos')
def pos():
    return render_template('pos.html')

@app.route('/gate')
def gate():
    return render_template('gate.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@socketio.on('enqueue')
def enqueue():
    conn = sqlite3.connect('queue.db')
    cursor = conn.cursor()

    timestamp = int(time.time())
    cursor.execute('INSERT INTO queue (timestamp, status) VALUES (?, ?)', (timestamp, 'waiting'))
    conn.commit()

    cursor.execute('SELECT MAX(id) FROM queue')
    ticket_id = cursor.fetchone()[0]

    conn.close()

    emit('enqueue', {'ticket_id': ticket_id}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)