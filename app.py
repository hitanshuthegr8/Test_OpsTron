import logging
import time
import threading
from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

request_count = 0

def background_heartbeat():
    while True:
        logger.info("✅ App heartbeat — all systems running normally.")
        time.sleep(10)

@app.route('/')
def index():
    global request_count
    request_count += 1
    logger.info(f"GET / — request #{request_count}")
    
    # Crash every 5th request to simulate a bug Yay
    if request_count % 5 == 0:
        logger.error(f"💥 Triggering intentional crash on request #{request_count}")
        result = 1 / 0  # ZeroDivisionError to test OpsTron

    return jsonify({"status": "ok", "message": "Hit /error to force a crash!"})

@app.route('/error')
def force_error():
    logger.error("🔴 CRITICAL: force_error endpoint triggered! ValueError: Amount cannot be negative")
    return jsonify({"error": "Simulated payment failure"}), 500

if __name__ == '__main__':
    threading.Thread(target=background_heartbeat, daemon=True).start()
    logger.info("🚀 Sample app starting on port 5000... hah     aha")
    app.run(host='0.0.0.0', port=5000)
