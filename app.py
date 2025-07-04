from flask import Flask, request, jsonify, redirect
from datetime import datetime, timedelta
from uuid import uuid4
from logger import Log  # Custom logging module that was specified

app = Flask(__name__)

# In-memory storage for shortcodes — not production ready, but great for quick testing
url_store = {}

def generate_shortcode():
    """
    Generates a 6-character unique shortcode using UUID4.
    """
    return uuid4().hex[:6]

@app.route('/shorturls', methods=['POST'])
def create_short_url():
    """
    Creates a new short URL entry. 
    Accepts JSON with 'url', optional 'validity' (in minutes), and optional 'shortcode'.
    """
    data = request.get_json()
    original_url = data.get('url')
    validity = data.get('validity', 30)  # Default: 30 minutes
    shortcode = data.get('shortcode') or generate_shortcode()

    # Validate presence of original URL
    if not original_url:
        Log("backend", "error", "shortener", "Missing URL")
        return jsonify({"error": "URL is required"}), 400

    # Ensure shortcode is unique and not repetitive to avoid mishandling
    if shortcode in url_store:
        Log("backend", "error", "shortener", "Shortcode already exists")
        return jsonify({"error": "Shortcode already exists"}), 409

    # Calculate expiry time based on current UTC time for generation
    expires_at = datetime.utcnow() + timedelta(minutes=validity)

    # Store entry in memory
    url_store[shortcode] = {
        "original": original_url,
        "expires": expires_at,
        "created": datetime.utcnow(),
        "hits": 0  # Keep track of redirects
    }

    Log("backend", "info", "shortener", f"Created shortcode {shortcode}")
    return jsonify({
        "shortUrl": f"http://localhost:5000/{shortcode}",
        "validUntil": expires_at.isoformat()
    }), 201

@app.route('/<shortcode>', methods=['GET'])
def redirect_to_original(shortcode):
    """
    Redirects to the original URL if the shortcode is valid and not expired.
    """
    entry = url_store.get(shortcode)

    # Check if shortcode exists
    if not entry:
        Log("backend", "error", "redirect", "Shortcode not found")
        return jsonify({"error": "Shortcode not found"}), 404

    # Check if shortcode has expired
    if datetime.utcnow() > entry['expires']:
        Log("backend", "error", "redirect", "Shortcode expired")
        return jsonify({"error": "Shortcode expired"}), 410

    # Increment hit counter and redirect
    entry["hits"] += 1
    Log("backend", "info", "redirect", f"Redirecting shortcode {shortcode}")
    return redirect(entry["original"], code=302)

if __name__ == '__main__':
    # Dev mode enabled. Remember to disable debug in production!
    app.run(debug=True)
