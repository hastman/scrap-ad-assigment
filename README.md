# Scrap Ad FullStack Assignment
![python versions](https://img.shields.io/badge/pyhton-%203.6%20%7C%203.7%20%7C%203.8%20-blue)
[![Build and deploy to Docker hub](https://github.com/hastman/scrap-ad-assigment/actions/workflows/deployment-apis.yml/badge.svg?branch=main)](https://github.com/hastman/scrap-ad-assigment/actions/workflows/deployment-apis.yml)
[![codecov](https://codecov.io/gh/hastman/scrap-ad-assigment/branch/main/graph/badge.svg?token=JAXZ6K1R0A)](https://codecov.io/gh/hastman/scrap-ad-assigment)

## RepoContent

- geofenceapi_v1 : First version of API, written in Python with FastAPI
- geofenceapi_v2 : Second version of API, written in Python with FastAPI
- nginx: Nginx conf for versioning strategy
- storage: Contains geojson file
- deploy.sh : Script for remote deployment
- docker-compose.yml : Docker compose file for deployment, deploy all api versions and nginx

## Build & Run images

### Env vars

- Volume for geofence : `STORAGE_LOCATION=/data/geofence.json`
- Sec X-API-KEY header:`API_KEY=your_choice`
- New Relic Monitoring file: `NEW_RELIC_CONFIG_FILE=newrelic.ini`
- New Relic Monitoring key: `NEW_RELIC_LICENSE_KEY=your_new_relic_key`

### geofecnceapi_v1

- Pull repo
- Move to geofenceapi_v1 folder
- Build command: `docker build -t geofence_api_v1`
- Move to parent folder
- Run command: `docker run -d -p 8000:8000 -v "$(pwd)/storage:/data" --env-file .env geofence_api_v1`

### geofecnceapi_v1

- Pull repo
- Move to geofenceapi_v2 folder
- Build command: `docker build -t geofence_api_v2`
- Move to parent folder
- Run command: `docker run -d -p 8000:8000 -v "$(pwd)/storage:/data" --env-file .env geofence_api_v2`

## Version Strategy

For the API versioning strategy following semantics version (Mayor.Minor.Bug), I have chosen versioning by url using different services.
I have chosen this strategy for the following reasons: - Easy to integrate via reverse proxy in backend - Easy to integrate in clients - Backward compatibility - Isolated deployments for fixing bugs or minor changes

The following diagram illustrates the strategy implemented:

![Versioning](https://www2.online-converting.com/upload/api_f149f584b9/result.jpg)

The repository contains a docker-compose.yml file with the implementation of this strategy. This file references pre-built images hosted in the docker hub repository.

## CI/CD

This project is integrated with Github actions for continuous integration, this action executes the tests,run coverage and builds the docker image and uploads it to the docker hub repository the actions fire on release event. This action also performs the deployment via a remote ssh script using `deploy.sh`.

Unit and end-to-end tests are used to test the api.

## Monitoring and Metrics

Both apis have a health check endpoint, that endoint is used in the container for monitoring.

For metrics collection and active monitoring, New Relic is used, which is installed as an agent within the APIs and also on the host where the containers are deployed.

## API Rate Limit

Nginx defines the ratio of requests supported by the services, it is configured for a limit of one request per second on average for a given ip.

Errors are indicated with status code 429 too many request.

```
 limit_req_zone $binary_remote_addr zone=scrapad:10m rate=1r/s;
 limit_req_status 429;
 limit_conn_status 429;
```

You can test it with [loadtest](https://www.npmjs.com/package/loadtest) using the following commands: `loadtest -t 5 -c 2 --rps 6 http://server_ip/v1/health` && `loadtest -t 5 -c 2 --rps 6 http://localhost/v2/health`. This command execute 6 request per second for 2 seconds with two concurrent clients.
