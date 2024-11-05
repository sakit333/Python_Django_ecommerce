import requests

url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"
        
payload = {  }
headers = {
            "accept": "text/plain",
            
 'Content-Type' : "application/json" 
        }
        
response = requests.post(url, json=payload, headers=headers)
        
print(response.text)