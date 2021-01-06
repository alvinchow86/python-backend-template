# python-backend-template

This is a template for writing a Python backend application or microservice. I have used this at my last few companies in production and it has worked very well, and it contains my ongoing learnings from seeing what works well and doesn't. Note that this can be used for either a monolithic application, a microservice, or anything else, but actually contains a superset of all the things you might want from these different use cases. I didn't feel like writing a code generator, so to use this, just copy the repo and delete the parts you don't need.

Here are the technologies used:
- Python3
- Flask (for web)
- Graphene (for graphql)
- gRPC (for grpc server)
- Celery (for async worker jobs)

## Background
