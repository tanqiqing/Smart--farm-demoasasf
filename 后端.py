  GNU nano 7.2                                                                                                   app.py                                                                                                             
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    temperature = data['temperature']
    humidity = data['humidity']
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO sensor_data (temperature, humidity) VALUES (?, ?)", (temperature, humidity))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"}), 200

# 显示数据
@app.route('/')
def index():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT temperature, humidity FROM sensor_data")
    data = c.fetchall()
    conn.close()
    
    return render_template('index.html', data=data)

# 获取最新数据
@app.route('/latest', methods=['GET'])
def latest_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT temperature, humidity FROM sensor_data ORDER BY ROWID DESC LIMIT 1")
    latest = c.fetchone()
    conn.close()

    if latest:
        return jsonify({"temperature": latest[0], "humidity": latest[1]})
    else:
        return jsonify({"temperature": None, "humidity": None})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)