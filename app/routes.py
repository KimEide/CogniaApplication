from flask import render_template
from app.backendAPI import find_parking_areas, find_rest_area
from app import app

@app.route('/')
def index():
    title = 'Home'

    return render_template('webpage/index.html', title=title)

@app.route('/restAreaWater')
def display_parking():
    title = 'Rasteplass med drikkevann'
    return render_template('webpage/displayWater.html', title=title)

@app.route('/restAreaShower')
def display_rest_area_shower():
    title = 'Rasteplass med dusj'
    return render_template('webpage/displayShowers.html', title=title)

@app.route('/restAreaElecticity')
def rest_area_electricity():
    title = 'Rasteplass med strøm'
    return render_template('webpage/displayElectricity.html', title=title)

@app.route('/updateRestAreas')
def updateRestArea():
    find_rest_area()
    return index()

@app.route('/updateParking')
def updateParking():
    find_parking_areas()
    return index()