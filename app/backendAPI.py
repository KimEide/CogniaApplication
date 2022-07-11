import requests

from app import db
from app.models import RestAreas, Dusj, Drikkevann, Strøm, Parkeringsområde, Parkeringstilbyder

def retrieve_data(url):
    r = requests.get(url)

    return r.json()

def addRestArea(id, name, numSmallVehicle, numBigVehicle, lokasjon, href):
    restArea = RestAreas(id= id, name=name, num_small_vehicle=numSmallVehicle, num_big_vehicle=numBigVehicle, lokasjon=lokasjon, href=href)
    db.session.add(restArea)
    db.session.commit()

def addParkingsområde(id, parkeringstilbyderNavn, breddegrad, lengdegrad, deaktivert, versjonsnummer, navn, adresse, postnummer, poststed, aktiveringsTidspunkt):
    parkeringsområde = Parkeringsområde(id=id, parkeringstilbyderNavn=parkeringstilbyderNavn, breddegrad=breddegrad, lengdegrad=lengdegrad, deaktivert=deaktivert, 
        versjonsnumber=versjonsnummer, navn=navn, adresse=adresse, postnummer=postnummer, poststed=poststed, aktiveringsTidspunkt=aktiveringsTidspunkt)

    db.session.add(parkeringsområde)
    db.session.commit()

def addParkeringstilbyder(id, organisasjonsnummer, navn):
    parkeringstilbyder = Parkeringstilbyder(id=id, organisasjonsnummer=organisasjonsnummer, navn=navn)
    db.session.add(parkeringstilbyder)
    db.session.commit()

def read_rest_area_details(restAreas):
    for restArea in restAreas:
        restAreaDetails = retrieve_data(restArea['href'])
        
        # Resetter verdier mellom rasteplassene
        navn = ""
        numSmallVehicle = 0
        numBigVehicle = 0
        lokasjon = ""

        if 'lokasjon' in restArea:
            lokasjon = restArea['lokasjon']

        for info in restAreaDetails['egenskaper']:
            
            # Finner navnet på rasteplassen
            if info['id'] == 1074:
                navn = info['verdi']
            # Finner antall parkeringsplasser for små kjøretøy
            if info['id'] == 1805:
                numSmallVehicle = int(info['verdi'])

            # Finner antall parkeringsplasser for store kjøretøy
            if info['id'] == 1816:
                numBigVehicle = int(info['verdi'])

            # Leser om det er tabel for dusj, og begge typer dusj som kan være på rasteplass og legger til i databasen
            if  info['id'] == 9418:
                if info['enum_id'] == 13264 or info['enum_id'] == 13265:
                    dusj = Dusj(id=restAreaDetails['id'], href=restAreaDetails['href'])
                    db.session.add(dusj)
                    db.session.commit()

            # Leser om det er strøm uttak på rasteplassen og legger til i databasen
            if info['id'] == 9419 and info['enum_id'] == 13267:
                strøm = Strøm(id=restAreaDetails['id'], href=restAreaDetails['href'])
                db.session.add(strøm)
                db.session.commit()

            # Leser om det er drikkevann på rasteplassen og legger til i databasen
            if info['id'] == 9417 and info['enum_id'] == 13262:
                drikkevann = Drikkevann(id=restAreaDetails['id'], href=restAreaDetails['href'])
                db.session.add(drikkevann)
                db.session.commit()

        addRestArea(restArea['id'], navn, numSmallVehicle, numBigVehicle, lokasjon, restArea['href'])


def find_rest_area_shower_rec(url):
    allRestAreas = retrieve_data(url)
    read_rest_area_details(allRestAreas['objekter'])
    print(allRestAreas['metadata'])

    if allRestAreas['metadata']['returnert'] > 0:
        find_rest_area_shower_rec(allRestAreas['metadata']['neste']['href'])
    else:
        return 

def find_rest_area():
    # Rest area ID is 39 from Vegvesenet
    # Rasteplass doc - http://labs.vegdata.no/nvdb-datakatalog/39-Rasteplass/
    allRestAreas = read_data_from_vegvesen(39)

    # Henter ut en liste over 
    find_rest_area_shower_rec(allRestAreas)
    
def read_data_from_vegvesen(objectId):
    url = 'https://nvdbapiles-v2.atlas.vegvesen.no/vegobjekter/{}'.format(objectId)
    return url

def find_parking_areas():
    url = 'https://www.vegvesen.no/ws/no/vegvesen/veg/parkeringsomraade/parkeringsregisteret/v1/'

    parkeringAreas = retrieve_data(url)

    parkeringsområdeURL = parkeringAreas[0]['href']
    parkeringsområde = retrieve_data(parkeringsområdeURL)

    for parkering in parkeringsområde:
        addParkingsområde(parkering['id'], parkering['parkeringstilbyderNavn'], parkering['breddegrad'], parkering['lengdegrad'], parkering['deaktivert'], parkering['versjonsnummer'], parkering['navn'], parkering['adresse'], parkering['postnummer'], parkering['poststed'], parkering['aktiverinpoststedgstidspunkt'])

    parkeringstilbyderURL = parkeringAreas[1]['href']
    parkeringstilbyder = retrieve_data(parkeringstilbyderURL)

    for parkering in parkeringstilbyder:
        addParkeringstilbyder(parkering['id'], parkering['organisasjonsnummer'], parkering['navn'])