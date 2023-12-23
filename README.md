# Daily Sales Forecasting Project

This project automates daily sales forecasting by integrating data from 8 different sales channels. It orchestrates 8 distinct model parameter configurations and provides a centralized API endpoint for internal access.

__Note__: The data displayed is deliberately distorted for data privacy reasons and only one product notebook is showcased for demonstration purposes.

## Tech Stacks
* __FastAPI__ for the API development
* __MLFlow__ for model monitoring
* __Papermill__ automate notebook creation
* __Facebook Prophet__ for forecast algorithm
* __DBManager__ developed exclusively for internal use within company

## Features

- **Multiple Sales Channels:** Integrates data from 8 different sales channels to provide a holistic view of daily sales.

- **Parameter Orchestrator:** Manages and orchestrates 8 different model parameter configurations for accurate and adaptable sales forecasting.

- **Hyperparameter Tuning:** Automates hyperparameter tuning and records results on a monitoring panel to track the performance of different parameter configurations.

![MLFLow](images/mlflow%20panel.jpg)

- **Daily Model Training:** Automatically trains models on a daily basis to ensure the latest data is used for forecasting.

- **Anomaly Detection:** Notifies users if an anomalous amount arises during sales forecasting, allowing for proactive intervention.

- **Model Notebook Generation:** Creates a model notebook for each provider automatically, containing all relevant artifacts such as graphs, metrics, and other useful information.

## Run
---
__initiate_process.py__ file triggers training process (can be convert into a CRON job on a regular basis e.g., daily).

__app/main.py__ starts API session which can be accessed at the PORT: 8000