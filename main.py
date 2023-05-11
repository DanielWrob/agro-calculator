from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from flask_wtf import FlaskForm
import chardet
from n_calculator_form import N_Calculator_Form, N_Calculator_Form_Cost
from flask_bootstrap import Bootstrap
import datetime

app = Flask(__name__)
app.config["STATIC_FOLDER"] = "static"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap(app)

current_year = datetime.datetime.now().year

nitrogen_requirements = pd.read_csv("Pobranie_N(kg_t)(4).csv", encoding='CP1250')

forecrops_category_with_nitrogen = {
    "Przyorane resztki pożniwne":
        {
        "Bobowate plon główny(czysty siew)": 30, "Bobowate międzyplon (czysty siew)": 15,
        "Bobowate plon główny(mieszanki)": 20, "Bobowate międzyplon (mieszanki)": 10

        },
    "Zielony nawóz":
        {
        "Bobowate plon główny(czysty siew) ": 65, "Bobowate międzyplon (czysty siew) ": 30, "Bobowate plon główny(mieszanki) ": 50,
        "Bobowate międzyplon (mieszanki) ": 20,
        }
    }

@app.route('/')
def home():

    return render_template('home.html')


@app.route('/agro_calc', methods=["GET", "POST"])
def agro_calculator():
    form = N_Calculator_Form()
    soil_agronomic_category = {"Bardzo lekka": 49, "Lekka": 59, "Średnia": 62, "Ciężka": 66}

    if request.method == "POST":
        if form.validate_on_submit():
            plant = request.form.get('plant')
            assumed_yield = request.form.get('assumed_yield')
            chosen_soil_category = request.form.get('chosen_soil_category')
            forecrop = request.form.get("forecrop")
            required_N_in_kg = nitrogen_requirements[nitrogen_requirements["Roślina uprawna"] == plant][
              "Pobranie N (kg na 1 tonę plonu)"]
            amount_of_nitrogen_doses = int(request.form.get("amount_of_nitrogen_doses"))

            forecrop_nitrogen = 0

            for key, value in forecrops_category_with_nitrogen.items():
                for sub_key, sub_value in value.items():
                    if sub_key == forecrop:
                        forecrop_nitrogen = sub_value

            required_N_per_h = round((float(required_N_in_kg) * float(assumed_yield)) - soil_agronomic_category[
                chosen_soil_category] - float(forecrop_nitrogen), 2)

            print(type(amount_of_nitrogen_doses))
            print(amount_of_nitrogen_doses)

            first_dose = None
            second_dose = None
            third_dose = None

            if amount_of_nitrogen_doses == 2:
                first_dose = round(required_N_per_h * 0.6, 2)
                second_dose = round(required_N_per_h * 0.4, 2)
            elif amount_of_nitrogen_doses == 3:
                first_dose = round(required_N_per_h * 0.4, 2)
                second_dose = round(required_N_per_h * 0.4, 2)
                third_dose = round(required_N_per_h * 0.2, 2)

            return redirect(url_for("n_required", required_N_per_h=required_N_per_h, first_dose=first_dose,
                                   second_dose=second_dose, third_dose=third_dose))

            # return n_required(required_N_per_h, first_dose, second_dose, third_dose)
    else:
        return render_template("agro_calc.html", form=form)


@app.route('/agro_calc/N_required.html', methods=["GET", "POST"])
def n_required():
    required_N_per_h = request.args.get('required_N_per_h')
    first_dose = request.args.get('first_dose')
    second_dose = request.args.get('second_dose')
    third_dose = request.args.get('third_dose')
    form = N_Calculator_Form_Cost()

    if request.method == "POST":
        if form.validate_on_submit():
            cultivation_area = request.form.get("cultivation_area")
            print(f" jajco kultywationsz area{cultivation_area}")

    print(f" jajco kultywationsz area")
    return render_template('N_required.html', N_per_h=required_N_per_h, first_dose=first_dose, second_dose=second_dose, third_dose=third_dose, form=form)


if __name__ == '__main__':
    app.run(debug=True)

