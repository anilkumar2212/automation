from flask import Flask, render_template, request, jsonify
import os
import subprocess
from rasa_structure import rasa_init
from rasa_data_injection import data_injection
import shutil
import tarfile
import datetime

current_directory = os.getcwd()
data_directory = "data"
source_file = "data.xlsx"
rasa_directory_name = "rasa"
rasa_directory = os.path.join(current_directory, rasa_directory_name)
rasa_model_directory = os.path.join(current_directory, rasa_directory_name, "models")

app = Flask(__name__)

def dvc_remote(product_name,comments):
    dvc_commands = [
    f'dvc add data/{product_name}',
    f'git add data/{product_name}.dvc data/.gitignore',
    f'git commit -m "{comments}"',
    'git push'] #'dvc push',
    for cmd in dvc_commands:
        subprocess.run(cmd, shell=True)

def model_dvc_remote(product_name):
    formatted_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M")
    model_dvc_commands = [
    f'dvc add models/{product_name}',
    f'git add models/{product_name}.dvc models/.gitignore',
    f'git commit -m "{product_name}_{formatted_datetime}"',
    'git push'] #'dvc push',
    for cmd in model_dvc_commands:
        subprocess.run(cmd, shell=True)


def build_model(product_directory):
    rasa_initilization = rasa_init()
    # Check if the folder exists
    if os.path.exists(rasa_model_directory) and os.path.isdir(rasa_model_directory):
        try:
            files = os.listdir(rasa_model_directory)
            for file in files:
                file_path = os.path.join(rasa_model_directory, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error deleting files in the 'rasa' folder - {e}")
    else:
        print(f"The 'rasa' folder does not exist or is not a directory.")

    if rasa_initilization:
        injecting_data = data_injection(product_directory=product_directory)
        if injecting_data:
            rasa_directory = os.path.join(current_directory, rasa_directory_name)
            try:
                subprocess.run("rasa train", shell=True, cwd=rasa_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            except Exception as e:
                print(e)
        else:
            print('data injection failed')
    else:
        print('rasa_initilization failed')

def drag_model(model_directory):
    current_directory = os.getcwd()
    rasa_model_directory = os.path.join(current_directory, "rasa", "models")

    model_target_folder = os.path.join(current_directory, "models", model_directory, "model.tar.gz")
    
    try:
        # Find the .tar.gz file in the directory
        tar_gz_file_path = None
        for file_name in os.listdir(rasa_model_directory):
            if file_name.endswith(".tar.gz"):
                tar_gz_file_path = os.path.join(rasa_model_directory, file_name)
                break  # Stop after finding the first .tar.gz file
        if tar_gz_file_path is None:
            print("No .tar.gz file found in the directory.")
            return
    except FileNotFoundError:
        print(f"Directory not found: {rasa_model_directory}")
    try:
        # Check if the target file already exists
        if os.path.exists(model_target_folder):
            os.remove(model_target_folder)  # Remove the existing file
        # Rename and drag the file
        os.rename(tar_gz_file_path, model_target_folder)
        print(f"Renamed '{tar_gz_file_path}' to '{model_target_folder}'.")
    except FileNotFoundError:
        print(f"File not found: {tar_gz_file_path}")

    if os.path.exists(rasa_directory) and os.path.isdir(rasa_directory):
        try:
            # Use shutil.rmtree to remove the entire directory
            shutil.rmtree(rasa_directory)
        except Exception as e:
            print(f"Error deleting the 'rasa' folder - {e}")
    else:
        print(f"The 'rasa' folder does not exist or is not a directory.")

@app.route('/', methods=['GET'])
def homePage():
    return render_template("index.html")

@app.route('/upload_otrim', methods=['POST'])
def upload_otrim():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file.save(os.path.join("data/otrim", "data.xlsx"))
                comments = request.form['comments']
                dvc_remote(product_name= 'otrim',comments=comments)
                return render_template("index.html", otrim_message="File is uploaded to Otrim")
        return render_template("index.html", message="")

@app.route('/upload_omail', methods=['POST'])
def upload_omail():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file.save(os.path.join("data/omail", "data.xlsx"))
                comments = request.form['comments']
                dvc_remote(product_name= 'omail',comments=comments)
                return render_template("index.html", omail_message="File is uploaded to Omail")
        return render_template("index.html", message="")

@app.route('/upload_onet', methods=['POST'])
def upload_onet():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file.save(os.path.join("data/onet", "data.xlsx"))
                comments = request.form['comments']
                dvc_remote(product_name= 'onet',comments=comments)
                return render_template("index.html", onet_message="File is uploaded to Onet")
        return render_template("index.html", message="")

@app.route('/build_otrim_model', methods=['POST'])
def build_otrim_model():
    product = "otrim"
    build_model(product_directory = product)
    drag_model(model_directory = product)
    model_dvc_remote(product_name = "otrim")
    return render_template("index.html")

@app.route('/build_omail_model', methods=['POST'])
def build_omail_model():
    product = "omail"
    build_model(product_directory = product)
    drag_model(model_directory = product)
    model_dvc_remote(product_name="omail")
    return render_template("index.html")

@app.route('/build_onet_model', methods=['POST'])
def build_onet_model():
    product = "onet"
    build_model(product_directory = product)
    drag_model(model_directory = product)
    model_dvc_remote(product_name="onet")
    return render_template("index.html")

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8080)
    app.run(host="0.0.0.0", port=8080, debug=True)
