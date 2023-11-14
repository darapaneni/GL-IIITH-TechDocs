from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import asyncio
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)  # Initialize Flask-Swagger

# - name: output_filepath
#         in: formData
#         type: string
#         required: true
#         description: The output filepath

@app.route('/process_image', methods=['POST'])
async def process_image():
    """
    Process an uploaded image and return extracted text.

    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: The image to process.
      - name: output_file
        in: formData
        type: string
        required: false
        description: The output file that to be returned
    responses:
      200:
        description: Text extracted from the image.
        schema:
          type: object
          properties:
            message:
              type: string
            output_file:
              type: string
      400:
        description: Bad Request. No image file provided.
      500:
        description: Internal Server Error.
    """
    try:
        # Get the uploaded image from the request
        image_file = request.files['image']
        # Check if an image was uploaded
        if not image_file:
            return jsonify({'error': 'No image file provided'}), 400

        # Get the output file name from the form data
        output_file_name = request.form.get('output_file', 'output.docx')

        # Open the image using Pillow (PIL)
        image = Image.open(image_file)
        # Perform OCR to extract text
        text = pytesseract.image_to_string(image)

        # Specify the path for the output text file
        output_file_path = output_file_name

        # Save the extracted text to a text file
        with open(output_file_path, 'w') as text_file:
            text_file.write(text)

        return jsonify({'message': 'Image processed successfully', 'output_file': output_file_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=8081)
