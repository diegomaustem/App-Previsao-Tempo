import requests
import json
import keyGenerate 

accuweatherAPIKey = keyGenerate.generateAPIKey()

requestPlugin = requests.get('http://www.geoplugin.net/json.gp')

if(requestPlugin.status_code != 200):
    print('Não foi possível obter a localização.')
else:
    location = json.loads(requestPlugin.text)
    lat  = location['geoplugin_latitude']
    long = location['geoplugin_longitude']

    locationAPIUrl = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey='+ accuweatherAPIKey +'&q='+ lat +'%2C'+ long +'&language=pt-br'

    requestAPI = requests.get(locationAPIUrl)
    if(requestPlugin.status_code != 200): 
        print('Não foi possível obter o código do local.')
    else:
        locationResponse = json.loads(requestAPI.text)
        nameLocal = locationResponse['LocalizedName'] + ',' + locationResponse['AdministrativeArea']['LocalizedName'] + '.' + locationResponse['Country']['LocalizedName']
        codeLocal  = locationResponse['Key']

        print(nameLocal)

        currentConditionAPIUrl = 'http://dataservice.accuweather.com/currentconditions/v1/'+ codeLocal +'?apikey='+ accuweatherAPIKey +'&language=pt-br'

        requestConditionsAPI = requests.get(currentConditionAPIUrl)
        if(requestConditionsAPI.status_code != 200):
            print('Não foi possível obter o código do local') 
        else:
            currentConditionsResponse = json.loads(requestConditionsAPI.text)

            textClimate = currentConditionsResponse[0]['WeatherText']
            temperature = round(currentConditionsResponse[0]['Temperature']['Metric']['Value'])
            
            print('Clima no momento: ' + textClimate)
            print('Temperatura: ' + str(temperature) + ' graus Celsius')
