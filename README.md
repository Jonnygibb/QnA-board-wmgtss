# QnA-board-wmgtss

This repository houses the Q&A Board for the WMGTSS system. This board provides students a tutors the opportunity to ask questions, give answers and leave comments on questions. The purpose of this board is to give students and tutors the opportunity to share information about their course with all of their students rather than just one to one email chains. 

## Prerequisites
In order to use the Q&A Board, docker and docker-compose are requried. This project is tested against docker version 20.10.12, build e91ed57 and docker-compose version v2.2.3 on all platforms (MacOS, Windows & Linux). All of these softwares can be aquried from https://docs.docker.com/get-docker/

## Instructions
 1. Open terminal of choice (bash, powershell, cmd etc.)
 2. Change directory to the wmgtss folder
 3. Build the docker image by running 'docker-compose build'
 4. Once the build has finished, spin up the container by running 'docker-compose up'
 5. After the container has become live, visit: http://0.0.0.0:8000/ or alternatively http://localhost:8000/
 6. This will bring you to the login page. Feel free to click the sign up link and login to the page to experiment with it's functinality!
 7. Alternativly, the database is seeded with users, questions, answers and more already. The user's usernames available are: jessday3, winbish, esmith1 and ceceparekh1. The password for all these users are 'password'.
 8. If you want to experiement with features only available to tutors, use the credentials Tutor:SecureTutorPassw0rd in order to log in.

The GitHub repository can be found at this location: https://github.com/Jonnygibb/QnA-board-wmgtss
