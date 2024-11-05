from flask import Flask
from flask import jsonify
from flask import request
from PIL import Image
from passporteye import read_mrz
import io

app = Flask(__name__)
@app.route('/passporteye', methods=['POST'])
def extractImageData():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Load the image file into a PIL Image object
    image = Image.open(file.stream)

    # Create a BytesIO object to hold the image data
    byte_stream = io.BytesIO()

    # Save the image to the BytesIO object in a specific format (e.g., JPEG, PNG)
    image.save(byte_stream, image.format)

    # Get the byte data from the BytesIO object
    image_data = byte_stream.getvalue()

    # Process image
    mrz = read_mrz(image_data)

    # Obtain image
    mrz_data = mrz.to_dict()

    # Close the BytesIO stream
    byte_stream.close()

    return jsonify({"message": "Image extracted successfully!", "data": (mrz_data)}), 200
