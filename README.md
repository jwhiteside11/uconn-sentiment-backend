# UConn Sentiment Backend

This repository is a collective effort of UConn students to provide backend services for the Sentiment Analysis application. 

The project is structured into subfolders that each represent a Docker container. These containers are designed to run on the Google Compute Engine production instance. Select a service for more information.

## Docker Compose

First, install docker if necessary.

```bash
sudo apt install docker.io
sudo apt install docker-compose-v2
```

Then, to run all services:
```bash
tmux new-session -A -t backend

# from tmux session
sudo docker compose up
# (Ctrl + B) + D
```

This will run the `docker-compose.yml` file, building the Docker images and running the containers for each service. The images can taken about 10 minutes to build.

The backend is now up and running. You can confirm by testing the 'hello, world' endpoint:
```bash
curl 'http://localhost:5100/api'
```

The main API is `data-fetchers` service for now. Refer to the [API reference](/data-fetchers#api-reference) for useful API endpoints.
  
**Containerized Services**:
- `data-fetchers` - Flask server for scraping news data, interfacing with Datastore, and interfacing with Typesense.
- `ckury-services` - Flask server for scoring and summarizing sentiment in text, interacting with model; code from original ckury repo. Used by `data-fetchers` service.
- `typesense` - Typesense server for searching news data. Used by `data-fetchers` service.
- `reverse-proxy` - Nginx server with routes pointing to `data-fetchers` service and `auth` service (TODO: JD). These two are the only public facing services exposed, the rest should only be used internally.

