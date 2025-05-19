# Player Insight: ML-Powered Game Analytics for Snake Game
By FatimaMarie 

## Project Overview

This project analyzes player behavior in a 2D Snake game by collecting gameplay data, applying machine learning to identify player patterns, predict failures, and generate design recommendations. The aim is to improve game design and player experience.

## Technologies Used

- Python  
- Browser-based 2D Snake game (HTML, CSS, JavaScript)  
- JSON session files for data collection  
- scikit-learn (K-Means clustering, Decision Tree)  
- pandas, matplotlib, seaborn for analysis and visualization  
- Streamlit for interactive dashboard  
- ngrok for exposing the dashboard online  


## Installation and Setup

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/snake-game-analytics.git
   cd snake-game-analytics

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Mount Google Drive and place session JSON files inside /snake_data.

4. Run data processing and analysis scripts.

5. Launch the dashboard:
    ```bash
   streamlit run app.py

#Running the Game and Dashboard
- Open the game files (index.html, style.css, script.js) locally to play and generate data.
- Session data saved in /snake_data.
- Analyze data and view insights via the Streamlit dashboard.


#Data Collection
- Logs player movements, duration, and apples eaten.
- Stores sessions as JSON files.


#Machine Learning
- Clusters players with K-Means based on session metrics.
- Uses Decision Tree to predict player failure.
- Extracts common 3-move patterns (3-grams).


#Folder Structure
   ```bash
    /game_code       # Game source files
    /data            # Session data and processed datasets
    /ml              # ML scripts and notebooks
    /dashboard       # Dashboard code
    /screenshots     # Documentation images
    README.md
    requirements.txt 
```


#References
```bash
   scikit-learn https://scikit-learn.org/stable/
   Streamlit https://docs.streamlit.io/ 
   Ngrok https://ngrok.com/docs ``
