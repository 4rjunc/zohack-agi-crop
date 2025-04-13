# NIH Dataset Preprocessor with Eliza Agents

A scalable Flask application designed to clean, standardize, and preprocess integrated NIH datasets using distributed Eliza agents.

## Project Overview

This application addresses the challenges of working with large, heterogeneous NIH datasets by automating the preprocessing workflow through distributed processing. By leveraging Eliza's decentralized agent framework, the application efficiently handles data cleaning tasks like detecting inconsistencies, managing missing data, and standardizing categorical variables across large datasets.

### Key Features

- **Automated Data Cleaning**: Automatically identifies and resolves data inconsistencies across integrated NIH datasets
- **Missing Data Handling**: Employs statistical methods and machine learning algorithms to predict and fill missing values
- **Outlier Detection and Treatment**: Identifies statistical outliers and applies appropriate correction methods
- **Categorical Data Standardization**: Normalizes categorical variables across different datasets
- **Distributed Processing**: Utilizes Eliza's decentralized agents to perform cleaning tasks in parallel
- **Scalable Architecture**: Designed to scale across large datasets and multiple computational nodes
- **User-Friendly API**: RESTful API interface for easy integration with existing workflows

## Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)
- node 
- pnpm


### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/4rjunc/zohack-agi-crop.git
   cd zohack-agi-crop
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   flask run
   ```

2. Start the Eliza agent workers:
    **The Eliza's Instructions are inside [eliza dir](https://github.com/4rjunc/zohack-agi-crop/tree/main/eliza#eliza-)**

The application will be available at `http://localhost:5000`.

## Acknowledgments

- NIH for providing access to public health datasets
- The Eliza framework developers for their distributed agent architecture
