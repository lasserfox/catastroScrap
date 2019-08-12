
from pycatastro import PyCatastro as catas
import json,pprint

#print(catas.ConsultaProvincia())
#print(catas.Consulta_DNPLOC(provincia='MADRID',municipio='PARACUELLOS DE JARAMA',sigla='CALLE',calle='CAMILO JOSE CELA',numero='7',planta='3', puerta='C'))
# print (json.dumps(catas.ConsultaNumero(provincia='madrid',municipio='paracuellos de jarama',tipovia='cl',nombrevia='camilo jose cela',numero='7')))
prov='MADRID'
munic='PARACUELLOS DE JARAMA'
calle='camilo jose cela'
nro = 7
planta = 2
puerta = 'a'

try:
    data_calle = json.loads(json.dumps(catas.ConsultaVia(provincia=prov,municipio=munic,nombrevia=calle)))
    cod_post=data_calle['consulta_callejero']['callejero']['calle']['loine']['cp']
    cod_munic=data_calle['consulta_callejero']['callejero']['calle']['loine']['cm']
    tipo_via=data_calle['consulta_callejero']['callejero']['calle']['dir']['tv']
    nnombre_via= data_calle['consulta_callejero']['callejero']['calle']['dir']['nv']
    cod_via =data_calle['consulta_callejero']['callejero']['calle']['dir']['cv']

    result=json.loads(json.dumps(catas.Consulta_DNPLOC(provincia=prov,municipio=munic,sigla=tipo_via,calle=calle,numero=nro,planta=planta,puerta=puerta)))
    ref = str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['pc1'])+str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['pc2'])+str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['car'])+str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['cc1'])+str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['cc2'])
    print (ref)
except Exception as e:
    print ('NO EXISTE NINGÚN INMUEBLE CON LOS PARÁMETROS INDICADOS')