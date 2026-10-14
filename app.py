from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/spin")
def spin():
    winner = random.randint(1, 32)
    return jsonify({"winner": winner})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
