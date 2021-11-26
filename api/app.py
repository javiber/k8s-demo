import logging

from flask import Flask, jsonify

# from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# metrics = PrometheusMetrics(app)
# metrics.info("app_info", "Toy API", version="1.0.0")

@app.route("/")
def hello_world():
    logger.info("request received")
    return jsonify({
        "message": "Hello world!"
    })

if __name__ == '__main__':
    logger.info("starting server")
    app.run(host='0.0.0.0', port=5000)
