#data and cleaning
import pandas as pd
import numpy as np
df =  pd.read_csv("data\medquad.csv")
print(df.columns)
df.drop(["source", "focus_area"], axis=1,inplace=True)
print(df.isnull().sum())
df.dropna(inplace= True)
print(df.duplicated().sum())
df.drop_duplicates(inplace= True)
df.to_csv("Embeddings\QA.csv", index=False)
