# app.py - VERSÃO FINAL 100% FUNCIONAL
import streamlit as st
import os
import json
import streamlit.components.v1 as components

# =============== CARREGA PRATOS SEM CACHE (ATUALIZA NA HORA) ===============
def carregar_pratos():
    """Carrega pratos do JSON - sempre atualizado"""
    if os.path.exists("pratos.json"):
        try:
            with open("pratos.json", "r", encoding="utf-8") as f:
                pratos = json.load(f)
                return pratos
        except Exception as e:
            st.error(f"Erro ao carregar pratos: {e}")
            return []
    else:
        # Se não existe, cria com pratos padrão
        pratos_padrao = [
            {"nome": "Burger Classic", "preco": 18.90, "cat": "hamburgers", "img": "burger-classic.jpg"},
            {"nome": "Burger Bacon", "preco": 22.90, "cat": "hamburgers", "img": "burger-bacon.jpg"},
            {"nome": "Double Cheese", "preco": 26.90, "cat": "hamburgers", "img": "cheese-duplo.jpg"},
            {"nome": "Refrigerante", "preco": 8.90, "cat": "bebidas", "img": "refri.jpg"},
            {"nome": "Suco Natural", "preco": 12.90, "cat": "bebidas", "img": "suco.jpg"},
            {"nome": "Batata Frita", "preco": 12.90, "cat": "acompanhamentos", "img": "batata-frita.jpg"},
            {"nome": "Onion Rings", "preco": 15.90, "cat": "acompanhamentos", "img": "onion-rings.jpg"},
            {"nome": "Milk Shake", "preco": 16.90, "cat": "sobremesas", "img": "milkshake.jpg"},
            {"nome": "Brownie", "preco": 14.90, "cat": "sobremesas", "img": "brownie.jpg"},
        ]
        with open("pratos.json", "w", encoding="utf-8") as f:
            json.dump(pratos_padrao, f, ensure_ascii=False, indent=2)
        return pratos_padrao

pratos = carregar_pratos()

st.set_page_config(page_title="Burger Express", layout="centered")

# =============== CSS ORIGINAL LINDO ===============
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .header {position: fixed;top:0;left:0;width:100%;z-index:999999;background:#fff;height:72px;box-shadow:0 2px 8px rgba(0,0,0,0.08);}
    .block-container {padding-top: 100px !important;}
    .full-width-section {width:100vw;position:relative;left:50%;right:50%;margin-left:-50vw;margin-right:-50vw;}
    .stButton > button[kind="primary"] {background:#EA1D2C !important;color:white !important;border:none !important;border-radius:8px !important;font-weight:600 !important;}
    .stButton > button:hover {background:#c91a26 !important;}
    div[data-testid="stImage"] > img {height:180px !important;object-fit:cover !important;border-radius:8px 8px 0 0 !important;width:100% !important;}
    .admin-btn {background:#EA1D2C;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:600;display:inline-flex;align-items:center;gap:8px;transition:all 0.3s;}
    .admin-btn:hover {background:#c91a26;transform:translateY(-2px);box-shadow:0 4px 12px rgba(234,29,44,0.4);}
    .hero {background:linear-gradient(rgba(0,0,0,0.5),rgba(0,0,0,0.5)),url('https://images.unsplash.com/photo-1553979459-d2229ba7433b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80') center/cover;min-height:calc(100vh - 72px);display:flex;align-items:center;text-align:center;color:white;}
    .hero h2 {font-size:3.8rem;font-weight:700;}
    .hero p {font-size:1.5rem;max-width:700px;margin:20px auto;}
    .btn {background:#EA1D2C;color:white;padding:16px 45px;border-radius:8px;font-weight:700;text-decoration:none;font-size:1.3rem;transition:all 0.3s;}
    .btn:hover {background:#c91a26;transform:scale(1.05);}
    .menu {padding:40px 0 80px;background:#fff;}
    .section-title {text-align:center;font-size:2rem;color:#2e2e2e;margin-bottom:30px;font-weight:700;}
    .products-grid {display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;max-width:1200px;margin:0 auto;padding:0 20px;}
    .product-card {background:white;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);transition:.3s;border:1px solid #f0f0f0;}
    .product-card:hover {transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,0,0,0.12);}
    .product-info {padding:16px;text-align:left;}
    .product-info h3 {margin:0 0 8px;font-size:1.1rem;color:#2e2e2e;font-weight:600;}
    .price {font-size:1.3rem;font-weight:700;color:#2e2e2e;}
    .about {padding:80px 0;background:#f8f8f8;}
    .about-content {display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start;max-width:1200px;margin:0 auto;padding:0 20px;}
    .about-text {font-size:1.1rem;line-height:1.6;color:#2e2e2e;}
    .map {border-radius:8px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.1);}
    .info-item {background:white;padding:25px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.08);border:1px solid #f0f0f0;}
    .info-item h3 {color:#EA1D2C;margin-bottom:10px;}
    .footer {background:linear-gradient(135deg,#2e2e2e,#1a1a1a);color:#fff;padding:60px 0 30px;position:relative;overflow:hidden;}
    .footer::before {content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#EA1D2C,#ff4757);}
    .footer-content {display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:50px;max-width:1200px;margin:0 auto;padding:0 20px;}
    .footer-section h3 {color:#EA1D2C;margin-bottom:24px;position:relative;padding-bottom:12px;}
    .footer-section h3::after {content:'';position:absolute;bottom:0;left:0;width:40px;height:3px;background:#EA1D2C;border-radius:2px;}
    .social-links a {color:#fff;background:rgba(255,255,255,0.1);padding:10px 16px;border-radius:8px;transition:all 0.3s;}
    .social-links a:hover {background:#EA1D2C;transform:translateY(-3px);}
</style>
""", unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">', unsafe_allow_html=True)

# =============== ESTADO DA SESSÃO ===============
if "carrinho" not in st.session_state: 
    st.session_state.carrinho = {}
if "categoria_atual" not in st.session_state: 
    st.session_state.categoria_atual = "hamburgers"
if "to_reset" not in st.session_state: 
    st.session_state.to_reset = False

if st.session_state.to_reset:
    for p in pratos:
        st.session_state[f"qtd_{p['nome']}"] = 0
    st.session_state.to_reset = False

def atualizar_carrinho():
    """Atualiza carrinho baseado nos number_inputs"""
    novo_carrinho = {}
    for p in pratos:
        key = f"qtd_{p['nome']}"
        if key in st.session_state and st.session_state[key] > 0:
            novo_carrinho[p["nome"]] = int(st.session_state[key])
    st.session_state.carrinho = novo_carrinho

# =============== HEADER ===============
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
            <div style="position:relative;">
                <i class="fas fa-shopping-cart" style="font-size:1.8rem;color:#2e2e2e;"></i>
                <span style="position:absolute;top:-10px;right:-10px;background:#EA1D2C;color:white;width:24px;height:24px;border-radius:50%;font-size:0.8rem;display:flex;align-items:center;justify-content:center;">
                    {sum(st.session_state.carrinho.values())}
                </span>
            </div>
        </div>
    </div>
</header>
""", unsafe_allow_html=True)

# =============== HERO SECTION ===============
st.markdown("""
<section id="inicio" class="hero full-width-section">
    <div style="max-width:800px;margin:0 auto;">
        <h2>Os Melhores Hambúrgueres da Cidade!</h2>
        <p>Experimente nosso menu exclusivo com ingredientes frescos e sabor inigualável</p>
        <a href="#menu" class="btn">Ver Menu</a>
    </div>
</section>
""", unsafe_allow_html=True)

# =============== MENU SECTION ===============
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
                     key=key):
            st.session_state.categoria_atual = key
            st.rerun()

st.markdown('<div class="products-grid">', unsafe_allow_html=True)

for prato in [p for p in pratos if p["cat"] == st.session_state.categoria_atual]:
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    
    # Imagem do produto
    caminho_imagem = os.path.join("images", prato["img"])
    try:
        if os.path.exists(caminho_imagem):
            st.image(caminho_imagem, use_container_width=True)
        else:
            st.image("https://via.placeholder.com/400x240/EA1D2C/white?text=Imagem+Indisponível", 
                    use_container_width=True)
    except:
        st.image("https://via.placeholder.com/400x240/EA1D2C/white?text=Erro+Imagem", 
                use_container_width=True)
    
    # Informações do produto
    st.markdown(f"""
    <div class="product-info">
        <h3>{prato['nome']}</h3>
        <span class="price">R$ {prato['preco']:.2f}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Controle de quantidade
    qtd_key = f"qtd_{prato['nome']}"
    st.number_input("Quantidade", min_value=0, max_value=20, 
                   value=st.session_state.get(qtd_key, 0),
                   key=qtd_key, label_visibility="collapsed", 
                   on_change=atualizar_carrinho)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div></section>', unsafe_allow_html=True)

# =============== CARRINHO ===============
if st.session_state.carrinho:
    total = 0
    itens_html = ""
    
    for nome, qtd in st.session_state.carrinho.items():
        preco = next((p["preco"] for p in pratos if p["nome"] == nome), 0)
        subtotal = qtd * preco
        total += subtotal
        itens_html += f"""
        <div style='display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid #eee;'>
            <span>{qtd} × {nome}</span>
            <span>R$ {subtotal:.2f}</span>
        </div>
        """
    
    components.html(f"""
    <div style="background:white;padding:50px;margin:60px 0;border-radius:16px;box-shadow:0 8px 30px rgba(0,0,0,0.1);text-align:center;">
        <h2 style="color:#EA1D2C;font-size:2.8rem;margin-bottom:30px;">📦 Seu Pedido</h2>
        <div style="background:#f9f9f9;padding:30px;border-radius:12px;margin:30px auto;max-width:600px;">
            {itens_html}
        </div>
        <h2 style="color:#EA1D2C;font-size:3rem;margin-top:20px;">TOTAL: R$ {total:.2f}</h2>
    </div>
    """, height=400 + len(st.session_state.carrinho) * 60)

    # Botões de ação do carrinho
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_confirm, col_clear = st.columns(2)
        with col_confirm:
            if st.button("✅ Finalizar Pedido", type="primary", use_container_width=True):
                st.balloons()
                st.success("🎉 Pedido enviado com sucesso! Em até 40 minutos na sua casa!")
                st.session_state.carrinho.clear()
                st.session_state.to_reset = True
                st.rerun()
        with col_clear:
            if st.button("🗑️ Limpar Carrinho", use_container_width=True):
                st.session_state.carrinho.clear()
                st.session_state.to_reset = True
                st.rerun()

# =============== SOBRE NÓS ===============
st.markdown("""
<section id="sobre" class="about full-width-section">
    <div style="max-width:1200px;margin:0 auto;padding:60px 20px;">
        <h2 class="section-title">Sobre Nós</h2>
        <div class="about-content">
            <div class="about-text">
                <p>Há mais de 10 anos servindo os melhores hambúrgueres da região, o Burger Express se consolidou como referência em qualidade e sabor.</p>
                <p>Utilizamos apenas carne 100% bovina, pães artesanais frescos diariamente e ingredientes selecionados para garantir a melhor experiência gastronômica.</p>
                <p>Nossa missão é proporcionar momentos especiais através de hambúrgueres excepcionais, com atendimento diferenciado e ambiente acolhedor.</p>
            </div>
            <div class="map">
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3838.683491753089!2d-48.07228762408775!3d-15.820634523603314!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x935a3391b366fc47%3A0x88c16b784a3ad98f!2sSenai%20Taguatinga!5e0!3m2!1spt-BR!2sbr!4v1762945909470!5m2!1spt-BR!2sbr"
                    width="100%" height="400" style="border:0;border-radius:8px;" allowfullscreen="" loading="lazy"></iframe>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin-top:40px;">
            <div class="info-item">
                <h3>🕒 Horário de Funcionamento</h3>
                <p>Segunda a Sábado: 11h às 23h</p>
                <p>Domingo: 12h às 22h</p>
            </div>
            <div class="info-item">
                <h3>🚚 Delivery</h3>
                <p>Entregamos em toda a região</p>
                <p>Taxa: R$ 5,00</p>
                <p>📞 Telefone: (61) 9999-9999</p>
            </div>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# =============== FOOTER ===============
st.markdown("""
<footer class="footer full-width-section" id="contato">
    <div style="max-width:1200px;margin:0 auto;padding:0 20px;">
        <div class="footer-content">
            <div class="footer-section">
                <h3>Burger Express</h3>
                <p>O melhor fast food da cidade! Há mais de 10 anos servindo qualidade e sabor incomparáveis.</p>
            </div>
            <div class="footer-section">
                <h3>📞 Contato</h3>
                <p><i class="fas fa-phone"></i> (61) 9999-9999</p>
                <p><i class="fas fa-envelope"></i> contato@burgerexpress.com</p>
                <p><i class="fas fa-map-marker-alt"></i> QNA 45 - Taguatinga Norte, Brasília-DF</p>
            </div>
            <div class="footer-section">
                <h3>🌐 Redes Sociais</h3>
<div class="social-links" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
    <a href="#"><i class="fab fa-instagram"></i> Instagram</a>
    <a href="#"><i class="fab fa-facebook"></i> Facebook</a>
    <a href="#"><i class="fab fa-whatsapp"></i> WhatsApp</a>
</div>
            </div>
        </div>
        <div style="text-align:center;padding-top:40px;border-top:1px solid rgba(255,255,255,0.1);margin-top:40px;">
            <p>© 2025 Burger Express. Todos os direitos reservados.</p>
        </div>
    </div>
</footer>
""", unsafe_allow_html=True)