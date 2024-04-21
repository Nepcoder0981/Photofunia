from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/sms/<number>')
def scrape_messages(number):
    # Define the URL using the provided phone number
    url = f"https://receive-smss.com/sms/{number}/"

    # Define the headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Referer": f"https://receive-smss.com/sms/{number}/",
        "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
    }

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all message details
    messages = soup.find_all('div', class_='message_details')

    # Initialize a list to store extracted data
    data = []

    # Loop through each message detail
    for message in messages:
        sender = message.find('div', class_='senderr').a.text
        # Check if the message text starts with "Message" and remove it if it does
        message_text = message.find('div', class_='msgg').text
        if message_text.startswith("Message"):
            message_text = message_text[len("Message"):].strip()
        message_time = message.find('div', class_='time').text
        # Check if the time starts with "Time" and remove it if it does
        if message_time.startswith("Time"):
            message_time = message_time[len("Time"):].strip()
        data.append({
            'sender': sender,
            'message': message_text,
            'time': message_time
        })

    # Convert the data to JSON format with unescaped slashes
    json_data = json.dumps(data, ensure_ascii=False)

    # Return the data as JSON
    return json_data

if __name__ == '__main__':
    app.run(debug=True)
    
