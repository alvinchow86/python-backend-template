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

