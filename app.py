# app.py - VERSÃO COM TABELA NUTRICIONAL PERSONALIZADA
import streamlit as st
import os
import json
import streamlit.components.v1 as components
from datetime import datetime

# =============== CONFIGURAÇÃO INICIAL ===============
st.set_page_config(page_title="Burger Express", layout="centered")

# =============== REMOVER CABEÇALHO STREAMLIT ===============
st.markdown("""
<style>
    #MainMenu {visibility: hidden !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    .stDeployButton {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    .block-container {padding-top: 2rem !important;}
</style>
""", unsafe_allow_html=True)

# =============== FUNÇÕES DE DADOS ===============
def carregar_pratos():
    if os.path.exists("pratos.json"):
        try:
            with open("pratos.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    else:
        pratos_padrao = [
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
            {"nome": "Refrigerante", "preco": 8.90, "cat": "bebidas", "img": "refri.jpg", "ingredientes": []},
            {"nome": "Suco Natural", "preco": 12.90, "cat": "bebidas", "img": "suco.jpg", "ingredientes": []},
            {"nome": "Batata Frita", "preco": 12.90, "cat": "acompanhamentos", "img": "batata-frita.jpg", "ingredientes": []},
            {"nome": "Onion Rings", "preco": 15.90, "cat": "acompanhamentos", "img": "onion-rings.jpg", "ingredientes": []},
            {"nome": "Milk Shake", "preco": 16.90, "cat": "sobremesas", "img": "milkshake.jpg", "ingredientes": []},
            {"nome": "Brownie", "preco": 14.90, "cat": "sobremesas", "img": "brownie.jpg", "ingredientes": []},
        ]
        with open("pratos.json", "w", encoding="utf-8") as f:
            json.dump(pratos_padrao, f, ensure_ascii=False, indent=2)
        return pratos_padrao

pratos = carregar_pratos()

# =============== FUNÇÕES PARA TABELA NUTRICIONAL PERSONALIZADA ===============
def salvar_informacoes_nutricionais(prato_nome, dados_nutricionais):
    """Salva informações nutricionais em um arquivo JSON"""
    arquivo_nutricional = "tabela_nutricional.json"
    
    try:
        if os.path.exists(arquivo_nutricional):
            with open(arquivo_nutricional, "r", encoding="utf-8") as f:
                tabela_existente = json.load(f)
        else:
            tabela_existente = {}
        
        # Adicionar ou atualizar os dados
        tabela_existente[prato_nome] = dados_nutricionais
        
        with open(arquivo_nutricional, "w", encoding="utf-8") as f:
            json.dump(tabela_existente, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados nutricionais: {e}")
        return False

def obter_informacoes_nutricionais(prato_nome):
    """Retorna informações nutricionais para cada prato - COM SUPORTE PARA DADOS PERSONALIZADOS"""
    # Primeiro tenta carregar do arquivo personalizado
    arquivo_nutricional = "tabela_nutricional.json"
    
    if os.path.exists(arquivo_nutricional):
        try:
            with open(arquivo_nutricional, "r", encoding="utf-8") as f:
                tabela_personalizada = json.load(f)
                if prato_nome in tabela_personalizada:
                    return tabela_personalizada[prato_nome]
        except:
            pass
    
    # Se não encontrar, usa a tabela padrão (fallback)
    tabela_nutricional = {
        "Burger Classic": {
            "calorias": 680,
            "proteinas": 42,
            "carboidratos": 45,
            "gorduras": 32,
            "gorduras_saturadas": 12,
            "fibra": 4,
            "sodio": 980,
            "descricao": "Hambúrguer clássico com carne 100% bovina, queijo, alface, tomate e molho especial.",
            "alergenicos": ["Glúten", "Lactose", "Leite"]
        },
        "Burger Bacon": {
            "calorias": 850,
            "proteinas": 45,
            "carboidratos": 50,
            "gorduras": 45,
            "gorduras_saturadas": 18,
            "fibra": 3,
            "sodio": 1250,
            "descricao": "Hambúrguer com bacon crocante, queijo cheddar duplo e pão brioche.",
            "alergenicos": ["Glúten", "Lactose", "Leite", "Soja"]
        },
        "Double Cheese": {
            "calorias": 920,
            "proteinas": 58,
            "carboidratos": 48,
            "gorduras": 52,
            "gorduras_saturadas": 22,
            "fibra": 5,
            "sodio": 1350,
            "descricao": "Dois hambúrgueres com dupla camada de queijo cheddar e mussarela.",
            "alergenicos": ["Glúten", "Lactose", "Leite"]
        },
        "Refrigerante": {
            "calorias": 150,
            "proteinas": 0,
            "carboidratos": 38,
            "gorduras": 0,
            "gorduras_saturadas": 0,
            "fibra": 0,
            "sodio": 45,
            "descricao": "Refrigerante gelado 350ml.",
            "alergenicos": []
        },
        "Suco Natural": {
            "calorias": 110,
            "proteinas": 1,
            "carboidratos": 26,
            "gorduras": 0,
            "gorduras_saturadas": 0,
            "fibra": 2,
            "sodio": 10,
            "descricao": "Suco natural de laranja espremido na hora.",
            "alergenicos": []
        },
        "Batata Frita": {
            "calorias": 420,
            "proteinas": 5,
            "carboidratos": 55,
            "gorduras": 18,
            "gorduras_saturadas": 3,
            "fibra": 6,
            "sodio": 320,
            "descricao": "Porção de batatas fritas crocantes temperadas.",
            "alergenicos": ["Glúten"]
        },
        "Onion Rings": {
            "calorias": 380,
            "proteinas": 4,
            "carboidratos": 42,
            "gorduras": 20,
            "gorduras_saturadas": 4,
            "fibra": 3,
            "sodio": 480,
            "descricao": "Anéis de cebola empanados e fritos, crocantes por fora e macios por dentro.",
            "alergenicos": ["Glúten", "Leite"]
        },
        "Milk Shake": {
            "calorias": 520,
            "proteinas": 12,
            "carboidratos": 75,
            "gorduras": 18,
            "gorduras_saturadas": 11,
            "fibra": 1,
            "sodio": 180,
            "descricao": "Milk shake cremoso de baunilha com cobertura de chocolate.",
            "alergenicos": ["Lactose", "Leite", "Soja"]
        },
        "Brownie": {
            "calorias": 380,
            "proteinas": 5,
            "carboidratos": 55,
            "gorduras": 16,
            "gorduras_saturadas": 8,
            "fibra": 3,
            "sodio": 220,
            "descricao": "Brownie de chocolate com nozes e calda de chocolate.",
            "alergenicos": ["Glúten", "Lactose", "Leite", "Ovos", "Nozes"]
        }
    }
    
    return tabela_nutricional.get(prato_nome, {
        "calorias": 0,
        "proteinas": 0,
        "carboidratos": 0,
        "gorduras": 0,
        "gorduras_saturadas": 0,
        "fibra": 0,
        "sodio": 0,
        "descricao": "Informações nutricionais não disponíveis.",
        "alergenicos": []
    })

# =============== FUNÇÃO PARA EXIBIR TABELA NUTRICIONAL ===============
def exibir_tabela_nutricional(prato_nome):
    """Exibe a tabela nutricional usando componentes do Streamlit"""
    info_nutricional = obter_informacoes_nutricionais(prato_nome)
    
    # Container com estilo
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border-left: 6px solid #EA1D2C;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    ">
    """, unsafe_allow_html=True)
    
    # Cabeçalho
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### {prato_nome}")
    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #EA1D2C, #c91a26);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-align: center;
            font-weight: bold;
            font-size: 1.1rem;
        ">
            {info_nutricional['calorias']} kcal
        </div>
        """, unsafe_allow_html=True)
    
    # Descrição
    st.info(f"**Descrição:** {info_nutricional['descricao']}")
    
    # Tabela nutricional usando st.dataframe ou st.table
    st.markdown("#### Informações Nutricionais")
    
    # Criar dados para a tabela
    dados_nutricionais = [
        ["Valor energético", f"{info_nutricional['calorias']} kcal", f"{info_nutricional['calorias']//80}%"],
        ["Proteínas", f"{info_nutricional['proteinas']}g", f"{info_nutricional['proteinas']*100//75}%"],
        ["Carboidratos", f"{info_nutricional['carboidratos']}g", f"{info_nutricional['carboidratos']*100//300}%"],
        ["Gorduras totais", f"{info_nutricional['gorduras']}g", f"{info_nutricional['gorduras']*100//55}%"],
        ["Gorduras saturadas", f"{info_nutricional['gorduras_saturadas']}g", f"{info_nutricional['gorduras_saturadas']*100//22}%"],
        ["Fibra alimentar", f"{info_nutricional['fibra']}g", f"{info_nutricional['fibra']*100//25}%"],
        ["Sódio", f"{info_nutricional['sodio']}mg", f"{info_nutricional['sodio']*100//2400}%"]
    ]
    
    # Exibir como tabela
    for i, (nutriente, quantidade, vd) in enumerate(dados_nutricionais):
        bg_color = "#f8f9fa" if i % 2 == 0 else "white"
        st.markdown(f"""
        <div style="
            background: {bg_color};
            padding: 12px 15px;
            border-radius: 8px;
            margin: 5px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div><strong>{nutriente}</strong></div>
            <div style="font-weight: bold;">{quantidade}</div>
            <div style="color: #EA1D2C; font-weight: bold;">{vd}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Resumo com ícones
    st.markdown("#### Resumo")
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <div style="color:#EA1D2C;font-size:1.5rem;">🔥</div>
            <div style="font-size:0.9rem;color:#6c757d;">Calorias</div>
            <div style="font-weight:bold;color:#2e2e2e;font-size:1.2rem;">{info_nutricional['calorias']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <div style="color:#EA1D2C;font-size:1.5rem;">💪</div>
            <div style="font-size:0.9rem;color:#6c757d;">Proteínas</div>
            <div style="font-weight:bold;color:#2e2e2e;font-size:1.2rem;">{info_nutricional['proteinas']}g</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <div style="color:#EA1D2C;font-size:1.5rem;">🍞</div>
            <div style="font-size:0.9rem;color:#6c757d;">Carboidratos</div>
            <div style="font-weight:bold;color:#2e2e2e;font-size:1.2rem;">{info_nutricional['carboidratos']}g</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <div style="color:#EA1D2C;font-size:1.5rem;">⚡</div>
            <div style="font-size:0.9rem;color:#6c757d;">Gorduras</div>
            <div style="font-weight:bold;color:#2e2e2e;font-size:1.2rem;">{info_nutricional['gorduras']}g</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Alérgenos
    if info_nutricional.get('alergenicos'):
        st.warning("**Alérgenos presentes:** " + ", ".join(info_nutricional['alergenicos']))
    
    # Nota de rodapé
    st.markdown("---")
    st.caption("*VD - Valores Diários de Referência: Com base em uma dieta de 2000 kcal ou 8400 kJ. Seus valores diários podem ser maiores ou menores dependendo de suas necessidades energéticas.*")
    
    st.markdown("</div>", unsafe_allow_html=True)

# =============== FUNÇÕES DE PEDIDOS ===============
def salvar_pedido_completo(pedido_completo):
    """Salva o pedido completo com todas as informações do checkout"""
    pedidos = carregar_pedidos()
    
    # Converter itens para formato do pedido
    itens_pedido = []
    for nome, qtd in pedido_completo["itens"].items():
        preco_prato = next((p["preco"] for p in pratos if p["nome"] == nome), 0)
        itens_pedido.append({
            "nome": nome, 
            "quantidade": qtd, 
            "preco": preco_prato
        })
    
    novo_pedido = {
        "id": len(pedidos) + 1,
        "cliente": "Cliente App",
        "itens": itens_pedido,
        "subtotal": pedido_completo["subtotal"],
        "taxa_entrega": pedido_completo["taxa_entrega"],
        "desconto": pedido_completo["desconto"],
        "total": pedido_completo["total"],
        "forma_entrega": pedido_completo["forma_entrega"],
        "forma_pagamento": pedido_completo["forma_pagamento"],
        "cupom": pedido_completo["cupom"],
        "endereco": pedido_completo["endereco"],
        "troco_para": pedido_completo["troco_para"],
        "status": "recebido",
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tempo_preparo_estimado": 40 if pedido_completo["forma_entrega"] == "delivery" else 25
    }
    
    pedidos.append(novo_pedido)
    
    # Salva no arquivo
    with open("pedidos.json", "w", encoding="utf-8") as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=2)
    
    return novo_pedido

def carregar_pedidos():
    """Carrega os pedidos existentes"""
    if os.path.exists("pedidos.json"):
        try:
            with open("pedidos.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# =============== FUNÇÕES DE INGREDIENTES ===============
def carregar_ingredientes():
    if os.path.exists("ingredientes.json"):
        try:
            with open("ingredientes.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def verificar_disponibilidade_prato(prato):
    """Verifica se o prato pode ser feito com os ingredientes disponíveis"""
    ingredientes = carregar_ingredientes()
    
    for ing_prato in prato.get('ingredientes', []):
        ingrediente = next((i for i in ingredientes if i['nome'] == ing_prato['nome']), None)
        if not ingrediente or ingrediente['estoque'] < ing_prato['quantidade']:
            return False, ing_prato['nome']
    return True, None

def produto_disponivel(nome_prato):
    """Verifica se um prato está disponível"""
    prato = next((p for p in pratos if p["nome"] == nome_prato), None)
    if prato:
        disponivel, _ = verificar_disponibilidade_prato(prato)
        return disponivel
    return False

# =============== FUNÇÕES DE FAVORITOS ===============
def toggle_favorito(nome_prato):
    """Alterna o estado de favorito de um prato"""
    if nome_prato in st.session_state.favoritos:
        st.session_state.favoritos.remove(nome_prato)
    else:
        st.session_state.favoritos.append(nome_prato)
    # Salvar imediatamente após modificar
    salvar_favoritos()

def salvar_favoritos():
    """Salva os favoritos em um arquivo JSON"""
    with open("favoritos.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.favoritos, f, ensure_ascii=False, indent=2)

def carregar_favoritos():
    """Carrega os favoritos do arquivo JSON"""
    if os.path.exists("favoritos.json"):
        try:
            with open("favoritos.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# =============== CSS ATUALIZADO ===============
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    .header {position: fixed;top:0;left:0;width:100%;z-index:999999;background:#fff;height:72px;box-shadow:0 2px 8px rgba(0,0,0,0.08);}
    .block-container {padding-top: 50px !important;}
    .full-width-section {width:100vw;position:relative;left:50%;right:50%;margin-left:-50vw;margin-right:-50vw;margin-top: -20px !important;}
    .stButton > button[kind="primary"] {background:#EA1D2C !important;color:white !important;border:none !important;border-radius:8px !important;font-weight:600 !important;}
    .stButton > button:hover {background:#c91a26 !important;}
    div[data-testid="stImage"] > img {height:180px !important;object-fit:cover !important;border-radius:8px 8px 0 0 !important;width:100% !important;}
    .admin-btn {background:#EA1D2C;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:600;}
    .hero {background:linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.5)),url('https://images.unsplash.com/photo-1553979459-d2229ba7433b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80') center/cover;min-height:calc(100vh - 72px);display:flex;align-items:center;text-align:center;color:white;}
    .hero h2 {font-size:3.8rem;font-weight:700;}
    .hero p {font-size:1.5rem;max-width:700px;margin:20px auto;}
    .btn {background:#EA1D2C;color:white;padding:16px 45px;border-radius:8px;font-weight:700;text-decoration:none;font-size:1.3rem;}
    .menu {padding:40px 0 80px;background:#fff;}
    .section-title {text-align:center;font-size:2rem;color:#2e2e2e;margin-bottom:30px;font-weight:700;}
    .products-grid {display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;max-width:1200px;margin:0 auto;padding:0 20px;}
    .product-card {background:white;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);transition:.3s;border:1px solid #f0f0f0;position:relative;}
    .product-card:hover {transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,0,0,0.12);}
    .product-info {padding:16px;text-align:left;}
    .product-info h3 {margin:0 0 8px;font-size:1.1rem;color:#2e2e2e;font-weight:600;}
    .price {font-size:1.3rem;font-weight:700;color:#2e2e2e;}
    .about {padding:80px 0;background:#f8f8f8;}
    .footer {background:linear-gradient(135deg,#2e2e2e,#1a1a1a);color:#fff;padding:60px 0 30px;}
    
    /* Estilos para botão de favorito FUNCIONAL */
    .favorite-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(255, 255, 255, 0.95);
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 100;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        font-size: 1.2rem;
    }
    
    .favorite-btn:hover {
        background: white;
        transform: scale(1.15);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .favorite-btn.favorited {
        color: #EA1D2C;
    }
    
    .favorite-btn:not(.favorited) {
        color: #999;
    }
    
    .favorite-btn.favorited:hover {
        color: #c91a26;
    }
    
    /* Estilos para botão de nutrição */
    .nutrition-btn {
        background: linear-gradient(135deg, #27ae60, #219653) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        margin-top: 8px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(39, 174, 96, 0.2) !important;
    }
    
    .nutrition-btn:hover {
        background: linear-gradient(135deg, #219653, #1e8449) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3) !important;
    }
    
    /* Mensagem quando não há favoritos */
    .no-favorites-container {
        text-align: center;
        padding: 60px 20px;
        background: #f9f9f9;
        border-radius: 12px;
        margin: 40px auto;
        max-width: 600px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .no-favorites-icon {
        font-size: 4rem;
        color: #EA1D2C;
        margin-bottom: 20px;
        opacity: 0.7;
    }
    
    .no-favorites-title {
        color: #2e2e2e;
        font-size: 1.8rem;
        margin-bottom: 15px;
        font-weight: 600;
    }
    
    .no-favorites-text {
        color: #666;
        font-size: 1.1rem;
        line-height: 1.6;
        max-width: 500px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">', unsafe_allow_html=True)

# =============== GESTÃO DE ESTADO ===============
if "carrinho" not in st.session_state: 
    st.session_state.carrinho = {}
if "categoria_atual" not in st.session_state: 
    st.session_state.categoria_atual = "hamburgers"
if "favoritos" not in st.session_state:
    st.session_state.favoritos = carregar_favoritos()
if "tabela_nutricional_ativa" not in st.session_state:
    st.session_state.tabela_nutricional_ativa = None

# Inicializar dados do checkout
if "checkout_data" not in st.session_state:
    st.session_state.checkout_data = {
        "forma_entrega": "retirada",
        "forma_pagamento": "dinheiro",
        "cupom": "",
        "desconto": 0,
        "taxa_entrega": 0,
        "endereco": "",
        "troco_para": ""
    }

# Função para adicionar/remover itens do carrinho
def atualizar_item_carrinho(nome_prato, quantidade):
    if quantidade > 0:
        st.session_state.carrinho[nome_prato] = quantidade
    else:
        if nome_prato in st.session_state.carrinho:
            del st.session_state.carrinho[nome_prato]

def limpar_carrinho():
    st.session_state.carrinho = {}
    st.session_state.checkout_data = {
        "forma_entrega": "retirada",
        "forma_pagamento": "dinheiro",
        "cupom": "",
        "desconto": 0,
        "taxa_entrega": 0,
        "endereco": "",
        "troco_para": ""
    }

# =============== HEADER ===============
st.markdown(f"""
<header class="header">
    <div style="max-width:1200px;margin:0 auto;padding:0 20px;display:flex;justify-content:space-between;align-items:center;height:100%;">
        <div style="color:#2e2e2e;font-size:1.9rem;font-weight:700;">Burger Express</div>
        <nav>
            <a href="#inicio" style="color:#2e2e2e;text-decoration:none;margin:0 20px;font-weight:600;">Início</a>
            <a href="#menu" style="color:#2e2e2e;text-decoration:none;margin:0 20px;font-weight:600;">Menu</a>
            <a href="#sobre" style="color:#2e2e2e;text-decoration:none;margin:0 20px;font-weight:600;">Sobre</a>
            <a href="#desenvolvedores" style="color:#2e2e2e;text-decoration:none;margin:0 20px;font-weight:600;">Devs</a>
        </nav>
        <div style="display:flex;gap:20px;align-items:center;">
            <a href="/admin" target="_self" class="admin-btn">
                <i class="fas fa-lock"></i> Admin
            </a>
            <a href="#carrinho" style="text-decoration:none;position:relative;cursor:pointer;">
                <i class="fas fa-shopping-cart" style="font-size:1.8rem;color:#2e2e2e;"></i>
                <span style="position:absolute;top:-10px;right:-10px;background:#EA1D2C;color:white;width:24px;height:24px;border-radius:50%;font-size:0.8rem;display:flex;align-items:center;justify-content:center;">
                    {sum(st.session_state.carrinho.values())}
                </span>
            </a>
        </div>
    </div>
</header>
""", unsafe_allow_html=True)

# =============== HERO ===============
st.markdown("""
<section id="inicio" class="hero full-width-section">
    <div style="max-width:800px;margin:0 auto;">
        <h2>Os Melhores Hambúrgueres da Cidade!</h2>
        <p>Experimente nosso menu exclusivo com ingredientes frescos e sabor inigualável</p>
        <a href="#menu" class="btn">Ver Menu</a>
    </div>
</section>
""", unsafe_allow_html=True)

# =============== MENU ===============
st.markdown("""
<section id="menu" class="menu">
    <div style="max-width:1200px;margin:0 auto;padding:0 20px;">
        <h2 class="section-title">Nosso Menu</h2>
""", unsafe_allow_html=True)

# Botões de categoria - AGORA COM 5 COLUNAS (incluindo favoritos)
cols = st.columns(5)
categorias = [
    ("hamburgers", "🍔 Hambúrgueres"), 
    ("bebidas", "🥤 Bebidas"), 
    ("acompanhamentos", "🍟 Acomp."), 
    ("sobremesas", "🍰 Sobremesas"),
    ("favoritos", f"❤️ Favoritos ({len(st.session_state.favoritos)})")
]

for i, (key, nome) in enumerate(categorias):
    with cols[i]:
        if st.button(nome, use_container_width=True, 
                     type="primary" if st.session_state.categoria_atual == key else "secondary",
                     key=f"cat_{key}"):
            st.session_state.categoria_atual = key
            st.rerun()

st.markdown('<div class="products-grid">', unsafe_allow_html=True)

# Mostrar conteúdo baseado na categoria selecionada
if st.session_state.categoria_atual == "favoritos":
    # Seção de favoritos
    pratos_mostrar = [p for p in pratos if p["nome"] in st.session_state.favoritos]
    
    if not pratos_mostrar:
        # Mensagem quando não há favoritos
        st.markdown("""
        <div class="no-favorites-container">
            <div class="no-favorites-icon">
                <i class="fas fa-heart-broken"></i>
            </div>
            <h3 class="no-favorites-title">Nenhum favorito ainda</h3>
            <p class="no-favorites-text">
                Explore nosso menu e clique no ícone ❤️ nos produtos para adicioná-los aos seus favoritos!
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Mostrar produtos favoritados
        for prato in pratos_mostrar:
            disponivel, ingrediente_faltante = verificar_disponibilidade_prato(prato)
            
            with st.container():
                # Card do produto
                if not disponivel:
                    st.markdown('<div class="product-card" style="opacity:0.6;position:relative;">', unsafe_allow_html=True)
                    st.markdown(f'<div style="position:absolute;top:10px;left:10px;background:#EA1D2C;color:white;padding:4px 8px;border-radius:4px;font-size:0.8rem;z-index:10;">SEM {ingrediente_faltante.upper()}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                
                # Botão de favorito (sempre favoritado nesta seção)
                if st.button("❤️", 
                           key=f"fav_heart_{prato['nome']}",
                           help="Remover dos favoritos",
                           type="secondary" if prato["nome"] in st.session_state.favoritos else "primary"):
                    toggle_favorito(prato["nome"])
                    st.rerun()
                
                # Ajustar estilo do botão manualmente
                st.markdown(f"""
                <style>
                    [data-testid="baseButton-secondary"][data-testid="baseButton-secondary"] {{
                        position: absolute;
                        top: 10px;
                        right: 10px;
                        background: white !important;
                        color: #EA1D2C !important;
                        border-radius: 50% !important;
                        width: 40px !important;
                        height: 40px !important;
                        min-width: 40px !important;
                        padding: 0 !important;
                        z-index: 100;
                        border: none !important;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
                    }}
                    [data-testid="baseButton-secondary"]:hover {{
                        background: white !important;
                        transform: scale(1.15);
                        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
                    }}
                </style>
                """, unsafe_allow_html=True)
                
                # Imagem
                caminho_imagem = os.path.join("images", prato["img"])
                if os.path.exists(caminho_imagem):
                    st.image(caminho_imagem, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/400x240/EA1D2C/white?text=Imagem+Indisponível", 
                            use_container_width=True)
                
                # Informações com ingredientes
                with st.expander(f"🍔 {prato['nome']} - R$ {prato['preco']:.2f}", expanded=False):
                    st.write("**Ingredientes:**")
                    if prato.get('ingredientes'):
                        for ing in prato['ingredientes']:
                            st.write(f"• {ing['nome']}")
                    else:
                        st.write("• Ingredientes padrão")
                
                # Botão para ver tabela nutricional - CORRIGIDO
                if st.button("📊 Ver Tabela Nutricional", 
                           key=f"btn_nutri_fav_{prato['nome']}",
                           type="primary",
                           use_container_width=True):
                    st.session_state.tabela_nutricional_ativa = prato['nome']
                    st.rerun()
                
                # Controle de quantidade
                quantidade_atual = st.session_state.carrinho.get(prato["nome"], 0)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if st.button("➖", key=f"fav_menos_{prato['nome']}", use_container_width=True, disabled=not disponivel):
                        nova_quantidade = max(0, quantidade_atual - 1)
                        atualizar_item_carrinho(prato["nome"], nova_quantidade)
                        st.rerun()
                
                with col2:
                    if disponivel:
                        st.markdown(f"<div style='text-align:center;padding:8px;background:#f5f5f5;border-radius:4px;font-weight:bold;'>{quantidade_atual}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align:center;padding:8px;background:#ffcccc;border-radius:4px;font-weight:bold;color:#cc0000;'>INDISPONÍVEL</div>", unsafe_allow_html=True)
                
                with col3:
                    if st.button("➕", key=f"fav_mais_{prato['nome']}", use_container_width=True, disabled=not disponivel):
                        nova_quantidade = quantidade_atual + 1
                        atualizar_item_carrinho(prato["nome"], nova_quantidade)
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
else:
    # Seção normal de produtos
    for prato in [p for p in pratos if p["cat"] == st.session_state.categoria_atual]:
        disponivel, ingrediente_faltante = verificar_disponibilidade_prato(prato)
        
        with st.container():
            # Card do produto
            if not disponivel:
                st.markdown('<div class="product-card" style="opacity:0.6;position:relative;">', unsafe_allow_html=True)
                st.markdown(f'<div style="position:absolute;top:10px;left:10px;background:#EA1D2C;color:white;padding:4px 8px;border-radius:4px;font-size:0.8rem;z-index:10;">SEM {ingrediente_faltante.upper()}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            # Botão de favorito - AGORA FUNCIONAL
            is_favorito = prato["nome"] in st.session_state.favoritos
            btn_type = "secondary" if is_favorito else "primary"
            btn_icon = "❤️" if is_favorito else "🤍"
            
            if st.button(btn_icon, 
                       key=f"heart_{prato['nome']}",
                       help="Adicionar aos favoritos" if not is_favorito else "Remover dos favoritos",
                       type=btn_type):
                toggle_favorito(prato["nome"])
                st.rerun()
            
            # Ajustar estilo do botão
            st.markdown(f"""
            <style>
                [data-testid="baseButton-{btn_type}"][data-testid="baseButton-{btn_type}"] {{
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: white !important;
                    color: {'#EA1D2C' if is_favorito else '#999'} !important;
                    border-radius: 50% !important;
                    width: 40px !important;
                    height: 40px !important;
                    min-width: 40px !important;
                    padding: 0 !important;
                    z-index: 100;
                    border: none !important;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
                    font-size: 1.2rem !important;
                }}
                [data-testid="baseButton-{btn_type}"]:hover {{
                    background: white !important;
                    transform: scale(1.15);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
                    color: {'#c91a26' if is_favorito else '#666'} !important;
                }}
            </style>
            """, unsafe_allow_html=True)
            
            # Imagem
            caminho_imagem = os.path.join("images", prato["img"])
            if os.path.exists(caminho_imagem):
                st.image(caminho_imagem, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/400x240/EA1D2C/white?text=Imagem+Indisponível", 
                        use_container_width=True)
            
            # Informações com ingredientes
            with st.expander(f"🍔 {prato['nome']} - R$ {prato['preco']:.2f}", expanded=False):
                st.write("**Ingredientes:**")
                if prato.get('ingredientes'):
                    for ing in prato['ingredientes']:
                        st.write(f"• {ing['nome']}")
                else:
                    st.write("• Ingredientes padrão")
            
            # Botão para ver tabela nutricional - CORRIGIDO
            if st.button("📊 Ver Tabela Nutricional", 
                       key=f"btn_nutri_{prato['nome']}",
                       type="primary",
                       use_container_width=True):
                st.session_state.tabela_nutricional_ativa = prato['nome']
                st.rerun()
            
            # Controle de quantidade
            quantidade_atual = st.session_state.carrinho.get(prato["nome"], 0)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("➖", key=f"menos_{prato['nome']}", use_container_width=True, disabled=not disponivel):
                    nova_quantidade = max(0, quantidade_atual - 1)
                    atualizar_item_carrinho(prato["nome"], nova_quantidade)
                    st.rerun()
            
            with col2:
                if disponivel:
                    st.markdown(f"<div style='text-align:center;padding:8px;background:#f5f5f5;border-radius:4px;font-weight:bold;'>{quantidade_atual}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align:center;padding:8px;background:#ffcccc;border-radius:4px;font-weight:bold;color:#cc0000;'>INDISPONÍVEL</div>", unsafe_allow_html=True)
            
            with col3:
                if st.button("➕", key=f"mais_{prato['nome']}", use_container_width=True, disabled=not disponivel):
                    nova_quantidade = quantidade_atual + 1
                    atualizar_item_carrinho(prato["nome"], nova_quantidade)
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</section>', unsafe_allow_html=True)

# =============== EXIBIR TABELA NUTRICIONAL ===============
if st.session_state.tabela_nutricional_ativa:
    prato_nome = st.session_state.tabela_nutricional_ativa
    
    # Cabeçalho destacado
    st.markdown("---")
    col_title, col_close = st.columns([5, 1])
    
    with col_title:
        st.markdown(f"## 📊 Tabela Nutricional - {prato_nome}")
    
    with col_close:
        if st.button("✕ Fechar", key="btn_fechar_tabela", type="secondary"):
            st.session_state.tabela_nutricional_ativa = None
            st.rerun()
    
    # Linha divisória
    st.markdown("---")
    
    # Exibir a tabela nutricional
    exibir_tabela_nutricional(prato_nome)
    
    # Botão para fechar
    if st.button("Fechar Tabela Nutricional", 
                 key="btn_fechar_tabela2",
                 type="primary",
                 use_container_width=True):
        st.session_state.tabela_nutricional_ativa = None
        st.rerun()
    
    st.markdown("---")

# =============== CARRINHO COM CHECKOUT COMPLETO ===============
if st.session_state.carrinho:
    total = 0
    itens_detalhados = []
    
    for nome, qtd in st.session_state.carrinho.items():
        preco = next((p["preco"] for p in pratos if p["nome"] == nome), 0)
        subtotal = qtd * preco
        total += subtotal
        itens_detalhados.append({"nome": nome, "quantidade": qtd, "preco": preco, "subtotal": subtotal})
    
    # Exibe o carrinho
    st.markdown("""
    <div id="carrinho" style='background:white;padding:30px;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.1);margin:40px 0;'>
        <h2 style='color:#EA1D2C;text-align:center;margin-bottom:25px;'>🛒 Seu Pedido</h2>
    """, unsafe_allow_html=True)
    
    for item in itens_detalhados:
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #f0f0f0;'>
            <div>
                <strong>{item['nome']}</strong>
                <br>
                <small>Quantidade: {item['quantidade']}</small>
            </div>
            <strong style='color:#EA1D2C;'>R$ {item['subtotal']:.2f}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;padding:20px 0;margin-top:15px;border-top:2px solid #EA1D2C;font-size:1.4rem;font-weight:bold;'>
            <span>SUBTOTAL:</span>
            <span style='color:#EA1D2C;'>R$ {total:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # =============== CHECKOUT EXPANDIBLE ===============
    with st.expander("💰 **Finalizar Pedido - Checkout**", expanded=False):
        
        # COLUNAS PRINCIPAIS
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚚 Entrega")
            
            # Forma de Entrega
            forma_entrega = st.radio(
                "Escolha a forma de entrega:",
                ["retirada", "delivery"],
                format_func=lambda x: "🏪 Retirada no Local" if x == "retirada" else "🚚 Delivery",
                key="forma_entrega"
            )
            
            st.session_state.checkout_data["forma_entrega"] = forma_entrega
            
            # Se for delivery, mostrar campo de endereço e taxa
            if forma_entrega == "delivery":
                st.session_state.checkout_data["taxa_entrega"] = 5.00
                endereco = st.text_input("📮 Endereço de Entrega:", placeholder="Digite seu endereço completo", key="endereco_input")
                st.session_state.checkout_data["endereco"] = endereco
                st.info("📍 Taxa de entrega: R$ 5,00")
            else:
                st.session_state.checkout_data["taxa_entrega"] = 0
                st.session_state.checkout_data["endereco"] = ""
                st.success("✅ Retirada gratuita no balcão")
        
        with col2:
            st.subheader("💳 Pagamento")
            
            # Forma de Pagamento
            forma_pagamento = st.radio(
                "Forma de pagamento:",
                ["dinheiro", "cartao", "pix"],
                format_func=lambda x: {
                    "dinheiro": "💵 Dinheiro",
                    "cartao": "💳 Cartão", 
                    "pix": "📱 PIX"
                }[x],
                key="forma_pagamento"
            )
            
            st.session_state.checkout_data["forma_pagamento"] = forma_pagamento
            
            # Se for dinheiro, pedir troco
            if forma_pagamento == "dinheiro":
                troco_para = st.text_input("💰 Troco para quanto?", placeholder="Ex: 50,00", key="troco_input")
                st.session_state.checkout_data["troco_para"] = troco_para
            else:
                st.session_state.checkout_data["troco_para"] = ""
        
        # CUPOM DE DESCONTO
        st.subheader("🎫 Cupom de Desconto")
        cupom_col1, cupom_col2 = st.columns([3, 1])
        
        with cupom_col1:
            cupom = st.text_input("Digite seu cupom:", placeholder="Ex: BURGER10", key="cupom_input")
        
        with cupom_col2:
            st.write("")  # Espaço
            st.write("")  # Espaço
            if st.button("Aplicar Cupom", use_container_width=True):
                cupom = cupom.upper().strip()
                # Cupons válidos
                cupons_validos = {
                    "BURGER10": 0.10,  # 10% de desconto
                    "BURGER20": 0.20,  # 20% de desconto
                    "PRIMEIRACOMPRA": 0.15,  # 15% de desconto
                    "BURGEREXPRESS": 0.05  # 5% de desconto
                }
                
                if cupom in cupons_validos:
                    desconto = total * cupons_validos[cupom]
                    st.session_state.checkout_data["desconto"] = desconto
                    st.session_state.checkout_data["cupom"] = cupom
                    st.success(f"🎉 Cupom aplicado! Desconto: R$ {desconto:.2f}")
                else:
                    st.session_state.checkout_data["desconto"] = 0
                    st.session_state.checkout_data["cupom"] = ""
                    st.error("❌ Cupom inválido ou expirado")
        
        # =============== RESUMO FINAL ===============
        st.markdown("---")
        st.subheader("📋 Resumo do Pedido")
        
        # Cálculos finais
        subtotal = total
        taxa_entrega = st.session_state.checkout_data["taxa_entrega"]
        desconto = st.session_state.checkout_data["desconto"]
        total_final = subtotal + taxa_entrega - desconto
        
        # Tabela de resumo
        resumo_data = {
            "Descrição": ["Subtotal", "Taxa de Entrega", "Desconto", "**TOTAL FINAL**"],
            "Valor": [
                f"R$ {subtotal:.2f}",
                f"R$ {taxa_entrega:.2f}" if taxa_entrega > 0 else "Grátis",
                f"-R$ {desconto:.2f}" if desconto > 0 else "R$ 0,00",
                f"**R$ {total_final:.2f}**"
            ]
        }
        
        # Exibir resumo
        for i, (desc, valor) in enumerate(zip(resumo_data["Descrição"], resumo_data["Valor"])):
            col_desc, col_valor = st.columns([3, 1])
            with col_desc:
                if i == 3:  # Total final
                    st.markdown(f"**{desc}**")
                else:
                    st.write(desc)
            with col_valor:
                if i == 3:  # Total final
                    st.markdown(f"<h3 style='color:#EA1D2C; margin:0;'>{valor}</h3>", unsafe_allow_html=True)
                else:
                    st.write(valor)
        
        # Informações adicionais
        if st.session_state.checkout_data["forma_pagamento"] == "pix":
            st.info("📱 **PIX**: Chave: (61) 99999-9999 - Envie o comprovante para confirmar")
        
        # BOTÃO FINALIZAR PEDIDO
        st.markdown("---")
        col_confirm, col_clear = st.columns(2)
        
        with col_confirm:
            if st.button("✅ **Finalizar Pedido**", type="primary", use_container_width=True):
                # Validar dados obrigatórios
                if (st.session_state.checkout_data["forma_entrega"] == "delivery" and 
                    not st.session_state.checkout_data["endereco"].strip()):
                    st.error("❌ Por favor, informe o endereço de entrega")
                else:
                    # Salvar pedido com todas as informações
                    pedido_completo = {
                        "itens": st.session_state.carrinho.copy(),
                        "subtotal": subtotal,
                        "taxa_entrega": taxa_entrega,
                        "desconto": desconto,
                        "total": total_final,
                        "forma_entrega": st.session_state.checkout_data["forma_entrega"],
                        "forma_pagamento": st.session_state.checkout_data["forma_pagamento"],
                        "cupom": st.session_state.checkout_data["cupom"],
                        "endereco": st.session_state.checkout_data["endereco"],
                        "troco_para": st.session_state.checkout_data["troco_para"]
                    }
                    
                    # Salvar pedido
                    pedido_salvo = salvar_pedido_completo(pedido_completo)
                    
                    # Feedback visual
                    st.balloons()
                    st.success(f"""
                    🎉 **Pedido #{pedido_salvo['id']} Confirmado!**
                    
                    **Tempo estimado:** {'30-40 minutos' if forma_entrega == 'delivery' else '15-20 minutos'}
                    **Forma de pagamento:** {forma_pagamento.upper()}
                    **Total:** R$ {total_final:.2f}
                    """)
                    
                    # Limpar carrinho e dados do checkout
                    limpar_carrinho()
                    st.rerun()
        
        with col_clear:
            if st.button("🗑️ **Limpar Tudo**", use_container_width=True):
                limpar_carrinho()
                st.rerun()

# =============== SOBRE NÓS ===============
st.markdown("""
<section id="sobre" class="about full-width-section">
    <div style="max-width:1400px;margin:0 auto;padding:100px 40px;">
        <h2 class="section-title">Sobre Nós</h2>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start;margin-bottom:100px;">
            <div style="font-size:1.2rem;line-height:1.8;color:#333;">
                <p style="margin-bottom:25px;">Há mais de 10 anos servindo os melhores hambúrgueres da região, o <strong style="color:#EA1D2C;">Burger Express</strong> se consolidou como referência em qualidade e sabor.</p>
                <p style="margin-bottom:25px;">Utilizamos apenas carne 100% bovina, pães artesanais frescos diariamente e ingredientes selecionados para garantir a melhor experiência gastronômica.</p>
                <p style="margin-bottom:25px;">Nossa missão é proporcionar momentos especiais através de hambúrgueres excepcionais, com atendimento diferenciado e ambiente acolhedor.</p>
            </div>
            <div style="border-radius:20px;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,0.15);">
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3838.683491753089!2d-48.07228772408775!3d-15.820634523603314!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x935a3391b366fc47%3A0x88c16b784a3ad98f!2sSenai%20Taguatinga!5e0!3m2!1spt-BR!2sbr" width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:60px;">
            <div style="background:white;padding:50px 40px;border-radius:24px;box-shadow:0 10px 35px rgba(0,0,0,0.1);text-align:center;">
                <h3 style="color:#EA1D2C;font-size:1.8rem;margin-bottom:30px;">🕒 Horário de Funcionamento</h3>
                <p style="font-size:1.2rem;margin:20px 0;padding:10px 0;border-bottom:1px solid #f0f0f0;"><strong>Segunda a Sábado:</strong><br>11h às 23h</p>
                <p style="font-size:1.2rem;margin:20px 0;padding:10px 0;"><strong>Domingo:</strong><br>12h às 22h</p>
            </div>
            <div style="background:white;padding:50px 40px;border-radius:24px;box-shadow:0 10px 35px rgba(0,0,0,0.1);text-align:center;">
                <h3 style="color:#EA1D2C;font-size:1.8rem;margin-bottom:30px;">🚚 Delivery</h3>
                <p style="font-size:1.2rem;margin:20px 0;padding:10px 0;border-bottom:1px solid #f0f0f0;">Entregamos em toda a região</p>
                <p style="font-size:1.2rem;margin:20px 0;padding:10px 0;border-bottom:1px solid #f0f0f0;"><strong>Taxa:</strong> R$ 5,00</p>
                <p style="font-size:1.2rem;margin:20px 0;padding:10px 0;"><strong>Telefone:</strong><br>(61) 9999-9999</p>
            </div>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# =============== SEÇÃO DESENVOLVEDORES ===============
st.markdown("""
<style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .dev-title {
        text-align: center;
        margin-bottom: 50px;
    }
    
    .dev-emoji {
        display: inline-block;
        animation: pulse 2s infinite ease-in-out;
        font-size: 2.5rem;
    }
    
    .dev-card-animated {
        background: white;
        border-radius: 16px;
        padding: 40px 30px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
        transition: all 0.3s ease;
        animation: float 4s infinite ease-in-out;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .dev-card-animated:hover {
        animation-play-state: paused;
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(234, 29, 44, 0.2);
    }
    
    .dev-card-animated::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #EA1D2C, #ff6b81, #EA1D2C);
        background-size: 200% 200%;
        animation: gradient 3s infinite linear;
    }
    
    .dev-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: 0 auto 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 3px solid white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .dev-card-animated:hover .dev-avatar {
        transform: scale(1.1);
        box-shadow: 0 8px 25px rgba(234, 29, 44, 0.3);
    }
    
    .github-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(90deg, #2e2e2e, #4a4a4a);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .github-btn:hover {
        background: linear-gradient(90deg, #EA1D2C, #c91a26);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(234, 29, 44, 0.4);
    }
    
    .github-btn::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .github-btn:hover::after {
        left: 100%;
    }
    
    .role-badge {
        background: linear-gradient(90deg, #EA1D2C, #ff6b81);
        color: white;
        padding: 6px 20px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 15px;
        font-size: 0.9rem;
        font-weight: 600;
        animation: pulse 3s infinite ease-in-out;
        animation-delay: 1s;
    }
    
    .delay-1 {
        animation-delay: 0.3s;
    }
    
    .delay-2 {
        animation-delay: 0.6s;
    }
    
    .delay-3 {
        animation-delay: 0.9s;
    }
</style>

<section id="desenvolvedores" class="full-width-section" style="padding:80px 0;background:#fff;">
    <div style="max-width:1200px;margin:0 auto;padding:0 20px;">
        <div class="dev-title">
            <span class="dev-emoji">👨‍💻</span>
            <h2 style="
                font-size: 2.5rem; 
                color: #2e2e2e; 
                margin: 15px 0; 
                font-weight: 700;
                background: linear-gradient(90deg, #EA1D2C, #2e2e2e);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">
                Desenvolvedores
            </h2>
            <p style="color:#666;font-size:1.2rem;max-width:600px;margin:0 auto;">
                Conheça a equipe que trouxe o Burger Express à vida!
            </p>
        </div>
""", unsafe_allow_html=True)

# Container dos cards de desenvolvedores
st.markdown("""
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:40px;margin-top:50px;">
""", unsafe_allow_html=True)

# Desenvolvedor 1 - Fabiane Sarres
st.markdown("""
<div class="dev-card-animated delay-1">
    <div class="dev-avatar" style="background:linear-gradient(135deg,#EA1D2C,#ff6b81);">
        <i class="fas fa-laptop-code" style="font-size:50px;color:white;"></i>
    </div>
    <h3 style="color:#2e2e2e;font-size:1.5rem;margin-bottom:10px;font-weight:700;">Fabiane Sarres</h3>
    <div class="role-badge">Desenvolvedora Frontend</div>
    <p style="color:#555;margin-bottom:25px;line-height:1.6;font-size:0.95rem;">
        Especialista em UI/UX, criou a interface responsiva e experiência do usuário da aplicação.
    </p>
    <a href="https://github.com/fabianesarres" target="_blank" class="github-btn">
        <i class="fab fa-github"></i> Ver GitHub
    </a>
</div>
""", unsafe_allow_html=True)

# Desenvolvedor 2 - Gabriel Duarte
st.markdown("""
<div class="dev-card-animated delay-2">
    <div class="dev-avatar" style="background:linear-gradient(135deg,#2e2e2e,#4a4a4a);">
        <i class="fas fa-server" style="font-size:50px;color:white;"></i>
    </div>
    <h3 style="color:#2e2e2e;font-size:1.5rem;margin-bottom:10px;font-weight:700;">Gabriel Duarte</h3>
    <div class="role-badge">Desenvolvedor Full Stack</div>
    <p style="color:#555;margin-bottom:25px;line-height:1.6;font-size:0.95rem;">
        Responsável pelo backend, integração de APIs e lógica de negócios do Burger Express.
    </p>
    <a href="https://github.com/Gabrobot5" target="_blank" class="github-btn">
        <i class="fab fa-github"></i> Ver GitHub
    </a>
</div>
""", unsafe_allow_html=True)

# Desenvolvedor 3 - Patrícia Rodrigues
st.markdown("""
<div class="dev-card-animated delay-3">
    <div class="dev-avatar" style="background:linear-gradient(135deg,#EA1D2C,#2e2e2e);">
        <i class="fas fa-mobile-alt" style="font-size:50px;color:white;"></i>
    </div>
    <h3 style="color:#2e2e2e;font-size:1.5rem;margin-bottom:10px;font-weight:700;">Patrícia Campos</h3>
    <div class="role-badge">Desenvolvedora Mobile</div>
    <p style="color:#555;margin-bottom:25px;line-height:1.6;font-size:0.95rem;">
        Focada na otimização mobile e integração com sistemas de pagamento e delivery.
    </p>
    <a href="https://github.com/Patricia470" target="_blank" class="github-btn">
        <i class="fab fa-github"></i> Ver GitHub
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Tecnologias utilizadas (opcional - com animação também)
st.markdown("""
<div style="text-align:center;margin-top:60px;padding:40px;background:linear-gradient(135deg,#f8f8f8,#fff);border-radius:16px;box-shadow:0 8px 25px rgba(0,0,0,0.05);border:1px solid #f0f0f0;">
    <h3 style="color:#EA1D2C;font-size:1.8rem;margin-bottom:30px;font-weight:700;">
        <i class="fas fa-cogs" style="margin-right:10px;"></i>
        Tecnologias Utilizadas
    </h3>
    <div style="display:flex;justify-content:center;flex-wrap:wrap;gap:15px;">
        <span style="background:#EA1D2C;color:white;padding:10px 20px;border-radius:8px;font-weight:600;transition:all 0.3s;cursor:default;" 
              onmouseover="this.style.transform='scale(1.1)';this.style.boxShadow='0 5px 15px rgba(234,29,44,0.3)';" 
              onmouseout="this.style.transform='scale(1)';this.style.boxShadow='none';">Python</span>
        <span style="background:#EA1D2C;color:white;padding:10px 20px;border-radius:8px;font-weight:600;transition:all 0.3s;cursor:default;"
              onmouseover="this.style.transform='scale(1.1)';this.style.boxShadow='0 5px 15px rgba(234,29,44,0.3)';" 
              onmouseout="this.style.transform='scale(1)';this.style.boxShadow='none';">Streamlit</span>
        <span style="background:#2e2e2e;color:white;padding:10px 20px;border-radius:8px;font-weight:600;transition:all 0.3s;cursor:default;"
              onmouseover="this.style.transform='scale(1.1)';this.style.boxShadow='0 5px 15px rgba(0,0,0,0.3)';" 
              onmouseout="this.style.transform='scale(1)';this.style.boxShadow='none';">HTML/CSS</span>
        <span style="background:#2e2e2e;color:white;padding:10px 20px;border-radius:8px;font-weight:600;transition:all 0.3s;cursor:default;"
              onmouseover="this.style.transform='scale(1.1)';this.style.boxShadow='0 5px 15px rgba(0,0,0,0.3)';" 
              onmouseout="this.style.transform='scale(1)';this.style.boxShadow='none';">JavaScript</span>
        <span style="background:#EA1D2C;color:white;padding:10px 20px;border-radius:8px;font-weight:600;transition:all 0.3s;cursor:default;"
              onmouseover="this.style.transform='scale(1.1)';this.style.boxShadow='0 5px 15px rgba(234,29,44,0.3)';" 
              onmouseout="this.style.transform='scale(1)';this.style.boxShadow='none';">JSON</span>
        <span style="background:#2e2e2e;color:white;padding:10px 20px;border-radius:8px;font-weight:600;transition:all 0.3s;cursor:default;"
              onmouseover="this.style.transform='scale(1.1)';this.style.boxShadow='0 5px 15px rgba(0,0,0,0.3)';" 
              onmouseout="this.style.transform='scale(1)';this.style.boxShadow='none';">Git/GitHub</span>
    </div>
</div>
</div>
</section>
""", unsafe_allow_html=True)

# Adicionar antes do footer
st.markdown("""
<a href="#inicio" style="
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: #EA1D2C;
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    text-decoration: none;
    box-shadow: 0 4px 12px rgba(234, 29, 44, 0.3);
    z-index: 1000;
    transition: all 0.3s;
">
    ↑
</a>
""", unsafe_allow_html=True)

# =============== FOOTER ===============
st.markdown("""
<style>
    .footer::before {content:'';position:absolute;top:0;left:0;right:0;height:5px;background:linear-gradient(90deg,#EA1D2C,#ff4757);}
    .footer-content {display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:50px;max-width:1200px;margin:0 auto;padding:0 20px;position:relative;}
    .footer-section h3 {color:#EA1D2C;margin-bottom:24px;position:relative;padding-bottom:12px;font-size:1.4rem;}
    .footer-section h3::after {content:'';position:absolute;bottom:0;left:0;width:40px;height:3px;background:#EA1D2C;border-radius:2px;}
    .social-links a {color:#fff;background:rgba(255,255,255,0.1);padding:12px 20px;border-radius:8px;text-decoration:none;display:inline-flex;align-items:center;gap:10px;transition:all 0.3s;margin:5px;}
    .social-links a:hover {background:#EA1D2C;transform:translateY(-3px);}
</style>

<footer class="footer full-width-section" id="contato" style="position:relative;">
    <div class="footer-content">
        <div class="footer-section">
            <h3>Burger Express</h3>
            <p>O melhor fast food da cidade! Há mais de 10 anos servindo qualidade e sabor incomparáveis.</p>
        </div>
        <div class="footer-section">
            <h3>Contato</h3>
            <p><i class="fas fa-phone"></i> (61) 9999-9999</p>
            <p><i class="fas fa-envelope"></i> contato@burgerexpress.com</p>
            <p><i class="fas fa-map-marker-alt"></i> QNA 45 - Taguatinga Norte, Brasília-DF</p>
        </div>
        <div class="footer-section">
            <h3>Redes Sociais</h3>
            <div class="social-links">
                <a href="#"><i class="fab fa-instagram"></i> Instagram</a>
                <a href="#"><i class="fab fa-facebook"></i> Facebook</a>
                <a href="#"><i class="fab fa-whatsapp"></i> WhatsApp</a>
            </div>
        </div>
    </div>
</footer>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    width:100%;
    box-sizing:border-box;
    padding:40px 20px 20px 20px;
    text-align:center;
    border-top:1px solid rgba(255,255,255,0.1);
    margin-top:40px;
">
    <p style="color:#aaa;font-size:0.9rem;">
        © 2025 Burger Express. Todos os direitos reservados.
    </p>
</div>
""", unsafe_allow_html=True)