from flask import Flask, render_template, jsonify
from flask_cors import CORS
from sample_blenderbot import BlenderBot

app = Flask(__name__)

CORS(
	app,
	support_credentials=True
)

b = BlenderBot(size="medium", device="cpu")

@app.route("/")
def index():
	return jsonify({"version": "0.01"})

@app.route("/send/<user_id>/<text>")
def send(user_id, text: str):
	splitted_text = text.split("_")
	merged_text = " ".join(splitted_text)
	_out = b.predict(user_id, merged_text)
	return jsonify({"text": _out})

if __name__ == "__main__":
	app.run(port=8888)