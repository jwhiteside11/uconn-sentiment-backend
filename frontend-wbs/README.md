# Frontend Flask application for Webster Bank

This subfolder holds all of the frontend code, and consists of HTML views and a client for accessing the backend API. This app was designed to run **seperately** from the backend, which is why is is excluded from `docker-compose.yml`.

The frontend is designed to be deployed and run from App Engine. As the App Engine is already in use in the `sentiment-analysis` project, we will be deploying this in App Engine in the `sentiment-test` project instead.

The client for the backend API assumes that the backend services are still running on the `sentiment-prod` VM in the `sentiment-analysis` project. Permissions on Google Cloud have been configured so we can call backend services over HTTP from the `sentiment-test` project's App Engine.

# Quick start

**TODO**