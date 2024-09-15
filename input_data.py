import pandas as pd

def read_csv_to_dict_list(csv_file_path):
    df = pd.read_csv(csv_file_path)
    
    data_list = df.to_dict(orient='records')
    
    return data_list

data_list = read_csv_to_dict_list("output.csv")

print(data_list)