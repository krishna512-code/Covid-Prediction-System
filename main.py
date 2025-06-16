from flask import Flask, render_template, request, flash, redirect, url_for
import pickle
import os
import numpy as np

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your-secret-key-here'  # Required for flash messages

def load_model():
    try:
        with open('model.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        flash('Model file not found. Please train the model first.', 'error')
        return None
    except Exception as e:
        flash(f'Error loading model: {str(e)}', 'error')
        return None

def validate_input(fever, age, pain, runny_nose, diff_breath):
    try:
        fever = int(fever)
        age = int(age)
        pain = int(pain)
        runny_nose = int(runny_nose)
        diff_breath = int(diff_breath)
        
        if not (0 <= fever <= 1):
            return False, "Fever must be 0 or 1"
        if not (0 <= age <= 100):
            return False, "Age must be between 0 and 100"
        if not (0 <= pain <= 1):
            return False, "Pain must be 0 or 1"
        if not (0 <= runny_nose <= 1):
            return False, "Runny nose must be 0 or 1"
        if not (0 <= diff_breath <= 1):
            return False, "Breathing difficulty must be 0 or 1"
            
        return True, None
    except ValueError:
        return False, "All inputs must be numbers"

def assess_risk(features, probability):
    fever, age, pain, runny_nose, diff_breath = features[0]
    
    # Count number of symptoms
    symptom_count = sum([fever, pain, runny_nose, diff_breath])
    
    # Adjust probability based on symptoms and age
    adjusted_probability = probability
    
    # Increase probability based on number of symptoms
    if symptom_count == 4:  # All symptoms present
        adjusted_probability = min(probability + 50, 100)  # Add 50% but cap at 100%
    elif symptom_count == 3:
        adjusted_probability = min(probability + 40, 100)  # Add 40% but cap at 100%
    elif symptom_count == 2:
        adjusted_probability = min(probability + 30, 100)  # Add 30% but cap at 100%
    
    # Increase probability based on age
    if age >= 60:
        adjusted_probability = min(adjusted_probability + 25, 100)  # Add 25% for elderly
    elif age >= 40:
        adjusted_probability = min(adjusted_probability + 20, 100)  # Add 20% for middle-aged
    elif age >= 25:
        adjusted_probability = min(adjusted_probability + 15, 100)  # Add 15% for age 25+
    
    # Determine risk level based on adjusted probability
    risk_level = "LOW"
    if adjusted_probability >= 50:  # Lowered threshold for high risk
        risk_level = "HIGH"
    elif adjusted_probability >= 30:
        risk_level = "MODERATE"
    
    # Additional risk factors
    risk_factors = []
    recommendations = []
    
    # Age-based risk
    if age >= 60:
        risk_factors.append("Advanced age (60+) - Higher risk of severe complications")
        recommendations.append("Take extra precautions and monitor symptoms closely")
    elif age >= 40:
        risk_factors.append("Middle age (40+) - Moderate risk of complications")
        recommendations.append("Monitor symptoms and maintain social distance")
    elif age >= 25:
        risk_factors.append("Adult age (25+) - Increased risk with multiple symptoms")
        recommendations.append("Monitor symptoms and maintain social distance")
    
    # Symptom combinations
    if symptom_count == 4:
        risk_factors.append("All symptoms present - High risk combination")
        recommendations.append("Seek immediate medical attention and get tested")
    elif symptom_count == 3:
        risk_factors.append(f"Multiple symptoms ({symptom_count} symptoms present) - Significant risk")
        recommendations.append("Seek medical attention and get tested")
    
    if fever and diff_breath:
        risk_factors.append("Fever with breathing difficulty - Critical combination")
        recommendations.append("Seek immediate medical attention")
    elif fever and pain:
        risk_factors.append("Fever with body pain - Common COVID-19 symptoms")
        recommendations.append("Monitor temperature and rest well")
    
    if diff_breath:
        risk_factors.append("Breathing difficulty - Serious symptom")
        recommendations.append("Seek medical attention if breathing worsens")
    
    if fever:
        risk_factors.append("Fever - Primary COVID-19 symptom")
        recommendations.append("Monitor temperature regularly")
    
    # Additional recommendations based on risk level
    if risk_level == "HIGH":
        recommendations.append("Self-isolate immediately and contact healthcare provider")
        recommendations.append("Get tested for COVID-19 as soon as possible")
        if symptom_count >= 3:
            recommendations.append("Consider emergency medical care if symptoms worsen")
    elif risk_level == "MODERATE":
        recommendations.append("Monitor symptoms and maintain social distance")
        recommendations.append("Consider getting tested if symptoms persist")
    else:
        recommendations.append("Continue following preventive measures")
        recommendations.append("Monitor for any new symptoms")
    
    return {
        'risk_level': risk_level,
        'probability': adjusted_probability,
        'risk_factors': risk_factors,
        'recommendations': recommendations
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        fever = request.form.get('fever')
        age = request.form.get('age')
        pain = request.form.get('pain')
        runny_nose = request.form.get('runnyNose')
        diff_breath = request.form.get('diffBreath')
        
        # Validate inputs
        is_valid, error_msg = validate_input(fever, age, pain, runny_nose, diff_breath)
        if not is_valid:
            flash(error_msg, 'error')
            return redirect(url_for('index'))
        
        # Load model
        model = load_model()
        if model is None:
            return redirect(url_for('index'))
        
        try:
            # Convert inputs to integers
            features = np.array([[
                int(fever),
                int(age),
                int(pain),
                int(runny_nose),
                int(diff_breath)
            ]], dtype=np.int64)
            
            # Make prediction
            probability = model.predict_proba(features)[0][1]
            
            # Convert probability to percentage
            inf_prob = round(probability * 100)
            
            # Get detailed risk assessment
            assessment = assess_risk(features, inf_prob)
            
            # Render result template
            return render_template('Backend.html', 
                                inf=assessment['probability'],
                                risk_level=assessment['risk_level'],
                                risk_factors=assessment['risk_factors'],
                                recommendations=assessment['recommendations'])
            
        except Exception as e:
            flash(f'Error making prediction: {str(e)}', 'error')
            return redirect(url_for('index'))
        
    return render_template('Frontend.html')

@app.route('/backend')
def backend():
    return render_template('Backend.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
      