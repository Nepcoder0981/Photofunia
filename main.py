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

def get_mediafire_download_info(url):
    try:
        headers = {
            "User-Agent": random.choice(user_agents),
            "Referer": url,
            "Useganet": "true"
        }
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        download_link_element = soup.find('a', {'id': 'downloadButton'})
        download_link = download_link_element['href']
        file_size_text = download_link_element.get_text(strip=True)
        file_size = re.search(r'(\d+(\.\d+)?)MB', file_size_text)
        if file_size:
            file_size_mb = float(file_size.group(1))
        else:
            file_size_mb = None
        return download_link, file_size_mb
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if url:
        direct_download_url, file_size_mb = get_mediafire_download_info(url)
        if direct_download_url:
            response_data = {'direct_download_url': direct_download_url}
            if file_size_mb is not None:
                response_data['file_size_mb'] = file_size_mb
            return jsonify(response_data)
        else:
            return jsonify({'error': 'Direct download URL not found.'}), 404
    else:
        return jsonify({'error': 'URL parameter is required.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
    
