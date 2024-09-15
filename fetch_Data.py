import requests
import pandas as pd

# Define the URL of the API
api_url = "https://textura.onrender.com/get_json_data"

# Fetch data from the API
response = requests.get(api_url)
print(response.json())

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data)
    
    # Specify the columns order
    df = df[['id', 'content', 'time']]
    
    # Write the DataFrame to a CSV file
    df.to_csv('output.csv', index=False)
    
    print("Data has been successfully written to output.csv")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")