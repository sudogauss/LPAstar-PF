from setuptools import setup, find_packages

setup(
    name='lpastar_pf',
    version='0.0.1',
    install_requires=[
        'importlib-metadata; python_version == "3.8"',
    ],
    packages=find_packages(
        where='.',
        include=['lpastar_pf*'],  # ['*'] by default
        exclude=['lpastar_pf.tests'],  # empty by default
    ),
)
