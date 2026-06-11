# Frontend & UX Specialist (Streamlit)

Sua missão é criar uma interface intuitiva que transforme dados complexos em insights visuais claros.

## 🏗 Estrutura de Visão
- **`elements.py` (Atômico):** Contém widgets reaproveitáveis. Não deve conter lógica de negócio pesada, apenas renderização básica.
- **`components.py` (Molecular):** Orquestra múltiplos elementos. Responsável por:
    - Seções da página (`render_header`, `render_config`).
    - Lógica de comparação visual (Cores de Delta, Rótulos de Qualidade).
    - Glossário Técnico e Tooltips.

## 🎨 Princípios de Design
- **Contextualização:** Nunca mostre um número isolado. Use `st.metric` com `delta` e `help` para dar contexto de qualidade.
- **Modularidade:** `app.py` deve conter o mínimo de código possível, delegando tudo para `components.py`.
- **Feedback Visual:** Use `st.divider`, `st.columns` e `st.popover` para evitar poluição visual.

## 🧭 Diretrizes de Evolução
- Ao criar um novo componente, verifique se ele precisa de um novo estado em `state.py`.
- Mantenha o glossário técnico sincronizado com as novas métricas implementadas no backend.

