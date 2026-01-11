# 🏏 IPL Outcome Predictor

A **machine learning powered Streamlit web application** that predicts:

- 🔢 **First Innings Final Score**
- 🏆 **Winning Probability of Teams during Second Innings (Chasing)**

based on real-time match conditions such as runs, overs, wickets, teams, and venue.

---

## 🚀 Live Demo

🔗 **Streamlit App**: https://ipl-outcome-predictor-avchpgaer9nax5hdozalpz.streamlit.app/

---

## 📌 Problem Statement

Cricket match outcomes, especially in T20 formats like the IPL, depend heavily on match context.  
This project aims to **predict match outcomes in real time** using machine learning models trained on historical IPL data.

---

## ⚙️ Features

### 🟢 First Innings Score Predictor
- Predicts final score based on:
  - Batting team
  - Bowling team
  - Venue
  - Toss decision
  - Current score, overs, wickets
- Displays:
  - Predicted final score
  - Expected score range

### 🔵 Match Winner Predictor (Second Innings)
- Predicts winning probability of both teams during a chase
- Uses:
  - Runs left
  - Balls left
  - Wickets remaining
  - Current & required run rate
- Displays:
  - Win probability of both teams
  - Likely match winner

---

## 🧠 Machine Learning Models Used

- **XGBoost Regression** → First innings score prediction
- **Logistic Regression** → Match winner prediction
- Feature engineering includes:
  - Current Run Rate (CRR)
  - Required Run Rate (RRR)
  - Balls left, wickets remaining

---

## 🛠️ Tech Stack

- **Python**
- **Pandas, NumPy**
- **Scikit-learn**
- **XGBoost**
- **Matplotlib**
- **RandomForest**
- **Streamlit**
- **Git & GitHub**
- **Git LFS** (for large CSV and model files)

---

## 📁 Project Structure


