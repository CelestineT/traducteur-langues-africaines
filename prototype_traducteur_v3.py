"""
PROTOTYPE TRADUCTEUR - LES LANGUES DE CHEZ NOUS
Version finale optimisée
"""

import streamlit as st
import json
from pathlib import Path
import difflib
import base64

# =========================================================
# CONFIGURATION
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
    
    /* Header personnalisé blanc cassé */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 140px;
        background-color: #FAF8F5;
        z-index: 999;
        display: flex;
        align-items: center;
        padding: 0 3rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .header-logo-container {
        flex-shrink: 0;
        margin-right: 2.5rem;
    }
    
    .header-logo {
        width: 140px;
        height: auto;
    }
    
    .header-text {
        flex: 1;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2C1810;
        margin: 0;
        line-height: 1.2;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        font-style: italic;
        color: #666;
        margin-top: 0.3rem;
    }
    
    /* Main content */
    .main {
        padding-top: 160px !important;
        background: white;
    }
    
    .block-container {
        max-width: 1200px;
        padding: 2rem 1rem;
    }
    
    /* Sidebar terracotta */
    section[data-testid="stSidebar"] {
        background-color: #B87060 !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #B87060 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #2C1810 !important;
        border: none !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Zones de traduction alignées */
    .stTextArea textarea {
        font-size: 1rem !important;
        padding: 1rem !important;
        border: 2px solid #E0E0E0 !important;
        border-radius: 8px !important;
        background: white !important;
        height: 220px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #B87060 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(184, 112, 96, 0.15) !important;
    }
    
    .zone-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #B87060;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #B87060 !important;
        border-radius: 8px !important;
    }
    
    .translation-result {
        background: white;
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        padding: 1rem;
        height: 220px;
        font-size: 1.1rem;
        color: #2c3e50;
        overflow-y: auto;
    }
    
    .badge-type {
        display: inline-block;
        background: #B87060;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
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
        border: 1px solid #E0E0E0;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    @media (max-width: 768px) {
        .custom-header {
            height: 100px;
            padding: 0 1rem;
        }
        .header-title {
            font-size: 1.5rem;
        }
        .header-subtitle {
            font-size: 0.85rem;
        }
        .header-logo {
            width: 90px;
        }
        .main {
            padding-top: 120px !important;
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
    <div class="header-logo-container">
        {f'<img src="data:image/png;base64,{logo_base64}" class="header-logo" alt="Logo">' if logo_base64 else ''}
    </div>
    <div class="header-text">
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
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
        
        import time
        timestamp = int(time.time() * 1000)
        unique_id = f"audio_{audio_id.replace(' ', '_')}_{timestamp}"
        
        audio_html = f'''
        <div style="margin: 10px 0;">
            <audio id="{unique_id}" controls preload="auto" playsinline webkit-playsinline
                   style="width: 100%; max-width: 500px;">
                <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
            </audio>
        </div>
        <script>
        (function() {{
            document.querySelectorAll('audio').forEach(a => {{
                if (a.id !== '{unique_id}') {{ a.pause(); a.src = ''; }}
            }});
            setTimeout(() => {{
                const audio = document.getElementById('{unique_id}');
                if (audio) {{ audio.load(); }}
            }}, 50);
        }})();
        </script>
        '''
        
        st.markdown(audio_html, unsafe_allow_html=True)
        return True
    except:
        return False

# =========================================================
# CHARGEMENT CORPUS
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

# =========================================================
# FONCTIONS RECHERCHE
# =========================================================

def normaliser_pour_recherche(texte):
    import string, unicodedata
    if not texte:
        return ""
    texte = texte.lower().strip()
    texte = texte.translate(str.maketrans('', '', string.punctuation))
    texte = ' '.join(texte.split())
    texte = ''.join(c for c in unicodedata.normalize('NFD', texte)
                   if unicodedata.category(c) != 'Mn')
    return texte

def rechercher_mot(texte_francais, langue_cible):
    try:
        texte_normalise = normaliser_pour_recherche(texte_francais)
        for item in corpus.get('items', []):
            texte_corpus = normaliser_pour_recherche(item.get('francais', ''))
            if texte_corpus == texte_normalise:
                traduction_data = item.get('traductions', {}).get(langue_cible, {})
                if traduction_data:
                    autres_langues = {}
                    for lang_code in ['eton', 'bamoun', 'fufulde', 'douala']:
                        if lang_code != langue_cible and lang_code in item.get('traductions', {}):
                            autres_langues[lang_code] = item['traductions'][lang_code]
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
        mots_disponibles = []
        for item in corpus.get('items', []):
            mot_original = item.get('francais', '')
            if mot_original:
                mot_normalise = normaliser_pour_recherche(mot_original)
                mots_disponibles.append((mot_original, mot_normalise))
        
        suggestions = []
        for mot_original, mot_normalise in mots_disponibles:
            ratio = difflib.SequenceMatcher(None, texte_normalise, mot_normalise).ratio()
            if ratio > 0.6:
                suggestions.append((mot_original, ratio))
        
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in suggestions[:max_suggestions]]
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
    
    langue_vocab = st.selectbox(
        "Voir les mots disponibles en :",
        options=['Eton', 'Bamoun', 'Fulfulde', 'Douala'],
        key="langue_sidebar"
    )
    
    lang_map = {'Eton': 'eton', 'Bamoun': 'bamoun', 'Fulfulde': 'fufulde', 'Douala': 'douala'}
    lang_code_sidebar = lang_map[langue_vocab]
    
    mots_langue = vocabulaire.get(lang_code_sidebar, [])
    st.metric("Mots français disponibles", len(mots_langue))
    
    recherche = st.text_input("🔍 Rechercher un mot :", key="recherche_vocab")
    
    if recherche:
        mots_filtres = [m for m in mots_langue if recherche.lower() in m.lower()]
        if mots_filtres:
            st.success(f"✅ {len(mots_filtres)} mot(s)")
            for mot in mots_filtres[:50]:
                st.caption(f"• {mot}")
            if len(mots_filtres) > 50:
                st.caption(f"... +{len(mots_filtres) - 50}")
        else:
            st.warning("❌ Aucun mot")
    else:
        st.caption("**Tous les mots :**")
        for mot in mots_langue[:100]:
            st.caption(f"• {mot}")
        if len(mots_langue) > 100:
            st.caption(f"... +{len(mots_langue) - 100}")
    
    st.markdown("---")
    st.markdown("### 📊 Statistiques")
    stats = corpus.get('statistiques', {})
    st.metric("Total", stats.get('total_items', 0))
    
    for lang, info in LANGUES_INFO.items():
        nb = len(vocabulaire.get(lang, []))
        st.caption(f"{info['nom_court']}: {nb}")
    
    st.markdown("---")
    st.caption("© 2025 Les Langues de Chez Nous")
    st.caption("Prototype MVP · Eton, Bamoun, Fulfulde, Douala")

# =========================================================
# INTERFACE PRINCIPALE
# =========================================================

# Sélection langue
col_l1, col_l2, col_l3 = st.columns([2, 1, 2])

with col_l1:
    st.markdown('<div class="zone-label">🇫🇷 Français</div>', unsafe_allow_html=True)

with col_l3:
    langues_codes = ['eton', 'bamoun', 'fufulde', 'douala']
    langues_options = [LANGUES_INFO[lang]['nom_affichage'] for lang in langues_codes]
    
    langue_selectionnee = st.selectbox(
        "Langue cible",
        options=langues_options,
        index=0,
        label_visibility="collapsed"
    )
    
    langue_code = langues_codes[0]
    for i, option in enumerate(langues_options):
        if option == langue_selectionnee:
            langue_code = langues_codes[i]
            break

st.markdown("<br>", unsafe_allow_html=True)

# Zones traduction
col_source, col_arrow, col_target = st.columns([5, 1, 5])

with col_source:
    texte_francais = st.text_area(
        "Texte source",
        height=220,
        placeholder="Tapez un mot ou une phrase en français...",
        key="input_francais",
        label_visibility="collapsed"
    )
    if texte_francais:
        st.caption(f"📝 {len(texte_francais)} caractères")

with col_arrow:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 2rem;'>→</div>", unsafe_allow_html=True)

with col_target:
    if texte_francais:
        resultat = rechercher_mot(texte_francais, langue_code)
        
        if resultat['trouve']:
            type_label = "📖 Mot" if resultat['type'] == 'mot' else "💬 Phrase"
            st.markdown(f'<div class="badge-type">{type_label}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="translation-result">{resultat["traduction"]}</div>', unsafe_allow_html=True)
        else:
            st.warning(f"❌ « {texte_francais} » non trouvé")
            suggestions = trouver_suggestions(texte_francais)
            if suggestions:
                st.info("💡 Suggestions : " + ", ".join(suggestions[:3]))
    else:
        st.markdown('<div class="translation-result" style="color: #999;">La traduction apparaîtra ici...</div>', unsafe_allow_html=True)

# Audio et autres langues
if texte_francais:
    resultat = rechercher_mot(texte_francais, langue_code)
    
    if resultat['trouve']:
        st.markdown("<br>", unsafe_allow_html=True)
        
        if resultat['audio_url']:
            st.markdown("### 🔊 Prononciation authentique")
            st.markdown('<div class="info-box">📱 Appuyez sur ▶️ pour écouter. Langue à tons – écoutez attentivement !</div>', unsafe_allow_html=True)
            
            audio_id = f"{langue_code}_{texte_francais[:20]}"
            if afficher_audio_local(resultat['audio_url'], audio_id):
                st.caption("✅ Audio chargé")
        
        if resultat['autres_langues']:
            with st.expander("🌐 Voir dans d'autres langues"):
                for lang_code_autre, data in resultat['autres_langues'].items():
                    st.markdown(f"**{LANGUES_INFO[lang_code_autre]['nom_court']}** : {data.get('texte', '')}")
                    if data.get('audio_url'):
                        audio_id_autre = f"{lang_code_autre}_{texte_francais[:20]}"
                        afficher_audio_local(data['audio_url'], audio_id_autre)
                    st.markdown("---")

# Footer stats
st.markdown('<div class="stats-footer">', unsafe_allow_html=True)

stats = corpus.get('statistiques', {})
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📚 Total", stats.get('total_items', 0))
with col2:
    st.metric("Eton", stats.get('eton', 0))
with col3:
    st.metric("Bamoun", stats.get('bamoun', 0))
with col4:
    st.metric("Fulfulde", stats.get('fufulde', 0))
with col5:
    st.metric("Duálá", stats.get('douala', 0))

st.markdown('</div>', unsafe_allow_html=True)
