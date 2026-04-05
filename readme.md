# Expense Tracker
This is full-stack web development project built using Django and React. It allows a user to upload a CSV file from their computer to help them track and visualise their expenses.

## Demo
<iframe width="560" height="315" src="https://www.youtube.com/embed/7MA7pSKy3J4?si=FJSCQZzi6wc-VkMa" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

[![Watch the video](https://img.youtube.com/vi/7MA7pSKy3J4/default.jpg)](https://youtu.be/7MA7pSKy3J4?si=g_dPMFLNBbLVfxWP)

## Features
- User authentication (login/register/logout)
- CSV upload for transactions
- Dashboard with charts (category, monthly, daily)
- Transaction history with delete functionality
- Summary cards (total spending, top category)

## Tech Stack
- Backend: Python, Django, Django REST Framework, Pandas (CSV processing)
- Frontend: React, Recharts (data visualisation)
- Database: SQLite

## How to Run

### Backend
cd backend
pip install -r requirements.txt
python manage.py runserver

### Frontend
cd frontend
npm install
npm start

## Example CSV format
amount, category, date, description
5.30,Transport,1-Apr-26,Train ticket
31.47,Food,1-Apr-26,Groceries

Please use the included expenses.csv file to demo this project or use it as a model when creating your own csv files.

Please note that the columns must be named according to this format: amount, category, date, description