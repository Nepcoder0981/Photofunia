import random
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# List of user-agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.43",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/86.0.4240.198",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
]

def get_mediafire_download_link(url):
    try:
        headers = {
            "User-Agent": random.choice(user_agents),
            "Referer": url,
            "Useganet": "true"
        }
        page = requests.get(url, headers=headers)
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
    
