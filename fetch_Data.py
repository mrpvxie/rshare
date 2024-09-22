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
    
    
# BACK UP
# @app.route('/upload_file', methods=['POST'])
# def upload_file():
#     print("--------------upload_file route is running---------")
#     global current_user
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'})
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})
#     if file:
#         filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{current_user.username}/{file.filename}")
#         file.save(filename)
#         return jsonify({'message': 'File Uploaded'})
#     return jsonify({'error': 'File upload failed'})

# #111
file_list  = []
@app.route('/upload_file')
def uploaded_files():
    print("--------------uploaded_files route is running---------")
    global file_list
    file_list = []
    folder_path = './uploads'
    items = os.listdir(folder_path)
    file_count = 0
    for item in items:
        file_count += 1
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            file_size = os.path.getsize(item_path) 
            file_size_mb = round(file_size / (1024 * 1024) ,2)
        file_list.append(CurrentFile(file_count,item,"N/A",file_size_mb))
    
    return render_template('uploaded_files.html',file_list = file_list)