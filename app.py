from flask import Flask, request, send_file, jsonify, render_template
import rembg
from PIL import Image
import io
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/remove-bg', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        input_image = Image.open(file).convert("RGBA")
        output_image = rembg.remove(input_image)
        result_path = os.path.join(RESULT_FOLDER, "processed.png")
        output_image.save(result_path, format="PNG")
        return send_file(result_path, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
