from setuptools import setup, find_packages

setup(
    name="hyperstition",
    version="0.1",
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'hyperstition=app.main:main',
        ],
    },
)
