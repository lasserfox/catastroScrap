import json


db_ciudad = json.load(open("cp-ciudad.json"))
db_municipio = json.load(open("cp-dic-2018.json"))

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ü", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def fillCPMunicipios():
    municipios={}
    with open('/home/e049773/Downloads/codigosdic-2018/codpostal-dic-2018') as f:
        data = f.readlines()
        for line in data:
            municipios[str(line.split(':')[0])] = str(line.split(':')[1]).strip()
    with open('cp-dic-2018.json', 'w') as file:
        file.write(json.dumps(municipios,ensure_ascii=False))
    return( json.dumps(municipios))

def fillCPProvincias():
    ciudad={}
    with open('/home/e049773/Downloads/codigosdic-2018/codciu.txt') as f:
        data = f.readlines()
        for line in data:
            print ("cod:",str(line)[0:3] , "ciudad:",str(line)[3:-1] )
            ciudad[str(line)[0:3]] = str(line)[3:-1]

    with open('cp-ciudad.json', 'w') as file:
        file.write(json.dumps(ciudad,ensure_ascii=False))

    return(json.dumps(ciudad))

def getProvincia(cp):
    try:
        nombreCiudad = str(db_ciudad[cp]).upper()
        return nombreCiudad
    except Exception as e:
        return None

