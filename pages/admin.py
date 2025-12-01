# pages/admin.py - PAINEL ADMIN COM DESIGN MELHORADO
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
    """Calcula custo estimado baseado nos ingredientes (valores fictícios)"""
    precos_ingredientes = {
        "Pão de Hambúrguer": 1.50, "Pão Brioche": 2.00, "Carne Bovina 180g": 6.00,
        "Queijo Cheddar": 1.50, "Queijo Mussarela": 1.20, "Bacon": 2.00,
        "Alface": 0.50, "Tomate": 0.30, "Cebola Roxa": 0.20, "Molho Especial": 1.00,
        "Maionese": 0.80, "Ketchup": 0.30, "Mostarda": 0.30, "Batata Palha": 1.50,
        "Coca-Cola 2L": 8.00, "Guaraná 2L": 7.00
    }
    
    custo_total = 0
    for ing_prato in prato.get('ingredientes', []):
        preco_unitario = precos_ingredientes.get(ing_prato['nome'], 1.00)
        custo_total += preco_unitario * ing_prato['quantidade']
    
    return custo_total

# =============== FUNÇÕES DE DADOS ===============
def carregar_ingredientes():
    if os.path.exists(INGREDIENTES_FILE):
        try:
            with open(INGREDIENTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    else:
        ingredientes_iniciais = [
            {"nome": "Pão de Hambúrguer", "categoria": "paes", "unidade": "unidade", "estoque": 100, "minimo": 20},
            {"nome": "Pão Brioche", "categoria": "paes", "unidade": "unidade", "estoque": 80, "minimo": 15},
            {"nome": "Carne Bovina 180g", "categoria": "carnes", "unidade": "unidade", "estoque": 50, "minimo": 10},
            {"nome": "Queijo Cheddar", "categoria": "queijos", "unidade": "fatia", "estoque": 200, "minimo": 30},
            {"nome": "Queijo Mussarela", "categoria": "queijos", "unidade": "fatia", "estoque": 150, "minimo": 25},
            {"nome": "Bacon", "categoria": "complementos", "unidade": "fatia", "estoque": 120, "minimo": 20},
            {"nome": "Alface", "categoria": "saladas", "unidade": "porção", "estoque": 30, "minimo": 5},
            {"nome": "Tomate", "categoria": "saladas", "unidade": "fatia", "estoque": 100, "minimo": 15},
            {"nome": "Cebola Roxa", "categoria": "saladas", "unidade": "fatia", "estoque": 80, "minimo": 10},
            {"nome": "Molho Especial", "categoria": "molhos", "unidade": "porção", "estoque": 50, "minimo": 8},
            {"nome": "Maionese", "categoria": "molhos", "unidade": "porção", "estoque": 40, "minimo": 6},
            {"nome": "Ketchup", "categoria": "molhos", "unidade": "sache", "estoque": 200, "minimo": 30},
            {"nome": "Mostarda", "categoria": "molhos", "unidade": "sache", "estoque": 180, "minimo": 25},
            {"nome": "Batata Palha", "categoria": "acompanhamentos", "unidade": "porção", "estoque": 25, "minimo": 5},
            {"nome": "Coca-Cola 2L", "categoria": "bebidas", "unidade": "unidade", "estoque": 30, "minimo": 6},
            {"nome": "Guaraná 2L", "categoria": "bebidas", "unidade": "unidade", "estoque": 25, "minimo": 5},
        ]
        with open(INGREDIENTES_FILE, "w", encoding="utf-8") as f:
            json.dump(ingredientes_iniciais, f, ensure_ascii=False, indent=2)
        return ingredientes_iniciais

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

# CSS PROFISSIONAL COM DESIGN MELHORADO E CORES CORRIGIDAS
# CSS PROFISSIONAL COM CORES CORRIGIDAS NOS SELECT BOXES
st.markdown("""
<style>
    /* FUNDO PROFISSIONAL COM PADRÃO SUTIL */
    [data-testid="stAppViewContainer"] {
        background: 
            linear-gradient(135deg, #0f0f0f 0%, #1a0f0f 50%, #0f0f0f 100%),
            radial-gradient(circle at 20% 80%, rgba(200, 40, 60, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(200, 40, 60, 0.08) 0%, transparent 50%),
            repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.01) 10px, rgba(255,255,255,0.01) 20px) !important;
        background-attachment: fixed !important;
    }
    
    /* CORREÇÃO ESPECÍFICA PARA SELECT BOXES - TEXTO PRETO LEGÍVEL */
    [data-baseweb="select"] > div {
        background-color: white !important;
        color: #000000 !important;
    }
    
    [data-baseweb="select"] input {
        color: #000000 !important;
        background-color: white !important;
    }
    
    [data-baseweb="select"] [role="listbox"] {
        background-color: white !important;
        color: #000000 !important;
    }
    
    [data-baseweb="select"] [role="listbox"] div {
        color: #000000 !important;
        background-color: white !important;
    }
    
    [data-baseweb="select"] [role="listbox"] div:hover {
        background-color: #f0f0f0 !important;
        color: #000000 !important;
    }
    
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] {
        color: #000000 !important;
    }
    
    /* TEXTO DOS LABELS EM BRANCO */
    [data-baseweb="select"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* BOTÕES DAS SELECTBOXES */
    [data-baseweb="select"] [data-baseweb="button"] {
        background-color: white !important;
        color: #000000 !important;
    }
    
    [data-baseweb="select"] svg {
        fill: #000000 !important;
    }

    /* HEADER COM DESIGN MELHORADO */
    .main-header {
        background: linear-gradient(135deg, rgba(180, 40, 60, 0.85) 0%, rgba(160, 35, 55, 0.9) 100%) !important;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    /* ANIMAÇÃO NO TÍTULO */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-title {
        animation: fadeInUp 0.8s ease-out;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .animated-subtitle {
        animation: fadeInUp 1s ease-out;
        animation-delay: 0.2s;
        animation-fill-mode: both;
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
    
    /* TEXTO BRANCO EM TODOS OS ELEMENTOS */
    .stApp, h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: white !important;
    }
    
    /* BOTÃO "Adicionar Ingrediente" COM TEXTO PRETO - CORREÇÃO ESPECÍFICA */
    div[data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        color: #000000 !important;
        background: #FFFFFF !important;
        border: 2px solid #b4283c !important;
        font-weight: bold !important;
    }
    
    div[data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
        background: #b4283c !important;
        color: white !important;
        border: 2px solid #b4283c !important;
    }
    
    /* BOTÃO "Cadastrar Prato" COM TEXTO BRANCO */
    div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
        color: white !important;
        background: linear-gradient(135deg, #b4283c 0%, #a02335 100%) !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
        background: linear-gradient(135deg, #a02335 0%, #8c1e2e 100%) !important;
        color: white !important;
    }
    
    /* LABEL "Imagem do Prato" EM BRANCO */
    .stFileUploader label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* TEXTO DO FILE UPLOADER EM PRETO */
    [data-testid="stFileUploader"] p {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #666666 !important;
    }
    
    /* BOTÃO DE UPLOAD EM PRETO */
    [data-testid="stFileUploader"] button {
        color: #000000 !important;
        background: #f8f9fa !important;
        border: 1px solid #ced4da !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: #e9ecef !important;
        color: #000000 !important;
    }
    
    /* ÁREA DE DROP EM PRETO */
    [data-testid="stFileUploader"] > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px dashed #b4283c !important;
        color: #000000 !important;
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
    
    /* INPUTS - TEXTO PRETO */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        color: #000000 !important;
        background: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    
    /* BOTÕES + E - VISÍVEIS */
    .stNumberInput button {
        color: #000000 !important;
        background: #f8f9fa !important;
        border: 1px solid #ced4da !important;
    }
    
    .stNumberInput button:hover {
        background: #e9ecef !important;
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
    
    /* CARDS DE MÉTRICA */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px;
        padding: 1.8rem;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    }
    
    /* ALERTAS */
    .stAlert {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        backdrop-filter: blur(15px);
        border-left: 5px solid #b4283c;
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #b4283c 0%, #d6455c 100%) !important;
        border-radius: 12px;
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
    
    .login-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(180, 40, 60, 0.15) 0%, transparent 70%);
        animation: float 8s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-25px) rotate(180deg); }
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
    
    .status-recebido { border-left-color: #ff6b6b !important; }
    .status-preparando { border-left-color: #feca57 !important; }
    .status-pronto { border-left-color: #1dd1a1 !important; }
    .status-entregue { border-left-color: #54a0ff !important; }
    .status-cancelado { border-left-color: #576574 !important; }
</style>
""", unsafe_allow_html=True)

# CSS PROFISSIONAL COM CORREÇÃO DIRETA DOS SELECT BOXES
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
    
    /* CORREÇÃO RADICAL PARA SELECT BOXES */
    .stSelectbox > div > div {
        background-color: white !important;
    }
    
    .stSelectbox > div > div > div {
        color: #000000 !important;
        background-color: white !important;
    }
    
    .stSelectbox input {
        color: #000000 !important;
        background-color: white !important;
    }
    
    /* LISTA DROPDOWN */
    [data-baseweb="popover"] {
        background-color: white !important;
    }
    
    [data-baseweb="popover"] div {
        color: #000000 !important;
        background-color: white !important;
    }
    
    [data-baseweb="popover"] div:hover {
        background-color: #f0f0f0 !important;
        color: #000000 !important;
    }
    
    /* LABEL DOS SELECTBOX */
    .stSelectbox label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* SETA DO SELECTBOX */
    [data-baseweb="select"] svg {
        fill: #000000 !important;
    }

    /* HEADER */
    .main-header {
        background: linear-gradient(135deg, rgba(180, 40, 60, 0.85) 0%, rgba(160, 35, 55, 0.9) 100%) !important;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        backdrop-filter: blur(15px);
    }
    
    /* TEXTO BRANCO GERAL */
    .stApp, h1, h2, h3, h4, h5, h6, p, div, span {
        color: white !important;
    }
    
    /* BOTÕES */
    .stButton > button {
        background: linear-gradient(135deg, #b4283c 0%, #a02335 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px;
        padding: 6px;
        gap: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: white !important;
        border-radius: 10px;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #b4283c 0%, #a02335 100%) !important;
        color: white !important;
    }
    
    /* FORMULÁRIOS */
    .stForm {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    /* INPUTS */
    .stTextInput input, .stNumberInput input {
        color: #000000 !important;
        background: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# CSS ESPECÍFICO PARA CORRIGIR O TEXTO SELECIONADO NOS SELECT BOXES
st.markdown("""
<style>
    /* CORREÇÃO ESPECÍFICA PARA O TEXTO SELECIONADO NOS SELECT BOXES */
    [data-baseweb="select"] > div > div > div {
        color: #000000 !important;
        background-color: white !important;
    }
    
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] {
        color: #000000 !important;
    }
    
    /* CORREÇÃO PARA O PLACEHOLDER/TEXTO DO SELECT */
    [data-baseweb="select"] input::placeholder {
        color: #666666 !important;
    }
    
    [data-baseweb="select"] input {
        color: #000000 !important;
    }
    
    /* CORREÇÃO PARA O CONTAINER PRINCIPAL DO SELECT */
    .stSelectbox > div > div {
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #b4283c !important;
    }
    
    /* GARANTIR QUE TODOS OS ELEMENTOS DO SELECT TENHAM CORRETA */
    [data-baseweb="select"] * {
        color: #000000 !important;
    }
    
    /* CORREÇÃO ESPECÍFICA PARA O TEXTO QUANDO ESTÁ FECHADO */
    [data-baseweb="select"] > div > div > div > div {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript para forçar as cores dos botões
st.markdown("""
<script>
// Aguardar carregamento da página
setTimeout(function() {
    // Corrigir botão "Adicionar Ingrediente"
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        if (button.textContent.includes('Adicionar Ingrediente')) {
            button.style.color = '#000000' !important;
            button.style.backgroundColor = '#FFFFFF' !important;
            button.style.border = '2px solid #b4283c' !important;
            button.style.fontWeight = 'bold' !important;
        }
    });
    
    // Corrigir textos das selectboxes
    const selectContainers = document.querySelectorAll('[data-baseweb="select"]');
    selectContainers.forEach(container => {
        const selectedText = container.querySelector('[data-testid="stMarkdownContainer"]');
        if (selectedText) {
            selectedText.style.color = '#000000' !important;
        }
    });
}, 500);
</script>
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
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                novo_nome = st.text_input("Nome do Ingrediente", placeholder="Ex: Pão Brioche")
            with col2:
                categorias = ["paes", "carnes", "queijos", "saladas", "molhos", "complementos", "bebidas", "acompanhamentos"]
                nova_categoria = st.selectbox("Categoria", categorias)
            with col3:
                nova_unidade = st.selectbox("Unidade", ["unidade", "kg", "litro", "fatia", "porção", "sache", "gramas"])
            with col4:
                novo_estoque = st.number_input("Estoque Inicial", min_value=0, value=10)
            
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
                            "minimo": 5
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
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                
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
                    if st.button("💾", key=f"save_ing_{ingrediente['nome']}"):
                        ingredientes[i]['estoque'] = novo_estoque
                        ingredientes[i]['minimo'] = novo_minimo
                        with open(INGREDIENTES_FILE, "w", encoding="utf-8") as f:
                            json.dump(ingredientes, f, ensure_ascii=False, indent=2)
                        st.success("✅ Atualizado!")
                        st.rerun()
                
                with col5:
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
                st.progress(percentual/100, text=f"Estoque: {novo_estoque} {ingrediente['unidade']} / Mínimo: {novo_minimo}")
            
            st.divider()

    
    with tab2:
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
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✏️ Editar", key=f"edit_{i}"):
                        st.info("Funcionalidade de edição em desenvolvimento")
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
        
        # Custo estimado dos pratos
        st.subheader("💲 Custo Estimado por Prato")
        for prato in pratos:
            custo_estimado = calcular_custo_prato(prato, ingredientes)
            lucro = prato['preco'] - custo_estimado
            margem = (lucro / prato['preco']) * 100 if prato['preco'] > 0 else 0
            
            st.write(f"**{prato['nome']}**")
            st.write(f"Preço: R$ {prato['preco']:.2f} | Custo: R$ {custo_estimado:.2f} | Lucro: R$ {lucro:.2f} ({margem:.1f}%)")
            st.progress(min(margem/100, 1), text=f"Margem: {margem:.1f}%")

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