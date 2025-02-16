from flask import Flask, render_template, request, send_from_directory, url_for
import cv2
import numpy as np
import os

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.static_folder = UPLOAD_FOLDER  # Explicitly set static folder

# ✅ Fix: Ensure Flask Serves Uploaded Images Correctly
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)



@app.route('/')
def index():
    return render_template('index.html', active_tab="encrypt", uploaded_image=None, encoded_image=None)

@app.route('/encode', methods=['POST'])
def encode():
    if 'file' not in request.files:
        return "No file uploaded"
    file = request.files['file']
    message = request.form['message']
    password = request.form['password']  # Store password
    
    if file.filename == '':
        return "No file selected"
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    img = cv2.imread(filepath)
    if img is None:
        return "Error: Unable to read the image."
    
    d = {chr(i): i for i in range(256)}

    # Add password at the beginning of the message
    message = password + "|" + message  # Delimiter `|` to separate password from message

    m, n, z = 0, 0, 0
    for i in range(len(message)):
        img[n, m, z] = d.get(message[i], 0)
        z = (z + 1) % 3
        if z == 0:
            m += 1
            if m >= img.shape[1]:
                m = 0
                n += 1
                if n >= img.shape[0]:
                    break  

    encoded_filename = "encoded_" + os.path.splitext(file.filename)[0] + ".png"
    encoded_path = os.path.join(UPLOAD_FOLDER, encoded_filename)
    cv2.imwrite(encoded_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    return render_template('index.html', message="Message encoded successfully.",
                           uploaded_image=None,  
                           encoded_image=url_for('uploaded_file', filename=encoded_filename),
                           download_link=url_for('uploaded_file', filename=encoded_filename),
                           active_tab="encrypt")

@app.route('/decode', methods=['POST'])
def decode():
    if 'file' not in request.files:
        return "No file uploaded"
    file = request.files['file']
    entered_password = request.form['password']  # Get entered password
    
    if file.filename == '':
        return "No file selected"
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    img = cv2.imread(filepath)
    if img is None:
        return "Error: Unable to read the image."
    
    c = {i: chr(i) for i in range(256)}
    
    m, n, z = 0, 0, 0
    extracted_text = ""
    
    try:
        for _ in range(100):  
            extracted_text += c.get(int(img[n, m, z]), '?')
            z = (z + 1) % 3
            if z == 0:
                m += 1
                if m >= img.shape[1]:
                    m = 0
                    n += 1
                    if n >= img.shape[0]:
                        break
    except KeyError:
        return "Error in decoding message", 400
    
    # Extract password and message
    if "|" in extracted_text:
        stored_password, decoded_message = extracted_text.split("|", 1)
    else:
        return "Error: Corrupt data or password not found", 400

    # 🔐 **Check Password Without Showing It**
    if entered_password != stored_password:
        return render_template('index.html', 
                               decoded_message="❌ Incorrect password!", 
                               active_tab="decrypt",
                               uploaded_image=None,
                               encoded_image=None)

    # ✅ **Show Only the Message (Not the Password)**
    return render_template('index.html', 
                           decoded_message=decoded_message,  # Only message is shown
                           active_tab="decrypt",
                           uploaded_image=None,
                           encoded_image=None)

if __name__ == '__main__':
    app.run(debug=True)
