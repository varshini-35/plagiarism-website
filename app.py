from flask import Flask, render_template, request, redirect, url_for
from ocr import extract_text_from_image
from plagiarism import check_plagiarism_online
from PIL import Image

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("file")
    text_input = request.form.get("text")

    text1 = ""

    # OCR for image
    if uploaded_file and uploaded_file.filename != "":
        try:
            img = Image.open(uploaded_file.stream)
            text1 = extract_text_from_image(img).strip()
        except Exception as e:
            return f"OCR Error: {e}"
    else:
        text1 = text_input.strip() if text_input else ""

    if text1 == "":
        return "Please upload an image or enter some text!"

    percent, source = check_plagiarism_online(text1)

    # ✅ REDIRECT instead of rendering directly
    return redirect(url_for(
        "result",
        text=text1,
        percent=percent,
        source=source
    ))

@app.route("/result")
def result():
    text = request.args.get("text")
    percent = request.args.get("percent")
    source = request.args.get("source")

    return render_template(
        "result.html",
        text=text,
        percent=percent,
        source=source
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

