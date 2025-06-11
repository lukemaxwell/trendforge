# auth.py

import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import os
import logging


logger = logging.getLogger(__name__)
logger.info("auth.py")


# Initialize Firebase Admin SDK once globally
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
    })
    firebase_admin.initialize_app(cred)


# Verify Firebase ID token
def verify_firebase_token(id_token):
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        logger.warning("❌ Token verification failed:", e)
        return None

# Authenticate user from query param and store in session
def authenticate_user():
    # If user already in session → use it
    if "user" in st.session_state:
        return st.session_state["user"]

    # Else → try to read token param
    token_list = st.query_params.get("token", [])

    if not token_list:
        return None

    id_token = token_list[0]
    user = verify_firebase_token(id_token)

    if user:
        st.session_state["user"] = user
        # Clean URL to remove token param (prevents re-auth loop)
        st.query_params.clear()
        return user
    else:
        return None

# Helper → get current user anywhere
def get_current_user():
    return st.session_state.get("user")

# Helper → require login (call this in your main.py or pages)
def require_login():
    user = authenticate_user()

    if not user:
        st.warning("Please log in to use this app.")
        st.stop()

    return user
