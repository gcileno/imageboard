# ImageBoard - Global Architecture & AI Guidelines

Este arquivo define a visão macro do projeto ImageBoard, um laboratório estatístico para análise de qualidade de imagem (foco em Modo Escuro).

## 🧩 Estrutura Modular
O projeto segue uma separação rigorosa de responsabilidades para facilitar o desenvolvimento assistido por IA:

- **Entry Point (`app.py`):** Apenas orquestra a renderização chamando componentes de alto nível.
- **UI Components (`src/view/components.py`):** Lógica de seções da página, organização de colunas e métricas visuais.
- **UI Elements (`src/view/elements.py`):** Widgets atômicos do Streamlit (botões, sliders, uploaders).
- **Backend/Statistics (`src/services/statistics.py` & `analises.py`):** Lógica pura de processamento de imagem e integração com IA (Gemini).
- **State Management (`src/state/state.py`):** Centralização do `st.session_state`.

## 🤖 AI Workflow (Vibe Coding)
Para expandir este projeto usando o Gemini CLI:
1. **Research:** Sempre valide as dimensões das imagens antes de operações comparativas (SSIM/PSNR).
2. **Strategy:** Mantenha a UI desacoplada da lógica estatística.
3. **Execution:** Novos modelos estatísticos devem ser funções puras em `services` antes de serem expostos na UI.

## 📄 Documentação Técnica
- [Instruções de Frontend](./src/view/GEMINI.md)
- [Instruções de Backend](./src/services/GEMINI.md)
- [Gestão de Estado](./src/state/GEMINI.MD)
