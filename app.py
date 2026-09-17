from flask import Flask, request, Response
from rembg import remove
import base64

app = Flask(__name__)

@app.route("/v1.0/removebg", methods=["POST"])
def removebg():
    try:
        data = request.get_json()
        img = base64.b64decode(data["image_file_b64"])
        result = remove(img)
        return Response(result, mimetype="image/png")
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
