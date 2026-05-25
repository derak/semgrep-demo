import uuid
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for

app = Flask(__name__)

# A secret key is required by Flask to securely encrypt and sign session cookies
app.secret_key = "super-secret-development-key-change-in-production"

# Mock database tracking internal state
IN_MEMORY_DB = {
    "items": [
        {"id": 1, "name": "Developer Laptop", "category": "Hardware"},
        {"id": 2, "name": "Mechanical Keyboard", "category": "Peripherals"}
    ]
}

# --- ENDPOINT 1: Static/Template Rendering (The Landing Page) ---
@app.route("/")
def home():
    # Standard HTML layout with a basic user profile tracker via sessions
    username = session.get("user", "Guest Visitor")
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Flask Demo Application</title></head>
    <body>
        <h1>Welcome to the Flask Demo Platform, {{ name }}!</h1>
        <p>This backend application showcases 5 typical architectural entry points.</p>
        <ul>
            <li><a href="/items">View JSON REST API</a></li>
            <li><a href="/user/dev_user_99">Test Dynamic Route Parameters</a></li>
        </ul>
        <hr/>
        <h3>Simulate User Session Login</h3>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Enter username" required />
            <button type="submit">Establish Session Context</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html_content, name=username)


# --- ENDPOINT 2: Form Processing & Redirects (State Management) ---
@app.route("/login", methods=["POST"])
def login():
    # Captures payload sent via standard HTTP POST form submissions
    username = request.form.get("username")
    if username:
        session["user"] = username  # Mutating client cookie state
    return redirect(url_for("home"))


# --- ENDPOINT 3: Dynamic URL Parameters (Resource Fetching) ---
@app.route("/user/<username>")
def profile(username):
    # Extracts the dynamic string portion out of the URL endpoint routing path
    # Useful for clean profile links: /user/john_doe
    user_agent = request.headers.get("User-Agent")
    return f"<h3>Profile Node for System User: @{username}</h3><p>Connecting Device Profile: {user_agent}</p>"


# --- ENDPOINT 4: JSON REST API Endpoint (Data Integration Layer) ---
@app.route("/items", methods=["GET"])
def get_items():
    # Serialization of data payloads to JSON format for SPA frontends or mobile integrations
    return jsonify({
        "status": "success",
        "total_records": len(IN_MEMORY_DB["items"]),
        "payload": IN_MEMORY_DB["items"]
    })


# --- ENDPOINT 5: Request Query Parameters & Mutation (Data Submission) ---
@app.route("/items/add", methods=["POST"])
def add_item():
    # Extracts arguments passed natively inside a JSON body payload
    data = request.get_json() or {}
    
    name = data.get("name")
    category = data.get("category", "General")
    
    if not name:
        return jsonify({"error": "Missing mandatory parameter: name"}), 400
        
    new_item = {
        "id": len(IN_MEMORY_DB["items"]) + 1,
        "name": name,
        "category": category
    }
    
    IN_MEMORY_DB["items"].append(new_item)
    return jsonify({"message": "Resource appended successfully", "item": new_item}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
