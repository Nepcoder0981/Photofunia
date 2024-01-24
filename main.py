from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def generate_image():
    text_parameter = request.args.get('text', '')
    url_parameter = request.args.get('url', '')

    # Ensure the URL is provided
    if not url_parameter:
        return jsonify({"error": "URL parameter is required."}), 400

    # Define your custom headers
    headers = {
        "Host": "m.photofunia.com",
        "Connection": "keep-alive",
        "Content-Length": "140",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Android WebView";v="120"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://m.photofunia.com",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryotPXwBaV73aQcr07",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2101K6G Build/TKQ1.221013.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.211 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "X-Requested-With": "mark.via.gp",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://m.photofunia.com/categories/all_effects/balloon",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "_ga=GA1.2.175010173.1705225604; PHPSESSID=fias7o2dk6n9ctk4unactps5k7; accept_cookie=true; _gid=GA1.2.342766436.1705941396; _gat=1"
    }

    # Define your custom payload
    payload = f"""------WebKitFormBoundaryotPXwBaV73aQcr07
Content-Disposition: form-data; name="text"

{text_parameter}
------WebKitFormBoundaryotPXwBaV73aQcr07--"""

    # Fetch HTML content from the provided URL with custom headers and payload
    response = requests.post(url_parameter, headers=headers, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract image URL from the HTML response
        image_start = response.text.find('<img src="') + len('<img src="')
        image_end = response.text.find('"', image_start)
        image_url = response.text[image_start:image_end]

        # Create JSON output with join parameter
        join_parameter = request.args.get('join', '@devsnp')
        result_json = {"generatedimage": image_url, "text": text_parameter, "join": join_parameter}
        return jsonify(result_json)
    else:
        return jsonify({"error": f"Request failed with status code {response.status_code}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
