"""
PROTOTYPE TRADUCTEUR - VERSION MOBILE/WEB
===========================================
Support : Eton, Bamoun, Fufulde, Douala
Optimisé pour mobile et déploiement
"""

import streamlit as st
import json
from pathlib import Path
import difflib
import base64
import os

# ============================================
# CONFIGURATION DE LA PAGE (MOBILE FIRST)
# ============================================

st.set_page_config(
    page_title="Traducteur Africain - Langues Africaines",
    page_icon="🌍",
    layout="wide",  # Changé pour mobile
    initial_sidebar_state="collapsed"
)

# ============================================
# CONFIGURATION DES CHEMINS AUDIO
# ============================================

# Déterminer si on est en local ou en ligne
def est_en_ligne():
    """Détecte si l'app est déployée en ligne"""
    try:
        # Streamlit Cloud met cette variable d'environnement
        return os.environ.get('STREAMLIT_SERVER_RUNNING_ON_CLOUD', 'false').lower() == 'true'
    except:
        return False

# URLs des audios sur GitHub (VOUS DEVEZ METTRE VOS VRAIS URLS ICI)
GITHUB_AUDIO_BASE_URL = "https://raw.githubusercontent.com/[VOTRE_USERNAME]/[VOTRE_REPO]/main/audios/"

# Dictionnaire de mapping audio local -> URL GitHub
AUDIO_MAPPING = {
    # Exemple : "audios/eton_bonjour.mp3": f"{GITHUB_AUDIO_BASE_URL}eton_bonjour.mp3"
    # Vous devrez remplir ce dictionnaire avec tous vos fichiers
}

def get_audio_path(audio_filename):
    """Retourne le chemin/URL adapté selon l'environnement"""
    if not audio_filename:
        return None
    
    # Si c'est déjà une URL complète
    if audio_filename.startswith(('http://', 'https://')):
        return audio_filename
    
    # Si en ligne, utiliser GitHub
    if est_en_ligne():
        # Extraire le nom de fichier du chemin
        filename = os.path.basename(audio_filename)
        return f"{GITHUB_AUDIO_BASE_URL}{filename}"
    
    # Sinon, utiliser le chemin local
    return audio_filename

# ============================================
# FONCTION AUDIO UNIVERSELLE
# ============================================

def afficher_audio(audio_path):
    """Affiche un audio quel que soit l'environnement"""
    if not audio_path:
        return False
    
    try:
        # Si c'est une URL web
        if audio_path.startswith(('http://', 'https://')):
            st.audio(audio_path, format='audio/mp3')
            return True
        # Si c'est un fichier local
        elif Path(audio_path).exists():
            st.audio(audio_path, format='audio/mp3')
            return True
        else:
            # Essayer avec le chemin relatif
            relative_path = f"audios/{os.path.basename(audio_path)}"
            if Path(relative_path).exists():
                st.audio(relative_path, format='audio/mp3')
                return True
            else:
                st.warning(f"Audio non trouvé: {os.path.basename(audio_path)}")
                return False
    except Exception as e:
        st.error(f"Erreur audio: {str(e)}")
        return False

# ============================================
# STYLES CSS MOBILE
# ============================================

st.markdown("""
<style>
    /* Base mobile-first */
    .main {
        padding: 1rem;
        max-width: 100%;
    }
    
    .main-title {
        text-align: center;
        color: #0F4C81;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        line-height: 1.4;
    }
    
    /* Input adapté mobile */
    .stTextArea textarea {
        font-size: 1rem;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        min-height: 120px;
    }
    
    .traduction-texte {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 15px 0;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 8px;
        text-align: center;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Audio full width */
    audio {
        width: 100%;
        margin: 10px 0;
        border-radius: 6px;
    }
    
    /* Boutons mobiles */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 10px;
        font-size: 0.9rem;
    }
    
    /* Métriques responsive */
    .stMetric {
        font-size: 0.8rem;
    }
    
    /* Cacher éléments sur mobile */
    @media (max-width: 768px) {
        .hide-on-mobile {
            display: none;
        }
        
        .main-title {
            font-size: 1.4rem;
        }
        
        .traduction-texte {
            font-size: 1.2rem;
            padding: 12px;
        }
        
        [data-testid="stExpander"] {
            font-size: 0.9rem;
        }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# ============================================
# CHARGEMENT ET PRÉPARATION DU CORPUS
# ============================================

@st.cache_data
def charger_et_preparer_corpus():
    """Charge et prépare le corpus pour mobile"""
    try:
        with open('corpus.json', 'r', encoding='utf-8') as f:
            corpus_data = json.load(f)
        
        # Convertir les chemins audio si nécessaire
        for item in corpus_data.get('items', []):
            for lang in ['eton', 'bamoun', 'fufulde', 'douala']:
                if lang in item.get('traductions', {}):
                    audio_path = item['traductions'][lang].get('audio_url', '')
                    if audio_path:
                        # Mettre à jour avec le chemin adapté
                        item['traductions'][lang]['audio_url'] = get_audio_path(audio_path)
        
        return corpus_data
    except FileNotFoundError:
        st.error("❌ **Fichier corpus.json non trouvé**")
        st.info("""
        📝 **Instructions pour mobile :**
        1. Assurez-vous que corpus.json est dans le même dossier
        2. Les audios doivent être sur GitHub
        3. Vérifiez votre connexion internet
        """)
        st.stop()
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
        st.stop()

corpus = charger_et_preparer_corpus()

# ============================================
# CONFIGURATION DES LANGUES
# ============================================

LANGUES_INFO = {
    'eton': {'nom_affichage': '🇨🇲 Eton', 'nom_court': 'Eton'},
    'bamoun': {'nom_affichage': '🇨🇲 Bamoun', 'nom_court': 'Bamoun'},
    'fufulde': {'nom_affichage': '🇨🇲 Fufulde', 'nom_court': 'Fufuldé'},
    'douala': {'nom_affichage': '🇨🇲 Douala', 'nom_court': 'Douala'}
}

# ============================================
# FONCTIONS DE RECHERCHE (inchangées)
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
        st.error(f"Erreur recherche: {e}")
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
            if ratio > 0.5:  # Seuil plus bas pour mobile
                suggestions.append((mot_original, ratio))
        
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in suggestions[:max_suggestions]]
    except:
        return []

# ============================================
# INTERFACE UTILISATEUR MOBILE
# ============================================

# HEADER SIMPLIFIÉ
st.markdown(
    '<h1 class="main-title">🌍 Traducteur Français<br>→ Langues Africaines</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="subtitle">Eton • Bamoun • Fufulde • Douala<br><small>Avec prononciation audio</small></p>',
    unsafe_allow_html=True
)

# SECTION INPUT - Optimisée mobile
col_input, col_langue = st.columns([2, 1])

with col_input:
    st.markdown("**🇫🇷 Mot/phrase en français**")
    texte_francais = st.text_area(
        "",
        height=100,
        placeholder="Ex: bonjour, merci, comment ça va...",
        key="input_francais_mobile",
        label_visibility="collapsed"
    )

with col_langue:
    st.markdown("**🌍 Traduire en**")
    langue_selectionnee = st.selectbox(
        "",
        options=[LANGUES_INFO[lang]['nom_affichage'] for lang in LANGUES_INFO.keys()],
        index=0,
        label_visibility="collapsed"
    )

# Déterminer le code langue
langue_code = 'eton'
for code, info in LANGUES_INFO.items():
    if info['nom_affichage'] == langue_selectionnee:
        langue_code = code
        break

st.markdown("---")

# SECTION TRADUCTION
if texte_francais:
    with st.spinner("Recherche..."):
        resultat = rechercher_mot(texte_francais, langue_code)
    
    if resultat['trouve']:
        # Afficher la traduction
        st.markdown(f'<div class="traduction-texte">{resultat["traduction"]}</div>', unsafe_allow_html=True)
        
        # Type
        type_emoji = "📖" if resultat['type'] == 'mot' else "💬"
        st.caption(f"{type_emoji} {resultat['type'].capitalize()}")
        
        # AUDIO
        if resultat['audio_url']:
            st.markdown("**🔊 Prononciation**")
            
            # Note pour mobile
            st.markdown("""
            <div style="background: #e8f5e9; padding: 10px; border-radius: 8px; margin: 10px 0; font-size: 0.9rem;">
            📱 <b>Sur mobile :</b> Activez le son et appuyez sur ▶️
            </div>
            """, unsafe_allow_html=True)
            
            # Afficher l'audio
            if afficher_audio(resultat['audio_url']):
                st.caption("✅ Audio disponible")
            
            # Info sur les tons
            st.info("🎯 **Langue à tons** - Écoutez attentivement la mélodie")
        
        # Autres langues (expandable pour économiser l'espace)
        if resultat['autres_langues']:
            with st.expander(f"🌐 Voir dans {len(resultat['autres_langues'])} autres langues"):
                for lang_code_autre, data in resultat['autres_langues'].items():
                    st.markdown(f"**{LANGUES_INFO[lang_code_autre]['nom_court']}** : {data.get('texte', '')}")
                    if data.get('audio_url'):
                        afficher_audio(data['audio_url'])
                    st.markdown("---")
    
    else:
        # MOT NON TROUVÉ - Interface mobile-friendly
        st.error(f"❌ « {texte_francais} » non trouvé")
        
        suggestions = trouver_suggestions(texte_francais, max_suggestions=4)
        if suggestions:
            st.warning("**Suggestions :**")
            
            # Afficher les suggestions en grille 2x2 sur mobile
            cols = st.columns(2)
            for i, suggestion in enumerate(suggestions):
                with cols[i % 2]:
                    if st.button(
                        suggestion,
                        key=f"sugg_mob_{i}",
                        use_container_width=True
                    ):
                        st.session_state.input_francais_mobile = suggestion
                        st.rerun()
        else:
            st.info("✨ Ce mot sera ajouté prochainement")

else:
    # Écran d'accueil mobile
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; color: #666;">
        <div style="font-size: 4rem; margin-bottom: 20px;">🌍</div>
        <h3 style="color: #0F4C81;">Bienvenue !</h3>
        <p>Entrez un mot en français ci-dessus pour commencer la traduction.</p>
        <p><small>Essayez : "bonjour", "merci", "au revoir"</small></p>
    </div>
    """, unsafe_allow_html=True)

# FOOTER MOBILE
st.markdown("---")

# Statistiques simplifiées pour mobile
try:
    stats = corpus.get('statistiques', {})
    
    # Sur mobile, on montre moins d'infos
    cols = st.columns(4)
    with cols[0]:
        st.metric("Total", stats.get('total_items', 0))
    with cols[1]:
        st.metric("Eton", stats.get('mots_par_langue', {}).get('eton', 0))
    with cols[2]:
        st.metric("Bamoun", stats.get('mots_par_langue', {}).get('bamoun', 0))
    with cols[3]:
        st.metric("Fufulde", stats.get('mots_par_langue', {}).get('fufulde', 0))
except:
    pass

# Copyright
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.8rem; padding: 10px;">
© 2025 Traducteur Africain | Optimisé pour mobile
</div>
""", unsafe_allow_html=True)

# Script JavaScript pour mobile
st.markdown("""
<script>
// Détection mobile
function isMobile() {
    return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

// Optimiser les audios pour mobile
if (isMobile()) {
    document.addEventListener('DOMContentLoaded', function() {
        // Forcer les attributs mobile
        const audios = document.querySelectorAll('audio');
        audios.forEach(audio => {
            audio.setAttribute('playsinline', '');
            audio.setAttribute('webkit-playsinline', '');
            audio.setAttribute('preload', 'metadata');
            audio.setAttribute('controlslist', 'nodownload');
        });
        
        // Empêcher le zoom sur les inputs
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.style.fontSize = '16px'; // Prévenir le zoom iOS
        });
    });
}
</script>
""", unsafe_allow_html=True)