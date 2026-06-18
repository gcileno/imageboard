import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

def display_combined_histogram(processed_images: Dict[str, Any]):
    """
    Renders a unified histogram for all processed images.
    """
    if not processed_images:
        return
        
    all_data = []
    for key, data in processed_images.items():
        hist = data["hist"]
        label = data["label"]
        df_temp = pd.DataFrame({
            "Intensity": range(256),
            "Frequency": hist,
            "Image": label
        })
        all_data.append(df_temp)
    
    df = pd.concat(all_data, ignore_index=True)
    fig = px.line(
        df, 
        x="Intensity", 
        y="Frequency", 
        color="Image", 
        title="📊 Comparativo de Histogramas (Escala de Cinza)",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_layout(
        height=450, 
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

def display_combined_stats_chart(processed_images: Dict[str, Any]):
    """
    Renders a grouped bar chart comparing general statistics across all images.
    """
    if not processed_images:
        return

    data_list = []
    for key, data in processed_images.items():
        stats = data["stats"]
        label = data["label"]
        
        # Mapping internal keys to friendly names
        metrics_map = {
            "mean": "Brilho (Média)",
            "std": "Contraste (Std Dev)",
            "sharpness": "Nitidez (Laplacian)",
            "snr": "SNR (Sinal-Ruído)"
        }
        
        for metric_key, metric_name in metrics_map.items():
            data_list.append({
                "Image": label,
                "Métrica": metric_name,
                "Valor": stats[metric_key]
            })

    df = pd.DataFrame(data_list)
    
    fig = px.bar(
        df,
        x="Métrica",
        y="Valor",
        color="Image",
        barmode="group",
        title="📊 Comparativo de Estatísticas Gerais",
        color_discrete_sequence=px.colors.qualitative.Safe,
        text_auto='.1f'
    )
    
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=None,
        yaxis_title="Valor"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_quality_comparison_chart(comparison_data: List[Dict[str, Any]], ref_label: str):
    """
    Renders a dual-axis bar chart for SSIM and PSNR comparison.
    """
    if not comparison_data:
        return

    df = pd.DataFrame(comparison_data)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # SSIM Bars (Primary Y)
    fig.add_trace(
        go.Bar(
            x=df["Label"], 
            y=df["SSIM"], 
            name="SSIM (Estrutura)",
            marker_color='#27ae60',
            text=df["SSIM"].map('{:.3f}'.format),
            textposition='outside',
        ),
        secondary_y=False,
    )

    # PSNR Bars (Secondary Y)
    fig.add_trace(
        go.Bar(
            x=df["Label"], 
            y=df["PSNR"], 
            name="PSNR (Fidelidade dB)",
            text=df["PSNR"].map('{:.1f}'.format),
            textposition='outside',
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title={
            'text': f"🏆 Fidelidade Técnica (Referência: {ref_label})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        barmode='group',
        height=450,
        margin=dict(l=20, r=20, t=100, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_yaxes(title_text="<b>SSIM</b> (0 a 1)", secondary_y=False, range=[0, 1.2])
    
    # Scale PSNR starting from 0 to avoid visual "equality"
    max_psnr = df["PSNR"].max() if not df.empty else 50
    fig.update_yaxes(title_text="<b>PSNR</b> (dB)", secondary_y=True, range=[0, max_psnr * 1.3])

    st.plotly_chart(fig, use_container_width=True)

def display_quality_radial_chart(comparison_data: List[Dict[str, Any]], ref_label: str):
    """
    Renders radial gauge charts for SSIM comparison.
    The reference is implicitly 100%. Target images are shown relative to it.
    """
    if not comparison_data:
        return

    st.write(f"### 🎯 Fidelidade Estrutural (Ref: {ref_label})")
    
    # Grid for multiple gauges
    cols = st.columns(len(comparison_data))
    
    for i, data in enumerate(comparison_data):
        with cols[i]:
            ssim_pct = data["SSIM"] * 100
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = ssim_pct,
                title = {'text': f"vs {data['Label']}", 'font': {'size': 16}},
                number = {'suffix': "%", 'font': {'size': 20}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#27ae60"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 90], 'color': '#f1c40f'}, # Warning
                        {'range': [90, 100], 'color': '#2ecc71'} # Good
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 95
                    }
                }
            ))
            
            fig.update_layout(
                height=250, 
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                font={'color': "darkblue", 'family': "Arial"}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.caption(f"PSNR: {data['PSNR']:.1f} dB")

def display_ssim_ring(comparison_data: List[Dict[str, Any]], ref_label: str):
    """
    Renders a radial ring chart for SSIM comparison.
    Reference image is 100%. Targets are shown relative to it.
    """
    labels = [ref_label] + [d["Label"] for d in comparison_data]
    values = [100.0] + [d["SSIM"] * 100.0 for d in comparison_data]
    
    fig = go.Figure()
    colors = px.colors.qualitative.Safe
    
    for i, (val, label) in enumerate(zip(values, labels)):
        # Each image gets its own "track"
        radius = len(values) - i
        arc_length = val * 3.6
        fig.add_trace(go.Barpolar(
            r=[radius],
            theta=[arc_length / 2], # Center of the arc
            width=[arc_length], # Length of the arc
            marker_color=colors[i % len(colors)],
            name=f"{label} ({val:.1f}%)",
            hovertemplate=f"<b>{label}</b>: {val:.1f}%<extra></extra>"
        ))
    
    fig.update_layout(
        title="✨ Fidelidade Estrutural (SSIM %)",
        polar=dict(
            radialaxis=dict(visible=False, range=[0, len(values) + 1]),
            angularaxis=dict(
                direction="clockwise",
                rotation=90,
                tickvals=[0, 90, 180, 270],
                ticktext=["0%", "25%", "50%", "75%"],
                gridcolor="rgba(0,0,0,0.1)"
            )
        ),
        showlegend=True,
        height=400,
        margin=dict(l=40, r=40, t=80, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)


def display_quality_gauges(comparison_data: List[Dict[str, Any]], ref_label: str):
    """
    Renders an elegant horizontal bar chart for SSIM and PSNR comparison.
    PSNR is normalized to 0-1 (with 50dB as 1.0).
    Scale: <0.70 (Ruim), 0.7-0.85 (Aceitável), 0.85-0.95 (Bom), >0.95 (Excelente).
    """
    if not comparison_data:
        return

    st.write(f"#### 🎯 Fidelidade vs {ref_label}")
    
    for data in comparison_data:
        target_label = data["Label"]
        ssim_val = data["SSIM"]
        psnr_val = data["PSNR"]
        psnr_norm = min(psnr_val / 50.0, 1.0) if psnr_val != float('inf') else 1.0
        
        # Professional color palette
        colors = {
            "Excelente": "#27ae60", # Emerald
            "Bom": "#78b159",       # Soft Green
            "Aceitável": "#f1c40f", # Sunflower Yellow
            "Ruim": "#e67e22"        # Soft Orange instead of aggressive red
        }
        
        # Lighter background colors
        bg_colors = {
            "Excelente": "#f1fcf6",
            "Bom": "#f7fcf0",
            "Aceitável": "#fffdf0",
            "Ruim": "#fff7f0"
        }

        def get_status_info(val):
            if val >= 0.95: return "Excelente", colors["Excelente"]
            if val >= 0.85: return "Bom", colors["Bom"]
            if val >= 0.70: return "Aceitável", colors["Aceitável"]
            return "Ruim", colors["Ruim"]

        ssim_status, ssim_color = get_status_info(ssim_val)
        psnr_status, psnr_color = get_status_info(psnr_norm)

        fig = go.Figure()

        # Background ranges (shapes)
        ranges = [
            (0, 0.70, bg_colors["Ruim"]),
            (0.70, 0.85, bg_colors["Aceitável"]),
            (0.85, 0.95, bg_colors["Bom"]),
            (0.95, 1.0, bg_colors["Excelente"])
        ]

        for r_start, r_end, r_color in ranges:
            fig.add_shape(
                type="rect", x0=r_start, x1=r_end, y0=-0.5, y1=1.5,
                fillcolor=r_color, line=dict(width=0), layer="below"
            )

        # SSIM Bar
        fig.add_trace(go.Bar(
            y=["SSIM"],
            x=[ssim_val],
            orientation='h',
            marker=dict(color=ssim_color, line=dict(color="#2c3e50", width=1.5)),
            text=f" <b>{ssim_val*100:.1f}%</b> ({ssim_status})",
            textposition='outside',
            cliponaxis=False,
            hovertemplate=f"<b>SSIM: {ssim_val*100:.2f}%</b><br>Status: {ssim_status}<extra></extra>"
        ))

        # PSNR Bar
        fig.add_trace(go.Bar(
            y=["PSNR"],
            x=[psnr_norm],
            orientation='h',
            marker=dict(color=psnr_color, line=dict(color="#2c3e50", width=1.5)),
            text=f" <b>{psnr_val:.1f} dB</b> ({psnr_status})",
            textposition='outside',
            cliponaxis=False,
            hovertemplate=f"<b>PSNR: {psnr_val:.1f} dB</b><br>Normalizado: {psnr_norm:.2f}<br>Status: {psnr_status}<extra></extra>"
        ))

        fig.update_layout(
            height=180,
            margin=dict(l=70, r=120, t=50, b=30), # Increased T for annotations and R for text
            xaxis=dict(
                range=[0, 1.05], 
                tickvals=[0, 0.7, 0.85, 0.95, 1.0],
                ticktext=["0", "0.7", "0.85", "0.95", "1.0"],
                showgrid=True,
                gridcolor="rgba(0,0,0,0.05)",
                zeroline=False
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(size=12, color="#2c3e50", family="Arial Black")
            ),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title=dict(
                text=f"📊 Comparação: <b>{target_label}</b>", 
                font=dict(size=15), 
                x=0.01,
                y=0.95
            )
        )
        
        # Add labels for categories at the top
        annotations = [
            dict(x=0.35, y=1.2, yref="paper", text="Ruim", showarrow=False, font=dict(size=11, color="#e67e22", family="Arial Black")),
            dict(x=0.775, y=1.2, yref="paper", text="Aceitável", showarrow=False, font=dict(size=11, color="#d4ac0d", family="Arial Black")),
            dict(x=0.90, y=1.2, yref="paper", text="Bom", showarrow=False, font=dict(size=11, color="#78b159", family="Arial Black")),
            dict(x=0.975, y=1.2, yref="paper", text="Excelente", showarrow=False, font=dict(size=11, color="#27ae60", family="Arial Black"))
        ]
        fig.update_layout(annotations=annotations)

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def display_regional_radar_chart(all_metrics: List[Dict[str, Any]]):
    """
    Renders a Radar Chart comparing multiple images across regional metrics.
    Metrics are normalized for visual comparison.
    """
    if not all_metrics:
        return

    fig = go.Figure()

    categories = ['Brilho', 'Contraste', 'Nitidez', 'SNR', 'SSIM', 'PSNR']
    
    # Calculate max sharpness for normalization in this specific view
    max_sharp = max([m.get('sharpness', 0) for m in all_metrics]) if all_metrics else 1
    if max_sharp == 0: max_sharp = 1

    for m in all_metrics:
        label = m['label']
        
        # Normalization logic
        v_mean = m['mean'] / 255.0
        v_std = min(m['std'] / 100.0, 1.0)
        v_sharp = m['sharpness'] / max_sharp
        v_snr = min(m['snr'] / 40.0, 1.0)
        v_ssim = m.get('ssim', 1.0)
        v_psnr = min(m.get('psnr', 50.0) / 50.0, 1.0) if m.get('psnr') != float('inf') else 1.0
        
        values = [v_mean, v_std, v_sharp, v_snr, v_ssim, v_psnr]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=label,
            hovertemplate=f"<b>{label}</b><br>" + 
                          "<br>".join([f"{cat}: {val:.3f}" for cat, val in zip(categories, values)]) +
                          "<extra></extra>"
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1.1],
                showticklabels=False,
                gridcolor="rgba(0,0,0,0.1)"
            ),
            angularaxis=dict(
                gridcolor="rgba(0,0,0,0.1)",
                linecolor="gray",
                tickfont=dict(size=14)
            )
        ),
        showlegend=True,
        height=600,
        margin=dict(l=60, r=60, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=12)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

def display_stats_table(stats: Dict[str, float], label: str):
    """
    Displays basic stats in a clean format.
    """
    st.write(f"**General Statistics - {label}**")
    # Transposing the dataframe makes it easier to read multiple metrics
    df = pd.DataFrame([stats]).T
    df.columns = ["Value"]
    st.table(df)

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
