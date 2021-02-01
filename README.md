# python-backend-template

## Intro
This is a template for writing a modern Python backend application or microservice, using what I personally feel are best practices and patterns. It is minimal and independent of any major frameworks. I have used this at my last few companies in production and it has worked very well, and it contains my ongoing learnings and iterations.

Note that this can be used for either a monolithic application, a microservice, or anything else, but actually contains a superset of all the things you might want from these different use cases. I didn't feel like writing a code generator, so to use this, just copy the repo and delete the parts you don't need, and customize it however you like. I think it is a good starting point as is with a lot of useful defaults, but you can obviously customize it, swap our libraries/technologies, etc.

Here are some possible use cases for this template:
- Build a monolithic app for your startup MVP, but in a way that can easily be refactored into microservices later
- Build a microservices-based architecture right away (use this template for each service)

### Features:
- GraphQL server (for modern SPA javascript apps)
- gRPC server (for use as microservice)
- Easy local development with docker-compose
- Deployment with AWS ECS
- CLI management commands
- Unit testing
- Basic user session/auth features (optional)

### Libraries/Technologies used:
- Python3
- Flask + uwsgi + nginx (for web)
- Graphene (for graphql)
- gRPC + protobuf3 (for grpc server)
- Celery (for async worker jobs)
- APScheduler for periodic jobs
- SQLAlchemy ORM
- PostgreSQL database
- Redis for Celery queue
- Supervisor for process management
- Docker
- pytest

Note that this depends on a few other libraries. The idea is to manage some common Python code in your own libraries, so that they can be shared among multiple Python backend services.
- https://github.com/alvinchow86/alvin-python-lib
- https://github.com/alvinchow86/alvin-grpc-py

## Background
There are a few trends in recent years with backend architecture. One is that frontends tend to be built more as Single Page Apps, where the backend's role is mostly to provide APIs (in REST or GraphQL format) for the frontend to fetch data. Another trend is that organizations tend to move towards microservices architectures at some point, even if they start from a monolithic approach.

In my opinion, large frameworks such as Django contain a lot of things that are irrelevant for a mostly API-based service or microservice, and even impede a monolith to microservices migration. Even Flask, while being a minimal framework, isn't necessary if you are building a gRPC microservice.

I think that it is better not to think of a Python-based backend app as a "Django" or "Flask" or some-other-framework app, but instead structure it as a framework agnostic Python application that uses appropriate libraries as needed (which could include things like SQLALchemy, Flask, Graphene, gRPC, etc). This permits maximum flexibility, and makes it more straightforward to say, start with a monolithic codebase and then later break it up into smaller pieces without unnecessarily expensive rewrites.

I've tried to distill the minimal set of things I think are useful for a backend service
- Env var configuration for different deployment environments
- Some place to do application initialization (like database or cache connection setup)
- Some hooks to do some cleanup between requests (e.g. DB session cleanup)

## Philosophy and Patterns
This template tries to encourage strong separation of concerns. For instance, API serving code should be in the `api` folder. Your application could serve multiple types of APIs, like GraphQL, REST, gRPC, but these could call the same DB or Business logic functions.

Database models and helpers should be in `db`. Business logic is recommended to go into the `service` package.

### 64-bit IDs
This template uses Postgres and SQLAlchemy, with 64-bit generated Snowflake/Instagram-style primary keys (courtesy of this library https://github.com/alvinchow86/sqlalchemy-postgres-bigint-id). These are much more futureproof than auto-incrementing 32-bit IDs, but have less overhead than 128-bit UUIDs.

### Database Repository
I'm using a "repository" pattern to provide a light-weight access layer on top of SQLAlchemy. It's sort of related to the repository pattern that's out there, but simplified with plain Python functions grouped in modules. The idea is to wrap most access to the database (queries, creation, deletion) in standalone functions. This ensures that that code is easily testable, and abstracts away ORM-specific details.

There is a folder called `db/repository` where these can live. I usually will create a simple Python module to wrap a model, (e.g. `db/repository/user.py`). You can add convenience imports in `db/repository/__init__.py` such as `from . import user as user_repo`. Then in application code do

```python
from alvinchow_backend.db.repository import user_repo
user = user_repo.get_user(123)
```

It can become cumbersome to make a separate "repo" for every model, I will usually group together related models into a larger "repo" package to simplify things.

### Common Code
Common utilities and helpers that may be useful for different services are put in a shared library (see below).

## How to Use
This is not a framework but a template. You will want to rename a bunch of folders and names, but I have made this easy but calling them something unique like "alvinchow".

See https://github.com/alvinchow86/python-backend-template/wiki/How-to-Use for more detailed instructions on how to use this template.

## Folder Structure

### `api/`
- API code (REST, GraphQL, gRPC)

### `app/`
- Global application configuration, initialization.
- Stores app instances for Flask, Celery, etc

### `commands/`
- Custom CLI commands

### `db/`
- Database models, helpers and setup
- Repository functions can go here

### `lib/`
- Helper code that is specific to this application

### `remote/`
- Put code related to accessing other microservices (e.g. abstraction clients) or vendor APIs

### `service/`
- Business logic (application logic) should go here
- Organize into separate modules/packages as you see fit

### `test/`
- Test factory functions and other helpers

### `utils/`
- Other helper code, that isn't specific to this application. The difference with `lib` is code here could theoretically be extracted into a separate Python library

## Local Development
Local development is based on Docker and docker-compose.

### Run containers
Build the image
```
docker-compose build
```

Run containers
```
docker-compose up -d
```

### Commands
The Docker image installs some useful shell commands

Launch a Python shell where ou can do stuff like make database queries and such
```
shell
```

Run tests
```
runtests
```

Management cli commands
```
manage <command>
```


## Testing
pytest is uses for tests. Follow standard pytest conventions to make test files (make a `test_**.py` file, with functions starting with `test_`, etc).

There is a Postgres test database, which is reset between tests, using nested transactions for fast test speed. If your test accesses the database, add a fixture dependency called `db`

To run tests, do `runtests.py` or `runtests`.

## Additional Documentation
See the [repo wiki](https://github.com/alvinchow86/python-backend-template/wiki) for additional documentation

## CI Status
[![<alvinchow86>](https://circleci.com/gh/alvinchow86/python-backend-template.svg?style=svg)](<https://app.circleci.com/pipelines/github/alvinchow86/python-backend-template>)
