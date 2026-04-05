# Expense Tracker
This is full-stack web development project built using Django and React. It allows a user to upload a CSV file from their computer to help them track and visualise their expenses.

## Demo
Click to watch the video on Youtube: 
<p align="center">
  <a href="https://youtu.be/7MA7pSKy3J4">
    <img src="https://img.youtube.com/vi/7MA7pSKy3J4/maxresdefault.jpg" alt="Watch the video" style="width:100%;">
  </a>
</p>

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
Type the following commands into your terminal:  

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Example CSV format
amount, category, date, description  
5.30,Transport,1-Apr-26,Train ticket  
31.47,Food,1-Apr-26,Groceries  

Please use the included expenses.csv file to demo this project or use it as a model when creating your own csv files.

Please note that the columns must be named according to this format: amount, category, date, description