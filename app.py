from flask import Flask, request, Response
from rembg import remove, new_session
import base64
import os

app = Flask(__name__)

print("Loading lightweight model...")
session = new_session("u2netp")  # ← tiny model
print("Model ready!")

@app.route("/v1.0/removebg", methods=["POST"])
def removebg():
    try:
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
