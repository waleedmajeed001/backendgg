import sys
import os
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        print("All dependencies are installed")
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main function to start the Flask server"""
    
    if not check_python_version():
        sys.exit(1)

    if not check_dependencies():
        sys.exit(1)

    port = os.environ.get('PORT', 5000)
    
    print(f" Todo backend started on port {port}")
    
    try:
        from app import app
        app.run(host='0.0.0.0', port=port, debug=True)
    except KeyboardInterrupt:
        print("\n Server stopped by user")
    except Exception as e:
        print(f" Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 