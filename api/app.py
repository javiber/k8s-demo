"""Very simple Flask API"""
import logging

from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def hello_world():
    logger.info("request received")
    return jsonify({"message": "Hello world!"})


if __name__ == "__main__":
    logger.info("starting server")
    app.run(host="0.0.0.0", port=5000)
