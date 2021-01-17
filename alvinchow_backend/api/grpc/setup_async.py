from setuptools import setup

__version__ = None
exec(open('alvinchow_backend_protobuf/version.py').read())


setup(
    name='alvinchow-backend-protobuf-async',
    version=__version__,
    description='Protobuf3 definitions for SERVICE_NAME (async version)',
    packages=['alvinchow_backend_protobuf'],
    include_package_data=True,
    install_requires=[],
)
