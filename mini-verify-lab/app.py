from flask import Flask, request
import hashlib
import qrcode
import os

app = Flask(__name__)

CERTIFICATE_FILE = "certificates/certificate_001.txt"


def calculate_file_hash(file_path):
    """Read certificate file and create SHA-256 hash."""
    with open(file_path, "rb") as file:
        file_data = file.read()
        file_hash = hashlib.sha256(file_data).hexdigest()
    return file_hash


@app.route("/")
def home():
    cert_hash = calculate_file_hash(CERTIFICATE_FILE)

    verify_url = request.host_url + "verify?hash=" + cert_hash

    # Create QR code
    qr = qrcode.make(verify_url)
    qr_path = "static/verify_qr.png"
    qr.save(qr_path)

    with open(CERTIFICATE_FILE, "r") as file:
        certificate_text = file.read()

    return f"""
    <html>
    <head>
        <title>Mini Blockchain Verify Lab</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #f4f6f8;
                padding: 30px;
            }}
            .box {{
                background: white;
                padding: 25px;
                border-radius: 10px;
                width: 700px;
                margin: auto;
                box-shadow: 0 0 10px #ccc;
            }}
            pre {{
                background: #eee;
                padding: 15px;
                border-radius: 5px;
            }}
            .hash {{
                word-break: break-all;
                color: green;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Mini Blockchain Certificate Verification</h1>

            <h2>Certificate Data</h2>
            <pre>{certificate_text}</pre>

            <h2>SHA-256 Hash</h2>
            <p class="hash">{cert_hash}</p>

            <h2>QR Code</h2>
            <p>Scan this QR code to verify the certificate.</p>
            <img src="/static/verify_qr.png" width="200">

            <h2>Verify Link</h2>
            <a href="{verify_url}">{verify_url}</a>
        </div>
    </body>
    </html>
    """


@app.route("/verify")
def verify():
    submitted_hash = request.args.get("hash")
    current_hash = calculate_file_hash(CERTIFICATE_FILE)

    if submitted_hash == current_hash:
        result = "VALID Certificate"
        color = "green"
        message = "The certificate data has not been changed."
    else:
        result = "INVALID Certificate"
        color = "red"
        message = "Warning: The certificate data may have been modified."

    return f"""
    <html>
    <head>
        <title>Verify Certificate</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #f4f6f8;
                padding: 30px;
            }}
            .box {{
                background: white;
                padding: 25px;
                border-radius: 10px;
                width: 700px;
                margin: auto;
                box-shadow: 0 0 10px #ccc;
                text-align: center;
            }}
            h1 {{
                color: {color};
            }}
            .hash {{
                word-break: break-all;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>{result}</h1>
            <p>{message}</p>

            <h3>Submitted Hash</h3>
            <p class="hash">{submitted_hash}</p>

            <h3>Current Certificate Hash</h3>
            <p class="hash">{current_hash}</p>

            <br>
            <a href="/">Back to Home</a>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
