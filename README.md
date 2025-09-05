# ✨ Perlimpinpin ✨, a secret app for awesome coders

[![Made with React](https://img.shields.io/badge/Made%20with-React-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Made with FastAPI](https://img.shields.io/badge/Made%20with-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Dockerized](https://img.shields.io/badge/Dockerized-Yes-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

Perlimpinpin is a personal assistant that suggests **micro-tasks** to developers based on:
- The state of their GitHub repository
- The amount of time they have available  

The goal: stay productive even with limited time by tackling small, concrete tasks.  

---

## 🚀 Features
- Backend in **FastAPI**  
- Frontend in **React**  
- **Dockerized** project for easy deployment  
- A simple and ergonomic interface  

---

## 📸 Preview
![Frontend Preview](website.gif)  

---

## 🛠️ Installation
```bash
# Clone the repository
git clone https://github.com/your-username/perlimpinpin.git
cd perlimpinpin
echo "GEMINI_API_KEY=Your-API-KEY" > .env

# Start the project with Docker
docker-compose up --build
```

This project is containerized using docker. In order to run it, you have to install [docker engine](https://docs.docker.com/engine/install/).  
Do not forget add your `GEMINI_API_KEY` beforehand. Your can get one on [Google AI studio](https://aistudio.google.com/app/apikey).  

Once the server is up, you can access it locally via your [browser on http://localhost:80](http://localhost:80)
You can delete all containers and images with `sudo docker system prune`.