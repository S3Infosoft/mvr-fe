# mvr-insights
Go To Application for all things at MVR

[![Build Status](https://travis-ci.org/S3Infosoft/mvr-insights.svg?branch=master)](https://travis-ci.org/S3Infosoft/mvr-insights) [![Coverage Status](https://coveralls.io/repos/github/S3Infosoft/mvr-insights/badge.svg)](https://coveralls.io/github/S3Infosoft/mvr-insights)
## Features
- User authentication i.e Registration, Login and Logout


#### Initial Steps
- Go to the project directory
  ```
  cd mvr-insights
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
- Reports: <http://localhost:8000/activity/report/>
- Activity Log: <http://localhost:8000/activity/log/>
- Enquiry:
  - All the data of a model<http://localhost:8000/enquiry/{model_name}>
  - Single object data <http://localhost:8000/enquiry/{model_name}/{id}/>
- API access:

  | **Endpoint**                  | **HTTP Method** | **CRUD Method** | **Response**                                  |
  |-------------------------------|-----------------|-----------------|-----------------------------------------------|
  | /api/v1/\<enquiry_model>/      | GET     | READ    | Get all the data of \<Equiry Model>            |
  | /api/v1/\<enquiry_model>/\<id>/ | GET     | READ    | Get a single instance \<Equiry Model>          |
  | /api/v1/\<enquiry_model>/      | POST    | CREATE  | Add a \<Enquiry Model> data                    |
  | /api/v1/\<enquiry_model>/\<id>/ | PUT     | UPDATE  | Update the single instance of \<Enquiry Model> |
  | /api/v1/\<enquiry_model>/\<id>/ | DELETE  | DELETE  | Delete the single instance of \<Enquiry Model> |
  | /api/v1/log/ | GET | READ | Get all the activities
  | /api/v1/report/ | GET| READ | Get the reports from a start date to end date
