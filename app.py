from flask import Flask, render_template, jsonify
import fetch_trending_topics

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['GET'])
def run_script():
    data = fetch_trending_topics.getTrendingTopics()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
