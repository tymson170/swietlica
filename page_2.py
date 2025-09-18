import streamlit as st
import datetime
from utils import load_dataframes, get_closest_session

st.title("Status świetlicy dla wybranego terminu")
timetable_df, students_df = load_dataframes()

date = st.date_input('Wprowadź datę')
time = st.time_input('Wprowadź godzinę', value=None)
if date is not None and time is not None:
    dt = datetime.datetime.combine(date, time)
    closest_session = get_closest_session(timetable_df, dt)
    st.text(f"Najbliższa sesja: {closest_session['dzien_tygodnia']} {closest_session['godzina_rozp']}-{closest_session['godzina_zak']}")

