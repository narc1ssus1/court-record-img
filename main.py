from flask import Flask, request, jsonify, send_file, after_this_request
import nanoid
from flask_cors import CORS


app = Flask(__name__)
app.json.sort_keys = False
CORS(app, supports_credentials=True)

@app.route('/directory-analyze', methods=['POST'])
def directory_analyze():
    tables = request.get_json()['table_result']
    result = {
        "律师事务所批办单":1,
        "风险告知书":2,
        "委托代理合同":3,
        "委托代理授权书":4,
        "委托代理人身份证明":5,
        "收费凭证":6,
        "其他":7
    }
    return jsonify(result)

@app.route('/background-detect', methods=['POST'])
def background_detect():
    file_name = f'/tmp/{nanoid.generate(size=10)}.jpg'
    request.files['jpg'].save(file_name)
    return send_file(file_name, mimetype='image/jpg')


if __name__ == "__main__":
    app.run("0.0.0.0", 5001)
