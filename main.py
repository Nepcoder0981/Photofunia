from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)

@app.route('/generate-image', methods=['GET', 'POST'])
def generate_image():
    prompt = None
    size = '1_1'  # Default size
    model = 'flux_1_schnell'  # Default model

    if request.method == 'GET':
        prompt = request.args.get('prompt')
        size = request.args.get('size', size)
        model = request.args.get('model', model)
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            prompt = data.get('prompt', prompt)
            size = data.get('size', size)
            model = data.get('model', model)

    if not prompt:
        return jsonify({"error": "Prompt parameter is missing."}), 400

    if model == 'techcoderai':
        url = f"https://fast-flux-demo.replicate.workers.dev/api/generate-image?text={prompt}"
        response = requests.get(url)

        if response.status_code == 200:
            image_data = response.content
            base64_image = base64.b64encode(image_data).decode('utf-8')
            return jsonify({"image_base64": base64_image})
        else:
            return jsonify({"error": response.text}), response.status_code

    elif model == 'logogen':
        # API request for logogen model
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://freeflux.ai",
            "referer": "https://freeflux.ai/",
            "user-agent": "Mozilla/5.0"
        }

        payload = {
            "prompt": prompt,
            "logo": True
        }

        url = "https://api.freeflux.ai/v1/images/generate"

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if "result" in data and data["result"].startswith("data:image/png;base64,"):
                image_data = data["result"].split(",", 1)[1]
                return jsonify({"image_base64": image_data})
            else:
                return jsonify({"error": "Invalid image data received."}), 500
        else:
            return jsonify({"error": response.text}), response.status_code

    else:
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://fastflux.co",
            "referer": "https://fastflux.co/",
            "user-agent": "Mozilla/5.0"
        }

        payload = {
            "isPublic": False,
            "model": model,
            "prompt": prompt,
            "size": size
        }

        url = "https://api.fastflux.co/v1/images/generate"

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if "result" in data and data["result"].startswith("data:image/png;base64,"):
                image_data = data["result"].split(",", 1)[1]
                return jsonify({"image_base64": image_data})
            else:
                return jsonify({"error": "Invalid image data received."}), 500
        else:
            return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
