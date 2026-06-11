import streamlit as st
from src.state.state import initialize_state
from src.view.components import (
    render_header,
    render_config_section,
    render_image_analysis,
    render_comparison_metrics,
    render_interactive_grid
)

# 1. Page Configuration
st.set_page_config(
    page_title="Image Compare",
    layout="wide"
)

# 2. State Initialization
initialize_state()

# 3. Header
render_header()

# 4. Config Section (Grid Range, Add/Remove Images)
grid_size = render_config_section()

# 5. Image Upload and Analysis (Individual)
image_keys = st.session_state["image_keys"]
processed_images = render_image_analysis(image_keys, grid_size)

# 6. Global Comparison Metrics (SSIM, PSNR)
render_comparison_metrics(processed_images)

# 7. Interactive Grid Analysis (Cell zoom and metrics)
render_interactive_grid(processed_images, grid_size)
