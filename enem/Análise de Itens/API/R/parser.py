from urllib.parse import urlencode
import requests
import json

def serialize_url(a, b, c, re):
    base_url = "http://127.0.0.1:8080/tri"
    
    params = {
        'a': ', '.join(map(str, a)),
        'b': ', '.join(map(str, b)),
        'c': ', '.join(map(str, c)),
        're': ', '.join(map(str, re))
    }
    
    encoded_params = urlencode(params, safe=', ')
    
    serialized_url = f"{base_url}?{encoded_params}"
    
    return serialized_url

# Exemplo de uso
a = [1.63948, 2.872, 1.56585, 3.92803]
b = [3.22867, 0.87565, -0.12884, 1.08796]
    #822,8    #587,56   #487,21  #608,79
c = [0.14221, 0.15092, 0.20389, 0.09238]


re = [1, 1, 1, 1]
url = serialize_url(a, b, c, re)
print(url)

# Fazer a solicitação HTTP
response = requests.get(url)

# Analisar a resposta JSON
data = json.loads(response.text)

# Extrair o número
nota = data['nota'][0]
nota_max = data['nota_max'][0]
nota_min = data['nota_min'][0]

print(f"Sua nota (acertando todas) foi: {nota}\n{round((nota/nota_max),2)*100}% da nota máxima.\n")

