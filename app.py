from flask import Flask, render_template, jsonify ,request
from flask_cors import CORS
import fetch_trending_topics

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_trending_topics', methods=['POST','GET'])
def run_script():
    inputs = {}
    if request.method == 'POST':
       inputs = request.get_json()
    data = fetch_trending_topics.getTrendingTopics(inputs)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
