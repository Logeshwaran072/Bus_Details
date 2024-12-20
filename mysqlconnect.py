import pandas as pd
import numpy as np
import pymysql



myconnection = pymysql.connect(host ='127.0.0.1', user="root", passwd="Logesh007$")

myconnection.cursor().execute("create database if not exists redbus")
myconnection.cursor().execute("use redbus")




# all route files
state_csv_files = ["D:/Project/project_redbus_local_drive/CTURTC.csv",
                   "D:/Project/project_redbus_local_drive/HRTC.csv",
                   "D:/Project/project_redbus_local_drive/jksrtc.csv",
                   "D:/Project/project_redbus_local_drive/KAAC.csv",
                   "D:/Project/project_redbus_local_drive/kerala_sctc.csv",
                   "D:/Project/project_redbus_local_drive/KTCL.csv",
                   "D:/Project/project_redbus_local_drive/NBSTC.csv",
                   "D:/Project/project_redbus_local_drive/PEPSU.csv",
                   "D:/Project/project_redbus_local_drive/TSRTC.csv",
                   "D:/Project/project_redbus_local_drive/WBSTC.csv"]

all_data = []

for file in state_csv_files:
    df = pd.read_csv(file)
    all_data.append(df)

df_data = pd.concat(all_data, ignore_index=True)
df_data["Price"] = df_data["Price"].str.replace("INR ","", regex=False).astype("float64")
df_data.insert(0,"ID",range(1,len(df_data)+1))


col = [i.replace(" ","_") for i in df_data.columns]

df_data.dropna()

columns = ",".join(f"{i} {j}" for i,j in zip(col,df_data.dtypes)).replace("object","VARCHAR(300)").replace("float64","FLOAT").replace("int64","INT")

table_name = "bus_details"
myconnection.cursor().execute(f"create table  {table_name} ({columns})")


for i in range(len(df_data)):
    row = tuple(df_data.iloc[i].apply(lambda x: int(x) if isinstance(x, np.int64) else float(x) if isinstance(x, np.float64) else str(x)))
    myconnection.cursor().execute(f"insert into {table_name} values {row}")
myconnection.commit()

df_data.to_csv("all_bus_details.csv", index = False)
myconnection.close()
























