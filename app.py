from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from routes.todo_routes import todo_bp
from routes.health_routes import health_bp
from migrate import create_tables

load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

PORT = int(os.environ.get('PORT', 5000))

create_tables()

app.register_blueprint(todo_bp)
app.register_blueprint(health_bp)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Route not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Something went wrong!'}), 500

if __name__ == '__main__':
    print(f"Todo backend started on port {PORT}")
    print(f"Database initialized: todo_app.db")
    app.run(host='0.0.0.0', port=PORT, debug=True)
    