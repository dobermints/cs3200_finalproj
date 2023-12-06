# MySQL + Flask Boilerplate Project

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## Project Description:

## How to setup and start the containers
**Important** - you need Docker Desktop installed
1. After cloning this repo, navigate to the project directory and create the db_password.txt and db_root_password.txt under the secrets directory. Make sure you have your ports cleared and your local database connected to port 3200.
2. Build the images with `docker compose build`
3. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. Now you should see 3 containers: "appsmith", "web", and "db". 
4. *NOTE*: the current version of this app is not hosted on the web, so you need to open the app on your local machine. 
Video Link: 


