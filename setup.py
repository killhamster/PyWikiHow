from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='whapi',
    version='0.6.1',
    packages=['whapi'],
    url='https://github.com/killhamster/WHAPI',
    install_requires=["requests", "bs4"],
    license='MIT',
    author='killhamster',
    author_email='killhamster@gmail.com',
    description='An unofficial WikiHow API wrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
