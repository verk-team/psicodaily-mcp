from pathlib import Path
import pandas as pd
import typing
import ast

df = pd.read_csv(Path(__file__).parent / "imdb_movies.csv")
df["Duration"] = df["Duration"].str.removesuffix(" min").astype("int64")
df["Stars"] = df["Stars"].apply(ast.literal_eval)

def find(
	limit: int = 10,
	min_rating: float = 0,
	ascending: bool = False,
	genre: str | None = None,
	director: str | None = None,
	order_by: typing.Literal["IMDb Rating", "Duration"] = "IMDb Rating",
):
	"""
	os filmes que entram nessa base são os top 1000 do imdb, a menor nota da base é 7.6,
	os dados são um recorte específico e não reflete necessáriamente numa conclusão generalista
	como: o pior filme de nolan é <filme>, sendo que não existem todas as obras do profissional
	para tirar essa conclusão, sabendo disso responda com: "De acordo com os dados disponíveis, [resto_da_resposta]"

	a base só tem filmes bem avaliados, então o "pior" é só o pior dentro desse recorte

	retorno
	movies: "Movie Name", "Certificate", "Director", "IMDb Rating", "Genre", "Duration" e "Stars"
	total: quantidade total de registros encontrados para aquela busca, pode ser maior que o retornado já que pode exceder o limite de 50 registros

	no campo Certificate há células como `null`, nesses casos o dado é "não informado"

	o filtro de `genre` faz uma busca de includes na str de `Genre` do filme, `min_rating` exclui os registros que tenham IMDb Rating menor que o valor informado

	o filtro de diretor (`director: str`) faz uma comparação de contains,
	sem case-sensitive nem "acento"-sensitive sobre o campo `Director` da row para facilitar a busca

	limit: o que acontece acima de 50 - o excedente não é incluído na resposta e o `total` exibe a quantidade franca de registros encontrados para aquela busca
	caso exceda, avisar o usuário

	"""

	res = df[["Movie Name", "Certificate", "Director", "IMDb Rating", "Genre", "Duration", "Stars"]]

	if director is not None:
		filtro_diretor = res["Director"].str.contains(director, case=False)
		res = res[filtro_diretor]

	if genre is not None:
		filtro_genre = res["Genre"].str.contains(genre, case=False)
		res = res[filtro_genre]

	filtro_min_rating = res["IMDb Rating"] >= min_rating
	res = res[filtro_min_rating]

	formatted_res = res.sort_values(
		by=order_by,
		ascending=ascending
	).head(limit).astype(object).where(res.notna(), None)

	formatted_res = formatted_res.to_dict(orient="records")

	return {
		'movies': formatted_res,
		'total': len(res)
	}
