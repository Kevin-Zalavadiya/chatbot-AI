@echo off
cd health-chatbot-backend
start "Backend" python main.py
cd ../health-chatbot-frontend  
start "Frontend" npm start
echo Servers starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000