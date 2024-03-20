from flask import Flask, render_template, request, jsonify, redirect, url_for
import pickle

app = Flask(__name__)

# Load the trained model and label encoder
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('label_encoder.pkl', 'rb') as file:
    le = pickle.load(file)

reports_database = { "Diabetes" : "HbA1C Test, Postprandial Sugar Test, FBST", 
                        "Maleria" : "Complete Blood Count Test, Malaria PCR", 
                        "Dengue" : "Complete Blood Count Test, (if platet count very low then NS1 Test and IgM/IgG Test)", 
                        "Typhoid" : "Widal Test, IgM/IgG Test", 
                        "Pyrexia of Unknown Origin" : "Complete Blood Count Test, IgM/IgG Test", 
                        "Chikungunya" : "IgM/IgG Test, RT-PCR", 
                        "Hepatitis A/B/D/E" : "Hepatitis Serology Test, Bilirubin Test", 
                        "Hepatitis C" : "Hepatitis Serology Test, Bilirubin Test", 
                        "Coronary Artey Disease" : "Electrocardiogram Test, 2D Echocardiography Test, Angiography", 
                        "High Blood Pressure" : "Oxymeter, Sphygmomanometer", 
                        "Jaundice" : "Bilirubin Test", 
                        "Fatty Liver Disease" : "Liver function Tests, Abdominal Ultrasound", 
                        "High Chloesterol" : "VLDL Test, HDL Test", 
                        "Sirosis of Liver" : "FibroScan", 
                        "Gall Stones" : "Abdominal Ultrasound, Abdominal Solid Mass CT Scan", 
                        "Cholera" : "Cholera RDT", 
                        "Diarrhea" : "Complete Blood Count Test, Stool Test", 
                        "Dysentry" : "Stool Test", 
                        "Kidney Stones" : "Abdominal Ultrasound", 
                        "Thyroid" : "Thyroid Stimulating Hormone Test", 
                        "Oseteoporosis" : "Calcium Test", 
                        "Arthritis" : "Anti-CCP Antibody Test", 
                        "Sinusitis" : "Sinus X-Ray, Sinus CT Scan", 
                        "Migraine" : "Brain CT Scan", 
                        "Food Poisoning" : "Stool Test", 
                        "Insomnia" : "Polysomnography(Sleep Study)"}

symptom_dict = {
            "Urge to Urinate at Night": 0, 
            "Craving Sweet Items": 1, 
            "Weight Loss": 2,
            "Chills": 3, 
            "Weakness": 4, 
            "Bleeding Tendencies": 5, 
            "Dizziness": 6,
            "Exhaustion": 7, 
            "Body Pain": 8, 
            "Joint Pain": 9, 
            "Yellowing of Skin": 10,
            "Yellowing of Sclera": 11, 
            "Anorexia": 12, 
            "Indigestion": 13, 
            "Nausea": 14,
            "Clay-Colored Stool": 15, 
            "Numbness": 16, 
            "Chest Pain": 17, 
            "Heart Attack": 18,
            "Anxiety": 19, 
            "Intense Sweating": 20, 
            "Dysphagia": 21, 
            "Redness of Sclera": 22,
            "Edema": 23, 
            "Fatigue": 24, 
            "Barfing": 25, 
            "Constipation": 26, 
            "Watery Stools": 27,
            "Dyspnea": 28, 
            "Emesis": 29, 
            "Weight Gain": 30, 
            "Abdominal Pain": 31,
            "Pain that radiates to the lower abdomen and groin": 32,
            "Pain or burning sensation while urinating": 33, 
            "Hairfall": 34,
            "Brittle Teeth": 35, 
            "Knocking Sound from Joints": 36, 
            "Swollen Joints": 37,
            "Headaches": 38, 
            "Stuffy Nose": 39, 
            "Constant Cold": 40,
            "Difficult Falling Asleep at Night": 41, 
            "Blood in Stools": 42
        }

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/templates/one.html')
def one():
    return render_template('one.html')

@app.route("/test")
def test():
    return redirect(url_for("one"))

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the request is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 400
    
    # Get JSON data from request
    data = request.json
    symptoms = data.get('symptoms', [])
    fever = data.get('fever', None)
    
    print(symptoms,fever)

    # Convert fever to float (if present)
    fever_value = float(fever) if fever else None

    # Initialize a binary array for fever
    b = [0] * 24

    # Handle fever logic
    if fever_value:
        fever *= 10  # Convert fever to match the logic in your code
        if fever >= 987 and fever <= 990:
            fever = 986
        elif fever > 1036:
            fever = 1036
        elif fever < 986:
            fever = 986
        else:
            fever = fever

        if (fever % 2) == 0:
            fever = fever
        else:
            fever = fever + 1

        if fever == 986:
            b[0] = 1
        elif 992 <= fever <= 1036:
            b[int((fever - 991)/2) + 1] = 1

    # Initialize a binary array for symptoms
    c = [0] * 43

    for symptom in symptoms:
        if symptom in symptom_dict:
            #print(symptom)
            c[symptom_dict[symptom]] = 1

    symptoms_vector = b + c

    predicted_disease = le.inverse_transform(model.predict([symptoms_vector]))[0]
    suggested_tests = reports_database.get(predicted_disease, "No tests found")
    
    #print(predicted_disease)
    #print(suggested_tests)

    return jsonify({'predicted_disease': predicted_disease, 'suggested_tests': suggested_tests})



if __name__ == '__main__':
    app.run(debug=True)