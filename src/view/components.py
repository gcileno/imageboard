import streamlit as st
from typing import Dict, Any, List
from src.view.elements import (
    select_image, 
    show_image,
    range_gride, 
    add_image, 
    remove_image, 
    display_combined_histogram,
    display_combined_stats_chart,
    display_quality_gauges,
    display_regional_radar_chart
)
from src.services.statistics import (
    process_to_grayscale, 
    calculate_histogram, 
    get_basic_stats, 
    draw_grid_overlay,
    calculate_ssim,
    calculate_psnr,
    calculate_sharpness,
    calculate_snr
)
from src.services.analises import analyze_metrics_with_ai

def render_header():
    st.title("🖼️ Image Compare")
    st.write(
        "Faça o upload de imagens para comparar estatísticas em escala de cinza."
    )

def render_config_section():
    with st.container(border=True):
        st.markdown("### ⚙️ Painel de Configuração")
        config_col1, config_col2 = st.columns([2, 1])

        with config_col1:
            range_gride()
            grid_size = st.session_state["grid"]

        with config_col2:
            st.write("") # vertical spacing alignment
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                add_image()
            with btn_col2:
                remove_image()
    return grid_size

def render_image_analysis(image_keys: List[str], grid_size: int) -> Dict[str, Any]:
    processed_images = {}
    
    with st.container(border=True):
        st.markdown("### 🖼️ Gerenciamento e Visualização de Imagens")
        cols = st.columns(len(image_keys))

        for idx, key in enumerate(image_keys):
            with cols[idx]:
                label = key.replace("_", " ").title()
                select_image(key_element=key, label=label)
                
                uploaded_file = st.session_state.get(key)
                if uploaded_file is not None:
                    gray_img = process_to_grayscale(uploaded_file.getvalue())
                    
                    # Show image with grid overlay
                    grid_img = draw_grid_overlay(gray_img, grid_size)
                    show_image(grid_img, label, caption=f"{label} (Grid {grid_size}x{grid_size})")
                    
                    # Basic Stats & Histogram
                    hist = calculate_histogram(gray_img)
                    stats = get_basic_stats(gray_img)
                    
                    # Add extra global stats
                    stats["sharpness"] = float(calculate_sharpness(gray_img))
                    stats["snr"] = float(calculate_snr(gray_img))
                
                    processed_images[key] = {
                        "img": gray_img,
                        "label": label,
                        "stats": stats,
                        "hist": hist
                    }
    return processed_images

def render_comparison_metrics(processed_images: Dict[str, Any]):
    if not processed_images:
        return

    with st.container(border=True):
        st.markdown("### 📊 Estatísticas Globais e Qualidade")
        
        # 0. Calculate Quality Metrics (SSIM / PSNR) if reference exists
        comparison_data = []
        ref_label = ""
        if len(processed_images) >= 2:
            keys = list(processed_images.keys())
            ref_key = keys[0]
            ref_data = processed_images[ref_key]
            ref_label = ref_data['label']

            for i in range(1, len(keys)):
                target_key = keys[i]
                target_data = processed_images[target_key]
                ssim_val = calculate_ssim(ref_data['img'], target_data['img'])
                psnr_val = calculate_psnr(ref_data['img'], target_data['img'])
                comparison_data.append({
                    "Label": target_data['label'],
                    "SSIM": ssim_val,
                    "PSNR": psnr_val
                })

        # 1. Unified Comparison Charts
        c1, c2 = st.columns(2)
        with c1:
            # Quality Gauges above Histogram
            if comparison_data:
                display_quality_gauges(comparison_data, ref_label)
            
            display_combined_histogram(processed_images)
            
        with c2:
            display_combined_stats_chart(processed_images)

    return

def render_interactive_grid(processed_images: Dict[str, Any], grid_size: int):
    if not processed_images:
        return

    with st.container(border=True):
        st.markdown("### 🔬 Análise Regional Interativa")
        
        c_config1, c_config2 = st.columns([1, 2])
        with c_config1:
            max_cells = grid_size * grid_size
            cell_idx = st.number_input("Célula Selecionada", 1, max_cells, 1, key="cell_idx_input")
        
        # Convert 1-based index to 0-based row/col
        idx_0 = cell_idx - 1
        row_sel = idx_0 // grid_size
        col_sel = idx_0 % grid_size

        # Prepare data for Radar Chart
        all_regional_metrics = []
        
        ref_key = list(processed_images.keys())[0]
        ref_data = processed_images[ref_key]
        h_ref, w_ref = ref_data["img"].shape
        ch_ref, cw_ref = h_ref // grid_size, w_ref // grid_size
        y1_ref, y2_ref = row_sel * ch_ref, (row_sel + 1) * ch_ref
        x1_ref, x2_ref = col_sel * cw_ref, (col_sel + 1) * cw_ref
        ref_cell = ref_data["img"][y1_ref:y2_ref, x1_ref:x2_ref]

        # Layout: Left for Images, Right for Radar Chart
        col_images, col_radar = st.columns([1, 2])

        with col_radar:
            st.subheader(f"📊 Radar de Métricas - Célula {cell_idx}")
            st.caption("Comparação normalizada de métricas técnicas (Brilho, Contraste, Nitidez, SNR, SSIM, PSNR).")
            # We need to loop once to collect all metrics
            for key, data in processed_images.items():
                h, w = data["img"].shape
                ch, cw = h // grid_size, w // grid_size
                y1, y2 = row_sel * ch, (row_sel + 1) * ch
                x1, x2 = col_sel * cw, (col_sel + 1) * cw
                cell_data = data["img"][y1:y2, x1:x2]
                
                stats = get_basic_stats(cell_data)
                from src.services.statistics import calculate_sharpness, calculate_snr, calculate_ssim, calculate_psnr
                sharp = calculate_sharpness(cell_data)
                snr = calculate_snr(cell_data)
                
                m_data = {
                    "label": data["label"],
                    "mean": stats["mean"],
                    "std": stats["std"],
                    "sharpness": sharp,
                    "snr": snr
                }
                
                if key != ref_key:
                    m_data["ssim"] = calculate_ssim(ref_cell, cell_data)
                    m_data["psnr"] = calculate_psnr(ref_cell, cell_data)
                else:
                    m_data["ssim"] = 1.0
                    m_data["psnr"] = 50.0 # Baseline
                    
                all_regional_metrics.append(m_data)
            
            display_regional_radar_chart(all_regional_metrics)

        with col_images:
            st.write(f"#### 🖼️ Recortes (Célula {cell_idx})")
            # Display images in a smaller grid or list
            img_cols = st.columns(2)
            for i, (key, data) in enumerate(processed_images.items()):
                h, w = data["img"].shape
                ch, cw = h // grid_size, w // grid_size
                y1, y2 = row_sel * ch, (row_sel + 1) * ch
                x1, x2 = col_sel * cw, (col_sel + 1) * cw
                cell_data = data["img"][y1:y2, x1:x2]
                
                with img_cols[i % 2]:
                    st.image(cell_data, caption=data["label"], use_container_width=True)

    return

def render_metrics_explanation():
    """
    Renders detailed documentation and interpretation guides for each metric.
    """
    st.divider()
    st.header("📚 Guia de Interpretação de Métricas")

    with st.expander("✨ SSIM (Structural Similarity Index)"):
        st.markdown("""
        **O que é:** Uma métrica que avalia a similaridade entre duas imagens focando em Luminância, Contraste e Estrutura, tentando imitar a percepção humana.
        
        **Como interpretar:**
        *   **1.0:** Imagens idênticas.
        *   **0.95 a 0.99:** Excelente qualidade, diferenças imperceptíveis ao olho humano.
        *   **Abaixo de 0.90:** Perda visível de texturas ou artefatos de compressão.
        
        **⚠️ Exceções e Cuidado (O Ponto Cego):**
        *   **Modo Escuro vs. Modo Claro:** O SSIM pune severamente mudanças globais de brilho. Se você comparar a mesma cena em modos de exposição diferentes, o SSIM será baixo, mesmo que a cena seja a mesma.
        *   **Desalinhamento:** Se a câmera tremer entre uma foto e outra (mesmo que 2 pixels), o SSIM cai drasticamente porque ele compara janelas fixas de pixels.
        *   **Prints vs. Fotos:** Um print de uma cena totalmente diferente pode ter um SSIM maior que uma foto real da mesma cena se o print tiver níveis de brilho e contraste mais próximos da referência.
        """)

    with st.expander("📉 PSNR (Peak Signal-to-Noise Ratio)"):
        st.markdown("""
        **O que é:** Mede a relação entre a potência máxima de um sinal e o ruído que afeta a sua fidelidade. É muito usado para medir a perda em compressão de imagem.
        
        **Como interpretar:**
        *   **Valores altos (30dB a 50dB):** Alta fidelidade em relação à referência.
        *   **Valores baixos (Abaixo de 25dB):** Presença de ruído digital ou artefatos pesados.
        *   **Infinito:** Indica que as imagens são matematicamente iguais.
        
        **Utilização:** No projeto, usamos para ver o quanto o processamento do "Modo Escuro" alterou os valores originais dos pixels.
        """)

    with st.expander("💡 Brilho Médio (Mean Intensity)"):
        st.markdown("""
        **O que é:** A média de todos os valores de pixel (0 a 255) da imagem ou célula.
        
        **Como interpretar:**
        *   **Próximo a 0:** Imagem muito escura (subexposta).
        *   **Próximo a 128:** Tons médios.
        *   **Próximo a 255:** Imagem muito clara (superexposta).
        
        **Utilização:** Ajuda a detectar se o software da câmera está "clareando" demais as sombras, o que costuma introduzir ruído.
        """)

    with st.expander("🌓 Contraste (Desvio Padrão)"):
        st.markdown("""
        **O que é:** Mede a dispersão dos valores de cinza. Quanto maior o desvio padrão, maior o contraste entre claros e escuros.
        
        **Como interpretar:**
        *   **Alto:** Imagem com "punch", pretos profundos e brancos definidos.
        *   **Baixo:** Imagem "lavada", cinzenta e sem profundidade.
        
        **Utilização:** Importante para ver se o Modo Escuro está mantendo a separação tonal ou se está "achatando" a imagem.
        """)

    with st.expander("🎯 Nitidez (Laplacian Variance)"):
        st.markdown("""
        **O que é:** Mede a quantidade de bordas e detalhes finos usando a variância do Laplaciano.
        
        **Como interpretar:**
        *   **Valor Alto:** Imagem nítida, com foco cravado e detalhes preservados.
        *   **Valor Baixo:** Imagem borrada, fora de foco ou com suavização excessiva via software (pós-processamento).
        
        **Utilização:** Identifica quando o algoritmo de redução de ruído "derrete" os detalhes finos da imagem para esconder o grão.
        """)

    with st.expander("🔊 SNR (Signal-to-Noise Ratio)"):
        st.markdown("""
        **O que é:** Razão entre a informação útil (sinal) e o ruído indesejado.
        
        **Como interpretar:**
        *   **Alto:** Imagem limpa e cristalina.
        *   **Baixo:** Imagem granulada, com "areia" digital visível.
        
        **Utilização:** Essencial para avaliar a qualidade de sensores em baixa luz. Um bom Modo Escuro deve manter o SNR alto sem sacrificar a Nitidez.
        """)

    with st.expander("📊 Histograma de Tons de Cinza"):
        st.markdown("""
        **O que é:** Um gráfico que mostra a distribuição da frequência de cada nível de brilho (de 0 a 255) na imagem.
        
        **Como interpretar:**
        *   **Pico à Esquerda (perto de 0):** Predomínio de tons escuros e pretos. Comum e esperado em interfaces Dark Mode.
        *   **Pico à Direita (perto de 255):** Predomínio de tons claros e brancos (áreas estouradas).
        *   **Distribuição Espalhada:** Indica uma imagem com alto contraste e grande variedade tonal.
        *   **Barras Isoladas (Gaps):** Podem indicar "posterização" ou perda de gradientes devido a um processamento digital agressivo.
        
        **Utilização:** No ImageBoard, o histograma ajuda a visualizar se o Modo Escuro está realmente preservando os pretos profundos ou se está elevando o piso de preto para um cinza escuro (gerando falta de contraste).
        """)

