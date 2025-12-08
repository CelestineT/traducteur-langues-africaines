"""
PROTOTYPE TRADUCTEUR - VERSION MOBILE-OPTIMIZED
================================================
Support : Eton, Bamoun, Fufulde, Douala
Audios : Fichiers locaux (audios/*.mp3) optimisés pour Safari iOS et tous mobiles

LANCEMENT :
streamlit run prototype_traducteur_v3.py
"""

import streamlit as st
import json
from pathlib import Path
import difflib
import base64

# ============================================
# CONFIGURATION DE LA PAGE
# ============================================

st.set_page_config(
    page_title="Traducteur Français - Langues Africaines",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# FONCTION AUDIO OPTIMISÉE POUR MOBILE
# ============================================

def afficher_audio_mobile(chemin_audio):
    """
    Affiche un fichier audio avec support complet mobile (Safari iOS inclus)
    Utilise un player HTML custom avec tous les attributs nécessaires
    """
    if not chemin_audio:
        return False
    
    # Vérifier que le fichier existe
    if not Path(chemin_audio).exists():
        st.warning(f"⚠️ Audio non disponible")
        return False
    
    try:
        # Lire le fichier audio et l'encoder en base64
        with open(chemin_audio, 'rb') as audio_file:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
        
        # Player HTML optimisé pour Safari iOS et tous les mobiles
        audio_html = f'''
        <div style="margin: 10px 0;">
            <audio 
                controls 
                controlslist="nodownload"
                preload="auto"
                playsinline
                webkit-playsinline
                x-webkit-airplay="allow"
                style="width: 100%; max-width: 400px; height: 40px;"
            >
                <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Votre navigateur ne supporte pas la lecture audio.
            </audio>
        </div>
        
        <script>
        // Script pour forcer le chargement sur mobile
        (function() {{
            const audios = document.querySelectorAll('audio');
            audios.forEach(audio => {{
                // Attributs pour iOS
                audio.setAttribute('playsinline', '');
                audio.setAttribute('webkit-playsinline', '');
                
                // Force le preload sur mobile
                if (/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)) {{
                    audio.load();
                    
                    // Gestionnaire d'erreur
                    audio.addEventListener('error', function(e) {{
                        console.log('Erreur audio:', e);
                    }});
                    
                    // Log quand l'audio peut être joué
                    audio.addEventListener('canplay', function() {{
                        console.log('Audio prêt à être joué');
                    }});
                }}
            }});
        }})();
        </script>
        '''
        
        st.markdown(audio_html, unsafe_allow_html=True)
        return True
        
    except Exception as e:
        st.error(f"❌ Erreur de chargement : {str(e)[:50]}")
        return False

# ============================================
# STYLES CSS OPTIMISÉS
# ============================================

st.markdown("""
<style>
    /* Style général */
    .main {
        padding: 1.5rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Titre principal */
    .main-title {
        text-align: center;
        color: #0F4C81;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }
    
    /* Sous-titre */
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 2rem;
        line-height: 1.4;
    }
    
    /* Zone de texte */
    .stTextArea textarea {
        font-size: 1.1rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 15px;
    }
    
    /* Boutons */
    .stButton button {
        width: 100%;
        background-color: #0F4C81;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        background-color: #0D3D6B;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(15, 76, 129, 0.3);
    }
    
    /* Carte de résultat */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .result-word {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .result-lang {
        font-size: 1.1rem;
        opacity: 0.9;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Sélecteur de langue */
    .stRadio > div {
        display: flex;
        flex-direction: row;
        gap: 10px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .stRadio > div > label {
        background-color: #f8f9fa;
        padding: 10px 20px;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .stRadio > div > label:hover {
        border-color: #0F4C81;
        background-color: #e8f4f8;
    }
    
    /* Audio player custom */
    audio {
        border-radius: 8px;
        margin: 10px auto;
        display: block;
    }
    
    audio::-webkit-media-controls-panel {
        background-color: #f8f9fa;
    }
    
    /* Messages */
    .stWarning, .stError, .stSuccess {
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Responsive mobile */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.6rem;
        }
        
        .result-word {
            font-size: 2rem;
        }
        
        .stButton button {
            font-size: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CHARGEMENT DU CORPUS
# ============================================

@st.cache_data
def charger_corpus():
    """Charge le corpus depuis le fichier JSON"""
    chemins_possibles = [
        'corpus.json',
        Path('corpus.json'),
        Path(__file__).parent / 'corpus.json'
    ]
    
    for chemin in chemins_possibles:
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            continue
    
    st.error("❌ Fichier corpus.json non trouvé")
    return None

corpus = charger_corpus()

# ============================================
# INFORMATIONS SUR LES LANGUES
# ============================================

LANGUES_INFO = {
    'eton': {
        'nom_affichage': 'Eton 🇨🇲',
        'description': 'Langue bantoue du centre du Cameroun'
    },
    'bamoun': {
        'nom_affichage': 'Bamoun 🇨🇲',
        'description': 'Langue de l\'Ouest Cameroun avec écriture propre'
    },
    'fufulde': {
        'nom_affichage': 'Fulfulde 🇨🇲',
        'description': 'Langue peule parlée au Nord Cameroun'
    },
    'douala': {
        'nom_affichage': 'Duálá 🇨🇲',
        'description': 'Langue du littoral camerounais'
    }
}

# ============================================
# FONCTIONS DE RECHERCHE
# ============================================

def normaliser_pour_recherche(texte):
    """Normalise le texte pour la recherche"""
    if not texte:
        return ""
    return texte.lower().strip()

def rechercher_mot(texte_francais, langue_cible):
    """Recherche un mot dans le corpus"""
    if not corpus:
        return {
            'trouve': False,
            'traduction': '',
            'audio_url': '',
            'type': '',
            'autres_langues': {}
        }
    
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
    """Trouve des suggestions de mots similaires"""
    if not corpus:
        return []
    
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

# En-tête
st.markdown("""
<div class="main-title">
    🌍 Traducteur Français -<br>
    Langues Africaines
</div>
<div class="subtitle">
    Prototype MVP - Eton, Bamoun, Fulfulde, Douala<br>
    avec audios authentiques
</div>
""", unsafe_allow_html=True)

# Sélection de la langue
langues_codes = ['eton', 'bamoun', 'fufulde', 'douala']
langues_options = [LANGUES_INFO[lang]['nom_affichage'] for lang in langues_codes]

col1, col2 = st.columns([3, 1])

with col1:
    langue_selectionnee = st.radio(
        "Langue cible :",
        langues_options,
        horizontal=True,
        label_visibility="collapsed"
    )

# Obtenir le code de la langue sélectionnée
langue_code = langues_codes[0]
for i, option in enumerate(langues_options):
    if option == langue_selectionnee:
        langue_code = langues_codes[i]
        break

# Zone de saisie
texte_francais = st.text_area(
    "Entrez un mot ou une phrase en français :",
    height=100,
    placeholder="Ex: bonjour, merci, comment vas-tu...",
    label_visibility="collapsed"
)

# Bouton de traduction
if st.button("🔍 Traduire", use_container_width=True):
    if texte_francais.strip():
        resultat = rechercher_mot(texte_francais, langue_code)
        
        if resultat['trouve']:
            # Affichage du résultat
            st.markdown(f"""
            <div class="result-card">
                <div class="result-word">{resultat['traduction']}</div>
                <div class="result-lang">{langue_selectionnee}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Audio
            if resultat['audio_url']:
                st.markdown("### 🔊 Prononciation authentique")
                afficher_audio_mobile(resultat['audio_url'])
            
            # Autres langues
            if resultat['autres_langues']:
                st.markdown("---")
                st.markdown("### 🌐 Dans d'autres langues")
                
                for lang_code, traduction_data in resultat['autres_langues'].items():
                    with st.expander(f"{LANGUES_INFO[lang_code]['nom_affichage']} : {traduction_data.get('texte', '')}"):
                        if traduction_data.get('audio_url'):
                            afficher_audio_mobile(traduction_data['audio_url'])
        
        else:
            st.warning(f"❌ Aucune traduction trouvée pour « {texte_francais} »")
            
            suggestions = trouver_suggestions(texte_francais)
            if suggestions:
                st.info(f"💡 Suggestions : {', '.join(suggestions)}")
    else:
        st.warning("⚠️ Veuillez entrer un mot ou une phrase")

# Pied de page
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>🎯 Prototype MVP • 937 mots disponibles</p>
    <p>🌍 Préservation des langues africaines • Audios authentiques</p>
</div>
""", unsafe_allow_html=True)
