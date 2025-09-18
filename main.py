import streamlit as st

def main():

    page_1 = st.Page("page_1.py", title="Aktualny status świetlicy")
    page_2 = st.Page("page_2.py", title="Status świetlicy w wybranym terminie")
    page_3 = st.Page("page_3.py", title="Modyfikacja stanu klas")

    pg = st.navigation([page_1, page_2, page_3], expanded=True)

    pg.run()

if __name__ == "__main__":
    main()