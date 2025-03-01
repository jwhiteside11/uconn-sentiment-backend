# UConn Sentiment Backend

This repository is a collective effort of UConn students to provide backend services for the Sentiment Analysis application. 

The project is structured into subfolders that each represent a Docker container. These containers are designed to run on the Google Compute Engine production instance. Select a service for more information.

**Services**:
- `data-fetchers` - Flask server for scraping news data, interfacing with Datastore, and interfacing with Typesense.
- `ckury-services` - Python scripts for scoring and summarizing sentiment in text, interacting with model; code from original ckury repo (**note:** not yet containerized).
