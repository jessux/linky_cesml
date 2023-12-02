import requests
import re
import json
import datetime

def get_accesstoken(resp, *args, **kwargs):
  global token
  at = re.search("\#(?:access_token)\=([\S\s]*?)\&",resp.url)
  if at:
      token = at.group(1)
        
def loginCESML(s,username,password,client_id):
  global token
  url = "https://moncompte-cesml-grd-eld.multield.net/application/auth/authorize-implicit-internet/authentification"
  payload = 'username='+username+'&password='+password+'&client_id='+client_id
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  response = s.post(url, headers=headers, data=payload,proxies={"https":"http://127.0.0.1:9000"},verify=False)
  url = "https://moncompte-cesml-grd-eld.multield.net/application/auth/authorize-implicit-internet?redirect_uri=https%3A%2F%2Fmoncompte-cesml-grd-eld.multield.net%2Fautorisation-callback.html&response_type=token&client_id=aelGRD"
  response = s.get( url, headers={}, data={},proxies={"https":"http://127.0.0.1:9000"},verify=False,hooks=dict(response=get_accesstoken))
  return token

def getMesures(s,dateDebut=datetime.datetime(2023,11,16,0,0,0,0)):
  url = "https://moncompte-cesml-grd-eld.multield.net/application/rest/interfaces/aelgrd/historiqueDeMesure"
  today=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
  payload = json.dumps({
    "typeObjet": "DonneesHistoriqueMesureRepresentation",
    "dateDebut": dateDebut.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "dateFin": today,
    "pointAccesServicesClient": {
      "typeObjet": "produit.PointAccesServicesClient",
      "id": "mYwiCcXoigcjneGm.Aan_ftwkvIpwjE8SbRZlJA=="
    },
    "groupesDeGrandeurs": [
      {
        "typeObjet": "produit.GroupeGrandeur",
        "codeGroupeGrandeur": {
          "code": "2"
        }
      },
      {
        "typeObjet": "produit.GroupeGrandeur",
        "codeGroupeGrandeur": {
          "code": "4"
        }
      },
      {
        "typeObjet": "produit.GroupeGrandeur",
        "codeGroupeGrandeur": {
          "code": "0"
        }
      }
    ]
  })
  headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'authorization': 'Bearer '+loginCESML(s)
    
  }
  response = s.post(url, headers=headers, data=payload,proxies={"https":"http://127.0.0.1:9000"},verify=False)
  return response.json()
