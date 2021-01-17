from setuptools import setup, find_packages

setup(
    name='python-backend-template',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    scripts=[
        'shortcuts/shell'
    ],
    entry_points='''
        [console_scripts]
        manage=alvinchow_backend.commands:cli
        runtests=runtests:main
    ''',
)
