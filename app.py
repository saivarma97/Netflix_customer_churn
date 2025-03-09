from flask import Flask, request, render_template
import joblib
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
model = joblib.load('model.pkl')

# Load the scaler properly
with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)  # ✅ Corrected variable name

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features from form
        features = [float(x) for x in request.form.values()]
        final_features = np.array(features).reshape(1, -1)
        final_features = scaler.transform(final_features)  # ✅ Use 'scaler' instead of 'scalar'
        prediction = model.predict(final_features)
        output = 'Churn' if prediction[0] == 1 else 'Not Churn'
    except Exception as e:
        output = f"Error: {str(e)}"
    return render_template('index.html', prediction_text=f'Customer will {output}')

if __name__ == '__main__':
    app.run(debug=True)
