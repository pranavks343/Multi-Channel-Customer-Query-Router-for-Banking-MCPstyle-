print("Python is working!")
print("Now testing Flask...")

try:
    from flask import Flask
    print("✓ Flask import successful")
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "Hello! Flask is working!"
    
    @app.route('/health')
    def health():
        return {"status": "ok"}
    
    print("✓ Flask app created")
    print("✓ Starting server on port 8000...")
    print()
    print("=" * 60)
    print("Open browser to: http://localhost:8000")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=8000, debug=True)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

