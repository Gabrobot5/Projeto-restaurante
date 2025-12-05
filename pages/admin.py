# pages/admin.py - PAINEL ADMIN - GESTÃO DE PRATOS, INGREDIENTES E PEDIDOS
import streamlit as st
import json
import os
import base64
from datetime import datetime

st.set_page_config(page_title="Admin • Burger Express", page_icon="🔒", layout="centered")

# =============== CONFIGURAÇÃO DE CAMINHOS ===============
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRATOS_FILE = os.path.join(BASE_DIR, "pratos.json")
ESTOQUE_FILE = os.path.join(BASE_DIR, "estoque.json")
INGREDIENTES_FILE = os.path.join(BASE_DIR, "ingredientes.json")
PEDIDOS_FILE = os.path.join(BASE_DIR, "pedidos.json")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
TABELA_NUTRICIONAL_FILE = os.path.join(BASE_DIR, "tabela_nutricional.json")

# =============== INICIALIZAÇÃO DE ESTADOS ===============
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False
if "editando_prato_index" not in st.session_state:
    st.session_state.editando_prato_index = None
if "editando_prato" not in st.session_state:
    st.session_state.editando_prato = None
if "modo_edicao" not in st.session_state:
    st.session_state.modo_edicao = False
if "ingredientes_editados" not in st.session_state:
    st.session_state.ingredientes_editados = []
if "ingredientes_para_remover" not in st.session_state:
    st.session_state.ingredientes_para_remover = []
if "novo_ing_nome" not in st.session_state:
    st.session_state.novo_ing_nome = ""
if "novo_ing_qtd" not in st.session_state:
    st.session_state.novo_ing_qtd = 1
if "adicionar_tabela_nutricional" not in st.session_state:
    st.session_state.adicionar_tabela_nutricional = False
if "editando_tabela_nutricional" not in st.session_state:
    st.session_state.editando_tabela_nutricional = False

# =============== FUNÇÕES PARA TABELA NUTRICIONAL ===============
def salvar_informacoes_nutricionais(prato_nome, dados_nutricionais):
    """Salva informações nutricionais em um arquivo JSON - COM VALIDAÇÃO"""
    # Validar se há dados significativos para salvar
    if (dados_nutricionais.get('calorias', 0) == 0 and 
        dados_nutricionais.get('proteinas', 0) == 0 and
        dados_nutricionais.get('carboidratos', 0) == 0 and
        dados_nutricionais.get('gorduras', 0) == 0 and
        dados_nutricionais.get('gorduras_saturadas', 0) == 0 and
        dados_nutricionais.get('fibra', 0) == 0 and
        dados_nutricionais.get('sodio', 0) == 0 and
        not dados_nutricionais.get('alergenicos') and
        ("não disponíveis" in dados_nutricionais.get('descricao', '').lower() or 
         not dados_nutricionais.get('descricao', '').strip())):
        # Não salvar tabelas vazias
        return False
    
    try:
        if os.path.exists(TABELA_NUTRICIONAL_FILE):
            with open(TABELA_NUTRICIONAL_FILE, "r", encoding="utf-8") as f:
                tabela_existente = json.load(f)
        else:
            tabela_existente = {}
        
        # Adicionar ou atualizar os dados
        tabela_existente[prato_nome] = dados_nutricionais
        
        with open(TABELA_NUTRICIONAL_FILE, "w", encoding="utf-8") as f:
            json.dump(tabela_existente, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados nutricionais: {e}")
        return False

def obter_informacoes_nutricionais(prato_nome):
    """Retorna informações nutricionais para cada prato - RETORNA NONE SE VAZIO"""
    try:
        if os.path.exists(TABELA_NUTRICIONAL_FILE):
            with open(TABELA_NUTRICIONAL_FILE, "r", encoding="utf-8") as f:
                tabela_personalizada = json.load(f)
                if prato_nome in tabela_personalizada:
                    # Verificar se tem dados válidos (não é uma tabela vazia)
                    dados = tabela_personalizada[prato_nome]
                    # Se todos os valores forem zero e não tiver descrição/alérgenos, considerar vazio
                    if (dados.get('calorias', 0) == 0 and 
                        dados.get('proteinas', 0) == 0 and
                        dados.get('carboidratos', 0) == 0 and
                        dados.get('gorduras', 0) == 0 and
                        dados.get('gorduras_saturadas', 0) == 0 and
                        dados.get('fibra', 0) == 0 and
                        dados.get('sodio', 0) == 0 and
                        not dados.get('alergenicos') and
                        "não disponíveis" in dados.get('descricao', '').lower()):
                        return None
                    return dados
    except:
        pass
    
    # Retorna None se não encontrar dados válidos
    return None

# =============== FUNÇÕES DE PEDIDOS ===============
def carregar_pedidos():
    if os.path.exists(PEDIDOS_FILE):
        try:
            with open(PEDIDOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    else:
        return []

def salvar_pedidos(pedidos):
    with open(PEDIDOS_FILE, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=2)

def criar_novo_pedido(itens, total, cliente="Cliente"):
    pedidos = carregar_pedidos()
    
    novo_pedido = {
        "id": len(pedidos) + 1,
        "cliente": cliente,
        "itens": itens,
        "total": total,
        "status": "recebido",  # recebido, preparando, pronto, entregue, cancelado
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tempo_preparo_estimado": 20  # minutos
    }
    
    pedidos.append(novo_pedido)
    salvar_pedidos(pedidos)
    return novo_pedido

def atualizar_status_pedido(pedido_id, novo_status):
    pedidos = carregar_pedidos()
    for pedido in pedidos:
        if pedido["id"] == pedido_id:
            pedido["status"] = novo_status
            if novo_status == "preparando":
                pedido["inicio_preparo"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            elif novo_status == "pronto":
                pedido["final_preparo"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            salvar_pedidos(pedidos)
            return True
    return False

# =============== FUNÇÕES AUXILIARES ===============
def verificar_disponibilidade_prato(prato, ingredientes):
    """Verifica se há ingredientes suficientes para fazer o prato"""
    faltantes = []
    for ing_prato in prato.get('ingredientes', []):
        ingrediente = next((i for i in ingredientes if i['nome'] == ing_prato['nome']), None)
        if not ingrediente or ingrediente['estoque'] < ing_prato['quantidade']:
            faltantes.append(ing_prato['nome'])
    return len(faltantes) == 0, faltantes

def calcular_custo_prato(prato, ingredientes):
    """Calcula custo estimado baseado nos preços reais dos ingredientes"""
    custo_total = 0
    
    # Criar dicionário com preços dos ingredientes
    precos_ingredientes = {}
    for ing in ingredientes:
        precos_ingredientes[ing['nome']] = ing.get('preco_custo', 1.00)
    
    # Calcular custo para cada ingrediente do prato
    for ing_prato in prato.get('ingredientes', []):
        preco_unitario = precos_ingredientes.get(ing_prato['nome'], 1.00)
        custo_total += preco_unitario * ing_prato['quantidade']
    
    return round(custo_total, 2)

# =============== FUNÇÕES DE DADOS ===============
def criar_ingredientes_iniciais():
    ingredientes_iniciais = [
        {"nome": "Pão de Hambúrguer", "categoria": "paes", "unidade": "unidade", 
         "estoque": 100, "minimo": 20, "preco_custo": 1.50},
        {"nome": "Pão Brioche", "categoria": "paes", "unidade": "unidade", 
         "estoque": 80, "minimo": 15, "preco_custo": 2.00},
        {"nome": "Carne Bovina 180g", "categoria": "carnes", "unidade": "unidade", 
         "estoque": 50, "minimo": 10, "preco_custo": 6.00},
        {"nome": "Queijo Cheddar", "categoria": "queijos", "unidade": "fatia", 
         "estoque": 200, "minimo": 30, "preco_custo": 1.50},
        {"nome": "Queijo Mussarela", "categoria": "queijos", "unidade": "fatia", 
         "estoque": 150, "minimo": 25, "preco_custo": 1.20},
        {"nome": "Bacon", "categoria": "complementos", "unidade": "fatia", 
         "estoque": 120, "minimo": 20, "preco_custo": 2.00},
        {"nome": "Alface", "categoria": "saladas", "unidade": "porção", 
         "estoque": 30, "minimo": 5, "preco_custo": 0.50},
        {"nome": "Tomate", "categoria": "saladas", "unidade": "fatia", 
         "estoque": 100, "minimo": 15, "preco_custo": 0.30},
        {"nome": "Cebola Roxa", "categoria": "saladas", "unidade": "fatia", 
         "estoque": 80, "minimo": 10, "preco_custo": 0.20},
        {"nome": "Molho Especial", "categoria": "molhos", "unidade": "porção", 
         "estoque": 50, "minimo": 8, "preco_custo": 1.00},
        {"nome": "Maionese", "categoria": "molhos", "unidade": "porção", 
         "estoque": 40, "minimo": 6, "preco_custo": 0.80},
        {"nome": "Ketchup", "categoria": "molhos", "unidade": "sache", 
         "estoque": 200, "minimo": 30, "preco_custo": 0.30},
        {"nome": "Mostarda", "categoria": "molhos", "unidade": "sache", 
         "estoque": 180, "minimo": 25, "preco_custo": 0.30},
        {"nome": "Batata Palha", "categoria": "acompanhamentos", "unidade": "porção", 
         "estoque": 25, "minimo": 5, "preco_custo": 1.50},
        {"nome": "Coca-Cola 2L", "categoria": "bebidas", "unidade": "unidade", 
         "estoque": 30, "minimo": 6, "preco_custo": 8.00},
        {"nome": "Guaraná 2L", "categoria": "bebidas", "unidade": "unidade", 
         "estoque": 25, "minimo": 5, "preco_custo": 7.00},
    ]
    
    # Salvar no arquivo
    with open(INGREDIENTES_FILE, "w", encoding="utf-8") as f:
        json.dump(ingredientes_iniciais, f, ensure_ascii=False, indent=2)
    return ingredientes_iniciais

def carregar_ingredientes():
    if os.path.exists(INGREDIENTES_FILE):
        try:
            with open(INGREDIENTES_FILE, "r", encoding="utf-8") as f:
                ingredientes = json.load(f)
                # Garantir que todos os ingredientes tenham preco_custo
                for ing in ingredientes:
                    if 'preco_custo' not in ing:
                        ing['preco_custo'] = 1.00  # Valor padrão
                return ingredientes
        except:
            return criar_ingredientes_iniciais()
    else:
        return criar_ingredientes_iniciais()

def carregar_estoque():
    if os.path.exists(ESTOQUE_FILE):
        try:
            with open(ESTOQUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    else:
        return {}

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
            {
                "nome": "Burger Classic", 
                "preco": 18.90, 
                "cat": "hamburgers", 
                "img": "burger-classic.jpg",
                "ingredientes": [
                    {"nome": "Pão de Hambúrguer", "quantidade": 1},
                    {"nome": "Carne Bovina 180g", "quantidade": 1},
                    {"nome": "Queijo Cheddar", "quantidade": 1},
                    {"nome": "Alface", "quantidade": 1},
                    {"nome": "Tomate", "quantidade": 2},
                    {"nome": "Molho Especial", "quantidade": 1}
                ]
            },
            {
                "nome": "Burger Bacon", 
                "preco": 22.90, 
                "cat": "hamburgers", 
                "img": "burger-bacon.jpg",
                "ingredientes": [
                    {"nome": "Pão Brioche", "quantidade": 1},
                    {"nome": "Carne Bovina 180g", "quantidade": 1},
                    {"nome": "Queijo Cheddar", "quantidade": 2},
                    {"nome": "Bacon", "quantidade": 3},
                    {"nome": "Alface", "quantidade": 1},
                    {"nome": "Molho Especial", "quantidade": 1}
                ]
            },
            {
                "nome": "Double Cheese", 
                "preco": 26.90, 
                "cat": "hamburgers", 
                "img": "cheese-duplo.jpg",
                "ingredientes": [
                    {"nome": "Pão de Hambúrguer", "quantidade": 1},
                    {"nome": "Carne Bovina 180g", "quantidade": 2},
                    {"nome": "Queijo Cheddar", "quantidade": 2},
                    {"nome": "Queijo Mussarela", "quantidade": 2},
                    {"nome": "Cebola Roxa", "quantidade": 3},
                    {"nome": "Molho Especial", "quantidade": 1}
                ]
            },
        ]
        with open(PRATOS_FILE, "w", encoding="utf-8") as f:
            json.dump(pratos_iniciais, f, ensure_ascii=False, indent=2)
        return pratos_iniciais
    
def salvar_pratos(pratos_atualizados):
    """Salva a lista de pratos no arquivo"""
    with open(PRATOS_FILE, "w", encoding="utf-8") as f:
        json.dump(pratos_atualizados, f, ensure_ascii=False, indent=2)

# CSS CORRIGIDO - TEXTO PRETO NOS SELECTS
st.markdown("""
<style>
    /* FUNDO PROFISSIONAL */
    [data-testid="stAppViewContainer"] {
        background: 
            linear-gradient(135deg, #0f0f0f 0%, #1a0f0f 50%, #0f0f0f 100%),
            radial-gradient(circle at 20% 80%, rgba(200, 40, 60, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(200, 40, 60, 0.08) 0%, transparent 50%) !important;
        background-attachment: fixed !important;
    }
    
    /* =============== CORREÇÕES CRÍTICAS PARA SELECT BOXES =============== */
    
    /* 1. CONTAINER PRINCIPAL DO SELECT - TEXTO PRETO */
    .stSelectbox > div > div {
        background-color: white !important;
        color: #000000 !important;
    }
    
    /* 2. TEXTO DO SELECT QUANDO FECHADO - PRETO */
    [data-baseweb="select"] > div > div > div > div {
        color: #000000 !important;
        background-color: white !important;
    }
    
    /* 3. INPUT DO SELECT - PRETO */
    [data-baseweb="select"] input {
        color: #000000 !important;
        background-color: white !important;
    }
    
    /* 4. DROPDOWN (LISTBOX) - TEXTO PRETO */
    [data-baseweb="popover"] div,
    [data-baseweb="popover"] span,
    [data-baseweb="popover"] p {
        color: #000000 !important;
        background-color: white !important;
    }
    
    /* 5. ITENS DO DROPDOWN - PRETO */
    [role="listbox"] div,
    [role="listbox"] li,
    [role="option"] {
        color: #000000 !important;
        background-color: white !important;
    }
    
    /* 6. ITENS DO DROPDOWN AO PASSAR MOUSE - PRETO */
    [role="listbox"] div:hover,
    [role="option"]:hover {
        color: #000000 !important;
        background-color: #f0f0f0 !important;
    }
    
    /* 7. CONTEÚDO DO MARKDOWN DENTRO DO SELECT - PRETO */
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] span {
        color: #000000 !important;
    }
    
    /* 8. LABEL DO SELECT - BRANCO (como deve ser) */
    .stSelectbox label,
    [data-baseweb="select"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* 9. SETA DO SELECT - PRETO */
    [data-baseweb="select"] svg {
        fill: #000000 !important;
    }
    
    /* 10. BOTÃO DO SELECT - PRETO */
    [data-baseweb="select"] button {
        color: #000000 !important;
        background-color: white !important;
    }
    
    /* =============== CORREÇÕES PARA INPUTS NUMÉRICOS =============== */
    .stNumberInput input {
        color: #000000 !important;
        background-color: white !important;
    }
    
    .stTextInput input {
        color: #000000 !important;
        background-color: white !important;
    }
    
    .stTextArea textarea {
        color: #000000 !important;
        background-color: white !important;
    }
    
    /* =============== CORREÇÕES PARA RADIO BUTTONS (CATEGORIAS) =============== */
    /* Radio buttons devem ter texto BRANCO (são diferentes dos selects) */
    .stRadio [data-testid="stMarkdownContainer"],
    .stRadio [data-testid="stMarkdownContainer"] p,
    .stRadio [data-testid="stMarkdownContainer"] span,
    .stRadio label {
        color: white !important;
    }
    
    /* =============== CORREÇÕES PARA CHECKBOXES =============== */
    .stCheckbox [data-testid="stMarkdownContainer"],
    .stCheckbox [data-testid="stMarkdownContainer"] p,
    .stCheckbox [data-testid="stMarkdownContainer"] span,
    .stCheckbox label {
        color: white !important;
    }
    
    /* =============== TEXTO GERAL - MANTÉM BRANCO =============== */
    /* Só textos que NÃO são inputs/selects devem ser brancos */
    h1, h2, h3, h4, h5, h6, 
    .stExpander [data-testid="stMarkdownContainer"],
    .stAlert [data-testid="stMarkdownContainer"],
    p:not([class*="st"]):not([data-testid*="Input"]) {
        color: white !important;
    }
    
    /* =============== HEADER E ESTILOS VISUAIS (MANTIDOS) =============== */
    .main-header {
        background: linear-gradient(135deg, rgba(180, 40, 60, 0.85) 0%, rgba(160, 35, 55, 0.9) 100%) !important;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        backdrop-filter: blur(15px);
    }
    
    .animated-title {
        color: white !important;
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
    }
    
    .animated-subtitle {
        color: rgba(255,255,255,0.9) !important;
        margin: 12px 0 0 0;
        font-size: 1.3rem;
        font-weight: 500;
    }
    
    /* BOTÕES DO HEADER */
    .header-buttons {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.12);
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .btn-header {
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        margin: 0 8px 8px 0 !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
    }
    
    .btn-atualizar {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
        color: white !important;
    }
    
    .btn-atualizar:hover {
        background: linear-gradient(135deg, #2980b9 0%, #2471a3 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.4) !important;
    }
    
    .btn-voltar-site {
        background: linear-gradient(135deg, #27ae60 0%, #219653 100%) !important;
        color: white !important;
    }
    
    .btn-voltar-site:hover {
        background: linear-gradient(135deg, #219653 0%, #1e8449 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(39, 174, 96, 0.4) !important;
    }
    
    /* CARDS PRINCIPAIS */
    .stTabs [role="tabpanel"] {
        background: rgba(25, 25, 25, 0.85) !important;
        border-radius: 18px;
        padding: 2rem;
        margin-top: 1rem;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 12px 40px rgba(0,0,0,0.25);
        backdrop-filter: blur(15px);
    }
    
    /* TABS ESTILIZADAS */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px;
        padding: 6px;
        gap: 6px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: white !important;
        border-radius: 10px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #b4283c 0%, #a02335 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(180, 40, 60, 0.3);
    }
    
    /* FORMULÁRIOS */
    .stForm {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    }
    
    /* BOTÕES PRINCIPAIS */
    .stButton > button {
        background: linear-gradient(135deg, #b4283c 0%, #a02335 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        box-shadow: 0 6px 20px rgba(180, 40, 60, 0.25) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #a02335 0%, #8c1e2e 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(180, 40, 60, 0.35) !important;
    }
    
    /* EXPANDER */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        margin: 8px 0;
    }
    
    .streamlit-expanderContent {
        background: rgba(0, 0, 0, 0.25) !important;
        border-radius: 0 0 12px 12px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* METRICS */
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2.2rem !important;
        font-weight: bold;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 600;
    }
    
    /* ALERTAS */
    .stAlert {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        backdrop-filter: blur(15px);
        border-left: 5px solid #b4283c;
    }
    
    /* DIVIDER */
    .stDivider {
        border-color: rgba(255, 255, 255, 0.15) !important;
        margin: 2.5rem 0;
    }
    
    /* CAIXA DE LOGIN */
    .login-box {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(50, 25, 30, 0.95) 100%) !important;
        color: white !important;
        border-radius: 25px;
        padding: 60px 70px;
        text-align: center;
        max-width: 480px;
        margin: 100px auto;
        border: 2px solid #b4283c;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    
    /* CARDS DE PEDIDOS */
    .pedido-card {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px;
        padding: 24px;
        margin: 18px 0;
        border-left: 6px solid #b4283c;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    }
            
</style>
""", unsafe_allow_html=True)

if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

if not st.session_state.admin_logado:
    st.markdown("""
    <div class="login-box">
        <div style="font-size: 5rem; margin-bottom: 15px; animation: float 6s ease-in-out infinite;">🍔</div>
        <h1 style="color: #b4283c; font-size: 2.8rem; font-weight: 700; text-shadow: 0 4px 8px rgba(0,0,0,0.3);">Área Restrita</h1>
        <p style="color:rgba(255,255,255,0.9);font-size:1.2rem;font-weight:500;margin-top:15px;">Acesso exclusivo para administradores</p>
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
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1 class="animated-title" style='color:white;margin:0;font-size:2.8rem;font-weight:800;'>🍔 Painel Administrativo</h1>
        <p class="animated-subtitle" style='color:rgba(255,255,255,0.9);margin:12px 0 0 0;font-size:1.3rem;font-weight:500;'>
        Gerencie ingredientes, pratos, pedidos e estoque</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botões abaixo do header
    st.markdown("""
    <div class="header-buttons">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Atualizar Dados", key="header_atualizar", use_container_width=True, 
                    help="Atualizar todos os dados em tempo real"):
            st.rerun()
    with col2:
        if st.button("🌐 Voltar ao Site", key="header_voltar_site", use_container_width=True):
            st.switch_page("app.py")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Carregar dados
    ingredientes = carregar_ingredientes()
    pratos = carregar_pratos()
    estoque_pratos = carregar_estoque()
    pedidos = carregar_pedidos()
    
    # =============== ABAS PRINCIPAIS ===============
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Controle de Ingredientes", "🍔 Gestão de Pratos", "📋 Pedidos em Tempo Real", "📊 Estoque & Relatórios"])
    
    with tab1:
        st.subheader("🧮 Controle de Ingredientes")
        
        # Formulário para novo ingrediente
        with st.form("novo_ingrediente"):
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            with col1:
                novo_nome = st.text_input("Nome do Ingrediente", placeholder="Ex: Pão Brioche")
            with col2:
                categorias = ["paes", "carnes", "queijos", "saladas", "molhos", "complementos", "bebidas", "acompanhamentos"]
                nova_categoria = st.selectbox("Categoria", categorias)
            with col3:
                nova_unidade = st.selectbox("Unidade", ["unidade", "kg", "litro", "fatia", "porção", "sache", "gramas"])
            with col4:
                novo_estoque = st.number_input("Estoque Inicial", min_value=0, value=10)
            with col5:
                novo_preco_custo = st.number_input("Custo Unitário R$", min_value=0.0, value=1.00, step=0.1, format="%.2f")
            
            if st.form_submit_button("➕ Adicionar Ingrediente", type="secondary"):
                if novo_nome:
                    # Verifica se já existe
                    if any(ing['nome'].lower() == novo_nome.lower() for ing in ingredientes):
                        st.error("❌ Ingrediente já existe")
                    else:
                        novo_ingrediente = {
                            "nome": novo_nome,
                            "categoria": nova_categoria,
                            "unidade": nova_unidade,
                            "estoque": novo_estoque,
                            "minimo": 5,
                            "preco_custo": novo_preco_custo
                        }
                        ingredientes.append(novo_ingrediente)
                        with open(INGREDIENTES_FILE, "w", encoding="utf-8") as f:
                            json.dump(ingredientes, f, ensure_ascii=False, indent=2)
                        st.success(f"✅ {novo_nome} adicionado!")
                        st.rerun()
                else:
                    st.error("❌ Digite o nome do ingrediente")
        
        # Lista de ingredientes por categoria
        categorias_ing = list(set(ing['categoria'] for ing in ingredientes))
        for categoria in categorias_ing:
            st.subheader(f"📁 {categoria.title()}")
            ingredientes_cat = [ing for ing in ingredientes if ing['categoria'] == categoria]
            
            for i, ingrediente in enumerate(ingredientes_cat):
                col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])
                
                with col1:
                    st.write(f"**{ingrediente['nome']}**")
                    st.caption(f"Unidade: {ingrediente['unidade']}")
                
                with col2:
                    novo_estoque = st.number_input(
                        "Estoque",
                        min_value=0,
                        value=ingrediente['estoque'],
                        key=f"est_{ingrediente['nome']}",
                        label_visibility="collapsed"
                    )
                
                with col3:
                    novo_minimo = st.number_input(
                        "Mínimo",
                        min_value=1,
                        value=ingrediente['minimo'],
                        key=f"min_{ingrediente['nome']}",
                        label_visibility="collapsed"
                    )
                
                with col4:
                    novo_preco = st.number_input(
                        "Custo R$",
                        min_value=0.0,
                        value=float(ingrediente.get('preco_custo', 1.00)),
                        step=0.1,
                        format="%.2f",
                        key=f"custo_{ingrediente['nome']}",
                        label_visibility="collapsed"
                    )
                
                with col5:
                    if st.button("💾", key=f"save_ing_{ingrediente['nome']}"):
                        ingredientes[i]['estoque'] = novo_estoque
                        ingredientes[i]['minimo'] = novo_minimo
                        ingredientes[i]['preco_custo'] = novo_preco
                        with open(INGREDIENTES_FILE, "w", encoding="utf-8") as f:
                            json.dump(ingredientes, f, ensure_ascii=False, indent=2)
                        st.success("✅ Atualizado!")
                        st.rerun()
                
                with col6:
                    if st.button("🗑️", key=f"del_ing_{ingrediente['nome']}"):
                        # Verifica se o ingrediente está sendo usado em algum prato
                        usado_em = []
                        for prato in pratos:
                            if any(ing['nome'] == ingrediente['nome'] for ing in prato.get('ingredientes', [])):
                                usado_em.append(prato['nome'])
                        
                        if usado_em:
                            st.error(f"❌ Não pode excluir! Usado em: {', '.join(usado_em)}")
                        else:
                            ingredientes.pop(i)
                            with open(INGREDIENTES_FILE, "w", encoding="utf-8") as f:
                                json.dump(ingredientes, f, ensure_ascii=False, indent=2)
                            st.rerun()
                
                # Barra de estoque
                percentual = min(novo_estoque / novo_minimo * 100, 100) if novo_minimo > 0 else 0
                cor = "red" if novo_estoque <= novo_minimo else "green"
                st.progress(percentual/100, text=f"Estoque: {novo_estoque} {ingrediente['unidade']} | Custo: R$ {novo_preco:.2f} | Mínimo: {novo_minimo}")
            
            st.divider()

    
    with tab2:
        # =============== MODO EDIÇÃO DE PRATO ===============
        if st.session_state.editando_prato_index is not None:
            st.subheader("✏️ Editando Prato")
            
            prato_editando = st.session_state.editando_prato
            index_editando = st.session_state.editando_prato_index
            
            # Inicializar listas de ingredientes se necessário
            if not st.session_state.ingredientes_editados:
                st.session_state.ingredientes_editados = prato_editando.get('ingredientes', []).copy()
            
            # =============== SEÇÃO DE EDITAR INGREDIENTES (FORA DO FORM) ===============
            st.subheader("🧂 Editar Ingredientes do Prato")
            
            # Mostrar ingredientes atuais
            st.write("**Ingredientes Atuais:**")
            if not st.session_state.ingredientes_editados:
                st.info("Nenhum ingrediente adicionado ainda.")
            
            # Gerenciar remoção de ingredientes
            ingredientes_para_remover = []
            
            for idx, ingrediente in enumerate(st.session_state.ingredientes_editados):
                col_ing1, col_ing2, col_ing3 = st.columns([3, 2, 1])
                
                with col_ing1:
                    # Selecionar ingrediente da lista disponível
                    nomes_ingredientes = [ing['nome'] for ing in carregar_ingredientes()]
                    ing_atual_idx = nomes_ingredientes.index(ingrediente['nome']) if ingrediente['nome'] in nomes_ingredientes else 0
                    ingrediente_nome = st.selectbox(
                        "Ingrediente",
                        options=nomes_ingredientes,
                        index=ing_atual_idx,
                        key=f"ing_nome_{idx}"
                    )
                
                with col_ing2:
                    # Quantidade do ingrediente
                    ingrediente_qtd = st.number_input(
                        "Quantidade",
                        min_value=1,
                        value=ingrediente['quantidade'],
                        key=f"ing_qtd_{idx}"
                    )
                
                with col_ing3:
                    # Botão para remover ingrediente (FORA DO FORM)
                    if st.button("🗑️ Remover", key=f"rem_ing_{idx}"):
                        if idx < len(st.session_state.ingredientes_editados):
                            ingredientes_para_remover.append(idx)
                
                # Atualizar na lista temporária
                if idx not in ingredientes_para_remover:
                    st.session_state.ingredientes_editados[idx] = {
                        "nome": ingrediente_nome,
                        "quantidade": int(ingrediente_qtd)
                    }
            
            # Remover ingredientes marcados para remoção (em ordem reversa)
            for idx in sorted(ingredientes_para_remover, reverse=True):
                if idx < len(st.session_state.ingredientes_editados):
                    st.session_state.ingredientes_editados.pop(idx)
            
            # Se houve remoções, recarregar
            if ingredientes_para_remover:
                st.rerun()
            
            # =============== ADICIONAR NOVO INGREDIENTE (FORA DO FORM) ===============
            st.write("**Adicionar Novo Ingrediente:**")
            col_add1, col_add2, col_add3 = st.columns([3, 2, 1])
            
            with col_add1:
                novo_ing_nome = st.selectbox(
                    "Selecionar Ingrediente",
                    options=[ing['nome'] for ing in carregar_ingredientes()],
                    key="novo_ing_nome_select"
                )
            
            with col_add2:
                novo_ing_qtd = st.number_input(
                    "Quantidade",
                    min_value=1,
                    value=st.session_state.novo_ing_qtd,
                    key="novo_ing_qtd_input"
                )
                st.session_state.novo_ing_qtd = novo_ing_qtd
            
            with col_add3:
                if st.button("➕ Adicionar", key="btn_add_ing"):
                    # Verificar se já existe
                    existe = False
                    for ing in st.session_state.ingredientes_editados:
                        if ing['nome'] == novo_ing_nome:
                            ing['quantidade'] += novo_ing_qtd
                            existe = True
                            break
                    
                    if not existe:
                        st.session_state.ingredientes_editados.append({
                            "nome": novo_ing_nome,
                            "quantidade": int(novo_ing_qtd)
                        })
                    st.rerun()
            
            # Mostrar resumo dos ingredientes
            st.write("**Resumo dos Ingredientes:**")
            if st.session_state.ingredientes_editados:
                for ing in st.session_state.ingredientes_editados:
                    # Encontrar unidade do ingrediente
                    ingrediente_info = next((i for i in carregar_ingredientes() if i['nome'] == ing['nome']), None)
                    unidade = ingrediente_info['unidade'] if ingrediente_info else "unidade"
                    st.write(f"• {ing['nome']}: {ing['quantidade']} {unidade}")
            else:
                st.warning("⚠️ Adicione pelo menos um ingrediente ao prato.")
            
            # =============== SEÇÃO: TABELA NUTRICIONAL (PARA EDIÇÃO) ===============
            st.subheader("📊 Tabela Nutricional")
            
            # Carregar dados existentes se houver
            dados_nutricionais_existentes = obter_informacoes_nutricionais(prato_editando['nome'])
            
            editar_tabela_nutricional = st.checkbox(
                "Editar tabela nutricional",
                value=st.session_state.get('editando_tabela_nutricional', False),
                key="chk_editar_tabela"
            )
            
            if editar_tabela_nutricional:
                st.session_state.editando_tabela_nutricional = True
                
                # Inicializar valores com dados existentes ou zeros
                calorias_existentes = dados_nutricionais_existentes.get('calorias', 0) if dados_nutricionais_existentes else 0
                proteinas_existentes = dados_nutricionais_existentes.get('proteinas', 0.0) if dados_nutricionais_existentes else 0.0
                carboidratos_existentes = dados_nutricionais_existentes.get('carboidratos', 0.0) if dados_nutricionais_existentes else 0.0
                gorduras_existentes = dados_nutricionais_existentes.get('gorduras', 0.0) if dados_nutricionais_existentes else 0.0
                gorduras_saturadas_existentes = dados_nutricionais_existentes.get('gorduras_saturadas', 0.0) if dados_nutricionais_existentes else 0.0
                fibra_existentes = dados_nutricionais_existentes.get('fibra', 0.0) if dados_nutricionais_existentes else 0.0
                sodio_existentes = dados_nutricionais_existentes.get('sodio', 0) if dados_nutricionais_existentes else 0
                descricao_existente = dados_nutricionais_existentes.get('descricao', '') if dados_nutricionais_existentes else ''
                alergenicos_existentes = dados_nutricionais_existentes.get('alergenicos', []) if dados_nutricionais_existentes else []
                
                col_nut1, col_nut2 = st.columns(2)
                
                with col_nut1:
                    calorias = st.number_input(
                        "Calorias (kcal)", 
                        min_value=0, 
                        value=calorias_existentes, 
                        step=10,
                        key="edt_calorias"
                    )
                    proteinas = st.number_input(
                        "Proteínas (g)", 
                        min_value=0.0, 
                        value=proteinas_existentes, 
                        step=1.0, 
                        format="%.1f",
                        key="edt_proteinas"
                    )
                    carboidratos = st.number_input(
                        "Carboidratos (g)", 
                        min_value=0.0, 
                        value=carboidratos_existentes, 
                        step=1.0, 
                        format="%.1f",
                        key="edt_carboidratos"
                    )
                    gorduras = st.number_input(
                        "Gorduras Totais (g)", 
                        min_value=0.0, 
                        value=gorduras_existentes, 
                        step=1.0, 
                        format="%.1f",
                        key="edt_gorduras"
                    )
                
                with col_nut2:
                    gorduras_saturadas = st.number_input(
                        "Gorduras Saturadas (g)", 
                        min_value=0.0, 
                        value=gorduras_saturadas_existentes, 
                        step=0.5, 
                        format="%.1f",
                        key="edt_gord_sat"
                    )
                    fibra = st.number_input(
                        "Fibra Alimentar (g)", 
                        min_value=0.0, 
                        value=fibra_existentes, 
                        step=0.5, 
                        format="%.1f",
                        key="edt_fibra"
                    )
                    sodio = st.number_input(
                        "Sódio (mg)", 
                        min_value=0, 
                        value=sodio_existentes, 
                        step=10,
                        key="edt_sodio"
                    )
                
                # Descrição
                descricao_nutricional = st.text_area(
                    "Descrição Nutricional",
                    value=descricao_existente,
                    height=80,
                    key="edt_desc_nutricional"
                )
                
                # Alérgenos
                st.write("**Alérgenos:**")
                alergenicos_opcoes = [
                    "Glúten", "Lactose", "Leite", "Ovos", "Soja", "Nozes",
                    "Amendoim", "Peixes", "Crustáceos", "Moluscos", "Sésamo",
                    "Sulfitos", "Aipo", "Mostarda"
                ]
                
                novos_alergenicos = []
                
                cols_alerg = st.columns(4)
                for i, alergenico in enumerate(alergenicos_opcoes):
                    with cols_alerg[i % 4]:
                        if st.checkbox(
                            alergenico, 
                            value=alergenico in alergenicos_existentes,
                            key=f"edt_alerg_{alergenico}"
                        ):
                            novos_alergenicos.append(alergenico)
                
                # Botão para salvar tabela nutricional separadamente
                col_btn_salvar, col_btn_limpar = st.columns(2)
                with col_btn_salvar:
                    if st.button("💾 Salvar Tabela Nutricional", key="btn_salvar_tabela", use_container_width=True):
                        # Verificar se há dados para salvar
                        campos_preenchidos = any([
                            calorias > 0,
                            proteinas > 0,
                            carboidratos > 0,
                            gorduras > 0,
                            gorduras_saturadas > 0,
                            fibra > 0,
                            sodio > 0,
                            descricao_nutricional.strip() != ""
                        ])
                        
                        if campos_preenchidos or novos_alergenicos:
                            dados_nutricionais = {
                                "calorias": calorias,
                                "proteinas": proteinas,
                                "carboidratos": carboidratos,
                                "gorduras": gorduras,
                                "gorduras_saturadas": gorduras_saturadas,
                                "fibra": fibra,
                                "sodio": sodio,
                                "descricao": descricao_nutricional if descricao_nutricional.strip() else f"{prato_editando['nome']} - {prato_editando.get('cat', 'prato')}",
                                "alergenicos": novos_alergenicos
                            }
                            
                            if salvar_informacoes_nutricionais(prato_editando['nome'], dados_nutricionais):
                                st.success("✅ Tabela nutricional atualizada!")
                                st.rerun()
                        else:
                            # Se não há dados, remover a tabela nutricional
                            if dados_nutricionais_existentes:
                                try:
                                    if os.path.exists(TABELA_NUTRICIONAL_FILE):
                                        with open(TABELA_NUTRICIONAL_FILE, "r", encoding="utf-8") as f:
                                            tabela_existente = json.load(f)
                                        if prato_editando['nome'] in tabela_existente:
                                            del tabela_existente[prato_editando['nome']]
                                        with open(TABELA_NUTRICIONAL_FILE, "w", encoding="utf-8") as f:
                                            json.dump(tabela_existente, f, ensure_ascii=False, indent=2)
                                        st.info("🗑️ Tabela nutricional removida (não havia dados)")
                                        st.rerun()
                                except:
                                    pass
                
                with col_btn_limpar:
                    if st.button("🗑️ Remover Tabela", key="btn_remover_tabela", use_container_width=True):
                        if dados_nutricionais_existentes:
                            try:
                                if os.path.exists(TABELA_NUTRICIONAL_FILE):
                                    with open(TABELA_NUTRICIONAL_FILE, "r", encoding="utf-8") as f:
                                        tabela_existente = json.load(f)
                                    if prato_editando['nome'] in tabela_existente:
                                        del tabela_existente[prato_editando['nome']]
                                    with open(TABELA_NUTRICIONAL_FILE, "w", encoding="utf-8") as f:
                                        json.dump(tabela_existente, f, ensure_ascii=False, indent=2)
                                    st.success("✅ Tabela nutricional removida!")
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao remover tabela: {e}")
            else:
                st.session_state.editando_tabela_nutricional = False
                
                # Mostrar resumo se existirem dados
                if dados_nutricionais_existentes:
                    st.info(f"📊 **Tabela Nutricional Atual:**")
                    st.write(f"• Calorias: {dados_nutricionais_existentes.get('calorias', 0)} kcal")
                    st.write(f"• Proteínas: {dados_nutricionais_existentes.get('proteinas', 0)}g")
                    st.write(f"• Carboidratos: {dados_nutricionais_existentes.get('carboidratos', 0)}g")
                    if dados_nutricionais_existentes.get('alergenicos'):
                        st.write(f"• Alérgenos: {', '.join(dados_nutricionais_existentes.get('alergenicos', []))}")
                else:
                    st.warning("⚠️ Este prato não possui tabela nutricional cadastrada.")
            
            # =============== FORMULÁRIO PRINCIPAL DE EDIÇÃO ===============
            with st.form("editar_prato_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome_editado = st.text_input("Nome do Prato", value=prato_editando['nome'])
                    preco_editado = st.number_input(
                        "Preço (R$)", 
                        min_value=1.0, 
                        value=float(prato_editando['preco']), 
                        step=0.5, 
                        format="%.2f"
                    )
                    
                    # Categoria
                    categoria_opcoes = {
                        "hamburgers": "🍔 Hambúrgueres",
                        "bebidas": "🥤 Bebidas", 
                        "acompanhamentos": "🍟 Acompanhamentos",
                        "sobremesas": "🍰 Sobremesas"
                    }
                    
                    # Encontrar índice da categoria atual
                    cat_atual = prato_editando['cat']
                    opcoes_keys = list(categoria_opcoes.keys())
                    index_cat = opcoes_keys.index(cat_atual) if cat_atual in opcoes_keys else 0
                    
                    categoria_editada = st.radio(
                        "Categoria:",
                        options=opcoes_keys,
                        index=index_cat,
                        format_func=lambda x: categoria_opcoes[x],
                        horizontal=True
                    )
                
                with col2:
                    st.write("**Imagem Atual:**")
                    st.info(f"{prato_editando['img']}")
                    
                    nova_imagem = st.file_uploader(
                        "Nova Imagem (opcional)", 
                        type=["jpg", "jpeg", "png"],
                        key="nova_imagem_uploader"
                    )
                
                # Botões do formulário de edição
                col_salvar, col_cancelar = st.columns(2)
                with col_salvar:
                    salvar_submit = st.form_submit_button("💾 Salvar Alterações", type="primary")
                    if salvar_submit:
                        # Validar dados
                        if not nome_editado:
                            st.error("❌ Digite o nome do prato")
                        elif not preco_editado:
                            st.error("❌ Digite o preço do prato")
                        elif not st.session_state.ingredientes_editados:
                            st.error("❌ Adicione pelo menos um ingrediente ao prato")
                        else:
                            # Verificar se o nome foi alterado (e se já existe outro com o novo nome)
                            if nome_editado != prato_editando['nome']:
                                # Verificar se já existe outro prato com o novo nome
                                if any(p['nome'].lower() == nome_editado.lower() for p in pratos if p['nome'] != prato_editando['nome']):
                                    st.error(f"❌ Já existe um prato com o nome '{nome_editado}'")
                                else:
                                    # Atualizar no estoque se o nome mudou
                                    if prato_editando['nome'] in estoque_pratos:
                                        estoque_info = estoque_pratos.pop(prato_editando['nome'])
                                        estoque_pratos[nome_editado] = estoque_info
                            else:
                                nome_editado = prato_editando['nome']
                            
                            # Atualizar imagem se fornecida
                            nome_imagem = prato_editando['img']
                            if nova_imagem:
                                os.makedirs(IMAGES_DIR, exist_ok=True)
                                extensao = nova_imagem.name.split('.')[-1]
                                nome_imagem = f"{nome_editado.lower().replace(' ', '_')}.{extensao}"
                                caminho_imagem = os.path.join(IMAGES_DIR, nome_imagem)
                                
                                with open(caminho_imagem, "wb") as f:
                                    f.write(nova_imagem.getbuffer())
                            
                            # Atualizar prato
                            pratos_atualizados = carregar_pratos()
                            pratos_atualizados[index_editando] = {
                                "nome": nome_editado,
                                "preco": float(preco_editado),
                                "cat": categoria_editada,
                                "img": nome_imagem,
                                "ingredientes": st.session_state.ingredientes_editados.copy()
                            }
                            
                            # Salvar alterações
                            salvar_pratos(pratos_atualizados)
                            with open(ESTOQUE_FILE, "w", encoding="utf-8") as f:
                                json.dump(estoque_pratos, f, ensure_ascii=False, indent=2)
                            
                            # Limpar estados
                            st.session_state.editando_prato_index = None
                            st.session_state.editando_prato = None
                            st.session_state.ingredientes_editados = []
                            st.session_state.ingredientes_para_remover = []
                            st.session_state.novo_ing_nome = ""
                            st.session_state.novo_ing_qtd = 1
                            st.session_state.editando_tabela_nutricional = False
                            
                            st.success(f"✅ Prato '{nome_editado}' atualizado com sucesso!")
                            st.rerun()
                
                with col_cancelar:
                    cancelar_submit = st.form_submit_button("❌ Cancelar", type="secondary")
                    if cancelar_submit:
                        # Limpar estados
                        st.session_state.editando_prato_index = None
                        st.session_state.editando_prato = None
                        st.session_state.ingredientes_editados = []
                        st.session_state.ingredientes_para_remover = []
                        st.session_state.novo_ing_nome = ""
                        st.session_state.novo_ing_qtd = 1
                        st.session_state.editando_tabela_nutricional = False
                        st.rerun()
        
        else:
            # =============== FORMA ORIGINAL (SEM EDIÇÃO) ===============
            st.subheader("🍔 Gestão de Pratos")
            
            # Formulário de cadastro de prato
            with st.form("cadastro_prato", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("Nome do Prato", placeholder="Ex: Burger Especial")
                    preco = st.number_input("Preço (R$)", min_value=1.0, value=20.0, step=0.5, format="%.2f")
                    
                    # Seleção de ingredientes
                    st.write("**Ingredientes do Prato:**")
                    ingredientes_selecionados = []
                    for ingrediente in ingredientes:
                        col_ing1, col_ing2 = st.columns([3, 1])
                        with col_ing1:
                            if st.checkbox(ingrediente['nome'], key=f"chk_{ingrediente['nome']}"):
                                with col_ing2:
                                    quantidade = st.number_input(
                                        "Qtd",
                                        min_value=1,
                                        value=1,
                                        key=f"qtd_{ingrediente['nome']}",
                                        label_visibility="collapsed"
                                    )
                                    ingredientes_selecionados.append({
                                        "nome": ingrediente['nome'],
                                        "quantidade": quantidade
                                    })
                
                with col2:
                    st.write("Categoria")
                    categoria_opcoes = {
                        "hamburgers": "🍔 Hambúrgueres",
                        "bebidas": "🥤 Bebidas", 
                        "acompanhamentos": "🍟 Acompanhamentos",
                        "sobremesas": "🍰 Sobremesas"
                    }
                    
                    categoria_selecionada = st.radio(
                        "Selecione a categoria:",
                        options=list(categoria_opcoes.keys()),
                        format_func=lambda x: categoria_opcoes[x],
                        label_visibility="collapsed",
                        horizontal=True
                    )
                    categoria = categoria_selecionada
                    
                    imagem = st.file_uploader("Imagem do Prato", type=["jpg", "jpeg", "png"])
                    
                    # Mostra ingredientes selecionados
                    if ingredientes_selecionados:
                        st.write("**Ingredientes selecionados:**")
                        for ing in ingredientes_selecionados:
                            st.write(f"- {ing['nome']} ({ing['quantidade']} {next((i['unidade'] for i in ingredientes if i['nome'] == ing['nome']), 'un')})")
                
                # Botão de submit
                submitted = st.form_submit_button("✅ Cadastrar Prato", type="primary")
                
                if submitted:
                    if not nome:
                        st.error("❌ Digite o nome do prato")
                    elif not preco:
                        st.error("❌ Digite o preço do prato")
                    elif not imagem:
                        st.error("❌ Selecione uma imagem")
                    elif not ingredientes_selecionados:
                        st.error("❌ Selecione pelo menos um ingrediente")
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
                                "img": nome_imagem,
                                "ingredientes": ingredientes_selecionados
                            }
                            
                            pratos.append(novo_prato)
                            with open(PRATOS_FILE, "w", encoding="utf-8") as f:
                                json.dump(pratos, f, ensure_ascii=False, indent=2)
                            
                            # Adiciona ao estoque de pratos
                            estoque_pratos[nome] = {'quantidade': 10, 'minimo': 5, 'ativo': True}
                            with open(ESTOQUE_FILE, "w", encoding="utf-8") as f:
                                json.dump(estoque_pratos, f, ensure_ascii=False, indent=2)
                            
                            st.success(f"🎉 Prato '{nome}' cadastrado com sucesso!")
                            st.balloons()
            
            # Lista de pratos com ingredientes
            st.subheader("📋 Pratos Cadastrados")
            for i, prato in enumerate(pratos):
                with st.expander(f"🍔 {prato['nome']} - R$ {prato['preco']:.2f}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Categoria:** {prato['cat']}")
                        st.write(f"**Imagem:** {prato['img']}")
                        
                        # Verifica disponibilidade baseada nos ingredientes
                        disponivel, faltantes = verificar_disponibilidade_prato(prato, ingredientes)
                        status = "✅ Disponível" if disponivel else f"❌ Faltam: {', '.join(faltantes)}"
                        st.write(f"**Status:** {status}")
                    
                    with col2:
                        st.write("**Ingredientes:**")
                        for ing in prato.get('ingredientes', []):
                            ingrediente_info = next((i for i in ingredientes if i['nome'] == ing['nome']), None)
                            if ingrediente_info:
                                st.write(f"- {ing['nome']}: {ing['quantidade']} {ingrediente_info['unidade']}")
                    
                    # Verificar se tem tabela nutricional
                    dados_nutricionais = obter_informacoes_nutricionais(prato['nome'])
                    if dados_nutricionais:
                        st.info(f"📊 Possui tabela nutricional: {dados_nutricionais.get('calorias', 0)} kcal")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        # BOTÃO EDITAR FUNCIONAL
                        if st.button("✏️ Editar", key=f"edit_{i}"):
                            st.session_state.editando_prato_index = i
                            st.session_state.editando_prato = prato.copy()
                            # Inicializar ingredientes para edição
                            st.session_state.ingredientes_editados = prato.get('ingredientes', []).copy()
                            st.rerun()
                    
                    with col_btn2:
                        if st.button("🗑️ Excluir", key=f"del_{i}"):
                            if prato['nome'] in estoque_pratos:
                                del estoque_pratos[prato['nome']]
                            pratos.pop(i)
                            with open(PRATOS_FILE, "w", encoding="utf-8") as f:
                                json.dump(pratos, f, ensure_ascii=False, indent=2)
                            with open(ESTOQUE_FILE, "w", encoding="utf-8") as f:
                                json.dump(estoque_pratos, f, ensure_ascii=False, indent=2)
                            st.rerun()
    
    with tab3:
        st.subheader("📋 Pedidos em Tempo Real")
        
        # Simulador de novos pedidos (para demonstração)
        with st.expander("🧪 Simular Novo Pedido"):
            col1, col2 = st.columns(2)
            with col1:
                cliente_simulado = st.text_input("Nome do Cliente", value="Cliente Teste")
                itens_simulados = []
                for prato in pratos:
                    if st.checkbox(f"{prato['nome']} - R$ {prato['preco']:.2f}", key=f"sim_{prato['nome']}"):
                        quantidade = st.number_input(f"Qtd {prato['nome']}", min_value=1, value=1, key=f"qtd_sim_{prato['nome']}")
                        itens_simulados.append({
                            "nome": prato['nome'],
                            "quantidade": quantidade,
                            "preco": prato['preco']
                        })
            
            with col2:
                if itens_simulados:
                    st.write("**Itens do Pedido:**")
                    total_simulado = 0
                    for item in itens_simulados:
                        subtotal = item['quantidade'] * item['preco']
                        total_simulado += subtotal
                        st.write(f"- {item['nome']} x{item['quantidade']} - R$ {subtotal:.2f}")
                    st.write(f"**Total: R$ {total_simulado:.2f}**")
                    
                    if st.button("🛒 Criar Pedido Simulado", type="primary"):
                        novo_pedido = criar_novo_pedido(itens_simulados, total_simulado, cliente_simulado)
                        st.success(f"✅ Pedido #{novo_pedido['id']} criado com sucesso!")
                        st.rerun()
        
        # Lista de pedidos em tempo real
        st.subheader("🕒 Pedidos Ativos")
        
        pedidos_ativos = [p for p in pedidos if p['status'] in ['recebido', 'preparando']]
        pedidos_finalizados = [p for p in pedidos if p['status'] in ['pronto', 'entregue', 'cancelado']]
        
        if not pedidos_ativos:
            st.info("📝 Nenhum pedido ativo no momento.")
        
        for pedido in pedidos_ativos:
            # Card do pedido
            status_class = f"status-{pedido['status']}"
            st.markdown(f"""
            <div class='pedido-card {status_class}'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='color: white; margin: 0;'>Pedido #{pedido['id']} - {pedido['cliente']}</h3>
                    <span style='
                        padding: 8px 18px; 
                        border-radius: 25px; 
                        font-weight: bold;
                        font-size: 0.9rem;
                        background: {{
                            '#ff6b6b' if pedido['status'] == 'recebido' else
                            '#feca57' if pedido['status'] == 'preparando' else
                            '#1dd1a1' if pedido['status'] == 'pronto' else
                            '#54a0ff' if pedido['status'] == 'entregue' else
                            '#576574'
                        }};
                        color: white;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                    '>{pedido['status'].upper()}</span>
                </div>
                <p style='color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 0.9rem;'>{pedido['data_hora']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Itens do pedido
            st.write("**Itens:**")
            for item in pedido['itens']:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"• {item['nome']}")
                with col2:
                    st.write(f"x{item['quantidade']}")
                with col3:
                    st.write(f"R$ {item['quantidade'] * item['preco']:.2f}")
            
            st.write(f"**Total: R$ {pedido['total']:.2f}**")
            
            # Controles de status
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            
            with col_btn1:
                if pedido['status'] == 'recebido':
                    if st.button("👨‍🍳 Iniciar Preparo", key=f"prep_{pedido['id']}", use_container_width=True):
                        atualizar_status_pedido(pedido['id'], 'preparando')
                        st.rerun()
            
            with col_btn2:
                if pedido['status'] == 'preparando':
                    if st.button("✅ Pronto", key=f"pronto_{pedido['id']}", use_container_width=True):
                        atualizar_status_pedido(pedido['id'], 'pronto')
                        st.rerun()
            
            with col_btn3:
                if pedido['status'] == 'pronto':
                    if st.button("🚚 Entregue", key=f"ent_{pedido['id']}", use_container_width=True):
                        atualizar_status_pedido(pedido['id'], 'entregue')
                        st.rerun()
            
            with col_btn4:
                if pedido['status'] in ['recebido', 'preparando']:
                    if st.button("❌ Cancelar", key=f"cancel_{pedido['id']}", use_container_width=True):
                        atualizar_status_pedido(pedido['id'], 'cancelado')
                        st.rerun()
            
            st.divider()
        
        # Pedidos finalizados (expandable)
        if pedidos_finalizados:
            with st.expander(f"📁 Pedidos Finalizados ({len(pedidos_finalizados)})"):
                for pedido in pedidos_finalizados[-10:]:  # Mostra os últimos 10
                    status_color = {
                        'pronto': '#1dd1a1',
                        'entregue': '#54a0ff', 
                        'cancelado': '#576574'
                    }
                    st.markdown(f"""
                    <div style='
                        background: rgba(255,255,255,0.05); 
                        border-radius: 10px; 
                        padding: 15px; 
                        margin: 8px 0;
                        border-left: 4px solid {status_color[pedido['status']]};
                    '>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <strong style='color: white;'>Pedido #{pedido['id']} - {pedido['cliente']}</strong>
                            <span style='
                                padding: 4px 12px; 
                                border-radius: 15px; 
                                font-size: 0.8rem;
                                background: {status_color[pedido['status']]};
                                color: white;
                            '>{pedido['status'].upper()}</span>
                        </div>
                        <p style='color: rgba(255,255,255,0.7); margin: 5px 0; font-size: 0.8rem;'>{pedido['data_hora']}</p>
                        <p style='color: white; margin: 0; font-size: 0.9rem;'>Total: R$ {pedido['total']:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("📊 Relatórios & Alertas")
        
        # Alertas de estoque baixo
        ingredientes_baixo = [ing for ing in ingredientes if ing['estoque'] <= ing['minimo']]
        if ingredientes_baixo:
            st.error("🚨 INGREDIENTES COM ESTOQUE BAIXO")
            for ing in ingredientes_baixo:
                st.write(f"❌ **{ing['nome']}**: {ing['estoque']} {ing['unidade']} (mínimo: {ing['minimo']})")
        
        # Estatísticas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Ingredientes", len(ingredientes))
        with col2:
            st.metric("Pratos Cadastrados", len(pratos))
        with col3:
            st.metric("Pedidos Hoje", len([p for p in pedidos if p['data_hora'].startswith(datetime.now().strftime("%d/%m/%Y"))]))
        with col4:
            st.metric("Ingredientes em Alerta", len(ingredientes_baixo))
        
        # Botão para exportar relatório de custos
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        with col_exp2:
            if st.button("📥 Exportar Relatório de Custos", use_container_width=True):
                # Criar relatório
                relatorio = {
                    "data_geracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "total_pratos": len(pratos),
                    "total_ingredientes": len(ingredientes),
                    "analise_pratos": []
                }
                
                for prato in pratos:
                    custo = calcular_custo_prato(prato, ingredientes)
                    lucro = prato['preco'] - custo
                    margem = (lucro / prato['preco'] * 100) if prato['preco'] > 0 else 0
                    
                    relatorio["analise_pratos"].append({
                        "nome": prato['nome'],
                        "categoria": prato['cat'],
                        "preco_venda": prato['preco'],
                        "custo_producao": custo,
                        "lucro_bruto": lucro,
                        "margem_percentual": margem
                    })
                
                # Salvar relatório em JSON
                relatorio_file = os.path.join(BASE_DIR, f"relatorio_custos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                with open(relatorio_file, "w", encoding="utf-8") as f:
                    json.dump(relatorio, f, ensure_ascii=False, indent=2)
                
                st.success(f"✅ Relatório exportado: {os.path.basename(relatorio_file)}")
        
        # =============== ANÁLISE DE CUSTOS E LUCROS ===============
        st.subheader("💲 Análise de Custos e Lucros")
        
        # Opções de filtro
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        with col_filtro1:
            filtrar_categoria = st.selectbox(
                "Filtrar por Categoria",
                options=["Todas"] + list(set(p['cat'] for p in pratos)),
                index=0
            )
        
        with col_filtro2:
            ordenar_por = st.selectbox(
                "Ordenar por",
                options=["Maior Lucro", "Menor Lucro", "Maior Margem", "Menor Margem", "Nome A-Z", "Nome Z-A"]
            )
        
        with col_filtro3:
            mostrar_detalhes = st.checkbox("Mostrar detalhes dos custos", value=False)
        
        # Filtrar pratos
        pratos_filtrados = pratos
        if filtrar_categoria != "Todas":
            pratos_filtrados = [p for p in pratos if p['cat'] == filtrar_categoria]
        
        if not pratos_filtrados:
            st.info("📝 Nenhum prato encontrado com os filtros selecionados.")
        else:
            # Calcular custos e preparar dados
            dados_pratos = []
            for prato in pratos_filtrados:
                custo_estimado = calcular_custo_prato(prato, ingredientes)
                lucro = prato['preco'] - custo_estimado
                margem = (lucro / prato['preco']) * 100 if prato['preco'] > 0 else 0
                
                dados_pratos.append({
                    'nome': prato['nome'],
                    'categoria': prato['cat'],
                    'preco': prato['preco'],
                    'custo': custo_estimado,
                    'lucro': lucro,
                    'margem': margem
                })
            
            # Ordenar dados
            if ordenar_por == "Maior Lucro":
                dados_pratos.sort(key=lambda x: x['lucro'], reverse=True)
            elif ordenar_por == "Menor Lucro":
                dados_pratos.sort(key=lambda x: x['lucro'])
            elif ordenar_por == "Maior Margem":
                dados_pratos.sort(key=lambda x: x['margem'], reverse=True)
            elif ordenar_por == "Menor Margem":
                dados_pratos.sort(key=lambda x: x['margem'])
            elif ordenar_por == "Nome A-Z":
                dados_pratos.sort(key=lambda x: x['nome'])
            elif ordenar_por == "Nome Z-A":
                dados_pratos.sort(key=lambda x: x['nome'], reverse=True)
            
            # Cards de análise
            total_preco = sum(p['preco'] for p in dados_pratos)
            total_custo = sum(p['custo'] for p in dados_pratos)
            total_lucro = sum(p['lucro'] for p in dados_pratos)
            margem_media = (total_lucro / total_preco * 100) if total_preco > 0 else 0
            
            # Usando HTML para mostrar números completos
            col_res1, col_res2, col_res3, col_res4 = st.columns(4)
            
            with col_res1:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 5px;">💰 Total Vendas</div>
                    <div style="color: white; font-size: 1.8rem; font-weight: bold;">R$ {total_preco:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_res2:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 5px;">📦 Total Custos</div>
                    <div style="color: white; font-size: 1.8rem; font-weight: bold;">R$ {total_custo:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_res3:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 5px;">💵 Total Lucro</div>
                    <div style="color: white; font-size: 1.8rem; font-weight: bold;">R$ {total_lucro:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_res4:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 5px;">📈 Margem Média</div>
                    <div style="color: white; font-size: 1.8rem; font-weight: bold;">{margem_media:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Lista detalhada de pratos
            for idx, dado in enumerate(dados_pratos):
                with st.expander(f"🍔 {dado['nome']} - R$ {dado['preco']:.2f} | 📈 {dado['margem']:.1f}%", 
                               expanded=(idx == 0 and mostrar_detalhes)):
                    
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        st.write("**Informações Financeiras:**")
                        
                        # Métricas em colunas
                        col_met1, col_met2, col_met3 = st.columns(3)
                        with col_met1:
                            st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; text-align: center;">
                                <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-bottom: 3px;">Preço</div>
                                <div style="color: white; font-size: 1.2rem; font-weight: bold;">R$ {dado['preco']:.2f}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_met2:
                            st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; text-align: center;">
                                <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-bottom: 3px;">Custo</div>
                                <div style="color: white; font-size: 1.2rem; font-weight: bold;">R$ {dado['custo']:.2f}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_met3:
                            st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; text-align: center;">
                                <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-bottom: 3px;">Lucro</div>
                                <div style="color: #1dd1a1; font-size: 1.2rem; font-weight: bold;">R$ {dado['lucro']:.2f}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Barra de margem com cores
                        st.write(f"**Margem de Lucro: {dado['margem']:.1f}%**")
                        
                        # Definir cor baseada na margem
                        if dado['margem'] > 50:
                            cor = "#1dd1a1"  # Verde - excelente
                        elif dado['margem'] > 30:
                            cor = "#54a0ff"  # Azul - boa
                        elif dado['margem'] > 15:
                            cor = "#feca57"  # Amarelo - média
                        else:
                            cor = "#ff6b6b"  # Vermelho - baixa
                        
                        # Barra de progresso customizada
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 2px; margin: 8px 0;">
                            <div style="background: {cor}; width: {min(dado['margem'], 100)}%; height: 20px; border-radius: 8px;"></div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Legenda da margem
                        if dado['margem'] > 50:
                            st.success("✅ Margem Excelente!")
                        elif dado['margem'] > 30:
                            st.info("📊 Margem Boa")
                        elif dado['margem'] > 15:
                            st.warning("⚠️ Margem Média")
                        else:
                            st.error("📉 Margem Baixa - Considere ajustar preço ou custos")
                    
                    with col_info2:
                        st.write("**Recomendações:**")
                        
                        # Análise e recomendações
                        if dado['margem'] < 15:
                            st.error("""
                            **Ações Sugeridas:**
                            - Aumente o preço de venda
                            - Reduza custos de ingredientes
                            - Otimize a receita
                            - Considere promoções para aumentar volume
                            """)
                        elif dado['margem'] < 30:
                            st.warning("""
                            **Oportunidades:**
                            - Avalie pequeno ajuste de preço
                            - Verifique fornecedores alternativos
                            - Considere versão premium
                            """)
                        else:
                            st.success("""
                            **Status: Ótimo!**
                            - Mantenha a estratégia atual
                            - Pode ser carro-chefe de vendas
                            - Considere expandir linha relacionada
                            """)
                        
                        # Indicador visual rápido
                        st.write("**Custo vs Preço:**")
                        
                        # Corrigir também as barras de progresso
                        percent_custo = (dado['custo'] / dado['preco'] * 100) if dado['preco'] > 0 else 0
                        percent_lucro = (dado['lucro'] / dado['preco'] * 100) if dado['preco'] > 0 else 0
                        
                        col_custo1, col_custo2 = st.columns(2)
                        with col_custo1:
                            st.markdown(f"""
                            <div style="margin-bottom: 10px;">
                                <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-bottom: 3px;">Custo: {percent_custo:.1f}%</div>
                                <div style="background: rgba(255,255,255,0.1); border-radius: 5px; height: 10px;">
                                    <div style="background: #ff6b6b; width: {min(percent_custo, 100)}%; height: 100%; border-radius: 5px;"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_custo2:
                            st.markdown(f"""
                            <div style="margin-bottom: 10px;">
                                <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-bottom: 3px;">Lucro: {percent_lucro:.1f}%</div>
                                <div style="background: rgba(255,255,255,0.1); border-radius: 5px; height: 10px;">
                                    <div style="background: #1dd1a1; width: {min(percent_lucro, 100)}%; height: 100%; border-radius: 5px;"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Detalhamento dos custos por ingrediente
                    if mostrar_detalhes:
                        st.markdown("**🧾 Detalhamento de custos por ingrediente:**")
                        
                        # Encontrar o prato correspondente
                        prato_detalhe = next((p for p in pratos_filtrados if p['nome'] == dado['nome']), None)
                        if prato_detalhe:
                            # Tabela de ingredientes e custos
                            custos_ingredientes = []
                            for ing_prato in prato_detalhe.get('ingredientes', []):
                                # Encontrar o ingrediente
                                ingrediente_info = next((i for i in ingredientes if i['nome'] == ing_prato['nome']), None)
                                if ingrediente_info:
                                    custo_unitario = ingrediente_info.get('preco_custo', 1.00)
                                    custo_total = custo_unitario * ing_prato['quantidade']
                                    custos_ingredientes.append({
                                        'ingrediente': ing_prato['nome'],
                                        'quantidade': ing_prato['quantidade'],
                                        'unidade': ingrediente_info['unidade'],
                                        'custo_unitario': custo_unitario,
                                        'custo_total': custo_total
                                    })
                            
                            # Mostrar tabela
                            for custo in custos_ingredientes:
                                col_det1, col_det2, col_det3, col_det4, col_det5 = st.columns([3, 1, 1, 1, 1])
                                with col_det1:
                                    st.write(f"• {custo['ingrediente']}")
                                with col_det2:
                                    st.write(f"{custo['quantidade']}")
                                with col_det3:
                                    st.write(f"{custo['unidade']}")
                                with col_det4:
                                    st.write(f"R$ {custo['custo_unitario']:.2f}")
                                with col_det5:
                                    st.write(f"R$ {custo['custo_total']:.2f}")
                            
                            # Total dos ingredientes
                            total_ingredientes = sum(c['custo_total'] for c in custos_ingredientes)
                            st.write(f"**Total ingredientes: R$ {total_ingredientes:.2f}**")
                            
                            # Se houver outros custos (mão de obra, embalagem, etc.)
                            outros_custos = dado['custo'] - total_ingredientes
                            if outros_custos > 0:
                                st.write(f"**Outros custos (mão de obra, embalagem): R$ {outros_custos:.2f}**")
                            
                            st.divider()

# =============== BOTÕES GLOBAIS ===============
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 Atualizar Tudo", use_container_width=True):
        st.rerun()
with col2:
    if st.button("🌐 Voltar ao Site", use_container_width=True):
        st.switch_page("app.py")
with col3:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.admin_logado = False
        st.rerun()