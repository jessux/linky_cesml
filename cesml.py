import requests
import re
import json
import datetime
import urllib3
urllib3.disable_warnings()

class Linky():
    def __init__(self,username,password,client_id):
      self.session=requests.Session()
      self.username = username
      self.password = password
      self.client_id = client_id
      self.token = ""
      
    def get_accesstoken(self,resp, *args, **kwargs):
      at = re.search("\#(?:access_token)\=([\S\s]*?)\&",resp.url)
      if at:
          self.token = at.group(1)
            
    def loginCESML(self):
      url = "https://moncompte-cesml-grd-eld.multield.net/application/auth/authorize-implicit-internet/authentification"
      payload = 'username='+self.username+'&password='+self.password+'&client_id='+self.client_id
      headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
      response = self.session.post(url, headers=headers, data=payload,proxies={"https":"http://127.0.0.1:9000"},verify=False)
      url = "https://moncompte-cesml-grd-eld.multield.net/application/auth/authorize-implicit-internet?redirect_uri=https%3A%2F%2Fmoncompte-cesml-grd-eld.multield.net%2Fautorisation-callback.html&response_type=token&client_id=aelGRD"
      response = self.session.get( url, headers={}, data={},proxies={"https":"http://127.0.0.1:9000"},verify=False,hooks=dict(response=self.get_accesstoken))
      return token
    
    def getMesures(self,dateDebut=datetime.datetime(2023,11,16,0,0,0,0)):
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
          },
          {
            "typeObjet": "produit.GroupeGrandeur",
            "codeGroupeGrandeur": {
              "code": "1"
            }
          }
        ]
      })
      headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'authorization': 'Bearer '+self.loginCESML()
        
      }
      response = s.post(url, headers=headers, data=payload,proxies={"https":"http://127.0.0.1:9000"},verify=False)
      return response.json()
