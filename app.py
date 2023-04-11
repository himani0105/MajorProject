from flask import Flask , render_template, request
import pickle
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
model = pickle.load(open("model_pickle.pkl", 'rb'))

app = Flask(__name__)

@app.route("/home")
def index():
    return render_template("home.html")

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        gender = request.form["gender"]
        age = int(request.form["age"])
        hypertension = (request.form["hypertension"])
        disease = int(request.form["disease"])
        married = request.form["married"]
        work = request.form["work"]
        residence = request.form["residence"]
        glucose = float(request.form["glucose"])
        bmi = float(request.form["bmi"])
        smoking = request.form["smoking"]

# HANDLING CATEGORICAL DATA
# GENDER
        if (gender == "Male"):
            gender_male = 1
            gender_other = 0
            gender_female=0
        elif (gender == "Other"):
            gender_male = 0
            gender_other = 1
            gender_female=0
        else:
            gender_male = 0
            gender_other =0 
            gender_female=1
# MARRIED
        if (married == "Yes"):
            married_yes = 1
            married_no=0
        else:
            married_yes = 0
            married_no=1
# WORK_TYPE
        if (work == 'Self-employed'):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 1
            work_type_children = 0
            work_type_Govt_job=0
        elif (work == 'Private'):
            work_type_Never_worked = 0
            work_type_Private = 1
            work_type_Self_employed = 0
            work_type_children = 0
            work_type_Govt_job=0
        elif (work == 'children'):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children = 1
            work_type_Govt_job=0
        elif (work == 'Never_worked'):
            work_type_Never_worked = 1
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children = 0
            work_type_Govt_job=0
        else:
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children = 0
            work_type_Govt_job=1
# RESIDENCE_TYPE
        if (residence == "Urban"):
            Residence_type_Urban = 1
            Residence_type_Rural=0
        else:
            Residence_type_Urban = 0
            Residence_type_Rural=1
# SMOKING_STATUS
        if (smoking == 'formerly smoked'):
            smoking_status_formerly_smoked = 1
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0
            smoking_status_Unknown=0
        elif (smoking == 'smokes'):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 1
            smoking_status_Unknown=0
        elif (smoking == 'never smoked'):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 1
            smoking_status_smokes = 0
            smoking_status_Unknown=0
        else:
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0
            smoking_status_Unknown=1

        feature =scaler.fit_transform([[age, hypertension, disease, glucose, bmi, gender_male,gender_female, gender_other, married_yes,married_no, work_type_Never_worked, work_type_Private,
                                       work_type_Self_employed, work_type_children, work_type_Govt_job,Residence_type_Urban,Residence_type_Rural, smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes,smoking_status_Unknown]])
        
        prediction = model.predict(feature)
        
        if (prediction==0):
            return render_template("nostroke.html")
        else:
            return render_template("stroke.html")
    else:
        return render_template("home.html")
 
if __name__ == " __main__":
    app.run(debug=True)
