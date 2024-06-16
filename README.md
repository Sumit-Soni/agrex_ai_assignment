# agrex.ai_assignment
Assignment to scrap product details from amazon.in

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Prerequisites

Requirements for the software and other tools to build, test and push 
- Python
- BeautifulSoup
- SQLAlchemy
- PostgreSQL - In case you want to use PostgreSQL database 

### Installing

A step by step series of examples that tell you how to get a development
environment running

First install the requirements.txt

    pip install -r requirements.txt

### Create Database file

Create database file inn current working directory of name -> product.db

## Running the App

After successfully installing the requirements, Run the FastAPI server

    python agrex.py

## To Do
- Concurrency handling - Can be done using Locks
- Test file (However piece of unit testing is done in main function)
