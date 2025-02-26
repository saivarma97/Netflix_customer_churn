from flask import Flask, request, render_template
import joblib
import pandas as pd
import pickle

app = Flask(__name__)

# Load the model
model = joblib.load('model/churn_model.pkl')

# Load the scaler
#scaler = joblib.load('model/scaler.pkl')

#using pickle
scalar = pickle.load(open('scalar.pkl', 'rb'))

# Load label encoders
label_encoders = joblib.load('model/label_encoders.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from form
    data = request.form.to_dict()
    
    # Convert to DataFrame
    df = pd.DataFrame([data])
    
    # Encode categorical variables
    for column, le in label_encoders.items():
        df[column] = le.transform(df[column])
    
    # Scale numerical features
    df[numerical_features] = scalar.transform(df[numerical_features])
    
    # Make prediction
    prediction = model.predict(df)
    
    # Decode prediction
    result = 'Churn' if prediction[0] == 1 else 'No Churn'
    
    return render_template('index.html', prediction_text=f'Customer will {result}')

if __name__ == '__main__':
    app.run(debug=True)
