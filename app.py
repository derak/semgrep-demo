from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the root/home URL
@app.route("/")
def hello_world():
    return "Hello, World!"

# Run the application if the script is executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
