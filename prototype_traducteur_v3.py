"""
PROTOTYPE TRADUCTEUR - VERSION AVEC AUDIOS LOCAUX
==================================================
Support : Eton, Bamoun, Fufulde, Douala
Audios : Fichiers locaux (audios/*.mp3) pour déploiement GitHub

LANCEMENT :
streamlit run prototype_traducteur_local.py
"""

import streamlit as st
import json
from pathlib import Path
import difflib
import base64

# ============================================
# CONFIGURATION DE LA PAGE
# ============================================

# Charger le logo
def get_logo_base64():
    """Convertit le logo en base64 pour l'affichage"""
    try:
        with open("assets/logo.png", "rb") as f:
            logo_bytes = f.read()
            return base64.b64encode(logo_bytes).decode()
    except:
        return None

st.set_page_config(
    page_title="Les Langues de Chez Nous - Traducteur",
    page_icon="assets/logo.png" if Path("assets/logo.png").exists() else "🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# FONCTION AUDIO LOCALE
# ============================================

def afficher_audio_local(chemin_audio, audio_id="default"):
    """Affiche un fichier audio local - OPTIMISÉ POUR SAFARI iOS"""
    if not chemin_audio:
        return False
    
    # Vérifier que le fichier existe
    if not Path(chemin_audio).exists():
        st.warning(f"⚠️ Fichier audio non trouvé : {chemin_audio}")
        return False
    
    try:
        # Lire le fichier audio et l'encoder en base64
        with open(chemin_audio, 'rb') as audio_file:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
        
        # ID unique avec timestamp pour forcer un nouveau rendu
        import time
        timestamp = int(time.time() * 1000)
        unique_id = f"audio_{audio_id.replace(' ', '_')}_{timestamp}"
        
        # Player HTML optimisé pour Safari iOS
        audio_html = f'''
        <div style="margin: 10px 0;" key="{unique_id}">
            <audio 
                id="{unique_id}"
                key="{unique_id}"
                controls 
                controlslist="nodownload"
                preload="auto"
                playsinline
                webkit-playsinline
                x-webkit-airplay="allow"
                style="width: 100%; max-width: 500px; height: 54px; display: block; margin: 0 auto;"
            >
                <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Votre navigateur ne supporte pas la lecture audio.
            </audio>
        </div>
        
        <script>
        (function() {{
            // Nettoyer les anciens audios
            document.querySelectorAll('audio').forEach(function(oldAudio) {{
                if (oldAudio.id !== '{unique_id}') {{
                    oldAudio.pause();
                    oldAudio.src = '';
                }}
            }});
            
            // Configurer le nouvel audio
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
        st.error(f"❌ Impossible de charger l'audio")
        return False

# ============================================
# STYLES CSS PERSONNALISÉS
# ============================================

st.markdown("""
<style>
    /* Fond dégradé subtil avec les couleurs du logo */
    .main {
        padding: 1.5rem;
        max-width: 800px;
        margin: 0 auto;
        background: linear-gradient(135deg, #FFF5E6 0%, #FFFFFF 50%, #E8F5E9 100%);
        min-height: 100vh;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem 0;
    }
    
    .logo-container img {
        width: 150px;
        height: auto;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
    }
    
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #E67E22 0%, #C0392B 50%, #27AE60 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1rem;
        margin-bottom: 2.5rem;
        line-height: 1.5;
    }
    
    /* Zone de texte avec bordure colorée */
    .stTextArea textarea {
        font-size: 1.1rem;
        border-radius: 10px;
        border: 2px solid #E67E22;
        padding: 15px;
        transition: all 0.3s;
    }
    
    .stTextArea textarea:focus {
        border-color: #C0392B;
        box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.1);
    }
    
    /* Traduction avec couleurs africaines */
    .traduction-texte {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 20px 0;
        padding: 25px;
        background: linear-gradient(135deg, #FFF3E0 0%, #FFEBEE 100%);
        border-radius: 15px;
        text-align: center;
        border-left: 5px solid #E67E22;
        box-shadow: 0 4px 12px rgba(230, 126, 34, 0.15);
    }
    
    /* Audio player stylisé */
    audio {
        width: 100%;
        margin: 15px 0;
        border-radius: 8px;
    }
    
    /* Info box avec couleur africaine */
    .info-box {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #E67E22;
        font-size: 0.9rem;
    }
    
    /* Bouton Traduire avec couleurs du logo */
    .stButton button {
        background: linear-gradient(135deg, #E67E22 0%, #C0392B 100%);
        color: white;
        border: none;
        padding: 12px 32px;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(230, 126, 34, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(230, 126, 34, 0.4);
    }
    
    /* Selectbox personnalisé */
    .stSelectbox > div > div {
        border: 2px solid #27AE60;
        border-radius: 10px;
    }
    
    /* Progress bar aux couleurs africaines */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #E67E22 0%, #C0392B 50%, #27AE60 100%);
    }
    
    /* Responsive mobile */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.6rem;
        }
        .subtitle {
            font-size: 0.9rem;
        }
        .traduction-texte {
            font-size: 1.4rem;
            padding: 15px;
        }
        .logo-container img {
            width: 120px;
        }
    }
    
    /* Masquer les éléments Streamlit par défaut */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)
        border-left: 4px solid #2196F3;
        font-size: 0.9rem;
    }
    
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.6rem;
        }
        .subtitle {
            font-size: 0.9rem;
        }
        .traduction-texte {
            font-size: 1.4rem;
            padding: 15px;
        }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================
# CHARGEMENT DU CORPUS
# ============================================

@st.cache_data
def charger_corpus():
    """Charge le corpus JSON"""
    try:
        with open('corpus.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("❌ **Fichier corpus.json non trouvé**")
        st.info("""
        📝 **Instructions :**
        1. Placez le fichier `corpus.json` dans le même dossier que ce script
        2. Utilisez le script `telecharger_audios.py` pour télécharger les audios
        3. Relancez l'application
        """)
        st.stop()
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
        st.stop()

corpus = charger_corpus()

# ============================================
# CONFIGURATION DES LANGUES
# ============================================

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
        'nom_court': 'Fufuldé',
        'emoji': '🇨🇲'
    },
    'douala': {
        'nom_affichage': '🇨🇲 Douala',
        'nom_court': 'Douala',
        'emoji': '🇨🇲'
    }
}

# ============================================
# FONCTIONS DE RECHERCHE
# ============================================

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

# ============================================
# INTERFACE UTILISATEUR
# ============================================

# LOGO
logo_base64 = get_logo_base64()
if logo_base64:
    st.markdown(f'''
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}" alt="Les Langues de Chez Nous">
    </div>
    ''', unsafe_allow_html=True)

# HEADER
st.markdown(
    '<h1 class="main-title">Traducteur Français - Langues Africaines</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="subtitle">Prototype MVP - Eton, Bamoun, Fufulde, Douala<br>avec audios authentiques</p>',
    unsafe_allow_html=True
)

# INPUT FRANÇAIS
st.markdown("### 🇫🇷 Français")

texte_francais = st.text_area(
    "Entrez un mot ou une phrase",
    height=150,
    placeholder="Exemple : bonjour, bonne nuit, merci...",
    key="input_francais",
    label_visibility="collapsed"
)

if texte_francais:
    st.caption(f"📝 {len(texte_francais)} caractères")

st.markdown("---")

# LANGUE CIBLE
st.markdown("### Langue cible")

langues_codes = ['eton', 'bamoun', 'fufulde', 'douala']
langues_options = [LANGUES_INFO[lang]['nom_affichage'] for lang in langues_codes]

langue_selectionnee = st.selectbox(
    "Choisissez la langue",
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

# Statistiques
try:
    stats = corpus.get('statistiques', {})
    stats_langue = stats.get('mots_par_langue', {}).get(langue_code, 0)
    max_mots = 150 if langue_code != 'fufulde' else 100
    progression = min(stats_langue / max_mots, 1.0) if max_mots > 0 else 0
    
    st.progress(progression)
    st.caption(f"📊 {stats_langue} mots disponibles")
except:
    st.caption("📊 Statistiques non disponibles")

st.markdown("---")

# AFFICHAGE TRADUCTION
if texte_francais:
    resultat = rechercher_mot(texte_francais, langue_code)
    
    if resultat['trouve']:
        # Badge type
        type_badge = "📖 Mot" if resultat['type'] == 'mot' else "💬 Phrase"
        st.caption(type_badge)
        
        # Traduction
        st.markdown(
            f'<div class="traduction-texte">{resultat["traduction"]}</div>',
            unsafe_allow_html=True
        )
        
        # AUDIO LOCAL
        if resultat['audio_url']:
            st.markdown("### 🔊 Prononciation")
            
            st.markdown("""
            <div class="info-box">
            📱 Appuyez sur ▶️ pour écouter la prononciation authentique.
            </div>
            """, unsafe_allow_html=True)
            
            # Afficher l'audio local avec ID unique
            audio_id = f"{langue_code}_{texte_francais[:20]}"
            if afficher_audio_local(resultat['audio_url'], audio_id):
                st.caption("✅ Audio chargé")
            
            st.info("🎯 Langue à tons - Écoutez attentivement la prononciation")
        else:
            st.warning("⚠️ Audio non disponible pour ce mot")
        
        # Autres langues
        if resultat['autres_langues']:
            with st.expander("🌐 Voir dans d'autres langues"):
                for lang_code_autre, data in resultat['autres_langues'].items():
                    st.markdown(f"**{LANGUES_INFO[lang_code_autre]['nom_court']}** : {data.get('texte', '')}")
                    
                    if data.get('audio_url'):
                        audio_id_autre = f"{lang_code_autre}_{texte_francais[:20]}"
                        afficher_audio_local(data['audio_url'], audio_id_autre)
                    
                    st.markdown("---")
    
    else:
        # Mot non trouvé
        st.error(f"❌ « {texte_francais} » non trouvé dans le corpus")
        
        suggestions = trouver_suggestions(texte_francais)
        if suggestions:
            st.info("💡 **Vouliez-vous dire :**")
            cols = st.columns(min(len(suggestions), 3))
            for i, suggestion in enumerate(suggestions):
                with cols[i % 3]:
                    if st.button(suggestion, key=f"sugg_{i}"):
                        st.session_state.input_francais = suggestion
                        st.rerun()
        else:
            st.info("💡 Ce mot sera ajouté dans les prochaines versions")
else:
    st.markdown(
        '<div style="text-align: center; color: #999; padding: 40px; font-size: 1.1rem;">⬆️ Entrez un mot en français ci-dessus</div>',
        unsafe_allow_html=True
    )

# FOOTER
st.markdown("---")

# Statistiques globales
try:
    stats = corpus.get('statistiques', {})
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total", stats.get('total_items', 0))
    with col2:
        st.metric("Eton", stats.get('eton', 0))
    with col3:
        st.metric("Bamoun", stats.get('bamoun', 0))
    with col4:
        st.metric("Fufulde", stats.get('fufulde', 0))
    with col5:
        st.metric("Douala", stats.get('douala', 0))
except:
    pass

st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #999; font-size: 0.9rem;">© 2025 Traducteur Africain | Prototype MVP v4 Local</p>',
    unsafe_allow_html=True
)

# Script pour mobile
st.markdown("""
<script>
if (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
    setTimeout(function() {
        document.querySelectorAll('audio').forEach(function(audio) {
            audio.setAttribute('playsinline', '');
            audio.setAttribute('webkit-playsinline', '');
            audio.setAttribute('preload', 'auto');
        });
    }, 500);
}
</script>
""", unsafe_allow_html=True)
