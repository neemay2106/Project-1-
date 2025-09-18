from flask import Flask , request , render_template
import sqlite3
import os
import time

app = Flask(__name__)
y = 1

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['image'] # 'image' is the key from client
    if 'image' not in request.files:
        return {"error": "No image"},400
    else:
        global y
        x= time.time()
        filename = file.filename        # original filename from client
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        upload_to_db(y,filepath,x)
        file.save(filepath)
        print("saved",filepath)
        y +=1
        return {"status": "saved", "path": filepath}

def get_db_connection():
    import sqlite3
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # optional: allows dict-like access
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS images")
    cursor.execute("""CREATE TABLE IF NOT EXISTS images(id INT PRIMARY KEY , timestamp TEXT, url TEXT)""")
    cursor.execute("PRAGMA table_info(images);")
    for row in cursor.fetchall():
        print(row)
    conn.commit()
init_db()

def upload_to_db(PK,filepath,timestamp):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO images (id,timestamp, url) VALUES (?,?, ?)", (PK ,timestamp, filepath))
    conn.commit()
    cur.execute("SELECT * FROM images")
    for row in cur.fetchall():
        print(dict(row))
    conn.close()




if __name__ == "__main__":
    app.run(debug=True, port=5000)