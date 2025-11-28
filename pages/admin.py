# pages/admin.py - PAINEL ADMIN COM CONTROLE DE INGREDIENTES
import streamlit as st
import json
import os
import base64

st.set_page_config(page_title="Admin • Burger Express", page_icon="🔒", layout="centered")

# =============== CONFIGURAÇÃO DE CAMINHOS ===============
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRATOS_FILE = os.path.join(BASE_DIR, "pratos.json")
ESTOQUE_FILE = os.path.join(BASE_DIR, "estoque.json")
INGREDIENTES_FILE = os.path.join(BASE_DIR, "ingredientes.json")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "images", "background-login.jpg")

# Função para converter imagem em base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

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

# Carregar imagem de background
background_b64 = get_base64_image(BACKGROUND_IMAGE)
if background_b64:
    background_css = f"url('data:image/jpeg;base64,{background_b64}')"
else:
    background_css = "url('https://images.unsplash.com/photo-1553979459-d2229ba7433b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80')"

st.markdown(f"""
<style>
    /* FUNDO MAIS ESCURO PARA MELHOR CONTRASTE */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.95)), {background_css} center/cover fixed !important;
    }}
    
    /* TEXTO BRANCO GERAL */
    .stApp {{
        color: white !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: white !important;
    }}
    
    /* RESTAURAR BOTÕES DO LOGIN */
    .stButton > button {{
        background: #EA1D2C !important; 
        color: white !important;
        border: none !important;
    }}
    
    .stButton > button:hover {{
        background: #c91a26 !important;
    }}
    
    /* TABS E OUTROS ELEMENTOS */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255,255,255,0.1);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: white !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: #EA1D2C !important;
    }}
</style>
""", unsafe_allow_html=True)

# JavaScript para corrigir cores específicas
st.markdown("""
<script>
// Aguardar o carregamento da página
setTimeout(function() {
    // File Uploader - texto preto
    const uploaders = document.querySelectorAll('[data-testid="stFileUploader"]');
    uploaders.forEach(uploader => {
        const texts = uploader.querySelectorAll('p, span, div');
        texts.forEach(text => {
            if (text.textContent.includes('Drag and drop') || 
                text.textContent.includes('Limit') || 
                text.textContent.includes('JPG') ||
                text.textContent.includes('JPEG') ||
                text.textContent.includes('PNG')) {
                text.style.color = '#000000 !important';
            }
        });
    });
    
    // Botão Adicionar Ingrediente - texto preto
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        if (button.textContent.includes('Adicionar Ingrediente')) {
            button.style.color = '#000000 !important';
            button.style.backgroundColor = '#FFFFFF !important';
            button.style.border = '2px solid #EA1D2C !important';
        }
    });
    
    // Selectboxes - texto preto
    const selects = document.querySelectorAll('[data-baseweb="select"]');
    selects.forEach(select => {
        const selectedValue = select.querySelector('[data-testid="stMarkdownContainer"]');
        if (selectedValue) {
            selectedValue.style.color = '#000000 !important';
        }
    });
    
    // Botões + e - do número
    const numberInputs = document.querySelectorAll('[data-testid="stNumberInput"]');
    numberInputs.forEach(input => {
        const buttons = input.querySelectorAll('button');
        buttons.forEach(button => {
            button.style.color = '#000000 !important';
            button.style.backgroundColor = '#f0f0f0 !important';
        });
    });
}, 1000);
</script>
""", unsafe_allow_html=True)

if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

if not st.session_state.admin_logado:
    st.markdown("""
    <div class="login-box" style="background: rgba(0,0,0,0.95); padding: 50px 60px; border-radius: 20px; text-align: center; max-width: 450px; margin: 100px auto;">
        <div style="font-size: 4.5rem; margin-bottom: 10px;">🍔</div>
        <h1 style="color: #EA1D2C; font-size: 2.5rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">Área Restrita</h1>
        <p style="color:rgba(255,255,255,0.9);font-size:1.1rem;font-weight:500;">Acesso exclusivo para administradores</p>
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
    st.markdown("<h1 style='color:white;text-align:center;margin-bottom:30px;text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>🍔 Painel Administrativo - Controle Completo</h1>", unsafe_allow_html=True)
    
    # Carregar dados
    ingredientes = carregar_ingredientes()
    pratos = carregar_pratos()
    estoque_pratos = carregar_estoque()
    
    # =============== ABA DE INGREDIENTES ===============
    tab1, tab2, tab3 = st.tabs(["📦 Controle de Ingredientes", "🍔 Gestão de Pratos", "📊 Estoque & Relatórios"])
    
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
            
            if st.form_submit_button("➕ Adicionar Ingrediente"):
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
        st.subheader("📊 Relatórios & Alertas")
        
        # Alertas de estoque baixo
        ingredientes_baixo = [ing for ing in ingredientes if ing['estoque'] <= ing['minimo']]
        if ingredientes_baixo:
            st.error("🚨 INGREDIENTES COM ESTOQUE BAIXO")
            for ing in ingredientes_baixo:
                st.write(f"❌ **{ing['nome']}**: {ing['estoque']} {ing['unidade']} (mínimo: {ing['minimo']})")
        
        # Estatísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Ingredientes", len(ingredientes))
        with col2:
            st.metric("Pratos Cadastrados", len(pratos))
        with col3:
            st.metric("Ingredientes em Alerta", len(ingredientes_baixo))
        
        # Custo estimado dos pratos (exemplo simplificado)
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