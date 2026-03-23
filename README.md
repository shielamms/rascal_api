# Demo Membership API

## Summary

A demo API with basic membership and event management endpoints.

While this demo app only covers the backend API, since this is built with FastAPI,
you can play around with the endpoints through a web-based interface containing the API documentation.

This API covers the following core use cases:
1. User login - upon application startup, the database 
2. Add user
2. Get list of users
3. Add event
4. Get list of events
5. Register for event

The following diagram illustrates a high-level overview of what the app does:
![High-Level Diagram](images/highlevel_diagram.png)

### Data persistence

All data is stored in a PostgreSQL database that runs alongside the app
    - TODO: use docker compose to automatically run and init the DB before the app

On startup, the DB is initialised with the following tables based on the FastAPI SQL models:
1. `user` - contains records of users (primary key is `id` which is UUID)
2. `event` - contains records of events (primary key is `id` which is UUID)
3. `user_registration` - contains mappings of user and event via foreign keys to `user.id` and `event.id` 


## Project setup

### Pre-requisites

The DB and the app both run in docker containers, orchestrated by docker compose (see `docker-compose.yaml` file).
To run the app, you must have Docker and docker compose - refer to the [online docker reference](https://docs.docker.com/compose/install/) to install docker in your machine

### Running the app

1. Create a `.env` file with the required environment vars

```
cp ./.env.example ./.env
```

2. In your `.env` file, replace the values for each variable:

POSTGRES_USER=arbitrary_username
POSTGRES_PASSWORD=arbitrary_password
FIRST_SUPERUSER_EMAIL=arbitrary_email
FIRST_SUPERUSER_PASSWORD=arbitrary_password
API_SECRET_KEY=arbitrary_str


3. Run docker-compose

The following command will automatically build the image through Dockerfile and set up the DB connection:

```
docker compose up
```

---

