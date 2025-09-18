import streamlit as st
import datetime
from utils import load_dataframes, get_closest_session

st.title("Aktualny status świetlicy")

timetable_df, students_df = load_dataframes()
closest_session = get_closest_session(timetable_df, datetime.datetime(2025, 9, 16, 15, 1))

st.text(f"Najbliższa sesja: {closest_session['dzien_tygodnia']} {closest_session['godzina_rozp']}-{closest_session['godzina_zak']}")