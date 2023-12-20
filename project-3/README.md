# Social-Media-Datascience-Pipeline

# Project: Interactive Dashboard and Analysis for Gun Culture and Hate Speech on Social Media

## Project Introduction
This project aims to provide insightful analysis and interactive visualizations of social media data, focusing on gun culture and hate speech. Utilizing datasets from platforms like 4Chan and Reddit, the project leverages Python and its robust libraries to process, analyze, and visualize trends and patterns. The centerpiece of the project is a Streamlit-based dashboard that allows users to interactively explore the data, complemented by a Jupyter Notebook for in-depth analysis.

### Project URL
Visit the interactive dashboard here: [reddit-4chan-dashboard.streamlit.app/](https://reddit-4chan-dashboard.streamlit.app/)

## Code Explanation
- **Dashboard.py (Streamlit Script):** This script creates an interactive web dashboard using Streamlit. It loads optimized datasets from 4Chan and Reddit, processes them, and then displays various visualizations like sentiment analysis, keyword frequency, and word clouds. Users can filter data based on dates and platforms.
  
- **Full Analysis.ipynb (Jupyter Notebook):** This notebook contains a detailed analysis of the datasets. It involves data cleaning, sentiment analysis, keyword frequency analysis, and time series visualization. The notebook uses libraries like Pandas, NLTK, and Matplotlib for data processing and visualization.

## How to Run This Project
### Dashboard.py
1. **Setup:**
   - Ensure Python is installed on your system.
   - Install required libraries: `streamlit`, `pandas`, `matplotlib`, `wordcloud`, `plotly`, `nltk`.
   - Use `pip install -r requirements.txt` to install these dependencies easily.
2. **Running the Dashboard:**
   - Navigate to the project directory in the terminal.
   - Run the command: `streamlit run dashboard.py`.
   - The dashboard should now be accessible in your web browser.
   - *Note: Sometimes there's a port issue. Navigate to vs code terminal. Inside ports add your port manually. i.e (ipadress.port)port of link which you got after running the above command. Then copy the localhost and port from ports and open it in browser.*

### Full Analysis.ipynb
1. **Setup:**
   - Ensure Jupyter Notebook is installed, or use JupyterLab or Google Colab.
   - Ensure all required libraries are installed as mentioned above.
2. **Installing jupyter notebook:**
   -`pip install notebook` to install these dependencies easily.
   -run `jupyter notebook` to view the analysis code.
   -run `Full\ Analysis.py` to run and view the analysis.
2. **Running the Analysis:**
   - Open `Full Analysis.ipynb` in your Jupyter environment.
   - Run each cell in the notebook to see the analysis and visualizations.

### Note:
1. **why there are two different csv files (optimized) along with main one:**
When you integrate the entire analysis process directly into your dashboard, it tends to become slower and less user-friendly. 
Each time you adjust the date, the system reprocesses the entire dataset, which is inefficient. To resolve this, after completing the analysis, 
we extracted the most valuable data into a new CSV file. This streamlined CSV is then utilized in the dashboard, enhancing performance and user convenience.

  2. In dashboard, actual date starts from Sept 29 to Dec 14


