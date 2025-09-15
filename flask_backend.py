from flask import Flask , request , render_template
import os

app = Flask(__name__)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['image'] # 'image' is the key from client
    if 'image' not in request.files:
        return {"error": "No image"},400
    else:
        filename = file.filename        # original filename from client
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        print("saved",filepath)
        return {"status": "saved", "path": filepath}

if __name__ == "__main__":
    app.run(debug=True, port=5000)