# UConn Sentiment Backend

This repository is a collective effort of UConn students to provide backend services for the Sentiment Analysis application. 

The project is structured into subfolders that each represent a Docker container. These containers are designed to run on the Google Compute Engine production instance. Select a service for more information.

## Docker Compose

To run all services:
```bash
docker compose up
```
This will run the `docker-compose.yml` file, building the Docker images and running the containers for each service.

The main API is `data-fetchers` service for now. Refer to the [API reference](/data-fetchers#api-reference) for useful API endpoints.
  
**Containerized Services**:
- `data-fetchers` - Flask server for scraping news data, interfacing with Datastore, and interfacing with Typesense.
- `ckury-services` - Flask server for scoring and summarizing sentiment in text, interacting with model; code from original ckury repo. Used by `data-fetchers` service.
- `typesense` - Typesense server for searching news data. Used by `data-fetchers` service.

