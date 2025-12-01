# app.py - VERSÃO COMPLETA COM CHECKOUT COMPLETO
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

# =============== CSS ORIGINAL ===============
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
    .product-card {background:white;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);transition:.3s;border:1px solid #f0f0f0;}
    .product-card:hover {transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,0,0,0.12);}
    .product-info {padding:16px;text-align:left;}
    .product-info h3 {margin:0 0 8px;font-size:1.1rem;color:#2e2e2e;font-weight:600;}
    .price {font-size:1.3rem;font-weight:700;color:#2e2e2e;}
    .about {padding:80px 0;background:#f8f8f8;}
    .footer {background:linear-gradient(135deg,#2e2e2e,#1a1a1a);color:#fff;padding:60px 0 30px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">', unsafe_allow_html=True)

# =============== GESTÃO DE ESTADO SIMPLIFICADA ===============
if "carrinho" not in st.session_state: 
    st.session_state.carrinho = {}
if "categoria_atual" not in st.session_state: 
    st.session_state.categoria_atual = "hamburgers"

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

# =============== HEADER COM CARRINHO CLICÁVEL ===============
st.markdown(f"""
<header class="header">
    <div style="max-width:1200px;margin:0 auto;padding:0 20px;display:flex;justify-content:space-between;align-items:center;height:100%;">
        <div style="color:#2e2e2e;font-size:1.9rem;font-weight:700;">Burger Express</div>
        <nav>
            <a href="#inicio" style="color:#2e2e2e;text-decoration:none;margin:0 20px;font-weight:600;">Início</a>
            <a href="#menu" style="color:#2e2e2e;text-decoration:none;margin:0 20px;font-weight:600;">Menu</a>
            <a href="#sobre" style="color:#2e2e2e;text-decoration:none;margin:0 20px;font-weight:600;">Sobre</a>
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

# Botões de categoria
cols = st.columns(4)
categorias = [
    ("hamburgers", "🍔 Hambúrgueres"), 
    ("bebidas", "🥤 Bebidas"), 
    ("acompanhamentos", "🍟 Acomp."), 
    ("sobremesas", "🍰 Sobremesas")
]

for i, (key, nome) in enumerate(categorias):
    with cols[i]:
        if st.button(nome, use_container_width=True, 
                     type="primary" if st.session_state.categoria_atual == key else "secondary",
                     key=f"cat_{key}"):
            st.session_state.categoria_atual = key
            st.rerun()

st.markdown('<div class="products-grid">', unsafe_allow_html=True)

# Loop que mostra os produtos
for prato in [p for p in pratos if p["cat"] == st.session_state.categoria_atual]:
    disponivel, ingrediente_faltante = verificar_disponibilidade_prato(prato)
    
    with st.container():
        # Card do produto
        if not disponivel:
            st.markdown('<div class="product-card" style="opacity:0.6;position:relative;">', unsafe_allow_html=True)
            st.markdown(f'<div style="position:absolute;top:10px;right:10px;background:#EA1D2C;color:white;padding:4px 8px;border-radius:4px;font-size:0.8rem;z-index:10;">SEM {ingrediente_faltante.upper()}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
        
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
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3838.683491753089!2d-48.07228762408775!3d-15.820634523603314!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x935a3391b366fc47%3A0x88c16b784a3ad98f!2sSenai%20Taguatinga!5e0!3m2!1spt-BR!2sbr!4v1762945909470!5m2!1spt-BR!2sbr" width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
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

# =============== FOOTER ORIGINAL ===============
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