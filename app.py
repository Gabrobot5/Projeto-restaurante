import streamlit as st
import os
import streamlit.components.v1 as components

# =============== CONFIGURAÇÃO ===============
st.set_page_config(page_title="Burger Express", layout="centered")

# =============== CSS GERAL ===============
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .header {position: fixed;top:0;left:0;width:100%;z-index:999999;background:#1A2522;height:72px;box-shadow:0 4px 15px rgba(0,0,0,0.3);}
    .block-container {padding-top: 100px !important;}
    .full-width-section {width:100vw;position:relative;left:50%;right:50%;margin-left:-50vw;margin-right:-50vw;}
    
    /* Botões dourados */
    .stButton > button[kind="primary"] {background:#BFA307 !important;color:#1A2522 !important;font-weight:bold !important;}
    .stButton > button {border:2px solid #BFA307 !important;color:#BFA307 !important;background:transparent !important;}
    .stButton > button:hover {background:#BFA307 !important;color:#1A2522 !important;}
    
    /* MATA O QUADRADO BRANCO DAS IMAGENS */
    div[data-testid="stImage"] {margin:0 !important; padding:0 !important;}
    div[data-testid="stImage"] > img {margin-top:0 !important;}
</style>
""", unsafe_allow_html=True)

# Font Awesome
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">', unsafe_allow_html=True)

# =============== CSS ORIGINAL ===============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    * {font-family:'Montserrat',sans-serif; margin:0; padding:0; box-sizing:border-box;}
    :root {--bg:#F8F1E9;--dark:#1A2522;--accent:#BFA307;--light:#F5E8C7;}
    
    .header .container {max-width:1200px;margin:0 auto;padding:0 20px;display:flex;justify-content:space-between;align-items:center;height:100%;}
    .logo h1 {color:var(--light);font-size:1.9rem;font-weight:700;margin:0;}
    .nav-link {color:var(--light);text-decoration:none;font-weight:600;margin:0 25px;}
    .nav-link:hover {color:var(--accent);}
    .cart {color:var(--light);font-size:1.8rem;position:relative;}
    .cart-count {position:absolute;top:-10px;right:-10px;background:var(--accent);color:var(--dark);font-weight:bold;width:24px;height:24px;border-radius:50%;font-size:0.8rem;display:flex;align-items:center;justify-content:center;border:3px solid var(--light);}
    
    .hero {background:linear-gradient(rgba(0,0,0,0.6),rgba(0,0,0,0.6)),url('https://images.unsplash.com/photo-1553979459-d2229ba7433b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80') center/cover;min-height:calc(100vh - 72px);display:flex;align-items:center;text-align:center;color:white;}
    .hero h2 {font-size:3.8rem;font-weight:700;}
    .hero p {font-size:1.5rem;max-width:700px;margin:20px auto;}
    .btn {background:var(--accent);color:var(--dark);padding:16px 45px;border-radius:50px;font-weight:700;text-decoration:none;font-size:1.3rem;}
    .btn:hover {background:var(--light);transform:scale(1.05);}
    
    .menu {padding:80px 0;background:var(--bg);}
    .section-title {text-align:center;font-size:2.5rem;color:var(--dark);margin-bottom:40px;font-weight:700;}
    .products-grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:25px;max-width:1200px;margin:0 auto;padding:0 20px;}
    .product-card {background:white;border-radius:15px;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,0.1);transition:.3s;display:flex;flex-direction:column;}
    .product-card:hover {transform:translateY(-8px);box-shadow:0 12px 30px rgba(0,0,0,0.15);}
    .product-info {padding:20px;text-align:center;flex-grow:1;display:flex;flex-direction:column;justify-content:space-between;}
    .product-info h3 {margin:0 0 12px;font-size:1.2rem;color:var(--dark);font-weight:600;}
    .price {font-size:1.5rem;font-weight:700;color:var(--accent);margin-bottom:15px;display:block;}
    
    .about {padding:80px 0;background:var(--light);}
    .about .container {max-width:1200px;margin:0 auto;padding:0 20px;}
    .about-content {display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start;}
    .about-text {font-size:1.1rem;line-height:1.6;color:var(--dark);}
    .about-text p {margin-bottom:20px;}
    .map {border-radius:15px;overflow:hidden;box-shadow:0 8px 25px rgba(0,0,0,0.1);}
    .about-info {display:grid;gap:20px;}
    .info-item {background:white;padding:25px;border-radius:10px;box-shadow:0 4px 15px rgba(0,0,0,0.1);}
    .info-item h3 {color:var(--accent);margin-bottom:10px;font-size:1.3rem;}
    .info-item p {margin:5px 0;color:var(--dark);}
    
    .footer {background:var(--dark);color:var(--light);padding:50px 0 20px;}
    .footer .container {max-width:1200px;margin:0 auto;padding:0 20px;}
    .footer-content {display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:40px;}
    .footer-section h3 {color:var(--accent);margin-bottom:20px;font-size:1.4rem;}
    .footer-section p {margin:8px 0;opacity:0.9;}
    .social-links {display:flex;gap:15px;flex-wrap:wrap;}
    .social-links a {color:var(--light);text-decoration:none;transition:color 0.3s;display:flex;align-items:center;gap:5px;}
    .social-links a:hover {color:var(--accent);}
    .footer-bottom {margin:40px auto 0;padding:20px 0;border-top:1px solid rgba(255,255,255,0.1);text-align:center;opacity:0.7;}
</style>
""", unsafe_allow_html=True)

# =============== DADOS INICIAIS ===============
if "carrinho" not in st.session_state:
    st.session_state.carrinho = {}
if "categoria_atual" not in st.session_state:
    st.session_state.categoria_atual = "hamburgers"
# flag para reset seguro de inputs (usada para setar valores ANTES dos widgets serem criados)
if "to_reset" not in st.session_state:
    st.session_state.to_reset = False

pratos = [
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

# Se um reset foi solicitado na execução anterior, zere os number_input antes de criar widgets
if st.session_state.to_reset:
    for p in pratos:
        q_key = f"qtd_{p['nome']}"
        # só seta se não existir ainda (ou seta de qualquer forma: estamos antes da criação dos widgets)
        st.session_state[q_key] = 0
    st.session_state.to_reset = False  # limpa a flag

# =============== Função para atualizar o carrinho (usada por on_change) ===============
def atualizar_carrinho():
    """
    Lê todos os number_input (qtd_*) do session_state e reconstrói st.session_state.carrinho.
    Chamado via on_change nos number_input para manter tudo sincronizado.
    """
    novo = {}
    for p in pratos:
        key = f"qtd_{p['nome']}"
        if key in st.session_state:
            value = st.session_state.get(key, 0)
            if isinstance(value, (int, float)) and value > 0:
                novo[p["nome"]] = int(value)
    st.session_state.carrinho = novo

# =============== HEADER + HERO ===============
st.markdown(f"""
<header class="header">
    <div class="container">
        <div class="logo"><h1>Burger Express</h1></div>
        <nav>
            <a href="#inicio" class="nav-link">Início</a>
            <a href="#menu" class="nav-link">Menu</a>
            <a href="#sobre" class="nav-link">Sobre</a>
            <a href="#contato" class="nav-link">Contato</a>
        </nav>
        <div class="cart">
            <i class="fas fa-shopping-cart"></i>
            <span class="cart-count">{sum(st.session_state.carrinho.values())}</span>
        </div>
    </div>
</header>

<section id="inicio" class="hero">
    <div style="max-width:800px;margin:0 auto;">
        <h2>Os Melhores Hambúrgueres da Cidade!</h2>
        <p>Experimente nosso menu exclusivo com ingredientes frescos e sabor inigualável</p>
        <a href="#menu" class="btn">Ver Menu</a>
    </div>
</section>
""", unsafe_allow_html=True)

# =============== MENU ===============
st.markdown('<section id="menu" class="menu"><div class="container">', unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>Nosso Menu</h2>", unsafe_allow_html=True)

cols = st.columns(4)
categorias = [("hamburgers","Hambúrgueres"), ("bebidas","Bebidas"), ("acompanhamentos","Acomp."), ("sobremesas","Sobremesas")]
for i, (key, nome) in enumerate(categorias):
    with cols[i]:
        if st.button(nome, use_container_width=True, 
                     type="primary" if st.session_state.categoria_atual == key else "secondary",
                     key=f"cat_{key}"):
            st.session_state.categoria_atual = key
            st.rerun()

st.markdown('<div class="products-grid">', unsafe_allow_html=True)

for prato in [p for p in pratos if p["cat"] == st.session_state.categoria_atual]:
    caminho = os.path.join("images", prato["img"])
    
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    # tenta exibir a imagem; se não existir, exibe placeholder
    try:
        st.image(caminho, use_container_width=True)
    except Exception:
        st.image("https://via.placeholder.com/400x240.png?text=Imagem", use_container_width=True)
    
    st.markdown(f"""
    <div class="product-info">
        <div>
            <h3>{prato['nome']}</h3>
            <span class="price">R$ {prato['preco']:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # number_input com on_change que atualiza o carrinho
    q_key = f"qtd_{prato['nome']}"
    # value=st.session_state.get(q_key, 0) para controlar visual; on_change atualiza st.session_state.carrinho
    st.number_input(
        "",
        min_value=0,
        max_value=20,
        value=st.session_state.get(q_key, 0),
        key=q_key,
        label_visibility="collapsed",
        on_change=atualizar_carrinho
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div></section>', unsafe_allow_html=True)

# =============== SOBRE ===============
st.markdown("""
<section id="sobre" class="about full-width-section">
    <div class="container">
        <h2 class="section-title">Sobre Nós</h2>
        <div class="about-content">
            <div class="about-text">
                <p>Há mais de 10 anos servindo os melhores hambúrgueres da região, o Burger Express se consolidou como referência em qualidade e sabor.</p>
                <p>Utilizamos apenas carne 100% bovina, pães artesanais frescos diariamente e ingredientes selecionados para garantir a melhor experiência gastronômica.</p>
                <p>Nossa missão é proporcionar momentos especiais através de hambúrgueres excepcionais, com atendimento diferenciado e ambiente acolhedor.</p>
            </div>
            <div class="map">
                <div style="position:relative;padding-bottom:75%;height:0;overflow:hidden;border-radius:15px;">
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3838.683491753089!2d-48.07228762408775!3d-15.820634523603314!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x935a3391b366fc47%3A0x88c16b784a3ad98f!2sSenai%20Taguatinga!5e0!3m2!1spt-BR!2sbr!4v1762945909470!5m2!1spt-BR!2sbr"
                        style="position:absolute;left:0;top:0;width:100%;height:100%;border:0;" 
                        allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                </div>
            </div>
            <div class="about-info">
                <div class="info-item">
                    <h3>Horário de Funcionamento</h3>
                    <p>Segunda a Sábado: 11h às 23h</p>
                    <p>Domingo: 12h às 22h</p>
                </div>
                <div class="info-item">
                    <h3>Delivery</h3>
                    <p>Entregamos em toda a região</p>
                    <p>Taxa: R$ 5,00</p>
                    <p>Telefone: (61) 9999-9999</p>
                </div>
            </div>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# =============== CARRINHO FINAL  ===============
if st.session_state.carrinho:
    # Calcula total
    total = sum(
        qtd * next(p["preco"] for p in pratos if p["nome"] == nome)
        for nome, qtd in st.session_state.carrinho.items()
    )

    # Monta itens_html
    itens_html = ""
    for nome, qtd in st.session_state.carrinho.items():
        preco = next(p["preco"] for p in pratos if p["nome"] == nome)
        itens_html += (
            f'<div style="padding:14px 0; font-size:1.3rem; border-bottom:1px solid rgba(255,255,255,0.25);">'
            f'{qtd} × {nome} → <strong>R$ {qtd * preco:.2f}</strong>'
            '</div>'
        )

    cart_html = f"""
    <div style="background: linear-gradient(135deg, #1A2522, #2A3A35);
                color: white; padding: 70px 20px; text-align: center;
                margin: 50px 0; border-radius: 25px;">

        <h2 style="color: #BFA307; font-size: 3.2rem; margin-bottom: 35px;">
            Seu Pedido
        </h2>

        <div style="background: rgba(255,255,255,0.12); max-width: 650px;
                    margin: 0 auto 45px; padding: 35px; border-radius: 20px;
                    backdrop-filter: blur(10px);">

            <h3 style="color: #BFA307; margin-bottom: 25px; font-size: 1.7rem;">
                Itens no carrinho:
            </h3>

            {itens_html}

        </div>

        <div style="font-size: 3rem; font-weight: bold; color: white;">
            TOTAL: <span style="color: #BFA307;">R$ {total:.2f}</span>
        </div>
    </div>
    """

    # ALTURA DINÂMICA 
    height = 350 + (len(st.session_state.carrinho) * 110)
    components.html(cart_html, height=height, scrolling=False)

    # BOTÕES (dentro do bloco do carrinho)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        c1, c2 = st.columns(2)

        with c1:
            if st.button("Finalizar Pedido", type="primary", use_container_width=True, key="finalizar"):
                st.balloons()
                st.success("Pedido enviado com sucesso! Entrega em 30–40 minutos.")
                # limpa carrinho e agenda reset visual dos inputs (flag)
                st.session_state.carrinho.clear()
                st.session_state.to_reset = True
                st.rerun()

        with c2:
            if st.button("Limpar Carrinho", use_container_width=True, key="limpar"):
                # limpa o dicionário do carrinho
                st.session_state.carrinho.clear()
                # marca flag para resetar os number_input ANTES da próxima criação dos widgets
                st.session_state.to_reset = True
                # atualiza a página agora
                st.rerun()

# =============== FOOTER ===============
st.markdown("""
<footer class="footer full-width-section" id="contato">
    <div class="container">
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
        <div class="footer-bottom">
            <p>© 2025 Burger Express. Todos os direitos reservados.</p>
        </div>
    </div>
</footer>
""", unsafe_allow_html=True)




# =============== FOOTER ===============
st.markdown("""
<footer class="footer full-width-section" id="contato">
    <div class="container">
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
        <div class="footer-bottom">
            <p>© 2025 Burger Express. Todos os direitos reservados.</p>
        </div>
    </div>
</footer>
""", unsafe_allow_html=True)
