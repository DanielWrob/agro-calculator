from flask import Flask, render_template
import pandas as pd
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, SelectField, DecimalField, HiddenField

nitrogen_requirements = pd.read_csv("Pobranie_N(kg_t)(4).csv", encoding='CP1250')

N_Fertilizares = pd.read_csv("zawartosc_N_w_nawozach_%.csv", encoding='CP1250')
soil_agronomic_category = ["Bardzo lekka", "Lekka", "Średnia", "Ciężka"]

######################### osuzkane ze spacja ####################3333

forecrops_category2 = {
    "Brak": ["Brak Przedplonu"],
    "Przyorane resztki pożniwne":
        [
        "Bobowate plon główny(czysty siew)", "Bobowate międzyplon (czysty siew)", "Bobowate plon główny(mieszanki)", "Bobowate międzyplon (mieszanki)"],
    "Zielony nawóz":
        [
            "Bobowate plon główny(czysty siew) ", "Bobowate międzyplon (czysty siew) ", "Bobowate plon główny(mieszanki) ",
            "Bobowate międzyplon (mieszanki) "]
    }

class N_Calculator_Form(FlaskForm):

    plants = nitrogen_requirements["Roślina uprawna"]
    plant = SelectField("Uprawa", choices=[plant for plant in plants], validators=[DataRequired()])
    assumed_yield = DecimalField("Zakładany Plon w tonach", places=2, validators=[DataRequired()])
    chosen_soil_category = SelectField("Rodzaj gleby", choices=[soil for soil in soil_agronomic_category], validators=[DataRequired()])
    forecrop = SelectField("Przedplon", choices=forecrops_category2, validators=[DataRequired()])
    amount_of_nitrogen_doses = SelectField("Ilość dawek N", choices=[2, 3], validators=[DataRequired()])

    submit = SubmitField("Oblicz")


class N_Calculator_Form_Cost(FlaskForm):

    cultivation_area = DecimalField("Zakładana powierzchnia urpawy w hektarach", places=2, validators=[DataRequired()])

    submit = SubmitField("Oblicz")