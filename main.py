from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def get_mediafire_download_link(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        download_link = soup.find('a', {'id': 'downloadButton'})['href']
        return download_link
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if url:
        direct_download_url = get_mediafire_download_link(url)
        if direct_download_url:
            return jsonify({'direct_download_url': direct_download_url})
        else:
            return jsonify({'error': 'Direct download URL not found.'}), 404
    else:
        return jsonify({'error': 'URL parameter is required.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
