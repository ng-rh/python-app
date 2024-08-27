from flask import Flask, jsonify, request, send_from_directory
import os
import logging

app = Flask(__name__, static_folder='static')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple in-memory counter
counter = 0

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/count', methods=['GET'])
def get_count():
    """
    Endpoint to get the current count.
    """
    try:
        return jsonify({'count': counter})
    except Exception as e:
        logger.error(f"Error fetching count: {e}")
        return jsonify({'error': 'Failed to fetch count'}), 500

@app.route('/increment', methods=['POST'])
def increment_count():
    """
    Endpoint to increment the counter.
    """
    global counter
    try:
        increment_by = request.json.get('increment_by', 1)
        if not isinstance(increment_by, int) or increment_by <= 0:
            return jsonify({'error': 'Invalid increment value'}), 400
        counter += increment_by
        return jsonify({'count': counter})
    except Exception as e:
        logger.error(f"Error incrementing count: {e}")
        return jsonify({'error': 'Failed to increment count'}), 500

@app.route('/info', methods=['GET'])
def app_info():
    """
    Endpoint to get application information.
    """
    try:
        return jsonify({
            'app_name': 'My Flask App',
            'version': '1.0.0',
            'description': 'A simple Flask application with a counter and JSON endpoints.'
        })
    except Exception as e:
        logger.error(f"Error fetching app info: {e}")
        return jsonify({'error': 'Failed to fetch app info'}), 500

if __name__ == "__main__":
    # Load environment configuration
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
