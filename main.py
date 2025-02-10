from flask import Flask, request, Response
from flask_cors import CORS
import requests
import json
import base64

app = Flask(__name__)
CORS(app)

@app.route('/generate-image', methods=['GET', 'POST'])
def generate_image():
    if request.method == 'GET':
        prompt = request.args.get('prompt')
    else:  # POST method
        data = request.get_json()
        prompt = data.get('prompt') if data else None

    if not prompt:
        return Response("Prompt parameter is missing.", status=400, mimetype='text/plain')

    # Define the headers and payload
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://fastflux.co",
        "referer": "https://fastflux.co/",
        "user-agent": "Mozilla/5.0"
    }

    payload = {
        "isPublic": False,
        "model": "flux_1_schnell",
        "prompt": prompt,
        "size": "1_1"  # Increased size
    }

    # Define the URL to send the request to
    url = "https://api.fastflux.co/v1/images/generate"

    # Send the POST request to the FastFlux API
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if "result" in data and data["result"].startswith("data:image/png;base64,"):
            # Extract base64 image data
            image_data = data["result"].split(",", 1)[1]
            image_binary = base64.b64decode(image_data)
            return Response(image_binary, mimetype='image/png')
        else:
            return Response("Invalid image data received.", status=500, mimetype='text/plain')
    else:
        return Response(f"Error: {response.text}", status=response.status_code, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
