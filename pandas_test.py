import pandas as pd
import ast

df = pd.read_csv("imdb_movies.csv")
df["Duration"] = df["Duration"].str.removesuffix(" min").astype("int64")

df["Stars"] = df["Stars"].apply(ast.literal_eval)
res = df[["Movie Name", "Certificate", "Director", "IMDb Rating", "Genre", "Duration", "Stars"]]

print(type(res["Stars"][0]), res["Stars"][0])

# print(res.tail(10))

# import json

# print(json.dumps(None)) # null - json válido
# print(json.dumps(float("nan"))) # NaN - json inválido

# print(res.dtypes)
# print(res.columns)

# como tu pediu:
# print(pd.isna(res).sum())