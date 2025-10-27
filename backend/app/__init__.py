from flask import Flask
from flask_cors import CORS
# # Import extensions like SQLAlchemy, Migrate, JWTManager later
# from .config import Config

# Import Blueprints
from .players import players_bp
# from .teams import teams_bp
# from .auth import auth_bp # Import later

def create_app():
    app = Flask(__name__)
    # app.config.from_object(config_class)

    # Initialize Flask extensions here
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}) # Allow frontend origin
    # db.init_app(app)       # Example for SQLAlchemy
    # migrate.init_app(app, db) # Example for Flask-Migrate
    # jwt.init_app(app)       # Example for Flask-JWT-Extended

    # # Register blueprints
    app.register_blueprint(players_bp, url_prefix='/api')
    # app.register_blueprint(teams_bp, url_prefix='/api')
    # # app.register_blueprint(auth_bp, url_prefix='/api/auth') # Example for auth

    # Add a simple health check route here if you like
    @app.route('/health')
    def health():
        return {"status": "healthy"}

    return app