from flask import Flask, request, Response
from rembg import remove, new_session
import base64
import os
import threading

app = Flask(__name__)
session = None

def load_model():
    global session
    print("Loading model...")
    session = new_session("u2netp")
    print("Model ready!")

# Load model in background AFTER Flask starts
threading.Thread(target=load_model, daemon=True).start()

@app.route("/")
def home():
    return "OK"

@app.route("/v1.0/removebg", methods=["POST"])
def removebg():
    try:
        if session is None:
            return Response("model loading", status=503)
        data = request.get_json()
        if not data or "image_file_b64" not in data:
            return Response("missing image", status=400)
        img = base64.b64decode(data["image_file_b64"])
        result = remove(img, session=session)
        return Response(result, mimetype="image/png")
    except Exception as e:
        print("Error:", str(e))
        return Response(str(e), status=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
