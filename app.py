import streamlit as st
from auth0_component import login_button
from config import AUTH0_CLIENT_ID, AUTH0_DOMAIN


gist = st.Page(
    "Gist_Creator.py", title="Gist Creator", icon=":material/robot_2:"
)
about = st.Page(
    "About.py", title="About", icon=":material/waving_hand:"
)

pg = st.navigation(
{
    "": [gist, about],
}
)
pg.run()

# Get the Auth0 client ID and domain from environment variables


# Use the login button to get user info
with st.sidebar:
    # st.divider()
    user_info = login_button(AUTH0_CLIENT_ID, domain=AUTH0_DOMAIN)

# Store the user info in session state if it's not None
if user_info:
    st.session_state.user_info = user_info

# Check if user info exists in session state and display it
if "user_info" in st.session_state and user_info:
    with st.sidebar:
        st.write(f"Welcome, {user_info['name']}")
