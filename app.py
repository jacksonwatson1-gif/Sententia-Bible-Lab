"""
Sententia Bible Lab
====================
A dual-mode Biblical research workstation spanning Discovery (age 8) to Scholar (graduate level).
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sententia Bible Lab",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# PALETTE CONSTANTS
# ─────────────────────────────────────────────
BIBLICAL_BLUE   = "#0038A8"
PURE_GOLD       = "#D4AF37"
TYRIAN_PURPLE   = "#66023C"
SCARLET         = "#B22222"
NAVY            = "#0A1628"
LIGHT_GOLD      = "#F5E17A"
CREAM           = "#FFF8DC"

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@300;400;600&display=swap');

/* ── Root reset ── */
html, body, [class*="css"] {{
    font-family: 'IBM Plex Mono', monospace;
    background-color: {BIBLICAL_BLUE};
    color: {PURE_GOLD};
}}

/* ── Main container ── */
.main .block-container {{
    background-color: {BIBLICAL_BLUE};
    padding-top: 1rem;
    max-width: 1400px;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {NAVY} 0%, {BIBLICAL_BLUE} 100%);
    border-right: 2px solid {PURE_GOLD};
}}
section[data-testid="stSidebar"] * {{
    color: {PURE_GOLD} !important;
    font-family: 'IBM Plex Mono', monospace !important;
}}

/* ── Title ── */
.sbl-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    color: {PURE_GOLD};
    text-shadow: 0 0 18px {PURE_GOLD}aa, 0 0 35px {PURE_GOLD}55;
    letter-spacing: 0.08em;
    margin-bottom: 0;
    line-height: 1;
}}
.sbl-subtitle {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: {LIGHT_GOLD};
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}}

/* ── Tab bar ── */
button[data-baseweb="tab"] {{
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    color: {LIGHT_GOLD} !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.1em;
}}
button[data-baseweb="tab"]:hover {{
    color: {PURE_GOLD} !important;
    text-shadow: 0 0 12px {PURE_GOLD}, 0 0 25px {PURE_GOLD}88;
    border-bottom: 2px solid {PURE_GOLD} !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {PURE_GOLD} !important;
    text-shadow: 0 0 14px {PURE_GOLD}, 0 0 30px {PURE_GOLD}99;
    border-bottom: 2px solid {PURE_GOLD} !important;
    background: {TYRIAN_PURPLE}44 !important;
}}

/* ── Cards ── */
.sbl-card {{
    background: linear-gradient(135deg, {NAVY}cc 0%, #001560cc 100%);
    border: 1px solid {PURE_GOLD}66;
    border-radius: 6px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 0 20px {PURE_GOLD}22;
}}
.sbl-card-scarlet {{
    border-color: {SCARLET};
    box-shadow: 0 0 20px {SCARLET}33;
}}
.sbl-card-purple {{
    border-color: {TYRIAN_PURPLE};
    box-shadow: 0 0 20px {TYRIAN_PURPLE}55;
}}

/* ── Section headers ── */
.sbl-section {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    color: {PURE_GOLD};
    letter-spacing: 0.1em;
    border-bottom: 1px solid {PURE_GOLD}55;
    padding-bottom: 0.3rem;
    margin-top: 1.2rem;
    margin-bottom: 0.8rem;
}}

/* ── Scripture text ── */
.scripture-text {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.95rem;
    line-height: 1.9;
    color: {CREAM};
    background: {NAVY}cc;
    border-left: 3px solid {PURE_GOLD};
    padding: 1rem 1.2rem;
    border-radius: 4px;
}}
.scripture-verse-num {{
    color: {SCARLET};
    font-weight: 600;
    font-size: 0.78rem;
}}

/* ── Keyword badges (Discovery mode) ── */
.sbl-keyword {{
    display: inline-block;
    background: {TYRIAN_PURPLE};
    color: {PURE_GOLD};
    font-size: 0.72rem;
    font-family: 'IBM Plex Mono', monospace;
    padding: 2px 8px;
    border-radius: 3px;
    border: 1px solid {PURE_GOLD}88;
    margin: 2px;
    cursor: help;
}}

/* ── Metrics ── */
[data-testid="metric-container"] {{
    background: {NAVY}cc;
    border: 1px solid {PURE_GOLD}44;
    border-radius: 5px;
    padding: 0.5rem;
}}
[data-testid="metric-container"] label {{
    color: {LIGHT_GOLD} !important;
    font-size: 0.7rem !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: {PURE_GOLD} !important;
    font-size: 1.4rem !important;
}}

/* ── Inputs ── */
.stTextInput input, .stSelectbox select {{
    background: {NAVY} !important;
    color: {PURE_GOLD} !important;
    border: 1px solid {PURE_GOLD}55 !important;
    font-family: 'IBM Plex Mono', monospace !important;
}}
.stButton > button {{
    background: {TYRIAN_PURPLE} !important;
    color: {PURE_GOLD} !important;
    border: 1px solid {PURE_GOLD}88 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em;
    transition: all 0.2s;
}}
.stButton > button:hover {{
    background: {PURE_GOLD} !important;
    color: {NAVY} !important;
    box-shadow: 0 0 15px {PURE_GOLD}88;
}}

/* ── Slider ── */
.stSlider [data-testid="stSlider"] {{
    color: {PURE_GOLD};
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {NAVY}; }}
::-webkit-scrollbar-thumb {{ background: {PURE_GOLD}66; border-radius: 3px; }}

/* ── Divider ── */
hr {{ border-color: {PURE_GOLD}44 !important; }}

/* ── Mobile responsive ── */
@media (max-width: 768px) {{
    .sbl-title {{ font-size: 2rem; }}
    .main .block-container {{ padding: 0.5rem; }}
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA STORES
# ─────────────────────────────────────────────

STRONGS_GREEK = {
    "grace":    {"strongs": "G5485", "greek": "χάρις", "transliteration": "charis",
                 "definition": "Unmerited divine favor; gift freely bestowed apart from works.",
                 "root": "χαίρω (chairō) — to rejoice"},
    "faith":    {"strongs": "G4102", "greek": "πίστις", "transliteration": "pistis",
                 "definition": "Conviction of truth; reliance upon Christ for salvation.",
                 "root": "πείθω (peithō) — to persuade"},
    "logos":    {"strongs": "G3056", "greek": "λόγος", "transliteration": "logos",
                 "definition": "Word; divine rational principle; the second Person of the Trinity in Johannine theology.",
                 "root": "λέγω (legō) — to speak"},
    "agape":    {"strongs": "G26",   "greek": "ἀγάπη", "transliteration": "agapē",
                 "definition": "Self-sacrificial, unconditional love; the highest form of divine love.",
                 "root": "ἀγαπάω (agapaō) — to love"},
    "covenant": {"strongs": "H1285", "hebrew": "בְּרִית", "transliteration": "berith",
                 "definition": "Binding agreement between parties; the backbone of redemptive history.",
                 "root": "בָּרָה (bara) — to cut"},
    "shalom":   {"strongs": "H7965", "hebrew": "שָׁלוֹם", "transliteration": "shalom",
                 "definition": "Completeness, wholeness, peace; holistic well-being and right relationship.",
                 "root": "שָׁלֵם (shalem) — to be complete"},
    "messiah":  {"strongs": "H4899", "hebrew": "מָשִׁיחַ", "transliteration": "mashiach",
                 "definition": "Anointed One; the divinely commissioned deliverer; fulfilled in Jesus of Nazareth.",
                 "root": "מָשַׁח (mashach) — to anoint"},
    "ekklesia": {"strongs": "G1577", "greek": "ἐκκλησία", "transliteration": "ekklēsia",
                 "definition": "Assembly of called-out ones; the Church as covenant community.",
                 "root": "ἐκ + καλέω — out of + to call"},
}

MANUSCRIPT_DATA = {
    "New Testament (Greek)":     {"manuscripts": 5856, "earliest_copy": "~AD 125",  "gap_years": 25,   "language_count": 25000},
    "Iliad (Homer)":             {"manuscripts": 643,  "earliest_copy": "~400 BC",  "gap_years": 400,  "language_count": 643},
    "Gallic Wars (Caesar)":      {"manuscripts": 251,  "earliest_copy": "~900 AD",  "gap_years": 950,  "language_count": 251},
    "Annals (Tacitus)":          {"manuscripts": 20,   "earliest_copy": "~1100 AD", "gap_years": 1000, "language_count": 20},
    "History (Thucydides)":      {"manuscripts": 96,   "earliest_copy": "~900 AD",  "gap_years": 1300, "language_count": 96},
    "Works (Plato)":             {"manuscripts": 210,  "earliest_copy": "~895 AD",  "gap_years": 1200, "language_count": 210},
    "Histories (Herodotus)":     {"manuscripts": 109,  "earliest_copy": "~900 AD",  "gap_years": 1350, "language_count": 109},
}

CROSS_REF_MATRIX = {
    "Matthew":    {"Psalms": 9, "Isaiah": 11, "Exodus": 4, "Daniel": 5, "Zechariah": 5, "Genesis": 3},
    "Mark":       {"Psalms": 5, "Isaiah": 6,  "Exodus": 3, "Daniel": 3, "Zechariah": 2, "Genesis": 2},
    "Luke":       {"Psalms": 7, "Isaiah": 8,  "Exodus": 5, "Daniel": 4, "Zechariah": 3, "Genesis": 5},
    "John":       {"Psalms": 6, "Isaiah": 7,  "Exodus": 6, "Daniel": 2, "Zechariah": 2, "Genesis": 4},
    "Romans":     {"Psalms": 8, "Isaiah": 9,  "Exodus": 4, "Daniel": 1, "Zechariah": 1, "Genesis": 6},
    "Hebrews":    {"Psalms": 12,"Isaiah": 5,  "Exodus": 8, "Daniel": 3, "Zechariah": 2, "Genesis": 5},
    "Revelation": {"Psalms": 10,"Isaiah": 8,  "Exodus": 7, "Daniel": 9, "Zechariah": 6, "Genesis": 4},
}

TIMELINE_EVENTS = [
    {"id":"1",  "content":"Creation / Eden",        "start":"4004-01-01", "group":"Biblical",  "style":f"background:{SCARLET};color:white"},
    {"id":"2",  "content":"Noah's Flood",            "start":"2350-01-01", "group":"Biblical",  "style":f"background:{SCARLET};color:white"},
    {"id":"3",  "content":"Call of Abraham",         "start":"2091-01-01", "group":"Biblical",  "style":f"background:{PURE_GOLD};color:{NAVY}"},
    {"id":"4",  "content":"Egyptian Empire Peak",    "start":"1550-01-01", "group":"World",     "style":f"background:{TYRIAN_PURPLE};color:white"},
    {"id":"5",  "content":"The Exodus",              "start":"1446-01-01", "group":"Biblical",  "style":f"background:{SCARLET};color:white"},
    {"id":"6",  "content":"King David's Reign",      "start":"1010-01-01", "group":"Biblical",  "style":f"background:{PURE_GOLD};color:{NAVY}"},
    {"id":"7",  "content":"Solomon's Temple Built",  "start":"966-01-01",  "group":"Biblical",  "style":f"background:{PURE_GOLD};color:{NAVY}"},
    {"id":"8",  "content":"Assyrian Empire",         "start":"900-01-01",  "group":"World",     "style":f"background:{TYRIAN_PURPLE};color:white"},
    {"id":"9",  "content":"Babylonian Exile",        "start":"605-01-01",  "group":"Biblical",  "style":f"background:{SCARLET};color:white"},
    {"id":"10", "content":"Persian Empire (Cyrus)",  "start":"539-01-01",  "group":"World",     "style":f"background:{TYRIAN_PURPLE};color:white"},
    {"id":"11", "content":"Temple Rebuilt",          "start":"516-01-01",  "group":"Biblical",  "style":f"background:{PURE_GOLD};color:{NAVY}"},
    {"id":"12", "content":"Roman Republic Founded",  "start":"509-01-01",  "group":"World",     "style":f"background:{TYRIAN_PURPLE};color:white"},
    {"id":"13", "content":"Maccabean Revolt",        "start":"167-01-01",  "group":"Biblical",  "style":f"background:{SCARLET};color:white"},
    {"id":"14", "content":"Roman Empire (Augustus)", "start":"27-01-01",   "group":"World",     "style":f"background:{TYRIAN_PURPLE};color:white"},
    {"id":"15", "content":"Birth of Christ",         "start":"4-01-01",    "group":"Biblical",  "style":f"background:{BIBLICAL_BLUE};color:{PURE_GOLD};border:2px solid {PURE_GOLD}"},
    {"id":"16", "content":"Ministry & Crucifixion",  "start":"30-04-01",   "group":"Biblical",  "style":f"background:{SCARLET};color:white;border:2px solid {PURE_GOLD}"},
    {"id":"17", "content":"Pentecost / Church Born", "start":"30-05-01",   "group":"Biblical",  "style":f"background:{PURE_GOLD};color:{NAVY}"},
    {"id":"18", "content":"Paul's Missionary Journeys","start":"46-01-01", "group":"Biblical",  "style":f"background:{PURE_GOLD};color:{NAVY}"},
    {"id":"19", "content":"Temple Destroyed (Titus)","start":"70-01-01",   "group":"World",     "style":f"background:{SCARLET};color:white"},
    {"id":"20", "content":"Revelation Written",      "start":"95-01-01",   "group":"Biblical",  "style":f"background:{BIBLICAL_BLUE};color:{PURE_GOLD}"},
]

GENEALOGY_DATA = {
    "nodes": [
        ("Abraham", {}), ("Sarah", {}), ("Isaac", {}), ("Rebekah", {}),
        ("Jacob", {}), ("Leah", {}), ("Judah", {}), ("Tamar", {}),
        ("Pharez", {}), ("Hezron", {}), ("Ram", {}), ("Amminadab", {}),
        ("Nahshon", {}), ("Salmon", {}), ("Rahab", {}), ("Boaz", {}),
        ("Ruth", {}), ("Obed", {}), ("Jesse", {}), ("David", {}),
        ("Bathsheba", {}), ("Solomon", {}), ("Rehoboam", {}),
        ("Abijah", {}), ("Asa", {}), ("Jehoshaphat", {}), ("Joram", {}),
        ("Uzziah", {}), ("Jotham", {}), ("Ahaz", {}), ("Hezekiah", {}),
        ("Manasseh", {}), ("Amon", {}), ("Josiah", {}), ("Jechoniah", {}),
        ("Shealtiel", {}), ("Zerubbabel", {}), ("Abiud", {}), ("Eliakim", {}),
        ("Azor", {}), ("Sadoc", {}), ("Achim", {}), ("Eliud", {}),
        ("Eleazar", {}), ("Matthan", {}), ("Jacob (Father of Joseph)", {}),
        ("Joseph (Husband of Mary)", {}), ("Mary", {}), ("Jesus of Nazareth", {}),
    ],
    "edges": [
        ("Abraham", "Isaac"), ("Sarah", "Isaac"),
        ("Isaac", "Jacob"), ("Rebekah", "Jacob"),
        ("Jacob", "Judah"), ("Leah", "Judah"),
        ("Judah", "Pharez"), ("Tamar", "Pharez"),
        ("Pharez", "Hezron"), ("Hezron", "Ram"), ("Ram", "Amminadab"),
        ("Amminadab", "Nahshon"), ("Nahshon", "Salmon"),
        ("Salmon", "Boaz"), ("Rahab", "Boaz"),
        ("Boaz", "Obed"), ("Ruth", "Obed"),
        ("Obed", "Jesse"), ("Jesse", "David"),
        ("David", "Solomon"), ("Bathsheba", "Solomon"),
        ("Solomon", "Rehoboam"), ("Rehoboam", "Abijah"), ("Abijah", "Asa"),
        ("Asa", "Jehoshaphat"), ("Jehoshaphat", "Joram"), ("Joram", "Uzziah"),
        ("Uzziah", "Jotham"), ("Jotham", "Ahaz"), ("Ahaz", "Hezekiah"),
        ("Hezekiah", "Manasseh"), ("Manasseh", "Amon"), ("Amon", "Josiah"),
        ("Josiah", "Jechoniah"), ("Jechoniah", "Shealtiel"),
        ("Shealtiel", "Zerubbabel"), ("Zerubbabel", "Abiud"),
        ("Abiud", "Eliakim"), ("Eliakim", "Azor"), ("Azor", "Sadoc"),
        ("Sadoc", "Achim"), ("Achim", "Eliud"), ("Eliud", "Eleazar"),
        ("Eleazar", "Matthan"), ("Matthan", "Jacob (Father of Joseph)"),
        ("Jacob (Father of Joseph)", "Joseph (Husband of Mary)"),
        ("Joseph (Husband of Mary)", "Jesus of Nazareth"),
        ("Mary", "Jesus of Nazareth"),
    ]
}

COMMENTARY_MAP = {
    "John 3:16":   "Raymond E. Brown (*Gospel According to John*, AB 29) identifies the Johannine 'world' (κόσμος) as the entire created order alienated from God—not a subset of humanity. The perfect-tense verb 'has given' (ἔδωκεν, aorist) signals a completed act with ongoing effect (Incarnation).",
    "Romans 8:28": "The BKC notes Paul's use of the divine passive here: God is the unnamed subject working in all circumstances. 'Those who love God' echoes Deut. 6:5, anchoring Romans in OT covenant theology.",
    "Genesis 1:1":  "Brown's historical-critical framework notes 'bārāʾ' (בָּרָא) is used exclusively with God as subject in the Hebrew Bible, denoting absolute creation ex nihilo—a concept alien to ANE cosmogonies like Enuma Elish.",
    "Isaiah 53:5":  "The BKC (Walvoord & Zuck) identifies this pericope as the apex of Servant Song theology: 'chastisement' (מוּסָר, musar) carries both disciplinary and penal substitutionary connotations, fulfilled in the Passion narrative.",
    "Hebrews 11:1": "The Greek ὑπόστασις (hypostasis) translated 'substance/assurance' carries philosophical weight: it was used in Patristic literature to describe the distinct subsistence of the Trinitarian persons. Faith, per the author, has ontological grounding.",
}

THEME_FREQ = {
    "Grace":       {"Genesis":2,"Psalms":8,"Isaiah":6,"John":12,"Romans":18,"Ephesians":15,"Hebrews":8},
    "Covenant":    {"Genesis":15,"Exodus":12,"Psalms":10,"Jeremiah":14,"Hebrews":12,"Revelation":6,"Romans":5},
    "Messiah":     {"Psalms":7,"Isaiah":18,"Daniel":5,"Matthew":14,"John":11,"Acts":9,"Revelation":8},
    "Judgment":    {"Genesis":5,"Psalms":12,"Isaiah":16,"Amos":10,"Romans":8,"Revelation":22,"John":6},
    "Redemption":  {"Exodus":9,"Psalms":11,"Isaiah":13,"Galatians":8,"Ephesians":10,"Revelation":9,"Romans":9},
}

SPY_CODEWORDS = {
    "GRACE":     "God's secret gift — getting good things you didn't earn! 🎁",
    "COVENANT":  "God's unbreakable promise — stronger than a pinky swear! 🤝",
    "MESSIAH":   "The Secret Hero sent to rescue everyone! 🦸",
    "LOGOS":     "The Word — Jesus as God's ultimate message to the world! 📜",
    "SHALOM":    "Super Peace — when everything is exactly right! ✨",
    "AGAPE":     "The strongest kind of love — it never runs out! ❤️",
    "EKKLESIA":  "The Team — God's special group of called-out people! 👥",
    "REDEMPTION":"Being bought back and set free! ⛓️→🕊️",
}

# ─────────────────────────────────────────────
# API FUNCTIONS
# ─────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_scripture(reference: str, translation: str = "kjv") -> dict:
    """Fetch scripture from bible-api.com."""
    url = f"https://bible-api.com/{requests.utils.quote(reference)}?translation={translation}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return {"error": "Unable to retrieve scripture. Check reference and connectivity.", "verses": []}

# ─────────────────────────────────────────────
# RENDER HELPERS
# ─────────────────────────────────────────────

def card(content_html: str, variant: str = ""):
    cls = f"sbl-card sbl-card-{variant}" if variant else "sbl-card"
    st.markdown(f'<div class="{cls}">{content_html}</div>', unsafe_allow_html=True)

def section_header(title: str):
    st.markdown(f'<div class="sbl-section">{title}</div>', unsafe_allow_html=True)

def render_scripture_pane(data: dict, depth: int):
    if "error" in data and not data.get("verses"):
        card(f'<span style="color:{SCARLET}">⚠ {data["error"]}</span>', "scarlet")
        return

    ref = data.get("reference", "")
    translation = data.get("translation_name", "")
    verses = data.get("verses", [])

    card(f"""
        <span style="font-family:'Bebas Neue';font-size:1.3rem;color:{PURE_GOLD}">{ref}</span>
        <span style="font-size:0.68rem;color:{LIGHT_GOLD};margin-left:1rem">[{translation.upper()}]</span>
    """)

    verse_html = ""
    for v in verses:
        num = v.get("verse", "")
        text = v.get("text", "").strip()
        verse_html += f'<span class="scripture-verse-num">[{num}]</span> {text} '

    if depth == 1:
        # Discovery mode: highlight spy codewords
        for word, meaning in SPY_CODEWORDS.items():
            if word.lower() in verse_html.lower():
                import re
                verse_html = re.sub(
                    f"(?i)({word})",
                    f'<span class="sbl-keyword" title="{meaning}">\\1 🔍</span>',
                    verse_html
                )

    st.markdown(f'<div class="scripture-text">{verse_html}</div>', unsafe_allow_html=True)

def render_sententia_sidebar(ref: str, depth: int):
    section_header("SENTENTIA // Academic Judgment")

    # Commentary
    commentary_key = ref.strip()
    commentary = COMMENTARY_MAP.get(commentary_key)
    if not commentary:
        # Try prefix match
        for k in COMMENTARY_MAP:
            if k.split(" ")[0].lower() in commentary_key.lower():
                commentary = COMMENTARY_MAP[k]
                break

    if commentary and depth == 2:
        card(f"""
            <div style="font-size:0.72rem;color:{LIGHT_GOLD};letter-spacing:0.1em;margin-bottom:0.4rem">
            📚 SCHOLARLY COMMENTARY
            </div>
            <div style="font-size:0.85rem;color:{CREAM};line-height:1.8">{commentary}</div>
        """, "purple")
    elif depth == 1:
        card(f"""
            <div style="font-size:0.8rem;color:{CREAM}">
            🔍 <strong style="color:{PURE_GOLD}">Biblical Detectives</strong> look for clues called
            <em>context</em> — WHO wrote it, WHEN, and WHY! Ask an adult about what was happening
            in history when this was written.
            </div>
        """)

    # Linguistic data
    if depth == 2:
        section_header("LEXICON // Strong's Analysis")
        matched_words = []
        for word, data in STRONGS_GREEK.items():
            if word in ref.lower():
                matched_words.append((word, data))

        if matched_words:
            for word, data in matched_words:
                greek = data.get("greek", data.get("hebrew", ""))
                card(f"""
                    <div style="font-size:0.7rem;color:{PURE_GOLD}">{data['strongs']} // {data['transliteration']}</div>
                    <div style="font-size:1.1rem;color:{CREAM}">{greek}</div>
                    <div style="font-size:0.78rem;color:{LIGHT_GOLD};margin-top:0.3rem">{data['definition']}</div>
                    <div style="font-size:0.68rem;color:{SCARLET};margin-top:0.3rem">Root: {data['root']}</div>
                """, "scarlet")
        else:
            st.markdown(f'<span style="font-size:0.75rem;color:{LIGHT_GOLD}88">Search a term (e.g., "grace", "logos") in the reference field to load lexical data.</span>', unsafe_allow_html=True)

def build_manuscript_chart():
    df = pd.DataFrame([
        {"Work": k, "Manuscripts": v["manuscripts"], "Gap (Years)": v["gap_years"],
         "Earliest Copy": v["earliest_copy"]}
        for k, v in MANUSCRIPT_DATA.items()
    ]).sort_values("Manuscripts", ascending=True)

    fig = go.Figure()
    GOLD  = "#D4AF37"
    SCAR  = "#B22222"
    NVY   = "#0A1628"
    BLUE  = "#0038A8"
    GGRID = "rgba(212,175,55,0.10)"

    colors = [SCAR if "New Testament" in w else GOLD for w in df["Work"]]

    fig.add_trace(go.Bar(
        y=df["Work"],
        x=df["Manuscripts"],
        orientation='h',
        marker_color=colors,
        marker_line_color=NVY,
        marker_line_width=1,
        text=[f"{v:,}" for v in df["Manuscripts"]],
        textposition='outside',
        textfont=dict(color=GOLD, size=11, family="monospace"),
        hovertemplate="<b>%{y}</b><br>Manuscripts: %{x:,}<extra></extra>",
    ))

    fig.update_layout(
        title={"text": "Manuscript Attestation: NT vs. Classical Antiquity",
               "font": {"family": "sans-serif", "size": 20, "color": GOLD}, "x": 0.5},
        plot_bgcolor=NVY,
        paper_bgcolor=BLUE,
        font={"family": "monospace", "color": GOLD},
        xaxis={"title": "Total Extant Manuscripts", "gridcolor": GGRID,
               "color": GOLD, "tickfont": {"size": 10}},
        yaxis={"gridcolor": "rgba(0,0,0,0)", "color": GOLD, "tickfont": {"size": 10}},
        margin={"l": 10, "r": 80, "t": 60, "b": 40},
        height=380,
    )
    return fig

def build_cross_ref_heatmap():
    nt_books = list(CROSS_REF_MATRIX.keys())
    ot_books = ["Psalms", "Isaiah", "Exodus", "Daniel", "Zechariah", "Genesis"]
    matrix = [[CROSS_REF_MATRIX[nt].get(ot, 0) for ot in ot_books] for nt in nt_books]

    fig = go.Figure(go.Heatmap(
        z=matrix,
        x=ot_books,
        y=nt_books,
        colorscale=[[0, NAVY], [0.4, SCARLET], [0.75, TYRIAN_PURPLE], [1.0, PURE_GOLD]],
        showscale=True,
        text=[[str(v) for v in row] for row in matrix],
        texttemplate="%{text}",
        textfont=dict(family="IBM Plex Mono", size=11),
        hovertemplate="<b>%{y}</b> → <b>%{x}</b><br>References: %{z}<extra></extra>",
    ))
    GOLD = "#D4AF37"
    NVY  = "#0A1628"
    BLUE = "#0038A8"

    fig.update_layout(
        title={"text": "NT Citation Density of OT Books",
               "font": {"family": "sans-serif", "size": 20, "color": GOLD}, "x": 0.5},
        plot_bgcolor=NVY,
        paper_bgcolor=BLUE,
        font={"family": "monospace", "color": GOLD},
        xaxis={"title": "Old Testament Book", "color": GOLD, "tickfont": {"size": 10}},
        yaxis={"title": "New Testament Book", "color": GOLD, "tickfont": {"size": 10}},
        margin={"l": 20, "r": 20, "t": 60, "b": 40},
        height=380,
    )
    return fig

def build_theme_heatmap():
    themes = list(THEME_FREQ.keys())
    books = ["Genesis", "Exodus", "Psalms", "Isaiah", "Jeremiah", "Amos",
             "Daniel", "John", "Romans", "Galatians", "Ephesians", "Hebrews",
             "Acts", "Revelation"]
    matrix = []
    for theme in themes:
        row = [THEME_FREQ[theme].get(book, 0) for book in books]
        matrix.append(row)

    fig = go.Figure(go.Heatmap(
        z=matrix,
        x=books,
        y=themes,
        colorscale=[[0, NAVY], [0.5, SCARLET], [1.0, PURE_GOLD]],
        showscale=True,
        hovertemplate="Theme: <b>%{y}</b><br>Book: <b>%{x}</b><br>Frequency Score: %{z}<extra></extra>",
    ))
    GOLD = "#D4AF37"
    NVY  = "#0A1628"
    BLUE = "#0038A8"

    fig.update_layout(
        title={"text": "Theological Theme Intensity Across Scripture",
               "font": {"family": "sans-serif", "size": 20, "color": GOLD}, "x": 0.5},
        plot_bgcolor=NVY,
        paper_bgcolor=BLUE,
        font={"family": "monospace", "color": GOLD},
        xaxis={"color": GOLD, "tickfont": {"size": 9}, "tickangle": -35},
        yaxis={"color": GOLD, "tickfont": {"size": 10}},
        margin={"l": 20, "r": 20, "t": 60, "b": 80},
        height=380,
    )
    return fig

def build_word_freq_chart(text: str, title: str = "Word Frequency Analysis"):
    """
    Build a word-frequency bar chart from scripture text.
    Guards: empty text, empty freq dict, zip-on-empty-sequence.
    All Plotly color values are strict 6-digit hex or rgba() strings.
    """
    import re

    # ── Guard: no text supplied ──
    if not text or not text.strip():
        return None

    GOLD_STR   = "#D4AF37"   # PURE_GOLD  — explicit literals avoid f-string suffix bugs
    SCARLET_STR= "#B22222"   # SCARLET
    NAVY_STR   = "#0A1628"   # NAVY
    BLUE_STR   = "#0038A8"   # BIBLICAL_BLUE
    GRID_COLOR = "rgba(212,175,55,0.12)"  # PURE_GOLD @ 12% opacity — valid Plotly rgba

    stop = {
        "the","and","of","a","in","to","is","he","that","his","for","they",
        "i","it","my","me","be","not","with","this","but","who","was","are",
        "him","her","you","your","we","our","shall","will","unto","thou",
        "thee","hath","have","had","were","their","them","then","when","from",
        "which","said","came","upon","into","all","one","an","so","by",
        "at","or","if","do","no","up","as","she","out","its","did","also",
        "hast","doth","may","let","more","even","therefore","thus","every",
    }

    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    freq: dict = {}
    for w in words:
        if w not in stop:
            freq[w] = freq.get(w, 0) + 1

    if not freq:
        return None

    top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # ── Guard: zip requires non-empty sequence ──
    if not top:
        return None

    words_out, counts = zip(*top)
    words_list  = list(words_out)
    counts_list = list(counts)
    max_count   = max(counts_list)

    bar_colors = [SCARLET_STR if c == max_count else GOLD_STR for c in counts_list]

    fig = go.Figure(
        go.Bar(
            x=words_list,
            y=counts_list,
            marker=dict(
                color=bar_colors,
                line=dict(color=NAVY_STR, width=1),
            ),
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
            "font": {"family": "sans-serif", "size": 18, "color": GOLD_STR},
        },
        plot_bgcolor=NAVY_STR,
        paper_bgcolor=BLUE_STR,
        font={"family": "monospace", "color": GOLD_STR, "size": 11},
        xaxis={
            "color": GOLD_STR,
            "tickfont": {"size": 9, "color": GOLD_STR},
            "tickangle": -40,
            "gridcolor": GRID_COLOR,
            "linecolor": GOLD_STR,
        },
        yaxis={
            "color": GOLD_STR,
            "tickfont": {"size": 9, "color": GOLD_STR},
            "gridcolor": GRID_COLOR,
            "linecolor": GOLD_STR,
        },
        margin={"l": 20, "r": 20, "t": 55, "b": 90},
        height=340,
    )
    return fig


def build_genealogy_dot(focus: str = "Full Lineage") -> str:
    """
    Build a raw Graphviz DOT string accepted directly by st.graphviz_chart.
    No 'graphviz' Python package import required — only the system binary
    installed via packages.txt is needed for rendering.
    """
    patriarchs = {"Abraham", "Isaac", "Jacob", "Judah", "David", "Solomon", "Jesus of Nazareth"}
    women       = {"Sarah", "Rebekah", "Leah", "Tamar", "Rahab", "Ruth", "Bathsheba", "Mary"}

    def nid(name: str) -> str:
        return '"' + name.replace('"', '\\"') + '"'

    GOLD  = "#D4AF37"
    PURP  = "#66023C"
    SCAR  = "#B22222"
    NVY   = "#0A1628"
    BLUE  = "#0038A8"
    CRM   = "#FFF8DC"

    lines = [
        "digraph G {",
        f'  graph [rankdir=TB bgcolor="{NVY}" fontcolor="{GOLD}" pad="0.5" nodesep="0.35" ranksep="0.55"];',
        f'  node  [shape=box style="filled,rounded" fillcolor="{BLUE}" color="{GOLD}" fontcolor="{GOLD}" fontname="Helvetica" fontsize="10"];',
        f'  edge  [color="{GOLD}" arrowhead=open arrowsize=0.7];',
    ]

    for name, _ in GENEALOGY_DATA["nodes"]:
        if focus == "Patriarchs" and name not in patriarchs and name not in women:
            continue
        n = nid(name)
        if name == "Jesus of Nazareth":
            lines.append(f'  {n} [fillcolor="{GOLD}" fontcolor="{NVY}" color="{GOLD}" penwidth=3 fontsize=12];')
        elif name in patriarchs:
            lines.append(f'  {n} [fillcolor="{PURP}" fontcolor="{GOLD}"];')
        elif name in women:
            lines.append(f'  {n} [fillcolor="{SCAR}" fontcolor="{CRM}"];')
        else:
            lines.append(f'  {n};')

    for src, dst in GENEALOGY_DATA["edges"]:
        if focus == "Patriarchs":
            if src not in patriarchs and src not in women:
                continue
            if dst not in patriarchs and dst not in women:
                continue
        lines.append(f"  {nid(src)} -> {nid(dst)};")

    lines.append("}")
    return "\n".join(lines)

def render_timeline():
    """Render timeline using HTML/JS vis-timeline."""
    items_json = json.dumps(TIMELINE_EVENTS)

    groups_json = json.dumps([
        {"id": "Biblical", "content": "📖 Biblical"},
        {"id": "World",    "content": "🌍 World History"},
    ])

    html = f"""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <div id="timeline" style="height:360px;background:{NAVY};border:1px solid {PURE_GOLD}66;border-radius:6px;"></div>
    <script>
      var container = document.getElementById('timeline');
      var items = new vis.DataSet({items_json});
      var groups = new vis.DataSet({groups_json});
      var options = {{
        stack: false,
        groupOrder: 'id',
        orientation: 'top',
        start: '-2100-01-01',
        end:   '200-01-01',
        min:   '-4500-01-01',
        max:   '400-01-01',
        zoomMin: 1000 * 60 * 60 * 24 * 365 * 50,
        moveable: true,
        zoomable: true,
        selectable: true,
        tooltip: {{ followMouse: true }},
        timeAxis: {{ scale: 'year', step: 100 }},
        style: 'background:{NAVY}',
      }};
      var timeline = new vis.Timeline(container, items, groups, options);
    </script>
    """
    st.components.v1.html(html, height=390, scrolling=False)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown(f"""
        <div style="text-align:center;padding:1rem 0 0.5rem">
            <div style="font-size:2rem">✝️</div>
            <div style="font-family:'Bebas Neue';font-size:1.6rem;color:{PURE_GOLD};
                        text-shadow:0 0 15px {PURE_GOLD}88;letter-spacing:0.1em">
                SENTENTIA<br>BIBLE LAB
            </div>
            <div style="font-size:0.62rem;color:{LIGHT_GOLD};letter-spacing:0.2em">
                CHRISTIAN APOLOGETICS CODEX v1.0
            </div>
        </div>
        <hr style="border-color:{PURE_GOLD}44;margin:0.5rem 0"/>
    """, unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:0.72rem;color:{LIGHT_GOLD};letter-spacing:0.15em;margin-bottom:0.3rem">⚙ INTELLECTUAL DEPTH</div>', unsafe_allow_html=True)
    depth = st.slider("Intellectual Depth", min_value=1, max_value=2, value=1, step=1,
                      format="%d", key="depth_slider", label_visibility="collapsed",
                      help="Level 1 = Discovery (all ages) | Level 2 = Scholar (graduate)")
    depth_label = "🔍 DISCOVERY MODE" if depth == 1 else "🎓 SCHOLAR MODE"
    depth_color = SCARLET if depth == 1 else TYRIAN_PURPLE
    st.markdown(f'<div style="text-align:center;font-size:0.75rem;color:{depth_color};font-weight:600;letter-spacing:0.1em;margin-top:0.3rem">{depth_label}</div>', unsafe_allow_html=True)

    st.markdown(f'<hr style="border-color:{PURE_GOLD}44;margin:0.8rem 0"/>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.72rem;color:{LIGHT_GOLD};letter-spacing:0.15em;margin-bottom:0.3rem">📖 TRANSLATION</div>', unsafe_allow_html=True)
    translation = st.selectbox("Translation", ["kjv", "web", "bbe"], index=0, label_visibility="collapsed",
                                format_func=lambda x: {"kjv":"King James Version (KJV)",
                                                        "web":"World English Bible (WEB)",
                                                        "bbe":"Bible in Basic English (BBE)"}[x])

    st.markdown(f'<hr style="border-color:{PURE_GOLD}44;margin:0.8rem 0"/>', unsafe_allow_html=True)
    if depth == 1:
        st.markdown(f"""
            <div class="sbl-card">
                <div style="font-size:0.68rem;color:{PURE_GOLD};letter-spacing:0.1em;margin-bottom:0.4rem">
                🕵️ SPY CODEBOOK ACTIVE
                </div>
                <div style="font-size:0.75rem;color:{CREAM}">
                Hover over <span style="color:{PURE_GOLD}">gold keywords</span> in the Scripture pane to decode secret theological terms!
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="sbl-card sbl-card-purple">
                <div style="font-size:0.68rem;color:{PURE_GOLD};letter-spacing:0.1em;margin-bottom:0.4rem">
                📚 SCHOLAR RESOURCES ACTIVE
                </div>
                <div style="font-size:0.75rem;color:{CREAM}">
                Strong's Concordance · Brown's Commentary · BKC · Dodson Lexicon · TSK Cross-References
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:0.62rem;color:{LIGHT_GOLD}44;text-align:center;margin-top:2rem">Sola Scriptura // Soli Deo Gloria</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown(f"""
    <div style="text-align:center;padding:1rem 0 0.5rem">
        <div class="sbl-title">SENTENTIA BIBLE LAB</div>
        <div class="sbl-subtitle">Christian Apologetics Codex // Sola Scriptura</div>
    </div>
""", unsafe_allow_html=True)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("✝️ Canonical Books", "66")
with col_m2:
    st.metric("✍️ NT Manuscripts", "5,856")
with col_m3:
    st.metric("🌍 Translations", "3,000+")
with col_m4:
    st.metric("📅 Span (Years)", "~1,600")

st.markdown('<hr/>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Scripture Lab",
    "📊 Theology Analytics",
    "⏳ Historical Timeline",
    "🌳 Lineage Graph",
    "🏛️ Apologetics Toolbox",
])

# ══════════════════════════════════════════════
# TAB 1 — SCRIPTURE LAB
# ══════════════════════════════════════════════
with tab1:
    st.markdown(f'<div style="font-size:0.75rem;color:{LIGHT_GOLD};letter-spacing:0.1em;margin-bottom:0.8rem">Enter any reference (e.g., <em>John 3:16</em>, <em>Romans 8:28-39</em>, <em>Psalm 23</em>)</div>', unsafe_allow_html=True)

    col_ref, col_btn = st.columns([4, 1])
    with col_ref:
        ref_input = st.text_input("Scripture Reference", value="John 3:16", placeholder="e.g. Isaiah 53:5",
                                   label_visibility="collapsed")
    with col_btn:
        fetch_btn = st.button("⟳ FETCH", use_container_width=True)

    if "scripture_data" not in st.session_state or fetch_btn:
        if ref_input:
            with st.spinner("Retrieving scripture..."):
                st.session_state.scripture_data = fetch_scripture(ref_input, translation)
                st.session_state.scripture_ref = ref_input

    scripture_data = st.session_state.get("scripture_data", {})
    scripture_ref  = st.session_state.get("scripture_ref", ref_input)

    col_left, col_right = st.columns([1, 1], gap="medium")

    with col_left:
        section_header("📖 SCRIPTURE TEXT")
        render_scripture_pane(scripture_data, depth)

        if depth == 2 and scripture_data.get("verses"):
            section_header("PARALLEL TRANSLATIONS")
            for trans in ["web", "bbe"]:
                if trans != translation:
                    with st.spinner(f"Loading {trans.upper()}..."):
                        alt_data = fetch_scripture(scripture_ref, trans)
                    if alt_data.get("verses"):
                        alt_text = " ".join(v.get("text","").strip() for v in alt_data["verses"])
                        card(f"""
                            <div style="font-size:0.65rem;color:{LIGHT_GOLD};letter-spacing:0.15em;margin-bottom:0.3rem">
                            [{trans.upper()}]
                            </div>
                            <div style="font-size:0.83rem;color:{CREAM};line-height:1.7">{alt_text}</div>
                        """)

    with col_right:
        render_sententia_sidebar(scripture_ref, depth)

        if depth == 1:
            section_header("🗺 STORY MAP")
            card(f"""
                <div style="font-size:0.8rem;color:{CREAM}">
                <strong style="color:{PURE_GOLD}">🧭 WHO</strong> wrote this? When? To whom?<br><br>
                <strong style="color:{PURE_GOLD}">📍 WHERE</strong> was this place?<br><br>
                <strong style="color:{PURE_GOLD}">❓ WHY</strong> does this matter today?<br><br>
                <em style="color:{LIGHT_GOLD}">These three questions are the secret tools
                of every great Bible detective!</em>
                </div>
            """)
        else:
            section_header("⚖ CROSS-REFERENCES (TSK)")
            tsk_refs = {
                "John 3:16":    ["John 1:14", "Rom 5:8", "1 John 4:9", "John 1:18"],
                "Romans 8:28":  ["Gen 50:20", "Ps 119:91", "Eph 1:11", "Phil 1:12"],
                "Isaiah 53:5":  ["1 Pet 2:24", "Isa 53:4", "2 Cor 5:21", "Rom 4:25"],
                "Genesis 1:1":  ["John 1:1", "Heb 11:3", "Ps 33:6", "Col 1:16"],
                "Hebrews 11:1": ["2 Cor 5:7", "Rom 8:24", "Heb 11:3", "Gal 5:5"],
            }
            refs = tsk_refs.get(scripture_ref.strip(), ["See Strong's for cross-reference data"])
            refs_html = "".join([f'<span class="sbl-keyword">{r}</span> ' for r in refs])
            card(f"""
                <div style="font-size:0.65rem;color:{LIGHT_GOLD};margin-bottom:0.5rem">
                TREASURY OF SCRIPTURE KNOWLEDGE
                </div>
                {refs_html}
            """, "scarlet")

# ══════════════════════════════════════════════
# TAB 2 — THEOLOGY ANALYTICS
# ══════════════════════════════════════════════
with tab2:
    section_header("📊 THEOLOGICAL ANALYTICS SUITE")

    col_a, col_b = st.columns(2, gap="medium")
    with col_a:
        st.plotly_chart(build_theme_heatmap(), width="stretch")
    with col_b:
        st.plotly_chart(build_cross_ref_heatmap(), width="stretch")

    st.markdown('<hr/>', unsafe_allow_html=True)

    section_header("WORD FREQUENCY ANALYSIS")
    scripture_text = ""
    if st.session_state.get("scripture_data", {}).get("verses"):
        scripture_text = " ".join(
            v.get("text","") for v in st.session_state.scripture_data["verses"]
        )

    if scripture_text and scripture_text.strip():
        try:
            wf_fig = build_word_freq_chart(
                scripture_text,
                f"Word Frequency — {st.session_state.get('scripture_ref', 'Selected Passage')}"
            )
            if wf_fig:
                st.plotly_chart(wf_fig, width="stretch")
            else:
                card(f'<span style="color:{LIGHT_GOLD}88">Passage too short or contains only common words — try a longer reference.</span>')
        except Exception as e:
            card(f'<span style="color:{SCARLET}">⚠ Chart error: {e}</span>', "scarlet")
    else:
        card(f'<span style="color:{LIGHT_GOLD}88">Load a scripture passage in the Scripture Lab tab to enable word frequency analysis.</span>')

    if depth == 2:
        st.markdown('<hr/>', unsafe_allow_html=True)
        section_header("LEXICAL DISTRIBUTION TABLE")
        lex_df = pd.DataFrame([
            {"Term": k, "Strong's": v["strongs"],
             "Transliteration": v["transliteration"],
             "Language": "Greek" if v["strongs"].startswith("G") else "Hebrew",
             "Definition": v["definition"][:60] + "..."}
            for k, v in STRONGS_GREEK.items()
        ])

        def style_lex_table(df):
            return df.style.set_properties(**{
                'background-color': NAVY,
                'color': PURE_GOLD,
                'font-family': 'IBM Plex Mono',
                'font-size': '11px',
                'border': f'1px solid {PURE_GOLD}44',
            }).set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', PURE_GOLD),
                    ('color', NAVY),
                    ('font-family', 'IBM Plex Mono'),
                    ('font-size', '11px'),
                    ('font-weight', '600'),
                    ('letter-spacing', '0.05em'),
                ]}
            ])

        st.dataframe(
            lex_df,
            width="stretch",
            hide_index=True,
            column_config={
                "Term":              st.column_config.TextColumn("TERM", width=90),
                "Strong's":          st.column_config.TextColumn("STRONG'S", width=80),
                "Transliteration":   st.column_config.TextColumn("TRANSLITERATION", width=120),
                "Language":          st.column_config.TextColumn("LANG", width=70),
                "Definition":        st.column_config.TextColumn("DEFINITION"),
            }
        )

# ══════════════════════════════════════════════
# TAB 3 — HISTORICAL TIMELINE
# ══════════════════════════════════════════════
with tab3:
    section_header("⏳ BIBLICAL-WORLD HISTORY TIMELINE")
    card(f"""
        <div style="font-size:0.78rem;color:{CREAM}">
        Interactive timeline overlay of Biblical events against World History.
        <strong style="color:{PURE_GOLD}">Drag to scroll</strong> ·
        <strong style="color:{PURE_GOLD}">Scroll to zoom</strong> ·
        <span style="color:{SCARLET}">■</span> Redemptive events ·
        <span style="color:{PURE_GOLD}">■</span> Covenant moments ·
        <span style="color:{TYRIAN_PURPLE}">■</span> World empires
        </div>
    """)

    render_timeline()

    if depth == 2:
        st.markdown('<hr/>', unsafe_allow_html=True)
        section_header("EVENT TABLE // Scholar Reference")
        timeline_df = pd.DataFrame([
            {"Event": e["content"], "Approx. Date": e["start"].split("-")[0] + " BC" if int(e["start"].split("-")[0]) < 100 else e["start"].split("-")[0] + " AD",
             "Category": e["group"]}
            for e in TIMELINE_EVENTS
        ])
        st.dataframe(timeline_df, width="stretch", hide_index=True,
                     column_config={
                         "Event":    st.column_config.TextColumn("BIBLICAL / WORLD EVENT"),
                         "Approx. Date": st.column_config.TextColumn("APPROX. DATE"),
                         "Category": st.column_config.TextColumn("CATEGORY"),
                     })
    else:
        card(f"""
            <div style="font-size:0.85rem;color:{CREAM}">
            🕵️ <strong style="color:{PURE_GOLD}">Detective Mission:</strong>
            Find the event when God rescued His people from Egypt — The Exodus!
            Can you spot where Jesus was born on the timeline? What empire ruled the world then?
            </div>
        """)

# ══════════════════════════════════════════════
# TAB 4 — LINEAGE GRAPH
# ══════════════════════════════════════════════
with tab4:
    section_header("🌳 MESSIANIC GENEALOGY // Abraham → Christ")

    col_g1, col_g2 = st.columns([3, 1])
    with col_g2:
        focus = st.radio("View", ["Full Lineage", "Patriarchs"], index=0)
        card(f"""
            <div style="font-size:0.72rem;color:{LIGHT_GOLD};margin-bottom:0.4rem">LEGEND</div>
            <span style="color:{PURE_GOLD}">■</span> Patriarchs<br>
            <span style="color:{SCARLET}">■</span> Women in Lineage<br>
            <span style="color:{PURE_GOLD};font-weight:600">★</span> Jesus of Nazareth<br>
            <div style="font-size:0.68rem;color:{CREAM};margin-top:0.5rem">
            Matthew 1:1-17 records 42 generations. The inclusion of women (Tamar, Rahab, Ruth, Bathsheba, Mary) was theologically radical in a 1st-century Jewish context.
            </div>
        """)

        if depth == 2:
            card(f"""
                <div style="font-size:0.68rem;color:{LIGHT_GOLD};letter-spacing:0.1em;margin-bottom:0.3rem">📚 SCHOLARLY NOTE</div>
                <div style="font-size:0.75rem;color:{CREAM}">
                Matthew's genealogy is structured in 3×14 groups (possibly a gematria device: David = דוד = 14), establishing Jesus as Davidic Messiah.
                Luke 3:23-38 traces through Nathan (not Solomon), reflecting Mary's line per many interpreters.
                </div>
            """, "purple")

    with col_g1:
        with st.spinner("Rendering genealogy graph..."):
            dot_src = build_genealogy_dot(focus)
        st.graphviz_chart(dot_src, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 5 — APOLOGETICS TOOLBOX
# ══════════════════════════════════════════════
with tab5:
    section_header("🏛️ APOLOGETICS TOOLBOX")

    if depth == 1:
        card(f"""
            <div style="font-size:0.85rem;color:{CREAM}">
            🔍 <strong style="color:{PURE_GOLD}">Question:</strong> How do we know the Bible is real?<br><br>
            Answer: Archaeologists keep digging up proof! Cities, kings, and events mentioned
            in the Bible have been confirmed by real discoveries. And the New Testament has
            <strong style="color:{SCARLET}">WAY more copies</strong> than any other ancient book — by a landslide!
            </div>
        """)

    col_ap1, col_ap2 = st.columns(2, gap="medium")
    with col_ap1:
        st.plotly_chart(build_manuscript_chart(), width="stretch")

    with col_ap2:
        section_header("MANUSCRIPT EVIDENCE TABLE")
        ms_df = pd.DataFrame([
            {"Work": k, "Manuscripts": f"{v['manuscripts']:,}",
             "Earliest Copy": v["earliest_copy"], "Compositional Gap": f"{v['gap_years']} yrs"}
            for k, v in MANUSCRIPT_DATA.items()
        ])
        st.dataframe(
            ms_df,
            width="stretch",
            hide_index=True,
            height=330,
            column_config={
                "Work":              st.column_config.TextColumn("ANCIENT WORK"),
                "Manuscripts":       st.column_config.TextColumn("EXTANT MSS"),
                "Earliest Copy":     st.column_config.TextColumn("EARLIEST COPY"),
                "Compositional Gap": st.column_config.TextColumn("COMP. GAP"),
            }
        )

    st.markdown('<hr/>', unsafe_allow_html=True)

    section_header("⚱️ NOTABLE ARCHAEOLOGICAL CONFIRMATIONS")

    arch_data = [
        {"Site/Discovery": "Pool of Siloam", "Location": "Jerusalem", "Biblical Ref": "John 9:7",
         "Significance": "Excavated 2004; confirms Johannine geography precisely."},
        {"Site/Discovery": "Pilate Inscription", "Location": "Caesarea Maritima", "Biblical Ref": "Luke 23:1",
         "Significance": "1961 discovery naming 'Pontius Pilatus, Prefect of Judaea.'"},
        {"Site/Discovery": "Tel Dan Stele", "Location": "Northern Israel", "Biblical Ref": "2 Sam 7:16",
         "Significance": "9th-c. BC Aramaic text references 'House of David' — corroborating the Davidic dynasty."},
        {"Site/Discovery": "Dead Sea Scrolls", "Location": "Qumran", "Biblical Ref": "Isaiah (entire)",
         "Significance": "Isaiah Scroll (1QIsa-a) dated ~125 BC matches MT with >95% fidelity."},
        {"Site/Discovery": "Ebla Tablets", "Location": "Tell Mardikh, Syria", "Biblical Ref": "Gen 14",
         "Significance": "~17,000 tablets confirm linguistic and cultural context of Patriarchal narratives."},
        {"Site/Discovery": "House of Peter", "Location": "Capernaum", "Biblical Ref": "Mark 1:29",
         "Significance": "1st-century domus ecclesia (house-church) with early Christian graffiti excavated."},
        {"Site/Discovery": "Ossuary of James", "Location": "Jerusalem (disputed)", "Biblical Ref": "Gal 1:19",
         "Significance": "Inscription reads 'James son of Joseph brother of Jesus'; contested but significant."},
    ]

    arch_df = pd.DataFrame(arch_data)
    st.dataframe(
        arch_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Site/Discovery":  st.column_config.TextColumn("SITE / DISCOVERY"),
            "Location":        st.column_config.TextColumn("LOCATION"),
            "Biblical Ref":    st.column_config.TextColumn("BIBLICAL REF"),
            "Significance":    st.column_config.TextColumn("SIGNIFICANCE"),
        }
    )

    if depth == 2:
        st.markdown('<hr/>', unsafe_allow_html=True)
        section_header("TEXTUAL CRITICISM // Bibliographic Test")
        card(f"""
            <div style="font-size:0.82rem;color:{CREAM};line-height:1.9">
            The <strong style="color:{PURE_GOLD}">Bibliographic Test</strong> (F.F. Bruce, Josh McDowell)
            evaluates reliability via (1) number of extant manuscripts and (2) temporal gap between
            composition and earliest surviving copy. The NT eclipses all classical antiquity by
            a factor of <strong style="color:{SCARLET}">9:1</strong> in manuscript count and possesses
            the shortest compositional gap of any ancient text (~25 years, P52 Rylands fragment).<br><br>
            Sir Frederic Kenyon (<em>The Bible and Archaeology</em>, 1940): <em>"The interval between
            the dates of original composition and the earliest extant evidence becomes so small
            as to be in fact negligible."</em>
            </div>
        """, "purple")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
    <hr/>
    <div style="text-align:center;font-size:0.65rem;color:{LIGHT_GOLD}55;letter-spacing:0.15em;padding:0.5rem 0 1rem">
    SENTENTIA BIBLE LAB // CHRISTIAN APOLOGETICS CODEX v1.0<br>
    Scripture via bible-api.com · Scholarship: Brown, BKC, Walvoord-Zuck · Lexica: Strong's G/H, Dodson<br>
    Sola Scriptura · Sola Gratia · Solus Christus · Sola Fide · Soli Deo Gloria
    </div>
""", unsafe_allow_html=True)
