import requests
import pandas as pd

api_url = "https://textura.onrender.com/get_json_data_content"

response = requests.get(api_url)
print(response.status_code)


if response.status_code == 200:
    data = response.json()
    
    df = pd.DataFrame(data)
    
    df = df[['id', 'content', 'time']]
    
    df.to_csv('output.csv', index=False)
    
    print("Data has been successfully written to output.csv")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    
    