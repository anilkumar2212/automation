from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homePage():
    return render_template("index.html")

@app.route('/upload_otrim', methods=['POST'])
def upload_otrim():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join("data/otrim", "data.xlsx"))
            return render_template("index2.html", otrim_message="File is uploaded to Otrim")
    return render_template("index2.html", message="")


@app.route('/upload_omail', methods=['POST'])
def upload_omail():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join("data/omail", "data.xlsx"))
            return render_template("index2.html", omail_message="File is uploaded to Omail")
    return render_template("index2.html", message="")


@app.route('/upload_onet', methods=['POST'])
def upload_onet():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join("data/onet", "data.xlsx"))
            return render_template("index2.html", onet_message="File is uploaded to Onet")
    return render_template("index2.html", message="")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
