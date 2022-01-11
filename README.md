# Scrap Ad FullStack Assignment

## RepoContent

- geofenceapi_v1 : First version of API
- geofenceapi_v2 : Second version of API
- nginx: Nginx conf for versioning strategy
- storage: Contains geojson file

## Build & Run images

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

This project is integrated with Github actions for continuous integration, this action executes the tests, builds the docker image and uploads it to the docker hub repository

## Monitoring and Metrics

Both apis have a health check endpoint, that endoint is used in the container for monitoring.

For metrics collection and active monitoring, New Relic is used, which is installed as an agent within the APIs and also on the host where the APIs are deployed.
