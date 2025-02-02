import streamlit as st

landing_page = st.Page(
    page="views/home_page.py",
    title="SEDVT",
    icon=":material/home:",
    default=True,
)
geographical_page = st.Page(
    page="views/geographical_data.py",
    title="Geographical Data",
    icon=":material/map:",
)
data_preparation = st.Page(
    page="views/data_preparation.py",
    title="Data Preparation",
    icon=":material/data_object:",
)
data_prediction = st.Page(
    page="views/data_prediction.py",
    title="Data Prediction",
    icon=":material/calculate:",
)
assistance_page = st.Page(
    page="views/assistance.py",
    title="Assistance Page",
    icon=":material/live_help:",
)
chatbot_page = st.Page(
    page="chat_bot.py",
    title="AI Chatbot",
    icon=":material/chat:",
)
# pg = st.navigation(pages=[landing_page, geographical_page])
pg = st.navigation(
    {
        "Home": [landing_page],
        "Pages": [geographical_page, data_preparation, data_prediction, assistance_page],
        "Live Chat": [chatbot_page],
    }
)

# st.sidebar.text("")

pg.run()