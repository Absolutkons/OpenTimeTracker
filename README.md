# Hi there, this is OpenTimeTracker
Coming up with names really isn't one of my strengths...

# What is it?
OpenTimeTracker is a very simple and basic time tracker app that let's you login/register, create projects and log time spent on those projects.
It uses the Django Framework and Docker to run.

# Why is it?
For my personal projects I would like to have simple GUIs that allow me to create Users and manage some data. Therefore I had a look into Django and really liked the whole concept. 
In order to get familiar with the framework I decided to code this little app and use some prebuilt snippets too. (Open Source ftw <3)

# How is it?
OpenTimeTracker uses Docker to run on. If you would like to run the app yourself just navigate into the /App/-folder and run <b>docker-compose build</b> and <b>docker-compose up -d</b>.
I have mapped the webapp to port 80 on the host. So just navigate to http://localhost in your browser and there you are :)

For the Login-Page I have used another Github-Project by the user earthcomfy: https://github.com/earthcomfy/Django-registration-and-login-system

To make the whole frontend design part easy I utilized https://tabler.io/. This internally uses Bootstrap5 and ApexCharts.

# How can I use this in my project?
Just copy/fork this and off you go.
