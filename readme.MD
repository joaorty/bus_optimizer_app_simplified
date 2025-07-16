
# Urban Bus Allocation Optimizer

This project is a **web-based decision support system** for optimizing bus allocation across multiple urban routes. It was developed as part of the *Cloud Computing* course and deployed on the **public AWS cloud**.

## Objective

The main goal of the system is to **optimize urban bus allocation** to minimize:

- Operational costs  
- Passenger waiting times  
- Standing passengers  

while **maximizing service coverage** based on demand forecasting and route characteristics.

## Optimization Engine

The system uses a **mathematical programming model** implemented with:

- [PuLP](https://github.com/coin-or/pulp) (Linear Programming in Python)  
- **CBC Solver** as the backend solver

Key model outputs:

- Number of buses allocated per route  
- Expected waiting times and passenger overflow  
- Trade-offs between cost and service quality

## Web Application Stack

| Component  | Description                                   |
|------------|-----------------------------------------------|
| Backend    | Flask-based REST API for scenario optimization |
| Frontend   | Streamlit UI for scenario creation, results visualization, and dashboards |
| Plotting   | Plotly used for interactive data visualization |
| Deployment | Deployed on AWS EC2 (public cloud)            |

## Features

- Scenario Management: Define and manage multiple allocation scenarios  
- Optimization Solver: Automatically run optimization models via API  
- Interactive Dashboards: Visualize key metrics and charts  
- User Authentication: Secure access to private scenarios

## Cloud Deployment

- Hosted on **AWS EC2** instance  
- Configured with `gunicorn` + `nginx` for Flask API  
- Streamlit app available through public URL  
- Dockerized version available for local testing (optional)

## Technologies Used

- Python 3.11  
- Flask  
- Streamlit  
- PuLP + CBC Solver  
- Plotly  
- Pandas  
- AWS EC2

## Academic Context

This project was developed for the **Cloud Computing course**, integrating optimization modeling with modern cloud deployment practices.

## How to Use

1. Access the Streamlit UI to create new scenarios.  
2. Define parameters such as number of buses, demand patterns, and operational limits.  
3. Run the optimization.  
4. View the allocation results and dashboards.



## How to Run Locally

### 1. Clone the repository

```bash
git clone <repo-url>
cd <repo-folder>
```

### 2. Create and activate a Python virtual environment (recommended)

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the backend (Flask API)

```bash
cd backend
docker-compose up --build
```

The Flask API will run at: `http://127.0.0.1:5000`

### 5. Run the frontend (Streamlit app)

Open a new terminal window (keep virtualenv active):

```bash
cd frontend
streamlit run app.py
```

Streamlit will open the app at: `http://localhost:8501`
