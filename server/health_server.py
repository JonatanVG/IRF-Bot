# flask_health_server.py
from flask import Flask, render_template, jsonify
from bot_managment.supabase_setup import Supabase2
from dotenv import load_dotenv
from waitress import serve
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

app.template_folder = 'views'

app.static_folder = 'static'
app.static_url_path = '/static'

# Health check endpoint
@app.route('/')
def index():
  try:
    response = Supabase2.table('DBChecker website items')\
      .select('*')\
      .eq('page', 3)\
      .order('id', desc=False)\
      .execute()
    
    if hasattr(response, 'error') and response.error:
      logger.error(f"Supabase error: {response.error}")
      return jsonify({"error": "Database query failed"}), 500
    
    data = response.data
    logger.info(f"Fetched {len(data)} items from Supabase for health check")
    return render_template('index.html', title='IRF Checker Bot - Health Check', items=data)
  except Exception as e:
    logger.error(f"Error in health check endpoint: {e}")
    return jsonify({"error": "Internal server error"}), 500

@app.route("/Privacy-Policy")
def privacy_policy():
  response = Supabase2.table('DBChecker website items')\
    .select('id, name, content')\
    .eq('page', 1)\
    .order('id', desc=False)\
    .execute()
    
  data = response.data
  return render_template('privacy-policy.html', title='Privacy Policy', items=data)

@app.route("/Terms-of-Service")
def terms_of_service():
  response = Supabase2.table('DBChecker website items')\
    .select('id, name, content')\
    .eq('page', 2)\
    .order('id', desc=False)\
    .execute()

  data = response.data
  return render_template('terms-of-service.html', title='Terms of Service', items=data)

def run_website():
  print("Starting Flask website on port 8000...")
  serve(app, host='0.0.0.0', port=8000)