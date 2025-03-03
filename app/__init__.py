import os
from flask import Flask
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Custom template filter for date and time formatting
    @app.template_filter('datetime')
    def format_datetime(timestamp):
        """Converts a Unix timestamp to a readable date and time."""
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    from .routes import main
    app.register_blueprint(main)

    return app
