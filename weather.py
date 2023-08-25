
import falcon
import json
import pandas
import wsgiref.simple_server

weather_data = None

class WeatherQueryResource:

    def __init__(self, data):
        # Note: In the absence of a more general interface abstraction, we're
        # simply assuming that the datasource is a pandas dataframe.  More
        # likely in production this will be a DB connection, or reference to
        # some other form of remote persistence.
        self.data = data

    def _serialize(self, dataframe):
        response_data = dataframe.to_dict(orient="records")
        # Wrap the dataframe records in a top-level key in the API response to
        # future-proof API responses by allowing for additional keys at the
        # top-level of the response.  We should - for example - mandate
        # pagination to protect the service, and that would require adding a
        # pagintation token to the response.
        return {
            "records": response_data
        }

    def on_get(self, req, rsp):
        rsp.media = self._serialize(self.data)


def select(dataframe, **kwargs):
    # FIX: validate keywords as valid column names
    query_terms = []
    for k in kwargs:
        query_terms.append(f"{k} == {kwargs[k]}")
    return dataframe.query("&".join(query_terms))

def limit(dataframe, n):
    return dataframe.head(n)


app = falcon.App()
app.add_route("/query", WeatherQueryResource(pandas.read_csv("seattle-weather.csv")))
# FIX: first time load (cold-start) is very slow; pre-load on deployment?

if __name__ == "__main__":
    with wsgiref.simple_server.make_server("", 8000, app) as httpd:
        print("... serving weather on port 8000...")
        httpd.serve_forever()
