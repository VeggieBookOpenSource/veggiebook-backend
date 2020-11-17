# VeggieBook API Server
This API server is the backend to several mobile applications.

## Table of Contents
1. [Setup](#setup)
    1. [Prerequisites](#prerequisites)
    2. [Instructions](#instructions)
    3. [IDE: PyCharm Configuration & Setup](#ide-pycharm-configuration-setup)
    4. [Create a Local Admin](#create-a-local-admin)
2. [Additional Resources](#additional-resources)

# Setup
Install or verify that you have the prerequisites listed below and follow the instructions below when all prerequistes have been installed.

## Prerequisites
* [Python 2.7](https://www.python.org/downloads/)
* [PIP](https://pip.pypa.io/en/stable/)
* [Virtualenv](https://virtualenv.pypa.io/en/stable/)
* [MySQL Database](https://www.mysql.com/downloads/)

## Instructions
1. Setup a virtual environment with virtualenv.
    ```sh
    # Move the directory where the virtual environment will be created.

    # Create the virtual environment. This command names it "veggiebook".
    $ virtualenv veggiebook
    ```
2. Install the project's dependencies in virtualenv from requirements.txt.
    ```sh
    # Move into the virtual env directory.
    $ cd veggiebook

    # Activate the virtual environment (`source bin/activate`).
    # Note: Running `deactivate` at any time in an active virtualenv will
    # return the system to its default state.
    $ source bin/activate

    # Install the VeggieBook requirements in the active virtualenv.
    $ pip install -r {insert path to requirements.txt here}
    ```
    * Note: Some installations may fail. Below are some notes on the known failing dependencies.
        - `pillow`: There are some additional library requirements for Pillow. Follow their [installation guide](https://pillow.readthedocs.io/en/3.0.0/installation.html) to correct the issue.
        - `py-wkhtmltox`: The package no longer appears to be available for install. Commenting out the dependent code will allow the application to launch.
3. Create database, setup a new user, and grant them permissions to the new database. `qhmobile` is used here since it is the set value in the default configuration file.
    ```sh
    # Login to MySQL as root.
    $ mysql -u root -p

    # Create a new database.
    mysql> create database qhmobile;

    # Create a new user and grant them permissions on the new database.
    mysql> create user 'qhmobile'@'localhost' identified by 'qhmobile';
    mysql> grant all privileges on qhmobile.* to 'qhmobile'@'localhost';
    ```
4. Create your local settings configuration by editing a copy of the sample local settings file and enabling it.
     ```sh
     # From the root of the project, copy the sample configuration file and
     # create a personal settings file.
     $ cp qhweb/conf/SAMPLElocal-settings.ini qaweb/conf/local-settings.ini

     # Open the file and change any necessary settings (database settings in
     # particular).

     # Enable the created personal settings.
     $ ./qhweb/use-local
     ```
5. Setup your database by importing an existing database or running the database migrations.
     * Import an existing database.
         1. Obtain a copy of an existing database from a staging environment or someone with a local development database. The command run should be something like `mysql -u root -p qhmobile > dump.sql`, where `qhmobile` is the database name and `dump.sql` is the file containing the database contents.
         2. Import the database info (should be in the form of a `.sql` file) into the one created earlier.
             ```sh
             $ mysql -u root -p qhmobile < DATABASE_DUMP_FILE_PATH_HERE.sql
             ```
         3. If the obtained database copy is older, migrations should be run in case there have been changes to the database structure since the SQL dump was created.
             ```sh
             $ python manage.py migrate qhmobile
             ```
     * (These currently abort due to errors, use alternative method) Or run database migrations.
         ```sh
         # Add South (Django database migration utility) tables to the database.
         $ python manage.py syncdb

         # Create initial migrations for all apps in the project.
         $ python manage.py schemamigration djcelery --initial
         $ python manage.py schemamigration qhmobile --initial
         $ python manage.py schemamigration easy_maps --initial

         # Run the migrations for each app.
         $ python manage.py migrate djcelery
         $ python manage.py migrate qhmobile
         $ python manage.py migrate easy_maps
         ```
6. Run the application. Ensure the virtualenv created earlier is active (`source bin/activate`) so that the proper Python interpreter and dependency versions are used. The name of the virtualenv will likely appear in parenthesis (`(veggiebook)`) at the beginning of the command prompt when a virtualenv is active.
    ```sh
    $ python qhweb/manage.py runserver
    ```
7. Visit [localhost:8000/qhmobile/](http://localhost:8000/qhmobile/) in your browser. The page will display "I'm Alive!!" if it is running.

## IDE: PyCharm Configuration & Setup
1. Add the virtual environment created with Virtualenv as a Python interpreter in PyCharm.
    1. With the project open, go to the Project Interpreter Settings panel by selecting the main menu > "File" > "Settings to open the Settings panel.
    2. Add the Python intpreter under the created virtualenv, if it hasn't already been added to PyCharm.
        1. Select the "Project: qhweb" menu item at the left of the Settings panel > "Project Interpreter" directly under "Project: qhweb" > Drop-down arrow for the "Project Interpreter" > "Show All...". A window for "Project Interpreters" will open.
        2. Select the "+" at the right side of the new window > "Add Local...".
        3. Fill in the prompts to select the virtualenv created previously.
    3. From the Settings panel, select the "Project: qhweb" menu item at the left  > "Project Interpreter" directly under "Project: qhweb" > Drop-down arrow for the "Project Interpreter" > select the desired virtualenv.
2. Create the build configurations to properly run the application from within PyCharm.
    1. From the main menu select > "Run" > "Edit Configurations..." to open the Run/Debug Configurations panel.
    2. Select the "+" icon at the top, left of the panel > "Python" to add a new configuration.
    3. Set the following values.
        * Name: "manage"
        * Script path: "/home/{path to your manage.py file}/qhweb/manage.py
        * Parameters: "runserver"
        * Project interpreter: Select the Python interpreter from the virtualenv created earlier
        * Working directory: Set the path to the `qhweb` directory.
3. Start the application by selecting from the main menu, "Run" > "Run 'manage'".
4. Visit [localhost:8000/qhmobile/](http://localhost:8000/qhmobile/) to see the "I'm Alive!!" message and verify the application is running.

## Create a Local Admin

1. From the command line, run the following.

    ```sh
    $ python manage.py createsuperuser
    ```
2. Follow the promprs to create an admin user.
3. Visit [localhost:8000/admin](http://127.0.0.1:8000/admin/) and log in to the admin website to view the admin dashboard.

# Additional Resources
* *[Django 1.7 Documentation](https://docs.djangoproject.com/en/1.7)* This project currently uses Django 1.6, which doesn't have documentation. The closest available set of documentation is for version 1.7 (no longer maintained, but still available).
