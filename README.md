
pyAccountsPayable
==============================
Accounts payable project developed with the Flask framework for Python

Overview
------------
This project was created for educational purposes. The goal is to create a backend component. The accounts payable system is a basic system but with all fully operational that exposes all functionality via REST API that can be used by any Frontend component.

We deciced use Flask framework because is very simple to develope and separate the diferent logical layers of the programming.


Getting Started
------------

Setting up the environment
---------

 - Create the environment using the virtualenv tool

```
virtualenv -p python accountsPayable
```

 - Installing project dependencies from a requirements.txt file

```
pip install -r requirements.txt
```
Running the application
---------

- Activate the virtualenv environment

```
accountsPayable\Scripts\activate
```
- Setting environment variables

```
set FLASK_APP=setup
set FLASK_ENV=development
set APP_SETTINGS_MODULE=config.local
```

- Start the application

```
python -m flask run
```

Project Organization
------------
    ├── README.md          <- The top-level README for developers using this project.
    ├── config             <- Enviroment configuration
    │   ├── __init__       <- Init file
    │   ├── default.py     <- Default configuration
    │   ├── local.py       <- Local configuration
    │   ├── dev.py         <- Development o integration configuration
    │   └── pro.py         <- Pro configuration
    │
    ├── sql                <- Create database schema
    │
    ├── setup.py           <- Application startup file
    │
    └── src                <- Main code folder
        ├── __init__       <- Init file
        ├── constants   
        ├── controllers 
        ├── domains     
        ├── libraries   
        ├── repositories
        ├── services    
        └── swagger     
     
    
--------

License
------------
This project uses the following license: [GNU GENERAL PUBLIC LICENSE](<link>).

#python #flask #mvc 
