# Perlimpinpin, a secret app for awesome coders


This project is containerized using docker. In order to run it, you have to install [docker engine](https://docs.docker.com/engine/install/).  
To launch the app in your browser, use `sudo docker-compose up --build`. Do not forget to create a `.env` file in the `backend` folder with a `GEMINI_API_KEY` beforehand.  
You can delete all containers and images with `sudo docker system prune`.