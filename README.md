# Social_Media_Datascience_Pipeline

## Overview

This repository houses a comprehensive pipeline for collecting, storing, and analyzing social media data from platforms like Reddit and 4chan. The pipeline consists of three projects, each serving a unique purpose in the data acquisition and analysis process.

## Projects

### Project 1: Reddit and 4chan Data Collection and Storage

#### Overview
This project focuses on collecting data from Reddit and 4chan, specifically targeting discussions related to firearms, guns, and political topics.

#### Scripts
1. **reddit.py**: Collects posts and comments from "guns" and "firearms" subreddits, storing the data in a PostgreSQL database and enabling export to CSV files.
2. **4chan.py**: Gathers posts from specified boards and threads on 4chan, storing the data in a PostgreSQL database and facilitating export to CSV for further analysis.

#### Scheduler Configuration
The **scheduler.py** script automates the data collection process using nohup and Python's schedule library, ensuring regular updates to the dataset.

### Project 2: Moderate Hate Speech Analysis

#### Overview
This project delves into analyzing moderate hate speech on Reddit and 4chan, enhancing the dataset with classification labels and sentiment analysis.

#### Key Features
- Enhanced dataset with classification columns: success, class, and confidence.
- Daily data collection from r/politics subreddit for ongoing enrichment.
- Generation of graphs for visual insights.
- Conducted sentiment analysis to deepen understanding of the dataset.

### Project 3: Social Media Data Science Pipeline

#### Overview
This project builds an interactive dashboard and performs in-depth analysis of social media data related to gun culture and hate speech.

#### Key Components
- **Dashboard.py (Streamlit Script)**: Creates an interactive web dashboard using Streamlit, allowing users to explore visualizations like sentiment analysis and keyword frequency.
- **Full Analysis.ipynb (Jupyter Notebook)**: Contains detailed analysis, including data cleaning, sentiment analysis, keyword frequency, and time series visualization.

## How to Run This Project

### Setting Up
- Ensure Python is installed on your system.
- Install necessary libraries listed in requirements.txt using `pip install -r requirements.txt`.
- For Jupyter Notebook, install it using `pip install notebook`.

### Running the Projects
1. **Reddit and 4chan Data Collection and Storage**:
   - Execute `python3 reddit.py` to collect data from Reddit.
   - Run `python3 4chan.py` to gather data from 4chan.
   - Schedule data retrieval using `nohup python3 scheduler.py &`.
2. **Moderate Hate Speech Analysis**:
   - Background jobs continuously collect data and update the dataset using `nohup python3 scheduling.py &`.
3. **Social Media Data Science Pipeline**:
   - Run `streamlit run dashboard.py` to access the interactive dashboard.
   - Open `Full Analysis.ipynb` in Jupyter environment for detailed analysis and visualizations.

This README provides an overview of the entire workflow, guiding users on setting up and running the projects for social media data collection and analysis.
