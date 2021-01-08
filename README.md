# python-backend-template

## Intro
This is a template for writing a modern Python backend application or microservice, using what I personally feel are best practices and patterns. It is minimal and independent of any major frameworks. I have used this at my last few companies in production and it has worked very well, and it contains my ongoing learnings and iterations.

Note that this can be used for either a monolithic application, a microservice, or anything else, but actually contains a superset of all the things you might want from these different use cases. I didn't feel like writing a code generator, so to use this, just copy the repo and delete the parts you don't need, and customize it however you like. I think it is a good starting point as is with a lot of useful defaults, but you can obviously customize it, swap our libraries/technologies, etc.

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
- Docker
- pytest

Note that this depends on a few other libraries. The idea is to manage some common Python code in your own libraries, so that they can be shared among multiple Python backend services.
- https://github.com/alvinchow86/alvin-python-lib
- https://github.com/alvinchow86/alvin-grpc-py

## Background
There are a few trends in recent years with backend architecture. One is that frontends tend to be built more as Single Page Apps, where the backend's role is mostly to provide APIs (in REST or GraphQL format) for the frontend to fetch data. Another trend is that organizations tend to move towards microservices architectures at some point, even if they start from a monolithic approach.

Django has been a popular and convenient framework on the Python side, but in my experience it itself is bloated and monolithic and contains a lot of things that are outdated for modern API-centric backends (e.g. forms). It bundles a lot of things like an ORM and templating language, but none of these are even the best available libraries at what they do. More importantly, relying too much on Django patterns and features actually makes it harder to refactor a monolith into microservices.

Flask is a much smaller "micro framework" which, comparatively speaking, is better designed and probably better suited for backend development and microservices. However given that modern microservices are likely to use something like gRPC and HTTP/2 instead of serving REST APIs, even Flask isn't really strictly necessary (it's really just bundling the Werkzeug web-app library and Jinja2 templating language).

I think that it is better not to think of a Python-based backend app as a "Django" or "Flask" or some-other-framework app, but instead structure it as a framework agnostic Python application that uses appropriate libraries as needed (which could include things like SQLALchemy, Flask, Graphene, gRPC, etc). This permits maximum flexibility, and makes it more straightforward to say, start with a monolithic codebase and then later break it up into smaller pieces without unnecessarily expensive rewrites.

I've tried to distill the minimal set of things I think are useful for a backend service
- Configuration for different environments (e.g. via env vars)
- Some place to do application initialization (like database or cache connection setup)
- Some hooks to do some cleanup between requests (e.g. DB session cleanup)

## Philosophy and Patterns
This template tries to encourage strong separation of concerns. For instance, API serving code should be in the `api` folder. Your application could serve multiple types of APIs, like GraphQL, REST, gRPC, but these could call the same DB or Business logic functions.

Database models and helpers should be in `db`. Business logic should belong in `service`.

### 64-bit IDs
This template uses Postgres and SQLAlchemy, with 64-bit generated Snowflake/Instagram-style IDs (courtesy of this library https://github.com/alvinchow86/sqlalchemy-postgres-bigint-id). These are much more futureproof than auto-incrementing 32-bit IDs, but have less overhead than 128-bit UUIDs.

### DB repository
I'm using a "repository" pattern to provide a light-weight access layer on top of SQLAlchemy. It's sort of related to the repository pattern that's been described, but simplified and less-opinionated. The idea is to wrap most access to the database (queries, creation, deletion) in separate functions. This ensures that that code is easily testable, and abstracts away ORM-specific details.

There is a folder called `db/repository` where these can live. I usually will create a simple Python module to wrap a model, (e.g. `db/repository/user.py`). You can add convenience imports in `db/repository/__init__.py` such as `from . import user as user_repo`. Then in application code do

```python
from alvinchow_service.db.repository import user_repo
user = user_repo.get_user(123)
```

It can become cumbersome to make a separate "repo" for every model, I will usually group together related models into a larger "repo" package to simplify things.

### Common code
Common utilities and helpers that may be useful for different services are put in a shared library (see below).


## How to Use

### Rename
This is not a framework but a template. You will want to rename a bunch of folders and names, but I have made htis easy but calling them something unique like "alvinchow".

Decide on a top-level package name. It might be something like `<ORG_NAME>_backend` or `<ORG_NAME>_<user>` (if you were building a "user" microservice).

1. Copy this project to a new folder
2. Global text-replace `alvinchow_service` to `<PACKAGE_NAME>`
3. Rename `alvinchow_service` folder to `<PACKAGE_NAME`
4. (if using gRPC) Rename protobuf folders `alvinchow_service_protobuf` and `api/grpc/protobuf/src/alvinchow_service_protobuf` to something else.
4. Global text-replace `alvinchow-service` with something else (e.g. `user-service`)
5. In `docker-compose.yml`, replace the text `alvinchow`

### Companion libraries
By default, this template requires close integration with companion libraries:

**alvin-python-lib** (https://github.com/alvinchow86/alvin-python-lib):
- Env-var app configuration
- Base exception classes
- Redis cache and SQLAlchemy helpers

**alvin-grpc-py** (https://github.com/alvinchow86/alvin-grpc-py) (only if using gRPC):
- Some useful gRPC utilities

Copy these libraries and rename as appropriate (grep for the words `alvin` and `alvinchow` and replace with your org name or something). You can then either build and distribute these on a private PyPi server, or just link these libraries as top-level GIt submodules in this project.



## Testing
pytest is uses for tests. Follow standard pytest conventions to make test files (make a `test_**.py` file, with functions starting with `test_`, etc).

There is a Postgres test database, which is reset between tests, using nested transactions for fast test speed. If your test accesses the database, add a fixture dependency called `db`
