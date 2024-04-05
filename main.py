from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def get_direct_download_url(url):
    res = requests.get(url, stream=True)
    contents = res.text

    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.group(1)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if url:
        direct_download_url = get_direct_download_url(url)
        if direct_download_url:
            return jsonify({'direct_download_url': direct_download_url})
        else:
            return jsonify({'error': 'Direct download URL not found.'}), 404
    else:
        return jsonify({'error': 'URL parameter is required.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
