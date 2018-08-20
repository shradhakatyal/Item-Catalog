# Item Catalog Project

## About the project
This project implements a basic item catalog using Flask, Sqlalchemy, Oauth 2.0, HTML and CSS.A user can log in using Google+ and can create, update, delete or read the database. If a user is not logged in, they can only read the database and not making any changes. The project serves up html files for all endpoints but there are a few json endpoints as follows:
1. localhost:5000/catalog/categories/json - Shows all the categories
2. locahost:5000/catalog/categories/<string:cat_name>/json - Shows all the items in a particular category
3. localhost:5000/catalog/full/json - Shows the complete data stored in the database
4. locahost:5000/catalog/<string:cat_name>/<string:item_title>/json - Displays info about a particular item

## Prerequisites
The project requires vagrant and VirtualBox to work. If you already have them installed, you can skip to the next section.
1. Downlaod vagrant [here](https://www.vagrantup.com/)
2. Download VirtualBox [here](https://www.virtualbox.org/)

## Project Setup
1. Clone this repo using this GitHub [link](https://github.com/shradhakatyal/Item-Catalog.git)
2. Navigate into the repo on your local system and then navigate to the vagrant folder(this is where the vagrant file is present)
3. In the vagrant folder, type the command ```vagrant up``` to start the virtual machine.
4. After the virtual machine has started, enter ```vagrant ssh``` to log in to the vm.
5. To access the common folders, type the command ```cd /vagrant```
6. Navigate into the catalog folder to access the project files.
7. Run ```python database_setup``` to setup the db.
8. Run ```python populate_db.py``` to populate db with initial data.
9. Run ```python app.py``` to start the server and open localhost:5000 on your browser.
10. If any of the dependencies are missing in your vm, you can install it using ```pip install package-name```
11. To log out of the vm simply type ```exit``` in the console/terminal
12. To exit the vm and preserve the state of the vm, type ```vagrant halt```
