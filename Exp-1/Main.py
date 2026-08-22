import zipfile
import os
import pandas as pd
extract_path = "./sp500_data"

# # Pass the full path directly into the ZipFile tool
# with zipfile.ZipFile("c:\\Users\\devel\\OneDrive\\Documents\\DataWareHousing\\Exp-1\\archive.zip", "r") as zip_ref:
#     zip_ref.extractall(extract_path)
    
# print('Extraction complete')


# for root,dirs, files in os.walk(extract_path):
#     for file in files:
#         print(os.path.join(root,file))

df = pd.read_csv("C:\\Users\\devel\\OneDrive\\Documents\\DataWareHousing\\Exp-1\\sp500_data\\all_stocks_5yr.csv")

print(df.head())