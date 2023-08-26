
import falcon
import json
import pandas
import wsgiref.simple_server

LIMIT_PARAM_NAME = "limit"

class WeatherQueryResource:

    def __init__(self, data: pandas.DataFrame):
        # Note: In the absence of a more general interface abstraction, we're
        # simply assuming that the datasource is a pandas dataframe.  More
        # likely in production this will be a DB connection, or reference to
        # some other form of remote persistence.
        self._data = data
        self._query_params = set(list(self._data.columns) + ["limit"])

        self._param_types = dict(self._data.apply(lambda x: pandas.api.types.infer_dtype(x, skipna=True), axis=0))
        self._param_type_formatters = {
            "string": lambda x: f"\"{x}\"",
            "floating": lambda x: f"{x}"
        }

    def _assert_request_params(self, params):
        for p in params:
            if not p in self._query_params:
                raise falcon.HTTPBadRequest(
                    title="Invalid Query Parameter",
                    description=f"invalid query parameter: {p}; expected one of {self._query_params}"
                )
        if LIMIT_PARAM_NAME in params:
            try:
                int(params[LIMIT_PARAM_NAME])
            except ValueError:
                raise falcon.HTTPBadRequest(
                    title="Invalid Query Parameter Value",
                    description=f"invalid query parameter value: {LIMIT_PARAM_NAME}"
                )

    def _param_type_formatter(self, typestr):
        if typestr in self._param_type_formatters:
            return self._param_type_formatters[typestr]
        else:
            raise Exception(f"unexpected type: {typestr}")

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

    def _format_param_for_query(self, pk, pv):
        formatter = self._param_type_formatter(self._param_types[pk])
        return formatter(pv)

    def on_get(self, req: falcon.Request, rsp: falcon.Response):
        self._assert_request_params(req.params)
        dataframe_query = " & ".join(
            [
                f"{k} == {self._format_param_for_query(k, req.params[k])}"
                for k in req.params
                if not k == LIMIT_PARAM_NAME
            ]
        )
        limit_fn = \
            (lambda df: df.head(int(req.params[LIMIT_PARAM_NAME]))) if (LIMIT_PARAM_NAME in req.params) \
            else lambda x: x
        rsp.media = self._serialize(limit_fn(self._data.query(dataframe_query)))


app = falcon.App()
app.add_route("/query", WeatherQueryResource(pandas.read_csv("seattle-weather.csv")))
# FIX: first time load (cold-start) is very slow; pre-load on deployment?

if __name__ == "__main__":
    with wsgiref.simple_server.make_server("", 8000, app) as httpd:
        print("... serving weather on port 8000...")
        httpd.serve_forever()
