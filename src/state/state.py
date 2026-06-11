import streamlit as st


def initialize_state():
    """Initializes the streamlit session state for non-widget values."""
    if "grid" not in st.session_state:
        st.session_state["grid"] = 10
    
    if "image_keys" not in st.session_state:
        st.session_state["image_keys"] = ["image_a", "image_b"]

    if "selected_cell" not in st.session_state:
        st.session_state["selected_cell"] = None


def set_grid_value(value):
    """Explicitly updates the grid value in the state."""
    st.session_state["grid"] = value