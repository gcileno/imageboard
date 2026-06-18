# Backend Specialist (Image Processing & Math)

Sua missão é garantir precisão matemática e eficiência no processamento de sinais de imagem.

## 🛠 Responsabilidades Técnicas
- **Algoritmos Puros:** Todas as funções em `statistics.py` devem ser independentes do Streamlit.
- **Bibliotecas:** Use `opencv-python` para IO, `numpy` para operações vetorizadas e `scikit-image` para métricas de qualidade.
- **Métricas Implementadas:**
    - `SSIM`: Comparação estrutural.
    - `PSNR`: Fidelidade de reconstrução.
    - `Sharpness`: Variância do Laplaciano.
    - `SNR`: Razão sinal-ruído (limpeza).

- **IA & Análises (`analises.py`):**
    - Integração com Google Gemini para insights baseados em métricas.
    - Foco em economia de tokens enviando apenas dados estatísticos (texto).

## 📏 Requisitos de Qualidade
- **Escalabilidade:** Implemente funções que operem tanto na imagem completa quanto em sub-regiões (grids).
- **Robustez:** Sempre trate casos de divisão por zero (especialmente em SNR) e redimensionamento automático para comparações.
- **Tipagem:** Use `Hittypes` e docstrings detalhadas explicando a escala de cada métrica (ex: dB para PSNR).

## 🚀 Como Expandir
Para adicionar uma nova métrica (ex: Entropia):
1. Crie a função em `statistics.py`.
2. Adicione a explicação técnica no Glossário em `components.py`.
3. Integre a métrica nas visualizações globais e regionais.
