## 10x Genomics Platform Engineering Technical Coding Response

### Overview

A lightweight web-service for weather data for the city of Seattle.  The serivce
supports filtering weather results by the following fields:

 * date
 * precipitation
 * temp_max
 * temp_min
 * wind
 * weather

For example:

```
curl "localhost:8000/query?weather=rain&wind=4.5&temp_min=11.1" | jq
```

Filtering is limited to "intersection" queries; that is: query parameters are
combined using logical AND, and only results matching ALL values are returned.
Matching records are returned as JSON, wrapped in a top-level key `records`; e.g.:

```
curl "localhost:80/query?weather=rain&wind=4.5&temp_min=11.1" | jq
{
  "records": [
    {
      "date": "2013-09-23",
      "precipitation": 2.8,
      "temp_max": 16.1,
      "temp_min": 11.1,
      "wind": 4.5,
      "weather": "rain"
    }
  ]
}
```

### Setup

Development requires: 

 * GNU Make
 * Docker
 * Python 3; Docker images are built using an appropriate base image, and local
   setup (to run the service locally, outside of a container) should match at
   least the minor version.
   
### Build images

From a fresh checkout of the repository, run

```
make
```

to build all images.

### Test images

Start two terminal sessions to test the service after building.  In the first,
start the service:

```
docker run -t -p 80:8000 10x/weather-service:0.0.1
```

In the second, run the test client to run some basic queries through the
locally running weather service container:

```
docker run -t 10x/weather-testclient:0.0.1
```
