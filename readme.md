# Image Steganography

## 📌 Overview
This project implements **Image Steganography** using **Flask and OpenCV**. It allows users to:
- **Encrypt** a secret message into an image with a password.
- **Decrypt** the message from the encoded image using the correct password.

## 🚀 Features
- Upload an image and hide a secret message inside it.
- Password protection for encryption and decryption.
- View and download the encoded image.
- Extract and display the hidden message from the image.
- Simple web interface using **Flask** and **Bootstrap**.

## 🛠 Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo/image-steganography.git
cd image-steganography
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Run the Flask Application**
```sh
python stego.py
```

The application will start on **http://127.0.0.1:5000**

## 🎨 Web Interface

The interface consists of two main tabs:

### **1️⃣ Encrypt Tab**
- Select an image to upload.
- Enter a secret message.
- Provide a password for encryption.
- Click **Encrypt** to hide the message.
- Download the encoded image.

### **2️⃣ Decrypt Tab**
- Upload the encoded image.
- Enter the correct password.
- Click **Decrypt** to reveal the hidden message.

## 📜 Project Structure
```
image-steganography/
│── templates/
│   ├── index.html      # Web Interface (Bootstrap-based)
│── uploads/            # Stores uploaded & encoded images
│── stego.py            # Main Flask application
│── requirements.txt    # Python dependencies
│── README.md           # Documentation
```

## 🔧 Dependencies
- **Flask** (for web interface)
- **OpenCV (cv2)** (for image processing)
- **NumPy** (for efficient image handling)
- **Bootstrap** (for styling the interface)

## 🔐 Security Note
- This implementation is a basic proof of concept and **not suitable for high-security encryption**.
- Avoid using sensitive data in the messages, as simple pixel manipulation is reversible.

---
**Happy Coding! 🎯**

