import pandas
import requests

df = pandas.read_csv('emotes.csv', index_col=0)

print(df)

for index, row in df.iterrows():
    # print(row.url)
    print(row['name'], row['url'])
    
    image_data = requests.get(row['url']).content
    
    with open(f"{row['name']}.png", 'wb') as file:
        file.write(image_data)