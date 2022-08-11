# Flask API Sample 

## Building and running locally via docker. 
### Building
From the directory with the Dockerfile execute the following `docker build -t flaskapisample .`

### Running
From the directory with the Dockerfile execute the following ` docker run -p 5000:5000 -d flaskapisample .`

## Usage
The container will bind to `localhost:5000`. A swagger doc is availalbe for the API. 
The swagger-ui can be reached via `http://localhost:5000/swagger-ui/` 

The API can be queried as follows 
`curl -X GET "http://localhost:5000/usage" -H  "accept: application/json"`

All reponses are using static data. 

### Ops Endpoints
Two other endpoints are availalbe on the app servicing the API `localhost:5000/healthcheck` and `localhost:5000/environment`. Those are operational endpoints used when the app runs for helping to manage the app.   The data they are returing here is also dummy data. 
