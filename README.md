Pre-requirements: 
1. Create a .env file which should contain the Google CLIENT_ID and CLIENT_SECRET.

2. This project is designed on Python version 3.10.0, so install the same version to avoid any packages/version issues. 

3. Activate a virtual environment using command 'virtualenv env'. 

4. Activate the virtual environment using command './env/Scripts/activate'

5. After the virtual enviroment has been updated, setup database (first-time only). 
    - pip install -r requirements.txt
    - python manage.py makemigrations
    - python manage.py migrate

    After the migrations have been applied move to Step 6.

6. Create a superuser/admin (first-time only). 

   - python manage.py createsuperuser
   - follow on-screen instructions to create the superuser. 

7. run 'python manage.py runserver' to run the project. Your project runs on 'localhost:8000'.

