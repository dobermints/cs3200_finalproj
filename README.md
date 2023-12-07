# MySQL + Flask Boilerplate Project

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## Project Description:
For our project, we decided to create an app for music listeners to be able to interact with he music they love. Think of it like a dating app for music: users will be able to like and dislikes songs as they scroll through a feed of songs clips. This app, which we call Chart, will generate daily, weekly, and monthly artist rankings for users to view!

## How to setup and start the containers
**Important** - you need Docker Desktop installed
1. After cloning this repo, navigate to the project directory and create the db_password.txt and db_root_password.txt under the secrets directory. Make sure you have your ports cleared and your local database connected to port 3200.
2. Build the images with `docker compose build`
3. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. Now you should see 3 containers: "appsmith", "web", and "db". 
4. *NOTE*: the current version of this app is not hosted on the web, so you need to open the app on your local machine. 

Video Link: 
https://drive.google.com/file/d/1UHSs3kHIsW1zSNVyKOx_lDg1X6BTj6OX/view?usp=drive_link

