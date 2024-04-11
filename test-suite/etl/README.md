Before any tests are run, make sure you have started the Docker containers.

To run ETL tests, Python needs to be installed.

For python, see if it is installed with 
- python3 --version

Otherwise:

- sudo apt update
- sudo apt install python3

Then install python3-virtualenv (if you do not have it already):

- sudo apt install python3-virtualenv

Now create a virtual environment in the direct using:

- virtualenv -p python3 venv

Now activate the virtual environment using:

- source venv/bin/activate

And install the required packages using:

- pip install -r requirements.txt

You may need to install pip using:

- sudo apt install python3-pip -y

Run etl tests in the venv by using:

- python3 core_etl_test.py
- python3 update_etl_test.py

The password is set to postgres in the files. If you have chanaged the DB password, change the global variable in the code file. 

Once done, using:

- deactivate