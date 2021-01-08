# python-backend-template

## Intro
This is a template for writing a modern Python backend application or microservice, using what I personally feel are best practices and patterns. It is minimal and independent of any major frameworks. I have used this at my last few companies in production and it has worked very well, and it contains my ongoing learnings and iterations.

Note that this can be used for either a monolithic application, a microservice, or anything else, but actually contains a superset of all the things you might want from these different use cases. I didn't feel like writing a code generator, so to use this, just copy the repo and delete the parts you don't need, and customize it however you like. I think it is a good starting point as is, but you can obviously customize it, swap our libraries/technologies, etc.

### Features:
- GraphQL server (for modern SPA javascript apps)
- gRPC server (for use as microservice)
- Basic user session/auth features
- Easy local development with docker-compose
- Deployment with AWS ECS
- CLI management commands
- Unit testing

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
