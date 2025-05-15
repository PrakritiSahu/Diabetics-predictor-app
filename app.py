from flask import Flask, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import webbrowser
import threading

# ✅ Load and train the model (without SkinThickness)
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
data = pd.read_csv(url, names=cols)

data = data.drop(columns=["SkinThickness"])  # Remove SkinThickness
X = data.drop('Outcome', axis=1)
y = data['Outcome']

model = RandomForestClassifier()
model.fit(X, y)

# ✅ Save model (optional)
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# ✅ Flask App
app = Flask(__name__)

# ✅ Input Fields (renamed labels)
fields = {
    'Pregnancies': 'Number of Pregnancies',
    'Glucose': 'Glucose Level (mg/dL)',
    'BloodPressure': 'Blood Pressure (mm Hg)',
    'Insulin': 'Insulin Level (mu U/mL)',
    'BMI': 'Body Mass Index (BMI)',
    'DiabetesPedigreeFunction': 'Genetic Risk Factor',
    'Age': 'Age (years)'
}

# ✅ Updated HTML Template with CheckMySugar branding
HTML = """
<!doctype html>
<html>
<head>
    <title>CheckMySugar</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #e3f2fd, #fce4ec);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .card {{
            background: #fff;
            padding: 40px 30px;
            border-radius: 16px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }}
        h2 {{
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }}
        label {{
            font-weight: 500;
            display: block;
            margin-top: 15px;
            margin-bottom: 5px;
            color: #444;
        }}
        input[type=number] {{
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
            transition: border-color 0.2s;
        }}
        input[type=number]:focus {{
            border-color: #2196f3;
            outline: none;
        }}
        input[type=submit] {{
            width: 100%;
            padding: 12px;
            background: #2196f3;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            margin-top: 25px;
            cursor: pointer;
            transition: background 0.3s ease;
        }}
        input[type=submit]:hover {{
            background: #1976d2;
        }}
        .result {{
            margin-top: 20px;
            padding: 15px;
            text-align: center;
            border-radius: 8px;
            font-weight: bold;
            font-size: 18px;
            color: white;
            background-color: {color};
        }}
    </style>
</head>
<body>
    <div class="card">
        <h2>CheckMySugar</h2>
        <form method="post">
            {inputs}
            <input type="submit" value="Predict">
        </form>
        {result}
    </div>
</body>
</html>
"""

# ✅ Flask route
@app.route('/', methods=['GET', 'POST'])
def index():
    result_html = ""
    if request.method == 'POST':
        try:
            values = [float(request.form.get(f)) for f in fields]
            prediction = model.predict([values])[0]
            label = "🟥 Diabetic" if prediction == 1 else "🟩 Not Diabetic"
            color = "#e53935" if prediction == 1 else "#43a047"
            result_html = f'<div class="result" style="background-color:{color};">{label}</div>'
        except Exception as e:
            result_html = f'<div class="result" style="background-color:#ff9800;">Error: {e}</div>'

    inputs = "".join([
        f"<label>{label}</label><input name='{key}' type='number' step='any' required>"
        for key, label in fields.items()
    ])
    return HTML.format(inputs=inputs, result=result_html, color="#ccc")

# ✅ Open browser on start
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

# ✅ Run the app
if __name__ == '__main__':
    print("App running at: http://127.0.0.1:5000")
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True, use_reloader=False)