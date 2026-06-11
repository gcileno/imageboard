# 📸 ImageBoard: Dark Mode Analysis Explorer

> **Experimental Project** developed with the "Vibe Coding" philosophy using **Gemini CLI**.

An advanced statistical laboratory designed to dissect the effectiveness of smartphone camera "Dark Mode" processing. ImageBoard provides deep insights into how mobile ISP (Image Signal Processors) handle noise, structural integrity, and sharpness in low-light environments.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Gemini CLI](https://img.shields.io/badge/Built%20with-Gemini%20CLI-blue?style=for-the-badge)

## 🌌 The Mission
Mobile photography often hides aggressive noise reduction and artificial sharpening under the "Night Mode" label. This tool exposes the math behind the pixels, allowing enthusiasts and engineers to compare multiple shots (Reference vs. Dark Mode) through standardized metrics like SSIM, PSNR, and Laplacian Variance.

## 🚀 Key Features
- **Multi-Image Comparison:** Side-by-side analysis with dynamic slot management.
- **Interactive Grid System:** Divide images into granular cells (up to 20x20) to find exactly where the sensor failed.
- **Advanced Metrics:**
    - **SSIM (Structural Similarity):** Perception-based quality analysis.
    - **PSNR (Fidelity):** Measuring noise and compression artifacts in dB.
    - **SNR (Signal-to-Noise Ratio):** Quantifying the "cleanliness" of the dark areas.
    - **Laplacian Variance:** Detecting focus loss or excessive software blurring.
- **Visual Diagnostics:** Real-time histograms and quality deltas (Excellent/Good/Degraded).
- **Technical Glossary:** Built-in documentation for every metric.

## 🛠 Built with "Vibe Coding"
This project was entirely orchestrated using **Gemini CLI**, an agentic workflow where the developer focuses on intent and architecture while the AI handles the surgical implementation.

- **Modular Architecture:** Clean separation between `services` (logic), `view` (UI), and `state`.
- **Iterative Design:** Evolved from a simple histogram viewer to a complex regional analysis tool.

## 📦 Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/youruser/imageboard.git
   cd imageboard
   ```

2. **Setup environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Run the lab:**
   ```bash
   streamlit run app.py
   ```

## 🔬 How to use
1. **Upload a reference image** (ideally a shot with good lighting).
2. **Upload your Dark Mode test images**.
3. **Adjust the Grid Slider** to increase granularity.
4. **Inspect Cells:** Use the cell selector to zoom into shadows or highlights and check the **Local SSIM/PSNR**.
5. **Analyze the Delta:** Look for red indicators suggesting quality degradation or noise.

## 🤝 Contributing
Since this is an experimental project, feel free to fork, open issues, or suggest new statistical models (like NIQE or BRISQUE) to further enhance the analysis!

---
*Created during an experimental session with Gemini CLI - June 2026*
