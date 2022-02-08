pyAccountsPayable
==============================
Accounts payable project developed with the Flask framework for Python

Getting Started
------------

##Setting up the environment

Create the environment using the virtualenv tool
virtualenv -p python accountsPayable

Installing project dependencies from a requirements.txt file
pip install -r requirements.txt

##Running the application

Activate the virtualenv environment
`accountsPayable\Scripts\activate`

Setting environment variables
`set FLASK_APP=setup`
`set FLASK_ENV=development`
`set APP_SETTINGS_MODULE=config.local`
`echo %FLASK_APP%`

Start the application
`python -m flask run`

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
