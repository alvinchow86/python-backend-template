from setuptools import setup

__version__ = None
exec(open('alvinchow_service_protobuf/version.py').read())


setup(
    name='alvinchow-service-protobuf-async',
    version=__version__,
    description='Protobuf3 definitions for SERVICE_NAME (async version)',
    packages=['alvinchow_service_protobuf'],
    include_package_data=True,
    install_requires=[],
)
