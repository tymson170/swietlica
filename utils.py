import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import datetime

def load_dataframes():
    conn = st.connection("gsheets", type=GSheetsConnection)
    timetable = conn.read(worksheet="0")
    students = conn.read(worksheet="1182062754")

    return pd.DataFrame(timetable), pd.DataFrame(students)

def parse_hour_min(time):
    hour = time[0:2]
    minute = time[-2:]

    return datetime.time(int(hour), int(minute))

def get_closest_session(timetable_df, dt=None):
    weekdays = {0: "poniedzialek",
                1: "wtorek",
                2: "sroda",
                3: "czwartek",
                4: "piatek",
                5: "sobota",
                6: "niedziela"}

    if dt is None:
        dt = datetime.datetime.now()

    weekday = weekdays[dt.weekday()]
    current_time = dt.time()

    closest_weekday = weekday if dt.weekday() < 5 else "poniedzialek"

    day_sessions = timetable_df[timetable_df["dzien_tygodnia"] == closest_weekday].copy()
    day_sessions["start_time"] = day_sessions["godzina_rozp"].apply(parse_hour_min)
    day_sessions["end_time"] = day_sessions["godzina_zak"].apply(parse_hour_min)

    if current_time > day_sessions["end_time"].iloc[-1]:
        next_day_index = dt.weekday() + 1
        while next_day_index >= 7 or weekdays[next_day_index] in ["sobota", "niedziela"]:
            next_day_index += 1
            if next_day_index >= 7:
                next_day_index = 0
        closest_weekday = weekdays[next_day_index]
        day_sessions = timetable_df[timetable_df["dzien_tygodnia"] == closest_weekday].copy()
        day_sessions["start_time"] = day_sessions["godzina_rozp"].apply(parse_hour_min)
        day_sessions["end_time"] = day_sessions["godzina_zak"].apply(parse_hour_min)
        closest_session = day_sessions.iloc[0]

    elif current_time < day_sessions["start_time"].iloc[0]:
        closest_session = day_sessions.iloc[0]

    else:
        ongoing_sessions = day_sessions[(current_time >= day_sessions["start_time"]) &
                                        (current_time <= day_sessions["end_time"])]
        if not ongoing_sessions.empty:
            closest_session = ongoing_sessions.iloc[0]
        else:
            future_sessions = day_sessions[day_sessions["start_time"] > current_time]
            closest_session = future_sessions.iloc[0]

    return closest_session