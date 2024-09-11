from flask import Flask, jsonify
from flask_cors import CORS
from routes import dashboard_bp

app = Flask(__name__)
CORS(app)


# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({'message': 'success!'})


app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    app.run(debug=True)
