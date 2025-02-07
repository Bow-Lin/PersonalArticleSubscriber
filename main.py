from flask import Flask, render_template
from src.tracker import DocumentTracker
from src.utils import load_config

app = Flask(__name__)

# Global variable to store trackers
trackers = {}

def initialize_trackers(config):
    """Initialize trackers for all websites"""
    global trackers
    for website in config['websites']:
        trackers[website['name']] = {
            'tracker': DocumentTracker(website['url']),
            'url': website['url']
        }

@app.route('/')
def index():
    """Check for updates when the page is loaded and return results"""
    updates = {}
    
    try:
        # Check updates for each website
        for site_name, site_data in trackers.items():
            tracker = site_data['tracker']
            new_updates = tracker.check_updates()
            # Always add the website to updates dictionary, even if there are no new updates
            updates[site_name] = {
                'updates': new_updates if new_updates else [],
                'url': site_data['url']
            }
    except Exception as e:
        print(f"Error checking updates: {e}")
        
    # Return the template with updates (empty or not)
    return render_template('index.html', websites=updates)

if __name__ == "__main__":
    config = load_config()  # defaults to "config.yaml"
    
    # Initialize trackers
    initialize_trackers(config)
    
    # Run Flask app
    app.run(debug=True, port=5000) 