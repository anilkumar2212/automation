from flask import Flask, render_template, request, jsonify
import os
import subprocess


app = Flask(__name__)

def dvc_remote(product_name,comments):
    dvc_commands = [
    f'dvc add data/{product_name}',
    f'git add data/{product_name}.dvc data/.gitignore',
    f'git commit -m "{comments}"',
    'dvc push',
    'git push']
    for cmd in dvc_commands:
        subprocess.run(cmd, shell=True)

@app.route('/', methods=['GET'])
def homePage():
    return render_template("index2.html")

@app.route('/upload_otrim', methods=['POST'])
def upload_otrim():
    if request.method == 'POST':
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>")
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file.save(os.path.join("data/otrim", "data.xlsx"))
                dvc_remote(product_name= 'otrim',comments="otrim version added")
                return render_template("index2.html", otrim_message="File is uploaded to Otrim")
        return render_template("index2.html", message="")


@app.route('/upload_omail', methods=['POST'])
def upload_omail():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file.save(os.path.join("data/omail", "data.xlsx"))
                dvc_remote(product_name= 'omail',comments="omail version added")
                return render_template("index2.html", omail_message="File is uploaded to Omail")
        return render_template("index2.html", message="")


@app.route('/upload_onet', methods=['POST'])
def upload_onet():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file.save(os.path.join("data/onet", "data.xlsx"))
                dvc_remote(product_name= 'onet',comments="onet version added")
                return render_template("index2.html", onet_message="File is uploaded to Onet")
        return render_template("index2.html", message="")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

    #app.run(host="0.0.0.0", port=8080, debug=True)
