# Chatters

A social meida site using django with email authenticated login system where users can 
- Create account 
- Reset their password
- Create any new post 
- Update their previous posts
- Delete their previous posts 
- Change their password 
- Update their profile picture and bio 
- Check each other's profile 
- See last seen of others 
- See own email
- See when their account was created 

A tab is made which will be visible only to superuser and it contains profiles of all users. 
# SCREENSHOTS
<p align="center">
  <h2> Home Page </h2>
  <img src="Previews/home_page.png" width="1000px" title="hover text">
  <h2> Profile Page </h2>
  <img src="Previews/profile_page.png" width="1000px" alt="accessibility text">
</p>

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone git@github.com:srbmaury/Chatters.git
$ cd Chatters
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
