import streamlit as st
from auth0_component import login_button
from helpers import build_markup_for_logo
from config import AUTH0_CLIENT_ID, AUTH0_DOMAIN


chat = st.Page(
    "file_chat.py", title="Gist creator", icon=":material/robot_2:"
)

pg = st.navigation(
{
    "Welcome!": [chat],
}
)
pg.run()

# Get the Auth0 client ID and domain from environment variables


# Use the login button to get user info
with st.sidebar:
    st.divider()
    user_info = login_button(AUTH0_CLIENT_ID, domain=AUTH0_DOMAIN)

# Store the user info in session state if it's not None
if user_info:
    st.session_state.user_info = user_info

# Check if user info exists in session state and display it
if "user_info" in st.session_state and user_info:
    with st.sidebar:
        st.write(f"Welcome, {user_info['name']}")


st.markdown(
    build_markup_for_logo("resources/logo.png"),
    unsafe_allow_html=True,
)