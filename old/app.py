from flask import Flask, render_template, jsonify, request, send_file, abort
import os

app = Flask(__name__)
OUTPUT_DIR = os.path.expanduser("output")


@app.route("/")
def index():
    file_data = {}
    
    for domain in os.listdir(OUTPUT_DIR):
        domain_path = os.path.join(OUTPUT_DIR, domain)
        if os.path.isdir(domain_path):
            files = [f for f in os.listdir(domain_path) if os.path.isfile(os.path.join(domain_path, f))]
            file_data[domain] = files
    return render_template("index.html", files=file_data)


@app.route("/files_list")
def list_files():
    result = {}
    for domain in os.listdir(OUTPUT_DIR):
        domain_path = os.path.join(OUTPUT_DIR, domain)
        if os.path.isdir(domain_path):
            files = [f for f in os.listdir(domain_path) if os.path.isfile(os.path.join(domain_path, f))]
            result[domain] = files
    return jsonify(result)


@app.route("/file_content")
def get_file():
    domain = request.args.get("domain")
    filename = request.args.get("file")

    if not domain or not filename:
        return abort(400, description="Missing domain or file")

    file_path = os.path.join(OUTPUT_DIR, domain, filename)

    if not os.path.isfile(file_path):
        return abort(404, description="File not found")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return content


if __name__ == "__main__":
    app.run(debug=True)
