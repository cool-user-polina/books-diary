import requests
response = requests.post('http://127.0.0.1:5000/create-books', json = {"name": "lmskks", "author" : "Виктор", "ganre": "", "year":""})
print(response.ok) 
print(response.text)