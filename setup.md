# Missing
- Include my own application in the Odoo app list

# Useful Commands
- Display all running docker containers
> docker ps
- Start the container when its turned off
> sudo docker-compose up
- SSH to container
> sudo docker exec -it [conatiner-id] sh
- Remove stopped containers so uping the next time will reflect changes
> docker-compose rm

# Setup
## Create Server
- ensure that the line below is not commented out
> restart: always 
- In the same directory level as the docker compose file, run the following:
> docker-compose up
- Go to the url 127.0.0.1:8069
- Install Project
- Create a sample project

## Check Database Longevity
- Down and up the container explicitly
- Check if the url is still active and if the sample project still exists
- Restart the computer without explicitly terminating the docker container
- Check if the url is still active and if the sample project still exists

## Setup Email Server
- Set a domain alias and Outgoing Mail Server
- Ensure that all new users to be added are whitelisted in the email server
- Create a new user
- Set the new user's password locally
- Login as new user

## Install Apps
- backend_theme_v13
- pharma-pos

## Setup Currency
- Go to Settings/Users & Companies/Companies/My Company
- Set currency PHP to active

## Import data
- Import the excel files to the appropriate menus in this order:
1. Product Info/Type
2. Product Info/Size
3. Product Info/Name
4. Product Info/Product
5. Product Info/Pack
6. Product Info/Price