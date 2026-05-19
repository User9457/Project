"""
app.py – Flask entry point (MVC pattern)
"""
from flask import Flask
from controllers.mission_controller       import mission_bp
from controllers.economic_controller      import economic_bp
from controllers.above_average_controller import above_average_bp

app = Flask(__name__)

# Đăng ký blueprints
app.register_blueprint(mission_bp)
app.register_blueprint(economic_bp)
app.register_blueprint(above_average_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
