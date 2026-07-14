import os
from flask import Flask, request

app = Flask(__name__)

# Simulated system file path for testing infrastructure
DUMMY_DIR = os.path.join(os.getcwd(), "dummy_server_root")
os.makedirs(DUMMY_DIR, exist_ok=True)

# Creating simulated sensitive files for cross-platform detection verification
with open(os.path.join(DUMMY_DIR, "passwd"), "w") as f:
    f.write("root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin")

with open(os.path.join(DUMMY_DIR, "win.ini"), "w") as f:
    f.write("[extensions]\n[fonts]\ncmaster=1")

@app.route('/')
def home():
    return "<h3>AegisVM Test Lab - Vulnerable Endpoint is Online. Use /view?file= to test.</h3>"

# INTENTIONALLY VULNERABLE ROUTE: Pure path sanitation bypass layout
@app.route('/view')
def view_file():
    filename = request.args.get('file')
    if not filename:
        return "Missing 'file' parameter. Example: /view?file=passwd", 400
    
    # CRITICAL SECURITY FLAW: Direct path concatenation without sanitation or realpath validation
    unsafe_filepath = os.path.join(DUMMY_DIR, filename)
    
    try:
        if os.path.exists(unsafe_filepath):
            with open(unsafe_filepath, 'r') as f:
                content = f.read()
            return f"<pre>{content}</pre>"
        else:
            return f"File not found: {filename}", 404
    except Exception as e:
        return f"Internal Error: {str(e)}", 500

if __name__ == '__main__':
    print("[*] Starting AegisVM Vulnerable Target Environment...")
    app.run(host='127.0.0.1', port=5000, debug=True)
