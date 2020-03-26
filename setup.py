from setuptools import setup

setup(
    name='whapi',
    version='0.5.3',
    packages=['whapi'],
    url='https://github.com/killhamster/WHAPI',
    install_requires=["requests", "bs4"],
    license='MIT',
    author='killhamster',
    author_email='killhamster@gmail.com',
    description='An unofficial WikiHow API'
)
