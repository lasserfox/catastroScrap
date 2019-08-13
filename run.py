import pandas as pd, helper, webbrowser, time
from datetime import datetime
from pycatastro import PyCatastro as catas
import json, pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



import threading

# print(catas.ConsultaProvincia())
# print(catas.Consulta_DNPLOC(provincia='MADRID',municipio='PARACUELLOS DE JARAMA',sigla='CALLE',calle='CAMILO JOSE CELA',numero='7',planta='3', puerta='C'))
# print (json.dumps(catas.ConsultaNumero(provincia='madrid',municipio='paracuellos de jarama',tipovia='cl',nombrevia='camilo jose cela',numero='7')))
OPENWEBONFAIL = True
FIRSTPAGE = True
SLEEP = 2
file = 'test.xlsx'
xl = pd.ExcelFile(file)

writer = pd.ExcelWriter('example.xlsx', engine='xlsxwriter')

from xlwt import Workbook
wb = Workbook()
sheet1 = wb.add_sheet('Script_Cat')


start = datetime.now()
time.sleep(1)
print ("Prueba:",datetime.now()-start)


from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

df1 = xl.parse('Script_Cat')
df = pd.DataFrame()




for i, row in enumerate(df1.values):
    print(i)

    codpost_ciudad = '{:02}'.format(int(str(row[10]).replace('<sp>', ' ').split('.')[0]))
    prov = helper.normalize(helper.getProvincia(codpost_ciudad + '0'))
    if prov is None:
        raise Exception('12', '-', 'LA PROVINCIA NO EXISTE')
    munic = helper.normalize (str(row[11]).replace('<sp>', ' '))
    calle = helper.normalize(str(row[12]).replace('<sp>', ' '))
    num = int(float(str(row[13]).replace('<sp>', ' ')))
    puerta = str(row[14]).replace('<sp>', ' ')
    piso = str(row[15]).replace('<sp>', ' ')

    try:
        datos_munic = catas.ConsultaMunicipio(provincia=prov, municipio=munic)
        data_calle = json.loads(json.dumps(catas.ConsultaVia(provincia=prov, municipio=munic, nombrevia=calle)))
        if (i == 48):
            print(i)
        cod_post = data_calle['consulta_callejero']['callejero']['calle']['loine']['cp']
        cod_munic = data_calle['consulta_callejero']['callejero']['calle']['loine']['cm']
        tipo_via = data_calle['consulta_callejero']['callejero']['calle']['dir']['tv']
        nombre_via = data_calle['consulta_callejero']['callejero']['calle']['dir']['nv']
        cod_via = data_calle['consulta_callejero']['callejero']['calle']['dir']['cv']


        result = json.loads(json.dumps(catas.Consulta_DNPLOC(provincia=prov, municipio=munic, sigla=tipo_via, calle=calle, numero=num, planta=piso, puerta=puerta)))
        try:
            ref = str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['pc1']) + str(
            result['consulta_dnp']['bico']['bi']['idbi']['rc']['pc2']) + str(
            result['consulta_dnp']['bico']['bi']['idbi']['rc']['car']) + str(
            result['consulta_dnp']['bico']['bi']['idbi']['rc']['cc1']) + str(
            result['consulta_dnp']['bico']['bi']['idbi']['rc']['cc2'])
        except Exception as e:
            data_calle['consulta_callejero'] = result['consulta_dnp']

            raise
        print(ref)
    except Exception as e:
        try:
            cod_error = data_calle['consulta_callejero']['lerr']['err']['cod']
            desc_error = data_calle['consulta_callejero']['lerr']['err']['des']
            row[8]=cod_error
            row[9]=desc_error

            for col,val in enumerate(row):
                sheet1.write(i, col, val)

            wb.save('example.xlsx')


            if OPENWEBONFAIL:
                if FIRSTPAGE :
                    driver = webdriver.Chrome()
                    FIRSTPAGE=False
                else:
                    driver.execute_script("window.open('');")
                    time.sleep(SLEEP)
                    Window_List = driver.window_handles
                    driver.switch_to.window(Window_List[-1])

                # driver.get("https://www1.sedecatastro.gob.es/Cartografia/mapa.aspx?buscar=S")
                driver.implicitly_wait(5)
                driver.get("https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCBusqueda.aspx?")
                # wait = WebDriverWait(driver, 10)

                driver.find_element_by_link_text("CALLE/NÚMERO").click()
                driver.find_element_by_id("ctl00_Contenido_provinceSelector").send_keys(prov)
                time.sleep(SLEEP)
                driver.find_element_by_id("ctl00_Contenido_provinceSelector").send_keys(Keys.TAB)
                driver.find_element_by_id("ctl00_Contenido_municipioSelector").send_keys(munic)
                time.sleep(SLEEP)
                driver.find_element_by_id("ctl00_Contenido_municipioSelector").send_keys(Keys.TAB)
                driver.find_element_by_id("ctl00_Contenido_viaSelector").send_keys(calle)
                # time.sleep(1)
                driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Vía'])[1]/following::i[1]").click()
                # time.sleep(1)
                # driver.find_element_by_id("ctl00_Contenido_txtTodasVias").click()
                time.sleep(SLEEP)
                driver.find_element_by_id("ctl00_Contenido_txtTodasVias").send_keys(str(calle).split(" ")[-1])
                time.sleep(SLEEP+1)
                driver.find_element_by_id("ctl00_Contenido_txtTodasVias").send_keys(Keys.TAB)
                try:
                    element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "AddVia")))
                except Exception as e:
                    continue

                driver.find_element_by_id("AddVia").click()


                element = WebDriverWait(driver, 3600).until(EC.element_to_be_clickable((By.ID, "ctl00_Contenido_txtNum")))
                driver.find_element_by_id("ctl00_Contenido_txtNum").send_keys(num)
                time.sleep(SLEEP)
                driver.find_element_by_id("ctl00_Contenido_btnDatos").click()
                driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Vía'])[1]/following::i[1]").click()

                # driver.find_element_by_id("ctl00_Contenido_btnNuevaCartografia").click()
                # driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Vía'])[1]/following::i[1]").click()
                # driver.find_element_by_id("ctl00_Contenido_Label12").click()
                # driver.find_element_by_id("ctl00_Contenido_txtNum").click()
                # driver.find_element_by_id("ctl00_Contenido_txtNum").clear()

                # driver.find_eleme nt_by_id("ctl00_Contenido_viaSelector").send_keys(Keys.TAB)
                # input("Press Enter to continue...")
                # driver.close()
                # cod=input("Press Enter to continue...")
                # print (cod)
            else:
                print("TODO: Completar EXCEL:", cod_error, '-', desc_error)

                    # driver.close()
        except Exception as e:
            print("ERROR DESONOCIDO:")
end = datetime.now()

print ("Tiempo:",end-start)

input("Press Enter to continue...")



# df1 = xl.parse('Informe_Resumido_Diario')
# for row in  df1.values:
#     dir = row[18]
#     cod_via = str(dir).split(' ')[0]
#     nombre_via = str(dir).split(cod_via+' ')[1].split(' N ')[0]
#     zip = '{:05}'.format(row[19])
#     cod_prov = zip[0:2]+'0'
#     munic = row[20]
#     # print ("Datos Excel",zip, mun , "Datos DB",zip, db_munic[zip])
#
#     if (munic == db_municipio[zip]):
#         try:
#             prov = db_ciudad[cod_prov]
#             data_calle = json.loads(json.dumps(catas.ConsultaVia(provincia=prov,municipio=munic,nombrevia=nombre_via)))
#             cod_post=data_calle['consulta_callejero']['callejero']['calle']['loine']['cp']
#             cod_munic=data_calle['consulta_callejero']['callejero']['calle']['loine']['cm']
#             tipo_via=data_calle['consulta_callejero']['callejero']['calle']['dir']['tv']
#             nnombre_via= data_calle['consulta_callejero']['callejero']['calle']['dir']['nv']
#             cod_via =data_calle['consulta_callejero']['callejero']['calle']['dir']['cv']
#
#             result=json.loads(json.dumps(catas.Consulta_DNPLOC(provincia=prov,municipio=munic,sigla=tipo_via,calle=calle,numero=nro,planta=planta,puerta=puerta)))
#             ref = str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['pc1'])+str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['pc2'])+str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['car'])+str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['cc1'])+str(result['consulta_dnp']['bico']['bi']['idbi']['rc']['cc2'])
#             print (ref)
#         except Exception as e:
#             print ('NO EXISTE NINGÚN INMUEBLE CON LOS PARÁMETROS INDICADOS')
#
#     else:
#         print("KO")
#
