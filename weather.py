
import pandas

weather_data = None

def init():
    global weather_data
    weather_data= pandas.read_csv("seattle-weather.csv")
    # FIX: first time load (cold-start) is very slow; pre-load on deployment?

def select(dataframe, **kwargs):
    # FIX: validate keywords as valid column names
    query_terms = []
    for k in kwargs:
        query_terms.append(f"{k} == {kwargs[k]}")
    return dataframe.query("&".join(query_terms))

def limit(dataframe, n):
    return dataframe.head(n)

def serialize(dataframe):
    return dataframe.to_json(orient="records")

if __name__ == "__main__":
    init()
    # print(serialize(limit(weather_data, 5)))
    print(serialize(limit(select(weather_data, wind=4.5), 5)))
