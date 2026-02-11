import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="IPL Predictor", layout="wide")

def load_models():
    try:
        first_inning_model = pickle.load(open("firstinning_model.pkl", "rb"))
        match_winner_model = pickle.load(open("ipl_model.pkl", "rb"))
        return first_inning_model, match_winner_model
    except FileNotFoundError:
        st.error("Model files not found.")
        return None, None

first_inning_pipe, match_winner_pipe = load_models()

teams = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Gujarat Titans',
    'Kolkata Knight Riders',
    'Lucknow Super Giants',
    'Mumbai Indians',
    'Punjab Kings',
    'Rajasthan Royals',
    'Royal Challengers Bengaluru',
    'Sunrisers Hyderabad'
]

cities = [
    'Ahmedabad', 'Bangalore', 'Bengaluru', 'Cape Town', 'Centurion', 'Chandigarh', 'Chennai', 'Cuttack',
    'Delhi', 'Dharamsala', 'Durban', 'East London', 'Guwahati', 'Hyderabad', 'Indore', 'Jaipur',
    'Johannesburg', 'Kanpur', 'Kimberley', 'Kolkata', 'Lucknow', 'Mohali', 'Mumbai', 'Nagpur',
    'Navi Mumbai', 'New Chandigarh', 'Port Elizabeth', 'Pune', 'Raipur', 'Rajkot', 'Ranchi',
    'Sharjah', 'Unknown', 'Visakhapatnam'
]


st.sidebar.title("🏏 IPL Predictor")
st.sidebar.markdown("---")
prediction_mode = st.sidebar.radio(
    "Choose Prediction Type:",
    ("First Inning Score Prediction", "Match Winner Prediction(Target Chasing)","Pressure Index Prediction")
)
st.sidebar.markdown("---")

if prediction_mode == "First Inning Score Prediction":
    banner_path = r"ipl2.jpeg"
    st.image(banner_path, width=800)
    st.header("First Inning Score Prediction")
    col1, col2 = st.columns(2)
    
    with col1:
        batting_team_1 = st.selectbox("Batting Team", sorted(teams), key="bat1")
        bowling_team_1 = st.selectbox("Bowling Team", sorted(teams), key="bowl1")
        city_1 = st.selectbox("Venue (City)", sorted(cities), key="city1")
        toss_winner_1 = st.selectbox("Toss Winner", sorted(teams), key="toss1")
        
    with col2:
        toss_decision_1 = st.radio("Toss Decision", ['bat', 'field'], horizontal=True, key="dec1")
        current_score_1 = st.number_input("Current Score", min_value=0, step=1, key="score1")
        overs_completed_1 = st.number_input("Overs Completed (e.g., 10.2)", min_value=0.0, max_value=20.0, step=0.1, key="over1")
        wickets_fallen_1 = st.slider("Wickets Down", 0, 10, 0, 1, key="wick1")

    if st.button("Predict Score"):
        if batting_team_1 == bowling_team_1:
            st.error("Batting and Bowling teams must be different!")
        else:
            overs_val = int(overs_completed_1)
            balls_val = int(round((overs_completed_1 - overs_val) * 10))
            if balls_val > 5: 
                balls_val = 6 
            
            balls_bowled = (overs_val * 6) + balls_val
            balls_left = 120 - balls_bowled
            overs_left = balls_left / 6.0
            
            crr = current_score_1 / (overs_completed_1) if overs_completed_1 > 0 else 0
            
            input_data = pd.DataFrame({
                'batting_team': [batting_team_1],
                'bowling_team': [bowling_team_1],
                'city': [city_1],
                'toss_winner': [toss_winner_1],
                'toss_decision': [toss_decision_1],
                'Overs_left': [overs_left],
                'balls_left': [balls_left],
                'current_score': [current_score_1],
                'Wicket_fallen': [wickets_fallen_1],
                'CRR': [crr]
            })
            
            try:
                prediction = first_inning_pipe.predict(input_data)
                final_score = int(prediction[0])
                st.subheader(f"Predicted Final Score: {final_score}")
                
                # Show range
                st.write(f"Estimated Range: {final_score - 10} - {final_score + 10}")
            except Exception as e:
                st.error(f"Error in prediction: {e}")

if prediction_mode == "Match Winner Prediction(Target Chasing)":
    banner_path = r"ipl1.jpeg"
    st.image(banner_path, width=800)
    st.header("Match Winner Prediction (Target Chasing)")
    
    col3, col4 = st.columns(2)
    
    with col3:
        batting_team_2 = st.selectbox("Batting Team (Chasing)", sorted(teams), key="bat2")
        bowling_team_2 = st.selectbox("Bowling Team (Defending)", sorted(teams), key="bowl2")
        city_2 = st.selectbox("Venue (City)", sorted(cities), key="city2")
    
    with col4:
        target_score = st.number_input("Target Score", min_value=1, step=1, key="target2")
        current_score_2 = st.number_input("Current Score", min_value=0, step=1, key="score2")
        overs_completed_2 = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, step=0.1, key="over2")
        wickets_fallen_2 = st.slider("Wickets Fallen", 0, 10, 0, 1, key="wick2")

    if st.button("Predict Winner"):
        if batting_team_2 == bowling_team_2:
            st.error("Teams must be different!")
        elif current_score_2 > target_score:
            st.success(f"{batting_team_2} Won!")
        else:
            runs_left = target_score - current_score_2
            
            overs_val_2 = int(overs_completed_2)
            balls_val_2 = int(round((overs_completed_2 - overs_val_2) * 10))
            balls_left = 120 - ((overs_val_2 * 6) + balls_val_2)
            
            wickets_remaining = 10 - wickets_fallen_2
            
            crr = current_score_2 / overs_completed_2 if overs_completed_2 > 0 else 0
            rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
            
            input_df_2 = pd.DataFrame({
                "batting_team": [batting_team_2],
                "bowling_team": [bowling_team_2],
                "city": [city_2],
                "runs_left": [runs_left],
                "balls_left": [balls_left],
                "wickets": [wickets_remaining],
                "runs_target": [target_score],
                "CRR": [crr],
                "RRR": [rrr]
            })
            
            try:
                result_proba = match_winner_pipe.predict_proba(input_df_2)
                loss_prob = result_proba[0][0]
                win_prob = result_proba[0][1]
                
                st.subheader("Winning Probability")
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    st.metric(label=batting_team_2, value=f"{round(win_prob * 100, 2)}%")
                with subcol2:
                    st.metric(label=bowling_team_2, value=f"{round(loss_prob * 100, 2)}%")
                    
                if win_prob > loss_prob:
                    st.success(f"**{batting_team_2}** is likely to win!")
                else:
                    st.error(f"**{bowling_team_2}** is likely to win!")
                    
            except Exception as e:
                st.error(f"Error during prediction: {e}")


if prediction_mode == "Pressure Index Prediction":
    banner_path = r"img3.png"
    st.image(banner_path, width=800)
    st.header("Pressure Index")
    st.caption("### *Pressure index → How tense is the situation right now?*")
    col1, col2 = st.columns(2)
    
    with col1:
        batting_team_1 = st.selectbox("Batting Team", sorted(teams), key="bat1")
        bowling_team_1 = st.selectbox("Bowling Team", sorted(teams), key="bowl1")
        target_score = st.number_input("Target Score", min_value=1, step=1, key="target2")
        
    with col2:
        current_score_2 = st.number_input("Current Score", min_value=0, step=1, key="score1")
        overs_completed_2 = st.number_input("Overs Completed (e.g., 10.2)", min_value=0.0, max_value=20.0, step=0.1, key="over1")
        wickets_fallen_2 = st.slider("Wickets Down", 0, 10, 0, 1, key="wick1")

    if st.button("Predict Pressure Index"):
        if batting_team_1 == bowling_team_1:
            st.error("Batting and Bowling teams must be different!")
        else:
            runs_left = target_score - current_score_2
            
            overs_val_2 = int(overs_completed_2)
            balls_val_2 = int(round((overs_completed_2 - overs_val_2) * 10))
            balls_left = 120 - ((overs_val_2 * 6) + balls_val_2)
            
            wickets_remaining = 10 - wickets_fallen_2
            
            crr = current_score_2 / overs_completed_2 if overs_completed_2 > 0 else 0
            rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0


            
            def calculate_pressure_index(rrr, balls_left, wickets_remaining):
                # Normalize RRR pressure
                rrr_pressure = min(rrr / 12, 1)

                # Normalize wicket pressure
                wicket_pressure = 1 - (wickets_remaining / 10)

                # Normalize balls pressure
                balls_pressure = 1 - (balls_left / 120)

                # Weighted combination
                pressure_index = (
                    0.4 * rrr_pressure +
                    0.35 * wicket_pressure +
                    0.25 * balls_pressure
             )
                pressure_score = round(pressure_index * 100, 2)
                return pressure_score
            


            def pressure_level(score):
                if score < 40:
                    return "Low Pressure 🟢"
                elif score < 70:
                    return "Medium Pressure 🟡"
                else:
                    return "High Pressure 🔴"
                

            pressure_score = calculate_pressure_index(
            rrr=rrr,
            balls_left=balls_left,
            wickets_remaining=wickets_remaining
             )

            pressure_label = pressure_level(pressure_score)

            st.markdown("---")
            st.subheader("Match Pressure Analysis")

            colp1, colp2 = st.columns(2)

            with colp1:
                st.metric(
                    label="Pressure Index",
                    value=f"{pressure_score} / 100"
                )

            with colp2:
                st.metric(
                    label="Pressure Level",
                    value=pressure_label
                )

            

st.markdown("---")
st.markdown("Developed by Satyam Singh | Powered by Machine Learning")

