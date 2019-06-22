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
- Profile View/Update: <http://localhost:8000/profile/>
- API access:

  | **Endpoint**                  | **HTTP Method** | **CRUD Method** | **Response**                                  |
  |-------------------------------|-----------------|-----------------|-----------------------------------------------|
  | /api/v1/\<enquiry_model>/      | GET             | READ            | Get all the data of \<Equiry Model>            |
  | /api/v1/\<enquiry_model>/\<id>/ | GET             | READ            | Get a single instance \<Equiry Model>          |
  | /api/v1/\<enquiry_model>/      | POST            | CREATE          | Add a \<Enquiry Model> data                    |
  | /api/v1/\<enquiry_model>/\<id>/ | PUT             | UPDATE          | Update the single instance of \<Enquiry Model> |
  | /api/v1/\<enquiry_model>/\<id>/ | DELETE          | DELETE          | Delete the single instance of \<Enquiry Model> |
