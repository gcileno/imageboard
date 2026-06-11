import streamlit as st
from typing import Dict, Any, List
from src.view.elements import (
    select_image, 
    show_image,
    range_gride, 
    add_image, 
    remove_image, 
    display_histogram, 
    display_stats_table
)
from src.services.statistics import (
    process_to_grayscale, 
    calculate_histogram, 
    get_basic_stats, 
    draw_grid_overlay,
    calculate_ssim,
    calculate_psnr
)

def render_header():
    st.title("🖼️ Image Compare")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(
            "Faça o upload de imagens para comparar estatísticas em escala de cinza."
        )
    with col2:
        with st.popover("📖 Glossário Técnico"):
            st.markdown("""
            ### Importância das Métricas no Projeto
            Este projeto visa analisar a fidelidade e o ruído em fotos de "Modo Escuro". Entenda como cada dado ajuda nessa avaliação:
            
            *   **Média (Mean):** Indica o nível de exposição. Em fotos noturnas, ajuda a identificar se o software da câmera está "forçando" um brilho artificial que pode gerar ruído.
            *   **Desvio Padrão (Std Dev):** Representa o contraste global. Uma queda drástica nesta métrica em relação a uma foto de referência indica perda de profundidade e "achatamento" de tons.
            *   **SSIM (Similaridade Estrutural):** É a métrica mais próxima da percepção humana. Ela detecta se a compressão ou o processamento do modo escuro está destruindo texturas e formas naturais da imagem.
            *   **PSNR (Fidelidade):** Mede a qualidade da reconstrução da imagem. Valores baixos indicam que o processamento introduziu artefatos digitais ou distorções visíveis em relação ao original.
            *   **Nitidez (Laplacian Variance):** Crucial para fotos noturnas. Mede se o foco foi mantido. O processamento excessivo para remover ruído costuma "borrar" a imagem, o que é detectado aqui.
            *   **SNR (Sinal-Ruído):** Quantifica a pureza da imagem. Em câmeras de celular, um SNR baixo significa uma imagem "granulada", onde o ruído eletrônico está competindo com os detalhes reais da cena.
            """)

def render_config_section():
    st.divider()
    config_col1, config_col2 = st.columns([2, 1])

    with config_col1:
        range_gride()
        grid_size = st.session_state["grid"]

    with config_col2:
        # Layout hack for buttons to be side by side if needed, 
        # but elements.py buttons are full width or stretch
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            add_image()
        with btn_col2:
            remove_image()
    
    st.divider()
    return grid_size

def render_image_analysis(image_keys: List[str], grid_size: int) -> Dict[str, Any]:
    cols = st.columns(len(image_keys))
    processed_images = {}

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
                stats["sharpness"] = float(calculate_sharpness_val(gray_img))
                stats["snr"] = float(calculate_snr_val(gray_img))
                
                display_histogram(hist, label)
                display_stats_table(stats, label)
                
                processed_images[key] = {
                    "img": gray_img,
                    "label": label,
                    "stats": stats
                }
    return processed_images

def render_comparison_metrics(processed_images: Dict[str, Any]):
    if len(processed_images) < 2:
        return

    st.divider()
    st.header("📊 Comparação de Qualidade Global")
    st.markdown("Comparação técnica baseada na primeira imagem como referência.")
    
    keys = list(processed_images.keys())
    ref_key = keys[0]
    ref_data = processed_images[ref_key]
    
    for i in range(1, len(keys)):
        target_key = keys[i]
        target_data = processed_images[target_key]
        
        st.subheader(f"Referência: {ref_data['label']} vs {target_data['label']}")
        m_col1, m_col2 = st.columns(2)
        
        ssim_val = calculate_ssim(ref_data['img'], target_data['img'])
        psnr_val = calculate_psnr(ref_data['img'], target_data['img'])
        
        # Ranges para SSIM: > 0.95 Excelente, 0.90-0.95 Bom, < 0.90 Perda de Qualidade
        ssim_label = "Excelente" if ssim_val > 0.95 else ("Bom" if ssim_val > 0.90 else "Degradado")
        ssim_color = "normal" if ssim_val > 0.90 else "inverse"
        
        # Ranges para PSNR: > 40 Excelente, 30-40 Bom, < 30 Ruído visível
        psnr_label = "Excelente" if psnr_val > 40 else ("Bom" if psnr_val > 30 else "Ruído Alto")
        psnr_color = "normal" if psnr_val > 30 else "inverse"

        m_col1.metric("SSIM (Estrutura)", f"{ssim_val:.4f}", delta=ssim_label, delta_color=ssim_color, 
                      help="Índice de Similaridade Estrutural. Acima de 0.95 indica preservação excelente de texturas.")
        m_col2.metric("PSNR (Fidelidade)", f"{psnr_val:.2f} dB", delta=psnr_label, delta_color=psnr_color,
                      help="Relação Sinal-Ruído de Pico. Acima de 30dB é o padrão para boa qualidade em fotografia digital.")

def render_interactive_grid(processed_images: Dict[str, Any], grid_size: int):
    if not processed_images:
        return

    st.divider()
    st.header("🔬 Análise Regional Interativa")
    st.info(f"Foco na célula para análise de micro-detalhes. Grade atual: {grid_size}x{grid_size}")

    # Single Cell Selection (1-based index)
    max_cells = grid_size * grid_size
    cell_idx = st.number_input("Célula Selecionada", 1, max_cells, 1, key="cell_idx_input")

    # Convert 1-based index to 0-based row/col
    idx_0 = cell_idx - 1
    row_sel = idx_0 // grid_size
    col_sel = idx_0 % grid_size

    comp_cols = st.columns(len(processed_images))
    
    ref_key = list(processed_images.keys())[0]
    ref_data = processed_images[ref_key]
    
    h_ref, w_ref = ref_data["img"].shape
    ch_ref, cw_ref = h_ref // grid_size, w_ref // grid_size
    y1_ref, y2_ref = row_sel * ch_ref, (row_sel + 1) * ch_ref
    x1_ref, x2_ref = col_sel * cw_ref, (col_sel + 1) * cw_ref
    ref_cell = ref_data["img"][y1_ref:y2_ref, x1_ref:x2_ref]
    ref_sharpness = float(calculate_sharpness_val(ref_cell))
    ref_snr = float(calculate_snr_val(ref_cell))

    for i, (key, data) in enumerate(processed_images.items()):
        with comp_cols[i]:
            h, w = data["img"].shape
            ch, cw = h // grid_size, w // grid_size
            y1, y2 = row_sel * ch, (row_sel + 1) * ch
            x1, x2 = col_sel * cw, (col_sel + 1) * cw

            cell_data = data["img"][y1:y2, x1:x2]
            cell_stats = get_basic_stats(cell_data)
            
            from src.services.statistics import calculate_sharpness, calculate_snr, calculate_ssim, calculate_psnr
            cur_sharpness = calculate_sharpness(cell_data)
            cur_snr = calculate_snr(cell_data)

            st.write(f"**{data['label']} - Cell {cell_idx}**")
            
            s_col1, s_col2 = st.columns(2)
            s_col1.metric("Brilho (Média)", f"{cell_stats['mean']:.1f}", help="Ideal em modo escuro: 30-80 (evita 'clipping').")
            s_col2.metric("Contraste (Std)", f"{cell_stats['std']:.1f}", help="Maior valor = mais separação entre luz e sombra.")
            
            s_col3, s_col4 = st.columns(2)
            # Sharpness comparison delta
            sharp_delta = f"{((cur_sharpness/ref_sharpness)-1)*100:.1f}%" if ref_sharpness > 0 else None
            s_col3.metric("Nitidez (Lap)", f"{cur_sharpness:.0f}", delta=sharp_delta, 
                          help="Preservação de bordas. Delta negativo indica perda de foco ou suavização excessiva.")
            
            # SNR comparison delta
            snr_delta = f"{cur_snr - ref_snr:.1f}" if i > 0 else None
            s_col4.metric("SNR (Limpeza)", f"{cur_snr:.1f}", delta=snr_delta, 
                          help="Pureza do sinal. Valores menores que 5 indicam ruído crítico em áreas escuras.")
            
            if key != ref_key:
                s_col5, s_col6 = st.columns(2)
                c_ssim = calculate_ssim(ref_cell, cell_data)
                c_psnr = calculate_psnr(ref_cell, cell_data)
                
                ssim_label = "Ok" if c_ssim > 0.9 else "Atenção"
                psnr_label = "Limpo" if c_psnr > 30 else "Ruído"
                
                s_col5.metric("Simil. Local", f"{c_ssim:.3f}", delta=ssim_label, 
                              help="Fidelidade estrutural da região vs referência.")
                s_col6.metric("Fid. Local", f"{c_psnr:.1f}dB", delta=psnr_label, 
                              help="Fidelidade de reconstrução. <20dB indica artefatos graves.")

            st.image(cell_data, caption=f"Zoom Célula {cell_idx}", use_container_width=True)

# Helper functions for the render_image_analysis to avoid circular or missing imports
def calculate_sharpness_val(img):
    from src.services.statistics import calculate_sharpness
    return calculate_sharpness(img)

def calculate_snr_val(img):
    from src.services.statistics import calculate_snr
    return calculate_snr(img)
