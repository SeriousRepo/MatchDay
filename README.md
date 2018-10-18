# matchday-site

## Requirements

* virtualenv

* python3


## Usage

cd into project root directory

### Preparation to using virtualenv
Make sure that you have python3 installed. 

Create separated environment
```
$ virtualenv -p python3 venv
```
Activate separated envirionment
```
$ source venv/bin/activate
```
Deactivate separated environment(while virtualenv is activated)
```
$ deactivate
```
### Install required packages
while virtualenv is active
```
$ pip3 install Flask
```
### Run Aplication
```
export FLASK_APP=app.views
export FLASK_ENV=development
flask run
```
