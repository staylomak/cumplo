from django.shortcuts import render
import requests
import json 
from django.http import JsonResponse


def management_date(fecha):
    f = fecha.split('-')
    f.reverse()

    if int(f[0]) < 15:
        if int(f[-2])-1 == 0:
            f[-2] = str(12)
            f[-1] = str(int(f[-1])-1)
        else:
            f[-2] = str(int(f[-2]) -1)
    return f

def encoder(codigo, f):
    cmf_key= "9c84db4d447c80c74961a72245371245cb7ac15f"
    print('aqui esta el problema')
    print(f[-2])
    url = "https://api.sbif.cl/api-sbifv3/recursos_api/tmc/"+f[-1]+"/"+f[-2]+"?apikey="+cmf_key+"&formato=JSON"
    print("SOY LA RUTA:" +url)
    response = requests.get(url)
    respuesta = ''
  
    if response.status_code == 200:
        codigo = str(codigo)
        response_json = json.loads(response.text)
    
        for j in response_json['TMCs']:
            if j['Tipo'] == codigo:
                respuesta=j['Valor']
    else:
        respuesta = 'No hay datos disponibles'
        
    return respuesta

def calculo(monto, dia, fecha):
    cod = None
    
    if dia >= 90:
        if monto <= 50:
            cod = '45'
            print('1')
        if monto <= 200 and monto > 50 :
            cod = '44'
            print('2')
        if monto > 200 and monto<= 5000 :
            cod = '35'
            print('3')
        if monto >5000:
            cod = '34'
            print('4')
    else:
        if monto <= 5000 :
            cod = '26'
            print('5')
        if monto >5000 :    
            cod = '25'
            print('6')
        
    tasa = encoder(cod, fecha)
    
    return tasa



def tmc(request):

    return render(request, 'tmc.html')




def searchTmc(request):



    monto = int(request.GET.get('uf')) if (request.GET.get('uf')) else request.GET.get('uf')
    dia = int(request.GET.get('dias')) if (request.GET.get('dias')) else request.GET.get('dias')
    f = request.GET.get('fecha')
    print(f)

    f = management_date(f)
 
    print(calculo(monto, dia, f))

    data = {
        'monto': monto,
        'dias': dia,
        'fecha': f,
        'TMC': calculo(monto, dia, f)
    }
    return JsonResponse(data)