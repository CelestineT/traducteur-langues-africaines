"""
LES LANGUES DE CHEZ NOUS
Version finale avec sidebar mobile + header fixe
"""

import streamlit as st
import json
from pathlib import Path
import difflib
import base64

# CONFIG
def get_logo_base64():
    chemins = [
        "assets/Logo_Apprendre_les_Langues_de_chez_Nous-removebg-preview.png",
        "assets/logo.png",
        "Logo_Apprendre_les_Langues_de_chez_Nous-removebg-preview.png"
    ]
    for chemin in chemins:
        try:
            with open(chemin, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except:
            continue
    return None

st.set_page_config(
    page_title="Les Langues de Chez Nous",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    /* BOUTON HAMBURGER MOBILE */
    button[kind="header"] {
        display: block !important;
        position: fixed !important;
        top: 110px !important;
        left: 10px !important;
        z-index: 1001 !important;
        background: white !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
    }
    
    [data-testid="collapsedControl"] {
        display: block !important;
        position: fixed !important;
        top: 110px !important;
        left: 10px !important;
        z-index: 1001 !important;
    }
    
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
    }
    
    header[data-testid="stHeader"] > div:not([data-testid="collapsedControl"]) {
        display: none !important;
    }
    
    /* HEADER FIXE */
    .custom-header {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 100px;
        background-color: #FAF8F5;
        z-index: 1000 !important;
        display: flex !important;
        align-items: center !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    }
    
    .header-logo {
        width: 80px;
        height: auto;
        margin-right: 1rem;
        flex-shrink: 0;
    }
    
    .header-center {
        flex: 1;
        text-align: center;
    }
    
    .header-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #456323;
        margin: 0;
        line-height: 1.2;
    }
    
    .header-subtitle {
        font-size: 0.85rem;
        font-style: italic;
        color: #333;
        margin-top: 0.2rem;
    }
    
    .main {
        padding-top: 120px !important;
        background: white !important;
    }
    
    .block-container {
        max-width: 1200px;
        padding: 1rem !important;
    }
    
    /* SIDEBAR NOIR */
    section[data-testid="stSidebar"] {
        background-color: #2C2C2C !important;
        z-index: 999 !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #2C2C2C !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 1.8rem !important;
    }
    
    /* ZONES */
    .stTextArea textarea {
        font-size: 0.95rem !important;
        padding: 0.8rem !important;
        border: 2px solid #E0E0E0 !important;
        border-radius: 8px !important;
        background: white !important;
        height: 200px !important;
        resize: none !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #456323 !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(69, 99, 35, 0.1) !important;
    }
    
    .translation-result-box {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        padding: 0.8rem;
        height: 200px;
        background: white;
        overflow-y: auto;
    }
    
    .translation-text {
        font-size: 1rem;
        color: #2c3e50;
        line-height: 1.5;
    }
    
    .zone-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #456323;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 0.3rem;
    }
    
    .badge-type {
        display: inline-block;
        background: #456323;
        color: white;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #456323 !important;
        border-radius: 8px !important;
    }
    
    audio {
        width: 100%;
        max-width: 500px;
        margin: 0.8rem 0;
    }
    
    .info-box {
        background: #FFF3E0;
        border-left: 3px solid #FF9800;
        padding: 0.8rem;
        border-radius: 4px;
        margin: 0.8rem 0;
        font-size: 0.85rem;
    }
    
    .stats-footer {
        margin-top: 2rem;
        padding: 1rem;
        background: #FAF8F5;
        border-radius: 8px;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* DESKTOP */
    @media (min-width: 769px) {
        .custom-header {
            height: 120px !important;
            padding: 0 2rem !important;
        }
        
        .header-logo {
            width: 120px !important;
            margin-right: 2rem !important;
        }
        
        .header-title {
            font-size: 2.2rem !important;
        }
        
        .header-subtitle {
            font-size: 1rem !important;
        }
        
        .main {
            padding-top: 140px !important;
        }
        
        .block-container {
            padding: 2rem 1rem !important;
        }
        
        .stTextArea textarea,
        .translation-result-box {
            height: 250px !important;
        }
        
        button[kind="header"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# HEADER
logo_base64 = get_logo_base64()

st.markdown(f'''
<div class="custom-header">
    {f'<img src="data:image/png;base64,{logo_base64}" class="header-logo" alt="Logo">' if logo_base64 else ''}
    <div class="header-center">
        <h1 class="header-title">Les Langues de Chez Nous</h1>
        <p class="header-subtitle">Traducteur Français - Langues Africaines</p>
    </div>
</div>
''', unsafe_allow_html=True)

# FONCTIONS
def afficher_audio_local(chemin_audio, audio_id="default"):
    if not chemin_audio or not Path(chemin_audio).exists():
        return False
    try:
        with open(chemin_audio, 'rb') as f:
            audio_base64 = base64.b64encode(f.read()).decode()
        import time
        unique_id = f"audio_{audio_id.replace(' ', '_')}_{int(time.time() * 1000)}"
        st.markdown(f'<audio id="{unique_id}" controls preload="auto" playsinline webkit-playsinline><source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg"></audio>', unsafe_allow_html=True)
        return True
    except:
        return False

@st.cache_data
def charger_corpus():
    try:
        with open('corpus.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        st.error("❌ corpus.json non trouvé")
        st.stop()

corpus = charger_corpus()

LANGUES_INFO = {
    'eton': {'nom_affichage': '🇨🇲 Eton', 'nom_court': 'Eton'},
    'bamoun': {'nom_affichage': '🇨🇲 Bamoun', 'nom_court': 'Bamoun'},
    'fufulde': {'nom_affichage': '🇨🇲 Fufulde', 'nom_court': 'Fulfulde'},
    'douala': {'nom_affichage': '🇨🇲 Douala', 'nom_court': 'Duálá'}
}

def normaliser_pour_recherche(texte):
    import string, unicodedata
    if not texte:
        return ""
    texte = texte.lower().strip()
    texte = texte.translate(str.maketrans('', '', string.punctuation))
    texte = ' '.join(texte.split())
    return ''.join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')

def rechercher_mot(texte_francais, langue_cible):
    try:
        texte_normalise = normaliser_pour_recherche(texte_francais)
        for item in corpus.get('items', []):
            if normaliser_pour_recherche(item.get('francais', '')) == texte_normalise:
                traduction_data = item.get('traductions', {}).get(langue_cible, {})
                if traduction_data:
                    autres_langues = {lc: item['traductions'][lc] for lc in ['eton', 'bamoun', 'fufulde', 'douala'] 
                                    if lc != langue_cible and lc in item.get('traductions', {})}
                    return {
                        'trouve': True,
                        'traduction': traduction_data.get('texte', ''),
                        'audio_url': traduction_data.get('audio_url', ''),
                        'type': item.get('type', 'mot'),
                        'autres_langues': autres_langues
                    }
        return {'trouve': False, 'traduction': '', 'audio_url': '', 'type': '', 'autres_langues': {}}
    except:
        return {'trouve': False, 'traduction': '', 'audio_url': '', 'type': '', 'autres_langues': {}}

def trouver_suggestions(texte_francais, max_suggestions=3):
    try:
        texte_normalise = normaliser_pour_recherche(texte_francais)
        mots_disponibles = [(item.get('francais', ''), normaliser_pour_recherche(item.get('francais', ''))) 
                           for item in corpus.get('items', []) if item.get('francais', '')]
        suggestions = [(mot, difflib.SequenceMatcher(None, texte_normalise, norm).ratio()) 
                      for mot, norm in mots_disponibles]
        return [s[0] for s in sorted([s for s in suggestions if s[1] > 0.6], key=lambda x: x[1], reverse=True)[:max_suggestions]]
    except:
        return []

def get_vocabulaire_par_langue():
    vocab = {'eton': set(), 'bamoun': set(), 'fufulde': set(), 'douala': set()}
    for item in corpus.get('items', []):
        mot_fr = item.get('francais', '').strip()
        if mot_fr:
            for lang in vocab.keys():
                if lang in item.get('traductions', {}):
                    vocab[lang].add(mot_fr)
    return {lang: sorted(list(mots)) for lang, mots in vocab.items()}

# SIDEBAR
with st.sidebar:
    st.markdown("### Vocabulaire")
    vocabulaire = get_vocabulaire_par_langue()
    langue_vocab = st.selectbox("Langue :", ['Eton', 'Bamoun', 'Fulfulde', 'Douala'], key="langue_sidebar")
    lang_map = {'Eton': 'eton', 'Bamoun': 'bamoun', 'Fulfulde': 'fufulde', 'Douala': 'douala'}
    mots_langue = vocabulaire.get(lang_map[langue_vocab], [])
    st.metric("Mots", len(mots_langue))
    recherche = st.text_input("🔍 Rechercher :", key="recherche_vocab")
    if recherche:
        mots_filtres = [m for m in mots_langue if recherche.lower() in m.lower()]
        if mots_filtres:
            for mot in mots_filtres[:50]:
                st.caption(f"• {mot}")
    else:
        for mot in mots_langue[:100]:
            st.caption(f"• {mot}")
    st.markdown("---")
    st.metric("Total", corpus.get('statistiques', {}).get('total_items', 0))

# INTERFACE
col1, col2, col3 = st.columns([2, 1, 2])
with col1:
    st.markdown('<div class="zone-label">🇫🇷 Français</div>', unsafe_allow_html=True)
with col3:
    langues_codes = ['eton', 'bamoun', 'fufulde', 'douala']
    langues_options = [LANGUES_INFO[lang]['nom_affichage'] for lang in langues_codes]
    langue_selectionnee = st.selectbox("Langue", langues_options, label_visibility="collapsed")
    langue_code = langues_codes[[i for i, o in enumerate(langues_options) if o == langue_selectionnee][0]]

st.markdown("<br>", unsafe_allow_html=True)

col_source, col_arrow, col_target = st.columns([5, 1, 5])

with col_source:
    texte_francais = st.text_area("Source", height=200, placeholder="Tapez ici...", key="input_francais", label_visibility="collapsed")
    if texte_francais:
        st.caption(f"📝 {len(texte_francais)} caractères")

with col_arrow:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 1.8rem;'>→</div>", unsafe_allow_html=True)

with col_target:
    if texte_francais:
        resultat = rechercher_mot(texte_francais, langue_code)
        if resultat['trouve']:
            st.markdown(f'<div class="translation-result-box"><div class="translation-text">{resultat["traduction"]}</div></div>', unsafe_allow_html=True)
            type_label = "📖 Mot" if resultat['type'] == 'mot' else "💬 Phrase"
            st.markdown(f'<div class="badge-type">{type_label}</div>', unsafe_allow_html=True)
        else:
            st.warning(f"❌ Non trouvé")
            suggestions = trouver_suggestions(texte_francais)
            if suggestions:
                st.info("💡 " + ", ".join(suggestions[:3]))
    else:
        st.markdown('<div class="translation-result-box" style="color: #999;">Traduction ici...</div>', unsafe_allow_html=True)

if texte_francais:
    resultat = rechercher_mot(texte_francais, langue_code)
    if resultat['trouve'] and resultat['audio_url']:
        st.markdown("### 🔊 Prononciation")
        st.markdown('<div class="info-box">📱 Langue à tons !</div>', unsafe_allow_html=True)
        afficher_audio_local(resultat['audio_url'], f"{langue_code}_{texte_francais[:20]}")
        if resultat['autres_langues']:
            with st.expander("🌐 Autres langues"):
                for lc, data in resultat['autres_langues'].items():
                    st.markdown(f"**{LANGUES_INFO[lc]['nom_court']}**: {data.get('texte', '')}")
                    if data.get('audio_url'):
                        afficher_audio_local(data['audio_url'], f"{lc}_{texte_francais[:20]}")

st.markdown('<div class="stats-footer">', unsafe_allow_html=True)
stats = corpus.get('statistiques', {})
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Total", stats.get('total_items', 0))
with c2:
    st.metric("Eton", stats.get('eton', 0))
with c3:
    st.metric("Bamoun", stats.get('bamoun', 0))
with c4:
    st.metric("Fulfulde", stats.get('fufulde', 0))
with c5:
    st.metric("Duálá", stats.get('douala', 0))
st.markdown('</div>', unsafe_allow_html=True)
