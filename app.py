"""
app.py – Flask entry point (MVC pattern)
"""
from flask import Flask

# Subtask A controllers
from controllers.landing_controller       import landing_bp
from controllers.vaccination_controller   import vaccination_bp
from controllers.improvement_controller   import improvement_bp

# Subtask B controllers
from controllers.mission_controller       import mission_bp
from controllers.economic_controller      import economic_bp
from controllers.above_average_controller import above_average_bp

app = Flask(__name__)

# Đăng ký blueprints cho Subtask A
app.register_blueprint(landing_bp)
app.register_blueprint(vaccination_bp)
app.register_blueprint(improvement_bp)

# Đăng ký blueprints cho Subtask B
app.register_blueprint(mission_bp)
app.register_blueprint(economic_bp)
app.register_blueprint(above_average_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
