"""
LES LANGUES DE CHEZ NOUS
Version MOBILE OPTIMISÉE
"""

import streamlit as st
import json
from pathlib import Path
import difflib
import base64

def get_logo_base64():
    chemins = [
        "assets/Logo_Apprendre_les_Langues_de_chez_Nous-removebg-preview.png",
        "assets/logo.png"
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

# CSS OPTIMISÉ MOBILE
st.markdown("""
<style>
    /* Sidebar accessible sur mobile */
    button[kind="header"] {
        display: block !important;
    }
    
    [data-testid="collapsedControl"] {
        display: flex !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 9999 !important;
        background: white !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    [data-testid="collapsedControl"] svg {
        color: #456323 !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* Header fixe */
    .custom-header {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 90px;
        background: #FAF8F5;
        z-index: 999 !important;
        display: flex !important;
        align-items: center !important;
        padding: 0.5rem 1rem 0.5rem 70px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .header-logo {
        width: 70px;
        height: auto;
        margin-right: 1rem;
    }
    
    .header-text {
        flex: 1;
    }
    
    .header-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #456323;
        margin: 0;
        line-height: 1.1;
    }
    
    .header-subtitle {
        font-size: 0.75rem;
        font-style: italic;
        color: #333;
        margin-top: 0.2rem;
    }
    
    .main {
        padding-top: 100px !important;
        background: white;
    }
    
    .block-container {
        padding: 1rem 0.8rem !important;
        max-width: 100% !important;
    }
    
    /* Sidebar noir */
    section[data-testid="stSidebar"] {
        background: #2C2C2C !important;
        z-index: 9998 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
    }
    
    /* Labels */
    .zone-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #456323;
        text-transform: uppercase;
        margin: 1rem 0 0.5rem 0;
    }
    
    /* Inputs */
    .stTextArea textarea {
        font-size: 1rem !important;
        padding: 1rem !important;
        border: 2px solid #E0E0E0 !important;
        border-radius: 8px !important;
        background: white !important;
        min-height: 140px !important;
        resize: vertical !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #456323 !important;
        box-shadow: 0 0 0 2px rgba(69, 99, 35, 0.1) !important;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #456323 !important;
        border-radius: 8px !important;
    }
    
    /* Résultat */
    .result-box {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        padding: 1rem;
        min-height: 120px;
        background: white;
        margin-bottom: 0.5rem;
    }
    
    .result-text {
        font-size: 1.1rem;
        color: #2c3e50;
        line-height: 1.5;
    }
    
    .badge {
        display: inline-block;
        background: #456323;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Info box */
    .info-box {
        background: #FFF3E0;
        border-left: 3px solid #FF9800;
        padding: 0.8rem;
        border-radius: 4px;
        margin: 1rem 0;
        font-size: 0.85rem;
    }
    
    audio {
        width: 100%;
        margin: 0.5rem 0;
    }
    
    /* Stats */
    .stats-footer {
        margin-top: 2rem;
        padding: 1rem;
        background: #FAF8F5;
        border-radius: 8px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Desktop */
    @media (min-width: 769px) {
        .custom-header {
            height: 120px !important;
            padding: 0 2rem !important;
        }
        
        .header-logo {
            width: 120px !important;
        }
        
        .header-title {
            font-size: 2.2rem !important;
        }
        
        .header-subtitle {
            font-size: 1rem !important;
        }
        
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        .block-container {
            max-width: 1200px !important;
            padding: 2rem 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# HEADER
logo_base64 = get_logo_base64()
st.markdown(f'''
<div class="custom-header">
    {f'<img src="data:image/png;base64,{logo_base64}" class="header-logo">' if logo_base64 else ''}
    <div class="header-text">
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
        unique_id = f"audio_{audio_id}_{int(time.time() * 1000)}"
        st.markdown(f'<audio id="{unique_id}" controls preload="auto" playsinline><source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg"></audio>', unsafe_allow_html=True)
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
    'eton': {'nom': '🇨🇲 Eton', 'court': 'Eton'},
    'bamoun': {'nom': '🇨🇲 Bamoun', 'court': 'Bamoun'},
    'fufulde': {'nom': '🇨🇲 Fufulde', 'court': 'Fulfulde'},
    'douala': {'nom': '🇨🇲 Douala', 'court': 'Duálá'}
}

def normaliser(texte):
    import string, unicodedata
    if not texte:
        return ""
    texte = texte.lower().strip()
    texte = texte.translate(str.maketrans('', '', string.punctuation))
    return ''.join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')

def rechercher_mot(texte_fr, langue):
    try:
        norm = normaliser(texte_fr)
        for item in corpus.get('items', []):
            if normaliser(item.get('francais', '')) == norm:
                trad = item.get('traductions', {}).get(langue, {})
                if trad:
                    autres = {lc: item['traductions'][lc] for lc in ['eton', 'bamoun', 'fufulde', 'douala'] 
                            if lc != langue and lc in item.get('traductions', {})}
                    return {
                        'trouve': True,
                        'traduction': trad.get('texte', ''),
                        'audio': trad.get('audio_url', ''),
                        'type': item.get('type', 'mot'),
                        'autres': autres
                    }
        return {'trouve': False}
    except:
        return {'trouve': False}

def suggestions(texte_fr):
    try:
        norm = normaliser(texte_fr)
        mots = [(item.get('francais', ''), normaliser(item.get('francais', ''))) 
               for item in corpus.get('items', []) if item.get('francais', '')]
        sugg = [(m, difflib.SequenceMatcher(None, norm, n).ratio()) for m, n in mots]
        return [s[0] for s in sorted([s for s in sugg if s[1] > 0.6], key=lambda x: x[1], reverse=True)[:3]]
    except:
        return []

def get_vocab():
    vocab = {'eton': set(), 'bamoun': set(), 'fufulde': set(), 'douala': set()}
    for item in corpus.get('items', []):
        mot = item.get('francais', '').strip()
        if mot:
            for lang in vocab.keys():
                if lang in item.get('traductions', {}):
                    vocab[lang].add(mot)
    return {lang: sorted(list(mots)) for lang, mots in vocab.items()}

# SIDEBAR
with st.sidebar:
    st.markdown("### 📚 Vocabulaire")
    vocabulaire = get_vocab()
    langue_vocab = st.selectbox("Langue :", ['Eton', 'Bamoun', 'Fulfulde', 'Douala'], key="vocab_lang")
    lang_map = {'Eton': 'eton', 'Bamoun': 'bamoun', 'Fulfulde': 'fufulde', 'Douala': 'douala'}
    mots = vocabulaire.get(lang_map[langue_vocab], [])
    st.metric("Mots disponibles", len(mots))
    recherche = st.text_input("🔍 Rechercher :", key="search")
    if recherche:
        filtres = [m for m in mots if recherche.lower() in m.lower()]
        if filtres:
            for m in filtres[:50]:
                st.caption(f"• {m}")
    else:
        for m in mots[:100]:
            st.caption(f"• {m}")
    st.markdown("---")
    st.metric("Total", corpus.get('statistiques', {}).get('total_items', 0))

# INTERFACE PRINCIPALE
st.markdown('<div class="zone-label">🎯 Choisissez la langue</div>', unsafe_allow_html=True)
langues_codes = ['eton', 'bamoun', 'fufulde', 'douala']
langues_options = [LANGUES_INFO[l]['nom'] for l in langues_codes]
langue_select = st.selectbox("Langue cible", langues_options, label_visibility="collapsed", key="lang_select")
langue_code = langues_codes[[i for i, o in enumerate(langues_options) if o == langue_select][0]]

st.markdown('<div class="zone-label">🇫🇷 Texte en Français</div>', unsafe_allow_html=True)
texte_fr = st.text_area("Français", height=140, placeholder="Tapez un mot ou une phrase en français...", key="input_fr", label_visibility="collapsed")
if texte_fr:
    st.caption(f"📝 {len(texte_fr)} caractères")

if texte_fr:
    st.markdown("<div style='text-align: center; font-size: 2rem; margin: 1rem 0;'>⬇️</div>", unsafe_allow_html=True)
    st.markdown(f'<div class="zone-label">✨ Traduction en {langue_select.split()[1]}</div>', unsafe_allow_html=True)
    
    resultat = rechercher_mot(texte_fr, langue_code)
    
    if resultat['trouve']:
        st.markdown(f'<div class="result-box"><div class="result-text">{resultat["traduction"]}</div></div>', unsafe_allow_html=True)
        type_label = "📖 Mot" if resultat['type'] == 'mot' else "💬 Phrase"
        st.markdown(f'<div class="badge">{type_label}</div>', unsafe_allow_html=True)
        
        if resultat['audio']:
            st.markdown("#### 🔊 Prononciation")
            st.markdown('<div class="info-box">📱 Langue à tons – écoutez attentivement !</div>', unsafe_allow_html=True)
            afficher_audio_local(resultat['audio'], f"{langue_code}_{texte_fr[:20]}")
        
        if resultat['autres']:
            with st.expander("🌐 Voir dans d'autres langues"):
                for lc, data in resultat['autres'].items():
                    st.markdown(f"**{LANGUES_INFO[lc]['court']}**: {data.get('texte', '')}")
                    if data.get('audio_url'):
                        afficher_audio_local(data['audio_url'], f"{lc}_{texte_fr[:20]}")
    else:
        st.warning(f"❌ « {texte_fr} » non trouvé")
        sugg = suggestions(texte_fr)
        if sugg:
            st.info("💡 Suggestions : " + ", ".join(sugg))

# FOOTER STATS
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
