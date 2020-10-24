# awwards

## Author
Omar Hussein

## Description
This is a django web application for rating projects.It mirrors awwards.The application allows users to post their projects for other users to rate according to design, usability and the content of the project.

## User Story
* A user can search for projects.
* A user can view projects overall score.
* A user can view posted projects and their details.
* A user can rate and/or review other users' projects.
* A user be able to post a project to be rated and/or reviewed.
* A user is able to view his/her profile page.

## SetUp instructions
To come up with the same project...

###### Clone the repository:
  * https://github.com/omarion3698/awwards.git
  
###### Navigate into the folder and install requirements
  * cd awwards 
  * pip install -r requirements.txt
  
###### Install and activate Virtual environment
  * virtualenv venv
  * source venv/bin/activate
  
###### Install Dependencies
  * pip install -r requirements.txt
  
##### Setup Database
###### SetUp your database User,Password, Host then make migrate
  * python manage.py makemigrations awwards
  
###### Now Migrate
  * python manage.py migrate
  
###### Run the application
  * python manage.py runserver
  
###### Testing the application
  * python manage.py test
  
Open the application on your browser 127.0.0.1:8000.

## Technologies Used
* Python3.8
* Django
* Heroku

## Contact Information
If you have any questions or contributions, please email me at [omaribinbakarivic@gmail.com]

## License
* License: MIT
* Copyright (c) 2020 Omar Hussein.
