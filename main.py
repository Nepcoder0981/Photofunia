from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def login():
    uid = request.args.get('uid')

    url = "https://shop.garena.sg/api/auth/player_id_login"

    headers = {
        "Host": "shop.garena.sg",
        "Connection": "keep-alive",
        "Content-Length": "59",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Android WebView\";v=\"120\"",
        "accept": "application/json",
        "content-type": "application/json",
        "x-datadome-clientid": "1iAO5XRKKzGKRzlbwX3RmRBp3g88nhvf9frgmlC50g1IM0CykBhU1GApn5gbo~ELqOE4DTHoJmxcFOyzA11_qbIvXH9iHUFjSyviiWahl8bectrZ4yAq6GF0LSDee8f1",
        "sec-ch-ua-mobile": "?1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "sec-ch-ua-platform": "\"Android\"",
        "Origin": "https://shop.garena.sg",
        "X-Requested-With": "mark.via.gp",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://shop.garena.sg/app/100067/idlogin",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,bn-BD;q=0.8,bn;q=0.7",
        
    }

    data = {
        "app_id": 100067,
        "login_id": uid,
        "app_server_id": 0
    }

    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Extract the desired fields
        region = json_response.get("region", "")
        nickname = json_response.get("nickname", "")

        # Create a new dictionary with the desired fields
        output_json = {"region": region, "nickname": nickname, "join": "-@devsnp"}

        # Convert the dictionary to a JSON-formatted string with unescaped slashes
        json_output = json.dumps(output_json, ensure_ascii=False)

        # Return the modified JSON output
        return json_output
    else:
        # Return an error message if the request was not successful
        return jsonify({"error": f"Error: {response.status_code}, {response.text}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
