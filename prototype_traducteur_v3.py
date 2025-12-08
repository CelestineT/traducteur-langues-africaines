"""
LES LANGUES DE CHEZ NOUS - Traducteur
Version finale optimisée desktop + mobile
"""

import streamlit as st
import json
from pathlib import Path
import difflib
import base64

# =========================================================
# CONFIG
# =========================================================

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

# =========================================================
# STYLES CSS
# =========================================================

st.markdown("""
<style>
    /* Masquer header Streamlit */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Header personnalisé */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 120px;
        background-color: #FAF8F5;
        z-index: 999;
        display: flex;
        align-items: center;
        padding: 0 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .header-logo {
        width: 120px;
        height: auto;
        margin-right: 2rem;
    }
    
    .header-center {
        flex: 1;
        text-align: center;
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #456323;
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 1rem;
        font-style: italic;
        color: #333;
        margin-top: 0.2rem;
    }
    
    /* Main */
    .main {
        padding-top: 140px !important;
        background: white;
    }
    
    .block-container {
        max-width: 1200px;
        padding: 2rem 1rem;
    }
    
    /* Sidebar NOIR */
    section[data-testid="stSidebar"] {
        background-color: #2C2C2C !important;
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
        font-size: 2rem !important;
    }
    
    /* Zones traduction */
    .translation-container {
        display: flex;
        gap: 2rem;
        align-items: flex-start;
    }
    
    .translation-box {
        flex: 1;
    }
    
    .stTextArea textarea {
        font-size: 1rem !important;
        padding: 1rem !important;
        border: 2px solid #E0E0E0 !important;
        border-radius: 8px !important;
        background: white !important;
        height: 250px !important;
        resize: none !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #456323 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(69, 99, 35, 0.1) !important;
    }
    
    .translation-result-box {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        padding: 1rem;
        height: 250px;
        background: white;
        overflow-y: auto;
    }
    
    .translation-text {
        font-size: 1.1rem;
        color: #2c3e50;
        line-height: 1.6;
    }
    
    .zone-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #456323;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .badge-type {
        display: inline-block;
        background: #456323;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #456323 !important;
        border-radius: 8px !important;
    }
    
    audio {
        width: 100%;
        max-width: 500px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #FFF3E0;
        border-left: 4px solid #FF9800;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .stats-footer {
        margin-top: 3rem;
        padding: 1.5rem;
        background: #FAF8F5;
        border-radius: 12px;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* RESPONSIVE MOBILE */
    @media (max-width: 768px) {
        .custom-header {
            height: 80px;
            padding: 0 1rem;
            flex-direction: column;
            justify-content: center;
        }
        
        .header-logo {
            width: 60px;
            margin-right: 1rem;
            position: absolute;
            left: 1rem;
        }
        
        .header-center {
            margin-left: 70px;
        }
        
        .header-title {
            font-size: 1.3rem;
        }
        
        .header-subtitle {
            font-size: 0.75rem;
        }
        
        .main {
            padding-top: 100px !important;
        }
        
        .translation-container {
            flex-direction: column;
            gap: 1rem;
        }
        
        .stTextArea textarea,
        .translation-result-box {
            height: 180px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

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

# =========================================================
# FONCTION AUDIO
# =========================================================

def afficher_audio_local(chemin_audio, audio_id="default"):
    if not chemin_audio or not Path(chemin_audio).exists():
        return False
    try:
        with open(chemin_audio, 'rb') as f:
            audio_base64 = base64.b64encode(f.read()).decode()
        import time
        unique_id = f"audio_{audio_id.replace(' ', '_')}_{int(time.time() * 1000)}"
        st.markdown(f'''
        <audio id="{unique_id}" controls preload="auto" playsinline webkit-playsinline style="width: 100%; max-width: 500px;">
            <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
        </audio>
        <script>
        (function(){{
            document.querySelectorAll('audio').forEach(a=>{{if(a.id!=='{unique_id}'){{a.pause();a.src='';}};}});
            setTimeout(()=>{{const audio=document.getElementById('{unique_id}');if(audio)audio.load();}},50);
        }})();
        </script>
        ''', unsafe_allow_html=True)
        return True
    except:
        return False

# =========================================================
# CORPUS
# =========================================================

@st.cache_data
def charger_corpus():
    try:
        with open('corpus.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        st.error("❌ Fichier corpus.json non trouvé")
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

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("### Vocabulaire du prototype")
    
    vocabulaire = get_vocabulaire_par_langue()
    
    langue_vocab = st.selectbox("Voir les mots en :", ['Eton', 'Bamoun', 'Fulfulde', 'Douala'], key="langue_sidebar")
    
    lang_map = {'Eton': 'eton', 'Bamoun': 'bamoun', 'Fulfulde': 'fufulde', 'Douala': 'douala'}
    mots_langue = vocabulaire.get(lang_map[langue_vocab], [])
    
    st.metric("Mots disponibles", len(mots_langue))
    
    recherche = st.text_input("🔍 Rechercher :", key="recherche_vocab")
    
    if recherche:
        mots_filtres = [m for m in mots_langue if recherche.lower() in m.lower()]
        if mots_filtres:
            st.success(f"✅ {len(mots_filtres)} mot(s)")
            for mot in mots_filtres[:50]:
                st.caption(f"• {mot}")
        else:
            st.warning("❌ Aucun")
    else:
        for mot in mots_langue[:100]:
            st.caption(f"• {mot}")
        if len(mots_langue) > 100:
            st.caption(f"... +{len(mots_langue) - 100}")
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Total", corpus.get('statistiques', {}).get('total_items', 0))
    for lang, info in LANGUES_INFO.items():
        st.caption(f"{info['nom_court']}: {len(vocabulaire.get(lang, []))}")

# =========================================================
# INTERFACE
# =========================================================

# Labels
col1, col2, col3 = st.columns([2, 1, 2])
with col1:
    st.markdown('<div class="zone-label">🇫🇷 Français</div>', unsafe_allow_html=True)
with col3:
    langues_codes = ['eton', 'bamoun', 'fufulde', 'douala']
    langues_options = [LANGUES_INFO[lang]['nom_affichage'] for lang in langues_codes]
    langue_selectionnee = st.selectbox("Langue", langues_options, label_visibility="collapsed")
    langue_code = langues_codes[[i for i, o in enumerate(langues_options) if o == langue_selectionnee][0]]

st.markdown("<br>", unsafe_allow_html=True)

# Zones traduction
col_source, col_arrow, col_target = st.columns([5, 1, 5])

with col_source:
    texte_francais = st.text_area("Source", height=250, placeholder="Tapez ici...", key="input_francais", label_visibility="collapsed")
    if texte_francais:
        st.caption(f"📝 {len(texte_francais)} caractères")

with col_arrow:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 2rem;'>→</div>", unsafe_allow_html=True)

with col_target:
    if texte_francais:
        resultat = rechercher_mot(texte_francais, langue_code)
        if resultat['trouve']:
            st.markdown(f'<div class="translation-result-box"><div class="translation-text">{resultat["traduction"]}</div></div>', unsafe_allow_html=True)
            type_label = "📖 Mot" if resultat['type'] == 'mot' else "💬 Phrase"
            st.markdown(f'<div class="badge-type">{type_label}</div>', unsafe_allow_html=True)
        else:
            st.warning(f"❌ « {texte_francais} » non trouvé")
            suggestions = trouver_suggestions(texte_francais)
            if suggestions:
                st.info("💡 " + ", ".join(suggestions[:3]))
    else:
        st.markdown('<div class="translation-result-box" style="color: #999;">La traduction apparaîtra ici...</div>', unsafe_allow_html=True)

# Audio
if texte_francais:
    resultat = rechercher_mot(texte_francais, langue_code)
    if resultat['trouve'] and resultat['audio_url']:
        st.markdown("### 🔊 Prononciation")
        st.markdown('<div class="info-box">📱 Langue à tons – écoutez attentivement !</div>', unsafe_allow_html=True)
        if afficher_audio_local(resultat['audio_url'], f"{langue_code}_{texte_francais[:20]}"):
            st.caption("✅ Chargé")
        
        if resultat['autres_langues']:
            with st.expander("🌐 Autres langues"):
                for lc, data in resultat['autres_langues'].items():
                    st.markdown(f"**{LANGUES_INFO[lc]['nom_court']}** : {data.get('texte', '')}")
                    if data.get('audio_url'):
                        afficher_audio_local(data['audio_url'], f"{lc}_{texte_francais[:20]}")

# Footer
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
