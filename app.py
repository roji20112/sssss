from flask import Flask, request, render_template_string
import subprocess
import sys
import tempfile
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Python Runner</title>
<style>
body {
    background:#111;
    color:white;
    font-family:Arial;
    margin:0;
    padding:20px;
}
.container {
    max-width:700px;
    margin:auto;
    background:#1d1d1d;
    padding:20px;
    border-radius:15px;
}
input, textarea, button {
    width:100%;
    box-sizing:border-box;
    margin-top:12px;
    padding:13px;
    border-radius:10px;
    border:0;
}
button {
    background:#00c853;
    color:white;
    font-size:17px;
    font-weight:bold;
}
textarea {
    height:250px;
    background:#000;
    color:#00ff66;
    direction:ltr;
    text-align:left;
}
pre {
    background:#000;
    color:#00ff66;
    padding:15px;
    border-radius:10px;
    white-space:pre-wrap;
    direction:ltr;
    text-align:left;
}
</style>
</head>

<body>
<div class="container">

<h2>🐍 Python Runner</h2>

<form method="POST" enctype="multipart/form-data">

<input type="file" name="file" accept=".py" required>

<textarea name="input" placeholder="اكتب الردود التي يحتاجها البرنامج، كل رد في سطر..."></textarea>

<button type="submit">▶️ تشغيل Python</button>

</form>

{% if result %}
<h3>📤 النتيجة:</h3>
<pre>{{ result }}</pre>
{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        uploaded = request.files.get("file")
        user_input = request.form.get("input", "")

        if not uploaded:
            return render_template_string(
                HTML,
                result="❌ لم يتم اختيار ملف"
            )

        if not uploaded.filename.endswith(".py"):
            return render_template_string(
                HTML,
                result="❌ يجب رفع ملف Python بصيغة .py"
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".py"
        ) as temp:

            uploaded.save(temp.name)
            file_path = temp.name

        try:

            process = subprocess.run(
                [sys.executable, file_path],
                input=user_input,
                text=True,
                capture_output=True,
                timeout=30
            )

            result = process.stdout

            if process.stderr:
                result += "\n\n❌ ERROR:\n" + process.stderr

        except subprocess.TimeoutExpired:
            result = "⏱️ توقف البرنامج لأنه تجاوز 30 ثانية."

        except Exception as e:
            result = "❌ خطأ:\n" + str(e)

        finally:
            try:
                os.remove(file_path)
            except:
                pass

    return render_template_string(
        HTML,
        result=result
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )