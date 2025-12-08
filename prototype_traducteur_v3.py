"""
PROTOTYPE TRADUCTEUR - LES LANGUES DE CHEZ NOUS
===============================================
Style inspiré de DeepL avec sidebar vocabulaire
Support : Eton, Bamoun, Fufulde, Douala
Audios : Fichiers locaux optimisés Safari iOS
"""

import streamlit as st
import json
from pathlib import Path
import difflib
import base64

# =========================================================
# CONFIGURATION DE LA PAGE
# =========================================================

def get_logo_base64():
    """Convertit le logo en base64"""
    try:
        with open("assets/logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

st.set_page_config(
    page_title="Les Langues de Chez Nous - Traducteur",
    page_icon="assets/logo.png" if Path("assets/logo.png").exists() else "🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# STYLES CSS - STYLE DEEPL + COULEURS DU LOGO
# =========================================================

st.markdown("""
<style>
    /* Fond dégradé avec couleurs du logo (orange, rouge, vert) */
    .main {
        background: radial-gradient(circle at top left,
                                    #FFF7EC 0%,
                                    #FFE8D6 25%,
                                    #FFF0E0 50%,
                                    #F0F8F0 100%);
        min-height: 100vh;
    }
    
    /* Container central comme DeepL */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    
    /* Logo header */
    .logo-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    
    .logo-header img {
        width: 120px;
        height: auto;
        filter: drop-shadow(0 2px 8px rgba(0,0,0,0.1));
    }
    
    /* Titre style dégradé */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #E67E22 0%, #C0392B 50%, #27AE60 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }
    
    /* Zone de traduction style DeepL */
    .translation-box {
        background: white;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        padding: 1.2rem;
        min-height: 220px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s;
    }
    
    .translation-box:hover {
        box-shadow: 0 4px 12px rgba(230, 126, 34, 0.15);
    }
    
    /* Headers des zones */
    .zone-header {
        font-size: 0.85rem;
        font-weight: 600;
        color: #666;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Textarea style DeepL */
    .stTextArea textarea {
        font-size: 1rem;
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
        resize: none;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    
    .stTextArea textarea:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Résultat traduction */
    .traduction-result {
        font-size: 1.1rem;
        color: #2c3e50;
        line-height: 1.6;
        padding: 0.5rem 0;
    }
    
    /* Audio player moderne */
    audio {
        width: 100%;
        margin: 1rem 0;
        border-radius: 8px;
        height: 40px;
    }
    
    /* Bouton langue */
    .stSelectbox > div > div {
        border: 2px solid #27AE60;
        border-radius: 10px;
        background: white;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #E67E22 0%, #C0392B 50%, #27AE60 100%);
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFF7EC 0%, #FFE8D6 100%);
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #E67E22;
        font-size: 0.85rem;
        margin: 1rem 0;
    }
    
    /* Badge type */
    .type-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        background: linear-gradient(135deg, #E67E22 0%, #C0392B 100%);
        color: white;
        margin-bottom: 0.8rem;
    }
    
    /* Stats footer */
    .stats-container {
        margin-top: 2rem;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .logo-header img {
            width: 100px;
        }
        .main-title {
            font-size: 1.5rem;
        }
        .translation-box {
            min-height: 180px;
        }
    }
    
    /* Masquer éléments Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# FONCTION AUDIO OPTIMISÉE SAFARI iOS
# =========================================================

def afficher_audio_local(chemin_audio, audio_id="default"):
    """Affiche un fichier audio local - OPTIMISÉ POUR SAFARI iOS"""
    if not chemin_audio:
        return False
    
    if not Path(chemin_audio).exists():
        return False
    
    try:
        with open(chemin_audio, 'rb') as audio_file:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
        
        import time
        timestamp = int(time.time() * 1000)
        unique_id = f"audio_{audio_id.replace(' ', '_')}_{timestamp}"
        
        audio_html = f'''
        <div style="margin: 10px 0;" key="{unique_id}">
            <audio 
                id="{unique_id}"
                controls 
                controlslist="nodownload"
                preload="auto"
                playsinline
                webkit-playsinline
                x-webkit-airplay="allow"
                style="width: 100%; max-width: 500px; height: 40px;"
            >
                <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>
        
        <script>
        (function() {{
            document.querySelectorAll('audio').forEach(function(oldAudio) {{
                if (oldAudio.id !== '{unique_id}') {{
                    oldAudio.pause();
                    oldAudio.src = '';
                }}
            }});
            
            setTimeout(function() {{
                const audio = document.getElementById('{unique_id}');
                if (audio) {{
                    audio.setAttribute('playsinline', '');
                    audio.setAttribute('webkit-playsinline', '');
                    audio.load();
                }}
            }}, 50);
        }})();
        </script>
        '''
        
        st.markdown(audio_html, unsafe_allow_html=True)
        return True
        
    except Exception as e:
        return False

# =========================================================
# CHARGEMENT DU CORPUS
# =========================================================

@st.cache_data
def charger_corpus():
    """Charge le corpus JSON"""
    try:
        with open('corpus.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("❌ Fichier corpus.json non trouvé")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
        st.stop()

corpus = charger_corpus()

# =========================================================
# CONFIGURATION DES LANGUES
# =========================================================

LANGUES_INFO = {
    'eton': {
        'nom_affichage': '🇨🇲 Eton',
        'nom_court': 'Eton',
        'emoji': '🇨🇲'
    },
    'bamoun': {
        'nom_affichage': '🇨🇲 Bamoun',
        'nom_court': 'Bamoun',
        'emoji': '🇨🇲'
    },
    'fufulde': {
        'nom_affichage': '🇨🇲 Fufulde',
        'nom_court': 'Fulfulde',
        'emoji': '🇨🇲'
    },
    'douala': {
        'nom_affichage': '🇨🇲 Douala',
        'nom_court': 'Duálá',
        'emoji': '🇨🇲'
    }
}

# =========================================================
# FONCTIONS DE RECHERCHE
# =========================================================

def normaliser_pour_recherche(texte):
    """Normalise le texte pour comparaison"""
    import string
    import unicodedata
    
    if not texte:
        return ""
    
    texte = texte.lower().strip()
    texte = texte.translate(str.maketrans('', '', string.punctuation))
    texte = ' '.join(texte.split())
    texte = ''.join(c for c in unicodedata.normalize('NFD', texte)
                   if unicodedata.category(c) != 'Mn')
    
    return texte

def rechercher_mot(texte_francais, langue_cible):
    """Recherche un mot dans le corpus"""
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
        
        return {
            'trouve': False,
            'traduction': '',
            'audio_url': '',
            'type': '',
            'autres_langues': {}
        }
    except Exception as e:
        return {
            'trouve': False,
            'traduction': '',
            'audio_url': '',
            'type': '',
            'autres_langues': {}
        }

def trouver_suggestions(texte_francais, max_suggestions=3):
    """Trouve des suggestions"""
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
    """Extrait le vocabulaire français disponible groupé par langue"""
    vocab = {'eton': set(), 'bamoun': set(), 'fufulde': set(), 'douala': set()}
    
    for item in corpus.get('items', []):
        mot_fr = item.get('francais', '').strip()
        if mot_fr:
            for lang in vocab.keys():
                if lang in item.get('traductions', {}):
                    vocab[lang].add(mot_fr)
    
    return {lang: sorted(list(mots)) for lang, mots in vocab.items()}

# =========================================================
# SIDEBAR - VOCABULAIRE DISPONIBLE
# =========================================================

with st.sidebar:
    st.markdown("### 📚 Vocabulaire du prototype")
    
    vocabulaire = get_vocabulaire_par_langue()
    
    # Sélection de langue pour voir le vocabulaire
    langue_vocab = st.selectbox(
        "Voir les mots disponibles en :",
        options=['Eton', 'Bamoun', 'Fulfulde', 'Douala'],
        key="langue_sidebar"
    )
    
    # Mapper le nom affiché au code
    lang_map = {'Eton': 'eton', 'Bamoun': 'bamoun', 'Fulfulde': 'fufulde', 'Douala': 'douala'}
    lang_code_sidebar = lang_map[langue_vocab]
    
    mots_langue = vocabulaire.get(lang_code_sidebar, [])
    st.metric("Mots français disponibles", len(mots_langue))
    
    # Recherche dans le vocabulaire
    recherche = st.text_input("🔍 Rechercher un mot :", key="recherche_vocab")
    
    if recherche:
        mots_filtres = [m for m in mots_langue if recherche.lower() in m.lower()]
        if mots_filtres:
            st.success(f"✅ {len(mots_filtres)} mot(s) trouvé(s)")
            # Afficher dans un container scrollable
            with st.container():
                for mot in mots_filtres[:50]:  # Limiter à 50 pour la performance
                    st.caption(f"• {mot}")
                if len(mots_filtres) > 50:
                    st.caption(f"... et {len(mots_filtres) - 50} autres")
        else:
            st.warning("❌ Aucun mot trouvé")
    else:
        # Afficher tous les mots dans un container scrollable
        with st.container():
            st.caption("**Tous les mots disponibles :**")
            for mot in mots_langue[:100]:  # Limiter à 100
                st.caption(f"• {mot}")
            if len(mots_langue) > 100:
                st.caption(f"... et {len(mots_langue) - 100} autres mots")
    
    st.markdown("---")
    
    # Stats globales
    st.markdown("### 📊 Statistiques")
    stats = corpus.get('statistiques', {})
    st.metric("Total mots", stats.get('total_items', 0))
    
    for lang, info in LANGUES_INFO.items():
        nb_mots = len(vocabulaire.get(lang, []))
        st.caption(f"{info['emoji']} {info['nom_court']}: {nb_mots} mots")
    
    st.markdown("---")
    st.caption("© 2025 Les Langues de Chez Nous")
    st.caption("Prototype MVP")

# =========================================================
# HEADER AVEC LOGO
# =========================================================

logo_base64 = get_logo_base64()
if logo_base64:
    st.markdown(f'''
    <div class="logo-header">
        <img src="data:image/png;base64,{logo_base64}" alt="Les Langues de Chez Nous">
    </div>
    ''', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Traducteur Français - Langues Africaines</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Prototype MVP · Eton, Bamoun, Fulfulde, Douala · avec audios authentiques</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# INTERFACE PRINCIPALE - STYLE DEEPL
# =========================================================

# Sélection langue cible (en haut, style DeepL)
col_lang1, col_lang2, col_lang3 = st.columns([2, 1, 2])

with col_lang1:
    st.markdown('<div class="zone-header">🇫🇷 Français</div>', unsafe_allow_html=True)

with col_lang3:
    langues_codes = ['eton', 'bamoun', 'fufulde', 'douala']
    langues_options = [LANGUES_INFO[lang]['nom_affichage'] for lang in langues_codes]
    
    langue_selectionnee = st.selectbox(
        "Langue cible",
        options=langues_options,
        index=0,
        label_visibility="collapsed"
    )
    
    # Récupération du code langue
    langue_code = langues_codes[0]
    for i, option in enumerate(langues_options):
        if option == langue_selectionnee:
            langue_code = langues_codes[i]
            break

# Zones de traduction côte à côte (style DeepL)
col_source, col_arrow, col_target = st.columns([5, 1, 5])

with col_source:
    # Zone source avec style personnalisé
    st.markdown('<div class="translation-box">', unsafe_allow_html=True)
    texte_francais = st.text_area(
        "Source",
        height=200,
        placeholder="Tapez un mot ou une phrase en français...",
        key="input_francais",
        label_visibility="collapsed"
    )
    if texte_francais:
        st.caption(f"📝 {len(texte_francais)} caractères")
    st.markdown('</div>', unsafe_allow_html=True)

with col_arrow:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 1.5rem;'>→</div>", unsafe_allow_html=True)

with col_target:
    # Zone cible
    st.markdown('<div class="translation-box">', unsafe_allow_html=True)
    
    if texte_francais:
        resultat = rechercher_mot(texte_francais, langue_code)
        
        if resultat['trouve']:
            # Badge type
            type_label = "📖 Mot" if resultat['type'] == 'mot' else "💬 Phrase"
            st.markdown(f'<div class="type-badge">{type_label}</div>', unsafe_allow_html=True)
            
            # Traduction
            st.markdown(f'<div class="traduction-result">{resultat["traduction"]}</div>', unsafe_allow_html=True)
            
        else:
            st.warning(f"❌ « {texte_francais} » non trouvé")
            suggestions = trouver_suggestions(texte_francais)
            if suggestions:
                st.info("💡 Suggestions : " + ", ".join(suggestions[:3]))
    else:
        st.markdown(
            '<div style="color: #999; padding: 2rem 0; text-align: center;">La traduction apparaîtra ici...</div>',
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# AUDIO ET AUTRES LANGUES (sous les zones)
# =========================================================

if texte_francais:
    resultat = rechercher_mot(texte_francais, langue_code)
    
    if resultat['trouve']:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Audio
        if resultat['audio_url']:
            st.markdown("### 🔊 Prononciation authentique")
            
            st.markdown("""
            <div class="info-box">
            📱 Appuyez sur ▶️ pour écouter la prononciation. Langue à tons – écoutez attentivement !
            </div>
            """, unsafe_allow_html=True)
            
            audio_id = f"{langue_code}_{texte_francais[:20]}"
            if afficher_audio_local(resultat['audio_url'], audio_id):
                st.caption("✅ Audio chargé")
        
        # Autres langues
        if resultat['autres_langues']:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🌐 Voir dans d'autres langues"):
                for lang_code_autre, data in resultat['autres_langues'].items():
                    st.markdown(f"**{LANGUES_INFO[lang_code_autre]['nom_court']}** : {data.get('texte', '')}")
                    
                    if data.get('audio_url'):
                        audio_id_autre = f"{lang_code_autre}_{texte_francais[:20]}"
                        afficher_audio_local(data['audio_url'], audio_id_autre)
                    
                    st.markdown("---")

# =========================================================
# FOOTER AVEC STATS
# =========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown('<div class="stats-container">', unsafe_allow_html=True)

stats = corpus.get('statistiques', {})
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📚 Total", stats.get('total_items', 0))
with col2:
    st.metric("🇨🇲 Eton", stats.get('eton', 0))
with col3:
    st.metric("🇨🇲 Bamoun", stats.get('bamoun', 0))
with col4:
    st.metric("🇨🇲 Fulfulde", stats.get('fufulde', 0))
with col5:
    st.metric("🇨🇲 Duálá", stats.get('douala', 0))

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<p style="text-align: center; color: #999; font-size: 0.85rem;">Prototype MVP – Données limitées à un sous-ensemble de mots et phrases</p>',
    unsafe_allow_html=True
)
