import re

from flask import Flask, request, jsonify, send_file, after_this_request
import nanoid
from flask_cors import CORS
import os

app = Flask(__name__)
app.json.sort_keys = False
CORS(app, supports_credentials=True)
try:
    os.mkdir('/tmp')
except:
    pass
@app.route('/directory-analyze', methods=['POST'])
def directory_analyze():
    table = request.get_json()['table_result']
    dpi = 300
    if 'dpi' in request.get_json():
        dpi = request.get_json()['dpi']
    row_count = 128
    row_height = dpi*11.69/row_count
    table = [{
        "pos": [item['location'][0][0],round(item['location'][0][1]/row_height)],
        "words": item['words'].replace("、","-").replace("--","-").split("-")[0],
    } for item in table]
    new_table = [[]]
    y_pos = table[0]['pos'][1]
    for cell in table:
        if abs(cell['pos'][1]-y_pos) > 2:
            new_table.append([cell['words']])
            y_pos = cell['pos'][1]
        else:
            new_table[-1].append(cell['words'])
    header = new_table[0]
    content_pos = 0
    page_pos = 0
    content_regex = re.compile(r"(标题|内容|名称)")
    for i in range(len(header)):
        if content_regex.findall(header[i]):
            content_pos = i
        if "页" in header[i]:
            page_pos = i
    table = [[item[content_pos],item[page_pos]] for item in new_table[1:] if len(item)==len(header)]
    table = [item for item in table if item!=["",""]]
    if table[0][1] == "":
        table[0][1] = "1"
    return jsonify(table=table)

@app.route('/background-detect', methods=['POST'])
def background_detect():
    file_name = f'/tmp/{nanoid.generate(size=10)}.jpg'
    request.files['jpg'].save(file_name)
    return send_file(file_name, mimetype='image/jpg')


if __name__ == "__main__":
    app.run("0.0.0.0", 5001)
