# pages/admin.py - PAINEL ADMIN COM FILE UPLOADER CORRIGIDO
import streamlit as st
import json
import os
import base64

st.set_page_config(page_title="Admin • Burger Express", page_icon="🔒", layout="centered")

# =============== CONFIGURAÇÃO DE CAMINHOS ===============
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRATOS_FILE = os.path.join(BASE_DIR, "pratos.json")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "images", "background-login.jpg")

# Função para converter imagem em base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Carregar imagem de background
background_b64 = get_base64_image(BACKGROUND_IMAGE)
if background_b64:
    background_css = f"url('data:image/jpeg;base64,{background_b64}')"
else:
    background_css = "url('https://images.unsplash.com/photo-1553979459-d2229ba7433b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80')"

st.markdown(f"""
<style>
    /* FUNDO PRINCIPAL */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), {background_css} center/cover fixed !important;
        background-attachment: fixed !important;
    }}
    
    /* TEXTO BRANCO GERAL */
    .stApp {{
        color: white !important;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: white !important;
    }}
    p, div, span {{
        color: white !important;
    }}
    
    /* FILE UPLOADER - TEXTO PRETO ESPECÍFICO */
    .stFileUploader * {{
        color: #000000 !important;
    }}
    .stFileUploader > div > div {{
        color: #000000 !important;
        background: white !important;
    }}
    .stFileUploader > div > div > div {{
        color: #000000 !important;
    }}
    .stFileUploader > div > div > small {{
        color: #000000 !important;
    }}
    div[data-testid="stFileUploader"] * {{
        color: #000000 !important;
    }}
    div[data-testid="stFileUploader"] > div > div {{
        color: #000000 !important;
    }}
    
    /* SELECTBOX - TEXTO PRETO */
    .stSelectbox * {{
        color: #000000 !important;
    }}
    .stSelectbox > div > div {{
        color: #000000 !important;
        background: white !important;
    }}
    .stSelectbox > div > div > div {{
        color: #000000 !important;
    }}
    div[data-testid="stSelectbox"] * {{
        color: #000000 !important;
    }}
    
    /* LABELS EM BRANCO */
    label {{
        color: white !important;
        font-weight: bold !important;
    }}
    
    /* INPUTS */
    .stTextInput > div > div > input {{
        color: #000000 !important;
        background: white !important;
    }}
    .stNumberInput > div > div > input {{
        color: #000000 !important;
        background: white !important;
    }}
    
    /* BOTÕES */
    .stButton > button {{
        background: #EA1D2C !important; 
        color: white !important; 
    }}
    
    /* CAIXA DE LOGIN */
    .login-box {{
        background: rgba(0,0,0,0.85) !important; 
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)

if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

if not st.session_state.admin_logado:
    st.markdown("""
    <div class="login-box" style="background: rgba(0,0,0,0.85); padding: 50px 60px; border-radius: 20px; text-align: center; max-width: 450px; margin: 100px auto;">
        <div style="font-size: 4.5rem; margin-bottom: 10px;">🍔</div>
        <h1 style="color: #EA1D2C; font-size: 2.5rem; font-weight: 700;">Área Restrita</h1>
        <p style="color:rgba(255,255,255,0.9);font-size:1.1rem;">Acesso exclusivo para administradores</p>
    </div>
    """, unsafe_allow_html=True)
    
    senha = st.text_input("Digite a senha", type="password", label_visibility="collapsed", placeholder="Senha de acesso")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Entrar", use_container_width=True):
            if senha == "123":
                st.session_state.admin_logado = True
                st.rerun()
            else:
                st.error("❌ Senha incorreta")
    with col2:
        if st.button("Voltar ao Site", use_container_width=True):
            st.switch_page("app.py")
else:
    st.markdown("<h1 style='color:white;text-align:center;margin-bottom:30px;'>🍔 Painel Administrativo</h1>", unsafe_allow_html=True)
    
    def carregar_pratos():
        if os.path.exists(PRATOS_FILE):
            try:
                with open(PRATOS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                st.error(f"❌ Erro ao carregar pratos: {e}")
                return []
        else:
            pratos_iniciais = [
                {"nome": "Burger Classic", "preco": 18.90, "cat": "hamburgers", "img": "burger-classic.jpg"},
                {"nome": "Burger Bacon", "preco": 22.90, "cat": "hamburgers", "img": "burger-bacon.jpg"},
                {"nome": "Double Cheese", "preco": 26.90, "cat": "hamburgers", "img": "cheese-duplo.jpg"},
                {"nome": "Refrigerante", "preco": 8.90, "cat": "bebidas", "img": "refri.jpg"},
                {"nome": "Suco Natural", "preco": 12.90, "cat": "bebidas", "img": "suco.jpg"},
            ]
            with open(PRATOS_FILE, "w", encoding="utf-8") as f:
                json.dump(pratos_iniciais, f, ensure_ascii=False, indent=2)
            return pratos_iniciais
    
    pratos = carregar_pratos()
    
    # =============== FORMULÁRIO DE CADASTRO ===============
    with st.form("cadastro_prato", clear_on_submit=True):
        st.subheader("➕ Cadastrar Novo Prato")
        
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Prato", placeholder="Ex: Burger Especial")
            preco = st.number_input("Preço (R$)", min_value=1.0, value=20.0, step=0.5, format="%.2f")
        with col2:
            categoria = st.selectbox(
                "Categoria",
                ["hamburgers", "bebidas", "acompanhamentos", "sobremesas"],
                format_func=lambda x: {
                    "hamburgers": "🍔 Hambúrgueres",
                    "bebidas": "🥤 Bebidas", 
                    "acompanhamentos": "🍟 Acompanhamentos",
                    "sobremesas": "🍰 Sobremesas"
                }[x]
            )
            imagem = st.file_uploader("Imagem do Prato", type=["jpg", "jpeg", "png"])
        
        submitted = st.form_submit_button("✅ Cadastrar Prato", type="primary")
        
        if submitted:
            if not nome:
                st.error("❌ Digite o nome do prato")
            elif not preco:
                st.error("❌ Digite o preço do prato")
            elif not imagem:
                st.error("❌ Selecione uma imagem")
            else:
                nomes_existentes = [p["nome"].lower() for p in pratos]
                if nome.lower() in nomes_existentes:
                    st.error("❌ Já existe um prato com este nome")
                else:
                    os.makedirs(IMAGES_DIR, exist_ok=True)
                    extensao = imagem.name.split('.')[-1]
                    nome_imagem = f"{nome.lower().replace(' ', '_')}.{extensao}"
                    caminho_imagem = os.path.join(IMAGES_DIR, nome_imagem)
                    
                    with open(caminho_imagem, "wb") as f:
                        f.write(imagem.getbuffer())
                    
                    novo_prato = {
                        "nome": nome,
                        "preco": float(preco),
                        "cat": categoria,
                        "img": nome_imagem
                    }
                    
                    pratos.append(novo_prato)
                    
                    with open(PRATOS_FILE, "w", encoding="utf-8") as f:
                        json.dump(pratos, f, ensure_ascii=False, indent=2)
                    
                    st.success(f"🎉 Prato '{nome}' cadastrado com sucesso!")
                    st.balloons()

    
    # =============== LISTA DE PRATOS CADASTRADOS ===============
    st.subheader(f"📋 Pratos Cadastrados ({len(pratos)} no total)")
    
    if pratos:
        for i, prato in enumerate(pratos):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{prato['nome']}** - R$ {prato['preco']:.2f}")
                st.caption(f"Categoria: {prato['cat']} • Imagem: {prato['img']}")
            with col2:
                if st.button("✏️", key=f"edit_{i}", help="Editar"):
                    st.info("Funcionalidade de edição em desenvolvimento")
            with col3:
                if st.button("🗑️", key=f"del_{i}", help="Excluir"):
                    pratos.pop(i)
                    with open(PRATOS_FILE, "w", encoding="utf-8") as f:
                        json.dump(pratos, f, ensure_ascii=False, indent=2)
                    st.rerun()
            st.divider()
    else:
        st.info("📝 Nenhum prato cadastrado ainda.")
    
    # =============== BOTÕES DE AÇÃO ===============
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Atualizar Lista", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("🌐 Voltar ao Site", use_container_width=True):
            st.switch_page("app.py")
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_logado = False
            st.rerun()
    
    # =============== INFORMAÇÕES DO SISTEMA ===============
    with st.expander("🔧 Informações do Sistema"):
        st.write(f"**Arquivo de dados:** `{PRATOS_FILE}`")
        st.write(f"**Pratos cadastrados:** {len(pratos)}")
        st.write(f"**Diretório de imagens:** `{IMAGES_DIR}`")
        
        if os.path.exists(IMAGES_DIR):
            imagens = [f for f in os.listdir(IMAGES_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]
            st.write(f"**Imagens salvas:** {len(imagens)}")
        
        categorias_count = {}
        for prato in pratos:
            cat = prato['cat']
            categorias_count[cat] = categorias_count.get(cat, 0) + 1
        
        st.write("**Pratos por categoria:**")
        for cat, count in categorias_count.items():
            st.write(f"  - {cat}: {count}")