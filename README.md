# linky_cesml
Récupération des informations de consomation linky pour le fournisseur CESML

## Utilisation 

#### Pour plus de facilité, j'utilise la librairie Pandas

```python
from cesml import Linky
import pandas as pd
linky = Linky(<username>,<password>,"aelGRD",{"https":"http://127.0.0.1:9000"})
json_data = linky.getMesures()
data = pd.DataFrame(json_data["periodesActivite"][0]["courbe"]['valeurs'])


import matplotlib
data["fulldate"]=data["heure"]+"-"+data["date"]
data.plot(x="fulldate",y="valeur")
```
