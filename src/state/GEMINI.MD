# State Management Specialist

Sua missão é garantir que a aplicação seja reativa e mantenha a persistência necessária durante a sessão.

## 🗝 Chaves de Estado
- `grid` (int): Tamanho da grade de análise (ex: 10 para 10x10).
- `image_keys` (List[str]): Lista dinâmica de chaves para os slots de imagem.
- `cell_idx_input` (int): Célula selecionada atualmente para análise regional.

## 🛠 Boas Práticas
- **Inicialização:** Todas as chaves devem ser inicializadas em `initialize_state()` para evitar `KeyError`.
- **Persistência:** Use chaves de widget (como `key="grid"`) para que o Streamlit gerencie o estado automaticamente.
- **Reatividade:** Sempre que uma alteração estrutural ocorrer (ex: adicionar imagem), use `st.rerun()` para atualizar a UI.

## 🚀 Como Expandir
Se precisar rastrear um novo parâmetro global (ex: modo de comparação):
1. Adicione a inicialização em `state.py`.
2. Use o valor no componente correspondente via `st.session_state`.
