import requests

url = 'http://127.0.0.1:5000/analyze'
file_path = 'C:/Users/kalya/OneDrive/Desktop/sentiment_analysis/customer_reviews.xlsx'

with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.json())
