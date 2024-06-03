import requests
import json
import keyGenerate 

accuweatherAPIKey = keyGenerate.generateAPIKey()

def getCoordinates():
    requestPlugin = requests.get('http://www.geoplugin.net/json.gp')

    if(requestPlugin.status_code != 200):
        print('Não foi possível obter a localização.')
        return None
    else:
        try:
            location = json.loads(requestPlugin.text)
            coordinates = {}
            coordinates['lat'] = location['geoplugin_latitude']
            coordinates['long'] = location['geoplugin_longitude']
            return coordinates
        except:
            return None
    
def getLocalCode(lat, long):
    locationAPIUrl = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey='+ accuweatherAPIKey +'&q='+ lat +'%2C'+ long +'&language=pt-br'

    requestAPI = requests.get(locationAPIUrl)
    if(requestAPI.status_code != 200): 
        print('Não foi possível obter o código do local.')
        return None
    else:
        try:
            locationResponse = json.loads(requestAPI.text)
            localInformation = {}
            localInformation['localName'] = locationResponse['LocalizedName'] + ',' + locationResponse['AdministrativeArea']['LocalizedName'] + '.' + locationResponse['Country']['LocalizedName']
            localInformation['localCode'] = locationResponse['Key']
            return localInformation
        except:
           return None 
        
def getCurrentWeather(localCode, localName):
    currentConditionAPIUrl = 'http://dataservice.accuweather.com/currentconditions/v1/'+ localCode +'?apikey='+ accuweatherAPIKey +'&language=pt-br'

    requestConditionsAPI = requests.get(currentConditionAPIUrl)
    if(requestConditionsAPI.status_code != 200):
        print('Não foi possível obter o clima atual') 
        return None
    else:
        try:
            currentConditionsResponse = json.loads(requestConditionsAPI.text)
            weatherInformation = {}
            weatherInformation['textClimate'] = currentConditionsResponse[0]['WeatherText']
            weatherInformation['temperature'] = round(currentConditionsResponse[0]['Temperature']['Metric']['Value'])
            weatherInformation['localName'] = localName
            return weatherInformation
        except:
            return None 
    
coordinates = getCoordinates()
try:
    local = getLocalCode(coordinates['lat'], coordinates['long'])
    currentWeather = getCurrentWeather(local['localCode'], local['localName'])
    print('Current weather in: ' + currentWeather['localName'])
    print(currentWeather['textClimate'])
    print('Temperatura: ' + str(currentWeather['temperature']) + '\xb0' + ' C')
except:
    print('Erro ao processar a solicitação. Entre em contato com o suporte.') 


