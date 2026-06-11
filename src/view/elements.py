import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any

def select_image(key_element: str, label: str):
    """
    Renders an image uploader.
    Uses key_element to sync with st.session_state.
    """
    st.subheader(label.upper())

    st.file_uploader(
        f"Select {label}",
        type=["png", "jpg", "jpeg"],
        key=key_element
    )

def show_image(image_data: np.ndarray, label: str, caption: str = ""):
    """
    Displays an image (optionally with grid overlay) with a fixed width.
    """
    st.image(image_data, caption=caption if caption else label, width=400)

def display_histogram(hist_data: np.ndarray, label: str):
    """
    Renders a histogram chart using Plotly.
    """
    df = pd.DataFrame({"Intensity": range(256), "Frequency": hist_data})
    fig = px.line(df, x="Intensity", y="Frequency", title=f"Histogram - {label}")
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def display_stats_table(stats: Dict[str, float], label: str):
    """
    Displays basic stats in a clean format.
    """
    st.write(f"**Stats - {label}**")
    st.table(pd.DataFrame([stats]))

def range_gride():
    """
    Renders a slider to select the grid range for image analysis.
    Updates st.session_state['grid'] automatically.
    """
    st.select_slider(
        "Select analysis grid size",
        options=list(range(1, 21)),
        key="grid",
        help="Defines the granularity of the statistical analysis."
    )


def add_image():
    """
    Renders a button to add a new image slot to the analysis.
    Updates st.session_state['image_keys'] and triggers a rerun.
    """
    if st.button("➕ Add Image", width='stretch'):
        new_id = len(st.session_state["image_keys"])
        # Use a simple naming convention for new images
        new_key = f"image_{chr(97 + new_id)}" if new_id < 26 else f"image_{new_id}"
        st.session_state["image_keys"].append(new_key)
        st.rerun()

def remove_image():
    """
    Renders a button to remove the last image slot.
    Keeps at least one images. Triggers a rerun.
    """
    if st.button("➖ Remove Image", width='stretch'):
        if len(st.session_state["image_keys"]) > 1:
            st.session_state["image_keys"].pop()
            st.rerun()
        else:
            st.warning("Minimum of one image required.")
