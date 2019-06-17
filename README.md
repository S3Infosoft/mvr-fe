# mvr-fe
Front End Application

## Features
- User authentication i.e Registration, Login and Logout


#### Initial Steps
- Go to the project directory
  ```
  cd mvr-fe
  ```
- Build the Docker image
  ```
  docker build .
  ```
- Build the Docker image using docker-compose
  ```
  docker-compose build
  ```
- Migrate the models to database
  ```
  docker-compose run --rm app sh -c 'python manage.py makemigrations'
  docker-compose run --rm app sh -c 'python manage.py migrate'
  ```


#### To run the server
-   ```
    docker-compose up
    ```
#### To create a superuser
- ```
  docker-compose run --rm app sh -c 'python manage.py createsuperuser'
  ```
- Login to admin page
  <http://localhost:8000/admin/>


#### To run the tests
- ```
  docker-compose run --rm app sh -c 'python manage.py test'
  ```


#### Links
- HomePage: <http://localhost:8000/dashboard/>
- Register: <http://localhost:8000/register/>
- Login: <http://localhost:8000/login/>
- Logout: <http://localhost:8000/logout/>
- Change Password: <http://localhost:8000/password_change/>
- Forgot Password: <http://localhost:8000/password_reset/>
  - Enter the link given in terminal to browser
- API: <http://localhost:8000/api/v1/>
 
