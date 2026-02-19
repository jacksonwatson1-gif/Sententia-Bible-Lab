"""
Sententia Bible Lab — Christian Apologetics Codex
==================================================
Graduate-level Biblical research workstation.
Architecture: Command Center | Academic Split (1:2.5) | Technical Basement
AI: Claude Haiku — cached on string inputs (correct pattern for st.cache_data)
Sources: ESV API | bible-api.com | hardcoded KJV offline fallback
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import re
import json
import math
import hashlib

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sententia Bible Lab",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────
NAVY      = "#0A1628"
BIB_BLUE  = "#0038A8"
GOLD      = "#D4AF37"
LT_GOLD   = "#F5E17A"
PURPLE    = "#66023C"
SCARLET   = "#B22222"
CREAM     = "#FFF8DC"
PARCHMENT = "#fdfaf3"
BROWN     = "#4a3728"
INK       = "#2c2c2c"

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown(
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&'
    'family=IBM+Plex+Mono:wght@300;400;500;600&'
    'family=Crimson+Text:ital,wght@0,400;0,600;1,400;1,600&'
    'family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">',
    unsafe_allow_html=True)

st.markdown(f"""
<style>
/* ════════════════════════════════════════════
   FOUNDATION
   ════════════════════════════════════════════ */
.stApp,[data-testid="stAppViewContainer"]{{
    background:{NAVY}!important;
    background-image:
        radial-gradient(ellipse at 20% 0%, rgba(212,175,55,.04) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 100%, rgba(0,56,168,.12) 0%, transparent 60%)!important;
}}
.stApp>header{{background:transparent!important;backdrop-filter:none!important}}
[data-testid="block-container"]{{
    background:transparent!important;
    padding-top:.6rem!important;
    max-width:1540px!important;
}}

/* ════════════════════════════════════════════
   NAVIGATION RAIL — SIDEBAR
   ════════════════════════════════════════════ */
[data-testid="stSidebar"]{{
    background:linear-gradient(180deg,#04091a 0%,#07101f 60%,#050d1a 100%)!important;
    border-right:1px solid rgba(212,175,55,.18)!important;
    box-shadow:4px 0 24px rgba(0,0,0,.45)!important;
}}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown div,
[data-testid="stSidebar"] span{{color:{GOLD}!important}}

/* Nav rail radio — transform into icon buttons */
[data-testid="stSidebar"] .stRadio>div{{gap:0!important;flex-direction:column!important}}
[data-testid="stSidebar"] .stRadio label{{
    display:flex!important;
    align-items:center!important;
    gap:.65rem!important;
    padding:.72rem 1.1rem!important;
    margin:.1rem 0!important;
    border-radius:6px!important;
    border:1px solid transparent!important;
    cursor:pointer!important;
    transition:all .18s ease!important;
    font-family:'IBM Plex Mono',monospace!important;
    font-size:.72rem!important;
    letter-spacing:.08em!important;
    color:rgba(245,225,122,.5)!important;
    background:transparent!important;
}}
[data-testid="stSidebar"] .stRadio label:hover{{
    background:rgba(212,175,55,.06)!important;
    border-color:rgba(212,175,55,.18)!important;
    color:{GOLD}!important;
}}
[data-testid="stSidebar"] .stRadio label[data-checked="true"],
[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label,
[data-testid="stSidebar"] .stRadio input:checked + div label{{
    background:rgba(212,175,55,.1)!important;
    border-color:rgba(212,175,55,.35)!important;
    color:{GOLD}!important;
    font-weight:600!important;
}}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"]{{display:none!important}}

/* Sidebar quick-load buttons */
[data-testid="stSidebar"] .stButton>button{{
    background:transparent!important;
    color:rgba(245,225,122,.6)!important;
    border:1px solid rgba(212,175,55,.14)!important;
    font-family:'IBM Plex Mono',monospace!important;
    font-size:.65rem!important;
    letter-spacing:.06em!important;
    border-radius:4px!important;
    padding:.35rem .6rem!important;
    text-align:left!important;
    justify-content:flex-start!important;
    transition:all .15s!important;
    margin-bottom:2px!important;
}}
[data-testid="stSidebar"] .stButton>button:hover{{
    background:rgba(212,175,55,.09)!important;
    color:{GOLD}!important;
    border-color:rgba(212,175,55,.32)!important;
}}

/* ════════════════════════════════════════════
   TYPOGRAPHY
   ════════════════════════════════════════════ */
body,.stMarkdown,p,div{{
    font-family:'IBM Plex Mono','Courier New',monospace;
    color:{CREAM};
}}

/* ════════════════════════════════════════════
   TABS — REFINED SCHOLARLY STRIP
   ════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"]{{
    background:rgba(4,9,26,.7)!important;
    border-bottom:1px solid rgba(212,175,55,.2)!important;
    gap:0!important;
    padding:0 .5rem!important;
    backdrop-filter:blur(8px)!important;
    border-radius:6px 6px 0 0!important;
}}
.stTabs [data-baseweb="tab"]{{
    background:transparent!important;
    color:rgba(245,225,122,.42)!important;
    font-family:'IBM Plex Mono',monospace!important;
    font-size:.68rem!important;
    letter-spacing:.12em!important;
    padding:10px 18px!important;
    border-bottom:2px solid transparent!important;
    border-top:2px solid transparent!important;
    transition:all .18s ease!important;
    text-transform:uppercase!important;
    position:relative!important;
}}
.stTabs [data-baseweb="tab"]:hover{{
    color:rgba(212,175,55,.8)!important;
    background:rgba(212,175,55,.04)!important;
}}
.stTabs [aria-selected="true"]{{
    color:{GOLD}!important;
    border-bottom:2px solid {GOLD}!important;
    font-weight:600!important;
    background:rgba(212,175,55,.06)!important;
}}
.stTabs [data-baseweb="tab-panel"]{{
    background:transparent!important;
    padding-top:1.4rem!important;
}}

/* ════════════════════════════════════════════
   INPUTS & CONTROLS
   ════════════════════════════════════════════ */
.stTextInput input,.stTextArea textarea{{
    background:rgba(4,9,26,.65)!important;
    color:{CREAM}!important;
    border:1px solid rgba(212,175,55,.22)!important;
    border-radius:5px!important;
    font-family:'IBM Plex Mono',monospace!important;
    font-size:.86rem!important;
    transition:border-color .15s,box-shadow .15s!important;
}}
.stTextInput input:focus,.stTextArea textarea:focus{{
    border-color:rgba(212,175,55,.6)!important;
    box-shadow:0 0 0 2px rgba(212,175,55,.1)!important;
    outline:none!important;
}}
.stTextArea textarea{{line-height:1.75!important}}
.stSelectbox>div>div{{
    background:rgba(4,9,26,.65)!important;
    color:{CREAM}!important;
    border:1px solid rgba(212,175,55,.22)!important;
    border-radius:5px!important;
    font-family:'IBM Plex Mono',monospace!important;
    font-size:.83rem!important;
}}

/* ════════════════════════════════════════════
   BUTTONS — TWO VARIANTS
   ════════════════════════════════════════════ */
/* Default: subtle ghost */
.stButton>button{{
    background:rgba(102,2,60,.5)!important;
    color:{GOLD}!important;
    border:1px solid rgba(212,175,55,.28)!important;
    font-family:'IBM Plex Mono',monospace!important;
    font-size:.69rem!important;
    letter-spacing:.13em!important;
    border-radius:4px!important;
    padding:.45rem 1rem!important;
    transition:all .16s ease!important;
    text-transform:uppercase!important;
}}
.stButton>button:hover{{
    background:{GOLD}!important;
    color:{NAVY}!important;
    border-color:{GOLD}!important;
    box-shadow:0 2px 12px rgba(212,175,55,.22)!important;
}}
.stButton>button:active{{transform:translateY(1px)!important}}

/* ════════════════════════════════════════════
   METRICS — ELEVATED TILES
   ════════════════════════════════════════════ */
[data-testid="metric-container"]{{
    background:linear-gradient(135deg,rgba(0,56,168,.18) 0%,rgba(4,9,26,.4) 100%)!important;
    border:1px solid rgba(212,175,55,.16)!important;
    border-top:2px solid rgba(212,175,55,.35)!important;
    border-radius:6px!important;
    padding:.7rem 1rem!important;
    transition:border-color .15s!important;
}}
[data-testid="metric-container"]:hover{{border-top-color:{GOLD}!important}}
[data-testid="metric-container"] label{{
    color:rgba(245,225,122,.55)!important;
    font-size:.61rem!important;
    letter-spacing:.14em!important;
    text-transform:uppercase!important;
    font-family:'IBM Plex Mono',monospace!important;
}}
[data-testid="stMetricValue"]{{
    color:{GOLD}!important;
    font-size:1.35rem!important;
    font-weight:600!important;
    font-family:'Playfair Display',Georgia,serif!important;
}}

/* ════════════════════════════════════════════
   EXPANDERS
   ════════════════════════════════════════════ */
.stExpander{{
    border:1px solid rgba(212,175,55,.14)!important;
    border-radius:6px!important;
    background:rgba(4,9,26,.35)!important;
    margin-bottom:.55rem!important;
}}
.stExpander summary{{
    color:{LT_GOLD}!important;
    font-family:'IBM Plex Mono',monospace!important;
    font-size:.75rem!important;
    letter-spacing:.08em!important;
    padding:.65rem 1rem!important;
}}
.stExpander summary:hover{{color:{GOLD}!important}}
.stExpander [data-testid="stExpanderDetails"]{{
    border-top:1px solid rgba(212,175,55,.1)!important;
    padding-top:.8rem!important;
}}

/* ════════════════════════════════════════════
   DATAFRAMES
   ════════════════════════════════════════════ */
[data-testid="stDataFrame"]{{
    border:1px solid rgba(212,175,55,.13)!important;
    border-radius:5px!important;
    overflow:hidden!important;
}}

/* ════════════════════════════════════════════
   HR DIVIDER
   ════════════════════════════════════════════ */
hr{{
    border:none!important;
    border-top:1px solid rgba(212,175,55,.12)!important;
    margin:1.2rem 0!important;
    position:relative!important;
}}

/* ════════════════════════════════════════════
   SCROLLBAR
   ════════════════════════════════════════════ */
::-webkit-scrollbar{{width:4px;height:4px}}
::-webkit-scrollbar-track{{background:rgba(4,9,26,.8)}}
::-webkit-scrollbar-thumb{{background:rgba(212,175,55,.2);border-radius:2px}}
::-webkit-scrollbar-thumb:hover{{background:rgba(212,175,55,.4)}}

/* ════════════════════════════════════════════
   COMMAND CENTER
   ════════════════════════════════════════════ */
.cmd-center{{
    background:linear-gradient(135deg,rgba(0,56,168,.08) 0%,rgba(4,9,26,.5) 100%);
    border:1px solid rgba(212,175,55,.2);
    border-top:3px solid {GOLD};
    border-radius:6px;
    padding:1.2rem 1.5rem 1rem;
    margin-bottom:1.2rem;
    box-shadow:0 4px 24px rgba(0,0,0,.25);
}}
.cmd-label{{
    font-size:.56rem;
    color:{LT_GOLD};
    opacity:.7;
    letter-spacing:.22em;
    margin-bottom:.4rem;
    text-transform:uppercase;
    font-family:'IBM Plex Mono',monospace;
}}

/* ════════════════════════════════════════════
   PARCHMENT — SCHOLARLY BOX (spec-exact + enhanced)
   ════════════════════════════════════════════ */
/* Update this specific section in your st.markdown CSS */
.scholarly-box {
    background-color: #fdfaf3 !important; /* Parchment white */
    border-left: 5px solid #4a3728 !important;
    padding: 25px !important;
    border-radius: 8px !important;
    font-family: 'serif' !important;
    color: #1a1a1a !important; /* FORCE DARK CHARCOAL TEXT */
    line-height: 1.6 !important;
}

/* Force all text inside the box (paragraphs, lists) to be dark */
.scholarly-box p, .scholarly-box li, .scholarly-box div {
    color: #1a1a1a !important;
    font-size: 1.1rem !important;
}
.scholarly-box h2{{
    font-family:'Playfair Display',Georgia,serif;
    color:{BROWN};
    border-bottom:1px solid rgba(74,55,40,.15);
    padding-bottom:.25rem;
    margin:1.3rem 0 .6rem;
    font-size:1.18rem;
    font-weight:600;
    letter-spacing:.015em;
    text-align:center;
}}
.scholarly-box h3{{
    font-family:'Crimson Text',Georgia,serif;
    color:#5a4030;
    margin:.9rem 0 .4rem;
    font-size:1.04rem;
    font-style:italic;
    font-weight:600;
}}
.scholarly-box strong{{color:{BROWN};font-weight:600}}
.scholarly-box em{{color:#5a4030;font-style:italic}}
.scholarly-box code{{
    background:rgba(74,55,40,.07);
    padding:1px 6px;
    border-radius:3px;
    font-family:'IBM Plex Mono',monospace;
    font-size:.88em;
    color:#5a3020;
}}
.scholarly-box p{{margin:.6rem 0;text-align:justify}}

/* ════════════════════════════════════════════
   METADATA PANEL
   ════════════════════════════════════════════ */
.meta-panel{{
    background:linear-gradient(180deg,rgba(0,56,168,.08) 0%,rgba(4,9,26,.3) 100%);
    border:1px solid rgba(212,175,55,.15);
    border-radius:6px;
    padding:1.05rem 1.1rem;
}}
.meta-lbl{{
    font-size:.55rem;
    color:{LT_GOLD};
    opacity:.65;
    letter-spacing:.18em;
    margin-bottom:.12rem;
    text-transform:uppercase;
    font-family:'IBM Plex Mono',monospace;
}}
.meta-val{{
    font-size:.78rem;
    color:{CREAM};
    margin-bottom:.7rem;
    line-height:1.6;
    font-family:'IBM Plex Mono',monospace;
    border-bottom:1px solid rgba(212,175,55,.07);
    padding-bottom:.5rem;
}}

/* ════════════════════════════════════════════
   SCHOLAR CARD
   ════════════════════════════════════════════ */
.scholar-card{{
    background:linear-gradient(135deg,rgba(4,9,26,.8) 0%,rgba(7,16,31,.95) 100%);
    border:1px solid rgba(212,175,55,.18);
    border-left:4px solid {GOLD};
    border-radius:0 5px 5px 0;
    padding:.95rem 1.15rem;
    margin-bottom:.8rem;
    box-shadow:0 2px 10px rgba(0,0,0,.2);
    transition:border-left-color .15s;
}}
.scholar-card:hover{{border-left-color:{LT_GOLD}}}

/* ════════════════════════════════════════════
   CROSS-REFERENCE BADGE
   ════════════════════════════════════════════ */
.xref-badge{{
    background:rgba(102,2,60,.45);
    color:{LT_GOLD};
    font-size:.6rem;
    padding:2px 8px;
    border-radius:3px;
    border:1px solid rgba(212,175,55,.25);
    white-space:nowrap;
    display:inline-block;
    margin:2px 3px 2px 0;
    letter-spacing:.06em;
    font-family:'IBM Plex Mono',monospace;
    transition:background .12s;
}}
.xref-badge:hover{{background:rgba(212,175,55,.15)}}

/* ════════════════════════════════════════════
   SECTION DIVIDER — ornamental
   ════════════════════════════════════════════ */
.ornament{{
    text-align:center;
    color:rgba(212,175,55,.3);
    font-size:.8rem;
    letter-spacing:.5em;
    margin:.6rem 0;
    user-select:none;
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# RENDERER UTILITIES
# ─────────────────────────────────────────────

def sec_head(title, sub=""):
    """Centered serif section header with optional subtitle."""
    sub_html = (
        f'<div style="font-size:.6rem;color:{LT_GOLD};opacity:.6;'
        f'letter-spacing:.12em;margin-top:.18rem;text-transform:uppercase;'
        f'font-family:IBM Plex Mono,monospace">{sub}</div>'
    ) if sub else ""
    st.markdown(
        f'<div style="text-align:center;margin:1.1rem 0 .7rem;padding-bottom:.5rem;'
        f'border-bottom:1px solid rgba(212,175,55,.22)">'
        f'<div style="font-family:Playfair Display,Georgia,serif;font-size:1.1rem;'
        f'font-weight:600;color:{GOLD};letter-spacing:.03em;line-height:1.3">'
        f'{title}</div>{sub_html}'
        f'</div>',
        unsafe_allow_html=True)


def ornament():
    """Thin decorative separator."""
    st.markdown(
        f'<div class="ornament">· · ✦ · ·</div>',
        unsafe_allow_html=True)


def card(body, accent=None):
    a = accent or GOLD
    st.markdown(
        f'<div style="background:linear-gradient(135deg,rgba(4,9,26,.8) 0%,'
        f'rgba(7,16,31,.95) 100%);border:1px solid rgba(212,175,55,.15);'
        f'border-left:3px solid {a};border-radius:0 5px 5px 0;'
        f'padding:.9rem 1.1rem;margin-bottom:.8rem;'
        f'box-shadow:0 2px 10px rgba(0,0,0,.18)">{body}</div>',
        unsafe_allow_html=True)


def scholar_card(author, work, body):
    st.markdown(
        f'<div class="scholar-card">'
        f'<div style="font-family:Playfair Display,Georgia,serif;font-size:.97rem;'
        f'font-weight:600;color:{GOLD};margin-bottom:.1rem">{author}</div>'
        f'<div style="font-size:.59rem;color:{LT_GOLD};opacity:.65;letter-spacing:.06em;'
        f'margin-bottom:.55rem;font-style:italic;font-family:IBM Plex Mono,monospace">{work}</div>'
        f'<div style="font-size:.82rem;color:{CREAM};line-height:1.9;'
        f'font-family:IBM Plex Mono,monospace">{body}</div>'
        f'</div>', unsafe_allow_html=True)


def parchment(md_text):
    """Render AI markdown inside the spec-exact scholarly-box with enhanced typography."""
    h = md_text
    h = re.sub(r'(?m)^## (.+)$', r'<h2>\1</h2>', h)
    h = re.sub(r'(?m)^### (.+)$', r'<h3>\1</h3>', h)
    h = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', h)
    h = re.sub(r'\*(.+?)\*', r'<em>\1</em>', h)
    h = re.sub(r'`(.+?)`', r'<code>\1</code>', h)
    parts = h.split("\n\n")
    html_parts = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<h"):
            html_parts.append(p)
        else:
            html_parts.append(f"<p>{p.replace(chr(10), '<br>')}</p>")
    st.markdown(
        f'<div class="scholarly-box">{" ".join(html_parts)}</div>',
        unsafe_allow_html=True)


# ─────────────────────────────────────────────
# API KEY GETTERS
# ─────────────────────────────────────────────

def get_anthropic_key():
    try: return st.secrets["ANTHROPIC_API_KEY"]
    except: return ""

def get_esv_key():
    try: return st.secrets["ESV_API_KEY"]
    except: return ""

def get_api_bible_key():
    try: return st.secrets["BIBLE_API_KEY"]
    except: return ""


# ─────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────

KJV_FALLBACK = {
    "John 3:16": [
        {"verse": 16, "text": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life."}
    ],
    "Romans 8:28": [
        {"verse": 28, "text": "And we know that all things work together for good to them that love God, to them who are the called according to his purpose."}
    ],
    "Isaiah 53:5": [
        {"verse": 5, "text": "But he was wounded for our transgressions, he was bruised for our iniquities: the chastisement of our peace was upon him; and with his stripes we are healed."}
    ],
    "Genesis 1:1": [
        {"verse": 1, "text": "In the beginning God created the heaven and the earth."}
    ],
    "Hebrews 11:1": [
        {"verse": 1, "text": "Now faith is the substance of things hoped for, the evidence of things not seen."}
    ],
    "John 1:1": [
        {"verse": 1, "text": "In the beginning was the Word, and the Word was with God, and the Word was God."},
        {"verse": 2, "text": "The same was in the beginning with God."},
        {"verse": 3, "text": "All things were made by him; and without him was not any thing made that was made."},
        {"verse": 14, "text": "And the Word was made flesh, and dwelt among us, (and we beheld his glory, the glory as of the only begotten of the Father,) full of grace and truth."},
    ],
    "Philippians 2:5": [
        {"verse": 5, "text": "Let this mind be in you, which was also in Christ Jesus:"},
        {"verse": 6, "text": "Who, being in the form of God, thought it not robbery to be equal with God:"},
        {"verse": 7, "text": "But made himself of no reputation, and took upon him the form of a servant, and was made in the likeness of men:"},
        {"verse": 8, "text": "And being found in fashion as a man, he humbled himself, and became obedient unto death, even the death of the cross."},
        {"verse": 9, "text": "Wherefore God also hath highly exalted him, and given him a name which is above every name:"},
        {"verse": 10, "text": "That at the name of Jesus every knee should bow, of things in heaven, and things in earth, and things under the earth;"},
        {"verse": 11, "text": "And that every tongue should confess that Jesus Christ is Lord, to the glory of God the Father."},
    ],
    "Psalm 22:1": [
        {"verse": 1, "text": "My God, my God, why hast thou forsaken me? why art thou so far from helping me, and from the words of my roaring?"},
        {"verse": 16, "text": "For dogs have compassed me: the assembly of the wicked have inclosed me: they pierced my hands and my feet."},
        {"verse": 18, "text": "They part my garments among them, and cast lots upon my vesture."},
    ],
    "Daniel 7:13": [
        {"verse": 13, "text": "I saw in the night visions, and, behold, one like the Son of man came with the clouds of heaven, and came to the Ancient of days, and they brought him near before him."},
        {"verse": 14, "text": "And there was given him dominion, and glory, and a kingdom, that all people, nations, and languages, should serve him: his dominion is an everlasting dominion, which shall not pass away, and his kingdom that which shall not be destroyed."},
    ],
    "Exodus 3:14": [
        {"verse": 14, "text": "And God said unto Moses, I AM THAT I AM: and he said, Thus shalt thou say unto the children of Israel, I AM hath sent me unto you."}
    ],
    "Romans 3:21": [
        {"verse": 21, "text": "But now the righteousness of God without the law is manifested, being witnessed by the law and the prophets;"},
        {"verse": 22, "text": "Even the righteousness of God which is by faith of Jesus Christ unto all and upon all them that believe: for there is no difference:"},
        {"verse": 23, "text": "For all have sinned, and come short of the glory of God;"},
        {"verse": 24, "text": "Being justified freely by his grace through the redemption that is in Christ Jesus:"},
        {"verse": 25, "text": "Whom God hath set forth to be a propitiation through faith in his blood, to declare his righteousness for the remission of sins that are past, through the forbearance of God;"},
        {"verse": 26, "text": "To declare, I say, at this time his righteousness: that he might be just, and the justifier of him which believeth in Jesus."},
    ],
    "Matthew 16:13": [
        {"verse": 13, "text": "When Jesus came into the coasts of Caesarea Philippi, he asked his disciples, saying, Whom do men say that I the Son of man am?"},
        {"verse": 14, "text": "And they said, Some say that thou art John the Baptist: some, Elias; and others, Jeremias, or one of the prophets."},
        {"verse": 15, "text": "He saith unto them, But whom say ye that I am?"},
        {"verse": 16, "text": "And Simon Peter answered and said, Thou art the Christ, the Son of the living God."},
        {"verse": 17, "text": "And Jesus answered and said unto him, Blessed art thou, Simon Bar-jona: for flesh and blood hath not revealed it unto thee, but my Father which is in heaven."},
    ],}


INTERLINEAR = {
    "John 3:16": [
        ("For",           "Οὕτως",       "G3779", "houtōs — in this manner, thus"),
        ("God",           "Θεός",        "G2316", "theos — God; the one true God"),
        ("so loved",      "ἠγάπησεν",    "G25",   "agapaō (aorist) — loved with self-giving love"),
        ("the world",     "τὸν κόσμον",  "G2889", "kosmos — the created order; humanity in alienation"),
        ("that he gave",  "ἔδωκεν",      "G1325", "didōmi (aorist) — gave as a completed, irreversible act"),
        ("his only Son",  "τὸν μονογενῆ","G3439", "monogenēs — unique, only of its kind; not merely 'only-begotten'"),
        ("that whoever",  "ἵνα πᾶς",     "G2443/G3956", "hina (purpose) + pas (every/all without exception)"),
        ("believes",      "πιστεύων",    "G4100", "pisteuō (present participle) — ongoing belief, not one-time decision"),
        ("should not perish","μὴ ἀπόληται","G622", "apollymi — to be utterly destroyed; Johannine antithesis to ζωή"),
        ("eternal life",  "ζωὴν αἰώνιον","G2222/G166","zōē aiōnios — life of the age to come; qualitative not merely durational"),
    ],
    "John 1:1": [
        ("In the beginning","Ἐν ἀρχῇ",   "G1722/G746","en archē — echoes LXX Gen 1:1 בְּרֵאשִׁית deliberately"),
        ("was",           "ἦν",          "G1510", "eimi (imperfect) — continuous existence prior to creation; not 'came to be'"),
        ("the Word",      "ὁ Λόγος",     "G3056", "ho Logos — the Word; divine rational principle; personal, not abstract"),
        ("with God",      "πρὸς τὸν Θεόν","G4314","pros — face to face with; intimate personal distinction within unity"),
        ("was God",       "Θεὸς ἦν",     "G2316", "theos — anarthrous predicate: qualitative divine nature; refutes Arian 'a god'"),
    ],
    "Philippians 2:6": [
        ("being",         "ὑπάρχων",     "G5225", "hyparchō — pre-existent, continuous state before Incarnation"),
        ("in the form",   "ἐν μορφῇ",    "G3444", "morphē — the essential, inner nature (vs. σχῆμα outward appearance)"),
        ("of God",        "Θεοῦ",        "G2316", "theou — genitive: the form that belongs to/constitutes God"),
        ("did not regard","οὐχ ἡγήσατο", "G2233", "hēgeomai — did not consider, reckon, calculate as something to exploit"),
        ("equality",      "ἴσα",         "G2470", "isos — equal in quantity and quality; equality of nature, not merely rank"),
        ("emptied himself","ἐκένωσεν",   "G2758", "kenoō — the kenōsis; stripped of divine prerogatives, not divine nature"),
        ("servant",       "δούλου",      "G1401", "doulos — slave, not merely servant; the lowest social status in Roman society"),
    ],
    "Romans 3:23": [
        ("all",           "πάντες",      "G3956", "pantes — all without exception; Jew and Gentile included"),
        ("have sinned",   "ἥμαρτον",     "G264",  "hamartanō (aorist) — sinned; completed act with universal scope"),
        ("fall short",    "ὑστεροῦνται", "G5302", "hystereō (present passive) — ongoing state of deficiency; not past event"),
        ("glory of God",  "δόξης τοῦ Θεοῦ","G1391","doxa — the divine splendor; the image-bearing capacity of humanity now corrupted"),
    ],
    "Exodus 3:14": [
        ("I AM",          "אֶהְיֶה",     "H1961", "ehyeh — first person imperfect of hayah: I will be/I am; causative existence"),
        ("THAT I AM",     "אֲשֶׁר אֶהְיֶה","H834/H1961","asher ehyeh — relative clause; self-defining existence; aseity"),
        ("LORD",          "יְהוָה",      "H3068", "YHWH — the tetragrammaton; derived from ehyeh; 'He who causes to be'"),
    ],
}  # end INTERLINEAR


STRONGS_LEXICON = {
    "grace":        {"num":"G5485","gk":"χάρις","tr":"charis","lang":"Greek",
                     "def":"Unmerited divine favor freely bestowed apart from works. Root: χαίρω (chairō) — to rejoice. Central to Pauline soteriology (Eph 2:8–9) and the Johannine Prologue (John 1:14,17)."},
    "faith":        {"num":"G4102","gk":"πίστις","tr":"pistis","lang":"Greek",
                     "def":"Conviction of truth; reliance upon Christ. Root: πείθω (peithō) — to persuade. In Heb 11:1 takes on juridical force: evidence presented in a legal proceeding."},
    "logos":        {"num":"G3056","gk":"λόγος","tr":"logos","lang":"Greek",
                     "def":"Word; divine rational principle; second Person in Johannine theology. Root: λέγω (legō) — to speak. Philo of Alexandria used logos as an intermediary between God and creation; John redefines it as personal and incarnate."},
    "agape":        {"num":"G26","gk":"ἀγάπη","tr":"agapē","lang":"Greek",
                     "def":"Self-sacrificial, unconditional love. Relatively rare in classical Greek; the LXX and NT elevate it as the characteristic divine love. Distinct from ἔρως (erotic) and φιλία (friendship)."},
    "covenant":     {"num":"H1285","gk":"בְּרִית","tr":"berith","lang":"Hebrew",
                     "def":"Binding agreement between parties; backbone of redemptive history. Root possibly בָּרָה (bara) — to cut (cf. 'cutting a covenant'). The OT traces six major covenants: Noahic, Abrahamic, Mosaic, Priestly, Davidic, New."},
    "shalom":       {"num":"H7965","gk":"שָׁלוֹם","tr":"shalom","lang":"Hebrew",
                     "def":"Completeness, wholeness, peace. Not merely absence of conflict but holistic flourishing. Root: שָׁלֵם (shalem) — to be complete. NT equivalent: εἰρήνη (eirēnē)."},
    "messiah":      {"num":"H4899","gk":"מָשִׁיחַ","tr":"mashiach","lang":"Hebrew",
                     "def":"Anointed One; divinely commissioned deliverer. LXX renders as Χριστός (Christos). Applied to priests (Lev 4:3), kings (1 Sam 24:6), and prophets (Ps 105:15) before finding its ultimate referent in Jesus."},
    "atonement":    {"num":"H3722","gk":"כָּפַר","tr":"kaphar","lang":"Hebrew",
                     "def":"To cover, atone, propitiate. Root meaning debated: 'to cover' (older view) or 'to wipe clean' (more recent). The Day of Atonement (Yom Kippur) derives from this root. NT equivalent: ἱλασμός (hilasmos, 1 John 2:2)."},
    "righteousness":{"num":"G1343","gk":"δικαιοσύνη","tr":"dikaiosynē","lang":"Greek",
                     "def":"Conformity to divine standard; in Paul, the status declared by God in justification (δικαίωσις). The Reformation debate: is imputed (forensic) or imparted (transformative)? Luther's tower experience centered on this word in Rom 1:17."},
    "propitiation": {"num":"G2435","gk":"ἱλαστήριον","tr":"hilastērion","lang":"Greek",
                     "def":"Mercy seat; place/means of appeasement. Used of the ark's cover (LXX Ex 25:17) and in Rom 3:25 of Christ. Debate: propitiation (wrath-satisfying, Packer, Morris) vs. expiation (sin-removing, Dodd). The former is supported by the OT background."},
    "justification":{"num":"G1347","gk":"δικαίωσις","tr":"dikaiōsis","lang":"Greek",
                     "def":"The act of declaring righteous; forensic acquittal. Paul uses this in Rom 4:25 and 5:18. Distinct from sanctification (ἁγιασμός): justification is instantaneous and complete; sanctification is progressive."},
    "sanctification":{"num":"G38","gk":"ἁγιασμός","tr":"hagiasmos","lang":"Greek",
                     "def":"The process of being set apart and made holy. Root: ἅγιος (hagios) — holy, set apart. In Pauline theology, distinct from justification; the ongoing work of the Spirit (Phil 2:12–13; 2 Cor 3:18)."},
    "pneuma":       {"num":"G4151","gk":"πνεῦμα","tr":"pneuma","lang":"Greek",
                     "def":"Spirit; wind; breath. Used of the Holy Spirit (capitalized) and the human spirit. Root: πνέω (pneō) — to blow. The Trinitarian debates of the 4th century turned partly on whether the Spirit proceeds from the Father alone (Eastern) or from Father and Son (Western filioque)."},
    "parousia":     {"num":"G3952","gk":"παρουσία","tr":"parousia","lang":"Greek",
                     "def":"Presence; arrival; the Second Coming of Christ. In Hellenistic usage, the technical term for a royal visit. Paul uses it for the return of Christ (1 Thess 4:15; 2 Thess 2:1). Central to both amillennial and premillennial eschatology."},
    "ekklesia":     {"num":"G1577","gk":"ἐκκλησία","tr":"ekklēsia","lang":"Greek",
                     "def":"Assembly of called-out ones; the Church. Root: ἐκ + καλέω — out of + to call. In Greek civic life, the assembly of citizens. Jesus uses it only in Matt 16:18 and 18:17 in the Gospels, but it becomes Paul's standard term."},
    "sozo":         {"num":"G4982","gk":"σῴζω","tr":"sōzō","lang":"Greek",
                     "def":"To save, rescue, preserve. Used of physical healing (Mark 5:34) and spiritual salvation (Eph 2:8). The range of meaning is important: salvation in the NT is holistic — body and soul."},
    "logos_sarx":   {"num":"G4561","gk":"σάρξ","tr":"sarx","lang":"Greek",
                     "def":"Flesh. In John 1:14 ('the Word became flesh'): not sinful nature but creaturely, physical human existence. Paul uses sarx for sinful nature (Rom 7:18); John uses it for the Incarnation's full humanity."},
    "bara":         {"num":"H1254","gk":"בָּרָא","tr":"bara'","lang":"Hebrew",
                     "def":"To create; used exclusively with God as subject throughout the Hebrew Bible. The strongest lexical support for creatio ex nihilo. Distinct from יָצַר (yatsar, to form) and עָשָׂה (asah, to make)."},
    "hesed":        {"num":"H2617","gk":"חֶסֶד","tr":"hesed","lang":"Hebrew",
                     "def":"Steadfast love, covenant loyalty, lovingkindness. Virtually untranslatable. Combines love, loyalty, mercy, and faithfulness. Used 247 times in OT, 127 in Psalms alone. The LXX renders it as ἔλεος (eleos, mercy) or χάρις (grace)."},
    "morphe":       {"num":"G3444","gk":"μορφή","tr":"morphē","lang":"Greek",
                     "def":"Essential form; inner nature as it shows itself outwardly. In Phil 2:6, 'form of God' denotes Christ's essential divine nature. Distinct from σχῆμα (schēma, outward fashion, v. 8) and εἰκών (eikōn, image)."},
}  # end STRONGS_LEXICON


COMMENTARY = {

"John 3:16": {
"label": "The Gospel in Miniature",
"context": "The Nicodemus discourse (John 3:1–21) occurs at night — Johannine irony: spiritual darkness meeting the divine light who declares himself the light of the world (8:12). Nicodemus is not a naive inquirer but a Pharisee and member of the Sanhedrin (ἄρχων, archōn), making his clandestine visit theologically loaded. The passage transitions at v. 13 from dialogue to Johannine reflection, meaning vv. 16–21 are likely the Evangelist's own theological commentary rather than the words of Jesus verbatim. This does not diminish their authority but contextualizes their rhetorical function.",
"scholars": [
{"author":"Raymond E. Brown","work":"The Gospel According to John, Anchor Bible (1966), Vol. I, pp. 133–136 — Analytical Summary",
"text":"Brown's treatment locates κόσμος not as a subset of humanity deserving love but as the created order in its totality, organized in alienation from its Creator. The aorist ἔδωκεν ('gave') signals an act completed and irreversible in its historical consequences — the Incarnation as the hinge of universal history. Brown reads this within his realized eschatology framework: for the Fourth Gospel, judgment is not deferred to a future tribunal but is operative now in the human response to the revealer. Faith in the Son is simultaneously acquittal; unbelief is simultaneously condemnation (v. 18)."},
{"author":"D.A. Carson","work":"The Gospel According to John, Pillar NT Commentary (1991), pp. 204–206 — Analytical Summary",
"text":"Carson argues the verse cannot sustain universalist readings: 'God so loved the world' functions rhetorically to stress the immensity of divine condescension — that God would love a world so utterly opposed to him — not as a guarantee of universal salvation. The μονογενής ('only-begotten' or more precisely 'unique, one-of-a-kind') must be distinguished from adoptive sonship language used elsewhere; the Son's filial relation to the Father is ontologically unique. Carson also addresses the ἵνα clause as expressing purpose, not mere result: the Incarnation is a teleological act aimed at eschatological rescue."},
{"author":"Leon Morris","work":"The Gospel According to John, NICNT, revised edition (1995), p. 225 — Analytical Summary",
"text":"Morris, one of the most rigorous Johannine scholars of the 20th century, underscores the gravity of the negative construction: 'should not perish' (μὴ ἀπόληται). Perdition — utter destruction — is the default condition without divine intervention. This is not the language of mild inconvenience but of eternal catastrophe. Morris also wrestles with the extent of the atonement: the 'world' (κόσμος) God loves is the world of sinners, not merely an elect subset, placing the verse in tension with limited atonement interpretations that require careful handling."},
],
"greek": [
("G2889","κόσμος","kosmos","The created order; in John, often the system of human existence organized in opposition to God. Used 78 times in John — more than any other NT book."),
("G3439","μονογενής","monogenēs","Only-begotten; unique; 'of a single kind.' Patristic Christology anchored the homoousios debates at Nicaea on this term. The Arian reading ('first-created') was refuted by appeal to the term's qualitative, not generative, force."),
("G622","ἀπόλλυμι","apollymi","To perish, be utterly ruined. The Johannine antithesis to ζωὴν αἰώνιον (eternal life). Not annihilation in the sleep-of-death sense but catastrophic, irreversible loss."),
("G4100","πιστεύω","pisteuō","To believe; trust; commit oneself to. The present active participle (πιστεύων) denotes ongoing, habitual trust — not a one-time intellectual assent but an abiding orientation."),
],
"cross_refs": [
("John 1:14","The Word became flesh — the Incarnation that John 3:16 presupposes, established in the Prologue"),
("Rom 5:8","God demonstrates His love: while we were still sinners, Christ died — Paul's parallel to the Johannine declaration"),
("1 John 4:9–10","By this the love of God was manifested — He sent His only-begotten Son; He is the propitiation"),
("Gen 22:2","Typological anticipation: God commands Abraham, 'Take your only son, Isaac, whom you love' — deliberate verbal echo"),
("John 12:47","I did not come to judge the world, but to save the world — the positive telos of the mission"),
],
"historical": "The Nicodemus pericope reflects the Sitz im Leben of the Johannine community's late-first-century debates with Pharisaic Judaism following the destruction of Jerusalem (AD 70) and the consolidation of rabbinic authority at Jamnia (c. AD 90). The night setting echoes Gethsemane (John 13:30: 'and it was night') and forms a bracketing motif. Nicodemus reappears at 7:50 (defending Jesus before the Sanhedrin) and 19:39 (anointing the body), his trajectory from nocturnal secrecy to public identification with the crucified Christ forming one of John's most carefully constructed character arcs.",
"apologetics": "John 3:16 anchors the coherence argument for Christian theism: it identifies divine agency (God acted), historical particularity (gave His Son at a specific point in history), the mechanism of appropriation (belief), and the eschatological stakes (eternal life vs. perishing). The verse answers the deist's objection that a transcendent Creator would have no reason to engage with particular human beings — it claims precisely such engagement as the central act of divine self-disclosure.",
},

"John 1:1-18": {
"label": "The Johannine Prologue",
"context": "John 1:1–18, the Prologue, is the most densely theological passage in the NT and the primary locus of Christological debate from the 2nd century to the present. Its hymnic structure (identified by most scholars as an early Christian hymn adapted by the Evangelist) moves from the Word's pretemporal existence (vv. 1–2), through creation (v. 3), revelation (vv. 4–9), rejection (vv. 10–11), reception (v. 12–13), and finally Incarnation (v. 14), before identifying the Word as Jesus Christ (v. 17). The chiastic structure mirrors Genesis 1, deliberately presenting Jesus as the agent of a new creation.",
"scholars": [
{"author":"Raymond E. Brown","work":"The Gospel According to John, Anchor Bible (1966), Vol. I, pp. 1–37 — Analytical Summary",
"text":"Brown's landmark analysis of the Prologue identifies three strata: the original hymn, prose insertions about John the Baptist (vv. 6–8, 15), and the Evangelist's interpretive additions. His treatment of ὁ Λόγος situates the background in both Hellenistic philosophy (Stoic logos as the rational principle pervading the cosmos) and Hebrew Wisdom traditions (Prov 8:22–31; Sirach 24; Wisdom of Solomon 7:22–8:1). Brown's conclusion: the Evangelist deliberately drew on both streams to present Jesus as the fulfillment of both the Greek philosophical quest and the Hebrew covenantal promise."},
{"author":"D.A. Carson","work":"The Gospel According to John, Pillar NT Commentary (1991), pp. 111–139 — Analytical Summary",
"text":"Carson's exegesis of v. 1c ('and the Word was God') addresses the anarthrous predicate theos with linguistic rigor. The absence of the article before θεός does not, pace Jehovah's Witness rendering, make it indefinite ('a god'). Colwell's Rule and the subsequent refinements by Harner and Dixon establish that anarthrous predicate nouns before the verb are typically qualitative — denoting the nature or essence of the subject. The Word shares the divine nature; John does not say 'the Word was the God' (which would collapse the distinction of persons) but 'the Word was God' (which affirms shared divine essence while preserving personal distinction)."},
{"author":"Andreas Köstenberger","work":"John, Baker Exegetical Commentary (2004), pp. 25–58 — Analytical Summary",
"text":"Köstenberger's structural analysis establishes the Prologue's chiastic architecture: A (the Word with God, v. 1–2), B (the Word as Creator, v. 3), C (the Word as Life and Light, v. 4–5), D (John's witness, v. 6–8), C' (the true Light, v. 9–11), B' (the new creation through reception, v. 12–13), A' (the Word incarnate with the Father, v. 14–18). This structure demonstrates that v. 14 — 'the Word became flesh' — is the structural and theological climax: the entire movement of the Prologue converges on the Incarnation as the defining event of the divine self-disclosure."},
],
"greek": [
("G3056","λόγος","logos","Word; rational principle; divine agent. In Stoic philosophy: the rational principle pervading the cosmos. In Hebraic Wisdom literature: the personified Wisdom of Prov 8. John takes both streams and identifies their referent as the historical Jesus."),
("G1510","ἦν","ēn","Was (imperfect of eimi). The continuous past tense is deliberate: the Word did not 'come to be' (γίνομαι, ginomai — used of creation in v. 3, 14) but existed continuously. This grammatical distinction is the exegetical basis for the eternal pre-existence of the Son."),
("G4561","σάρξ","sarx","Flesh; in v. 14, full creaturely human existence, not merely a body. Against Docetism (the heresy that Christ only appeared human), John insists the Word became genuinely, materially human — the strongest anti-Docetic statement in the NT."),
("G3306","μονογενής — see John 3:16 entry","—","In v. 14 and 18, the 'only-begotten' or 'unique' Son mediates the revelation of the Father — making the Prologue's Christology simultaneously about the Son's nature and his epistemological function."),
],
"cross_refs": [
("Gen 1:1","In the beginning God created — the deliberate verbal echo establishes Jesus as the agent of a new creation"),
("Prov 8:22–31","Wisdom present at creation, beside God as a master craftsman — the Wisdom Christology background"),
("Col 1:15–17","He is the image of the invisible God, the firstborn over all creation; in Him all things were created"),
("Heb 1:1–3","God, having spoken in many ways, has in these last days spoken to us in His Son — parallel Christological prologue"),
("Rev 19:13","His name is called The Word of God — the Apocalypse returns to Johannine Logos Christology"),
],
"historical": "The Prologue's Logos language reflects the 1st-century intellectual environment in which the Johannine community operated. Philo of Alexandria (c. 20 BC – AD 50) had already used logos as an intermediary divine principle between the transcendent God and material creation. By identifying Jesus as the Logos who 'became flesh' (ἐσκήνωσεν, 'pitched his tent' — deliberately evoking the Tabernacle), John makes the most radical claim in religious history: the mediating principle of the cosmos is not an abstract force but a specific human being who lived in first-century Palestine.",
"apologetics": "The Prologue is the primary NT text for the Christological argument. The deity of Christ claim rests on three grammatical observations: (1) the imperfect ἦν ('was') vs. the aorist ἐγένετο ('became') establishes pretemporal existence vs. created origin; (2) the anarthrous θεός in v. 1c is qualitative, not indefinite; (3) v. 18 identifies Jesus as the 'only-begotten God' (μονογενὴς θεός in P66, P75, Sinaiticus, Vaticanus — the best manuscript tradition). Against the Jehovah's Witnesses' 'a god' rendering: no first-century monotheistic Jew could write 'in the beginning was the Word, and the Word was with God, and the Word was a god' — that would be polytheism.",
},

"Romans 3:21-26": {
"label": "The Heart of Pauline Soteriology",
"context": "Romans 3:21–26 is, as Leon Morris called it, 'possibly the most important single paragraph ever written.' It constitutes the theological pivot of the entire letter: having established universal human guilt (1:18–3:20), Paul now presents the divine solution. The passage introduces three foundational soteriological concepts simultaneously: justification (δικαίωσις), redemption (ἀπολύτρωσις), and propitiation (ἱλαστήριον). The density of theological vocabulary in six verses is unparalleled in Paul.",
"scholars": [
{"author":"Douglas Moo","work":"The Letter to the Romans, NICNT, 2nd edition (2018), pp. 219–248 — Analytical Summary",
"text":"Moo's treatment of ἱλαστήριον ('propitiation,' v. 25) engages the debate between C.H. Dodd's expiation reading (sin is removed, wrath is not in view) and Leon Morris's propitiation reading (divine wrath is satisfied). Moo sides decisively with Morris: the OT background of the mercy seat (כַּפֹּרֶת, the lid of the Ark in Lev 16), the context of Romans 1:18–3:20 which has established God's wrath as the presenting problem, and the Pauline parallel in Romans 5:9 all require that God's righteous anger against sin is the referent being addressed. The verse does not present an internal divine conflict (the Father punishing the Son) but the Father himself providing what justice requires."},
{"author":"Thomas R. Schreiner","work":"Romans, Baker Exegetical Commentary (1998), pp. 183–200 — Analytical Summary",
"text":"Schreiner's exegesis of 'the righteousness of God' (δικαιοσύνη θεοῦ) in vv. 21–22 navigates the major interpretive options: (a) God's own attribute of justice (the Reformation reading, Luther); (b) God's saving activity (Ernst Käsemann); (c) the righteous status God gives believers (traditional Protestant). Schreiner argues the phrase is intentionally polyvalent — it denotes both God's attribute (he is righteous) and his saving action (he declares sinners righteous), resolving the seeming contradiction of how God can be simultaneously just and the justifier of the ungodly (v. 26)."},
{"author":"N.T. Wright","work":"Romans, New Interpreter's Bible Commentary (2002), pp. 464–480 — Analytical Summary",
"text":"Wright's New Perspective reading reframes 'righteousness of God' as covenant faithfulness — God's faithfulness to the Abrahamic covenant promises. The problem Paul addresses is not primarily 'how can sinful individuals be accepted by a holy God?' (the Lutheran framing) but 'how does God's covenantal faithfulness extend to Gentiles?' Wright's reading does not eliminate individual justification but relocates it within corporate, eschatological, and covenantal categories. This reading is contested by Schreiner, Moo, and Piper, who argue it underweights Paul's concern for personal guilt and acquittal."},
],
"greek": [
("G1343","δικαιοσύνη","dikaiosynē","Righteousness; the divine standard and the status declared when met. The Reformation debate turned on whether this is imputed (forensic, external) or imparted (transformative, internal). Paul's use in vv. 21–22 supports the former: it is 'witnessed by the Law and Prophets' and 'through faith in Jesus Christ.'"),
("G629","ἀπολύτρωσις","apolytrōsis","Redemption; literally 'the buying back' of slaves or prisoners of war. The metaphor imports the slave market and the battlefield — humanity as enslaved to sin requires a ransom price."),
("G2435","ἱλαστήριον","hilastērion","Mercy seat / propitiation. LXX uses this term for the כַּפֹּרֶת in Lev 16 — the place where blood was sprinkled on the Day of Atonement. Paul presents Christ as the new, final, and sufficient mercy seat."),
("G3952","πάρεσις","paresis","Passing over (v. 25); distinct from ἄφεσις (forgiveness). God had passed over sins previously committed without final adjudication — the cross resolves the outstanding moral debt of all pre-Incarnation history."),
],
"cross_refs": [
("Lev 16:2–16","The Day of Atonement ritual — the direct OT background for ἱλαστήριον in v. 25"),
("Isa 53:11","By his knowledge the Righteous One will justify the many — the Servant Song background for justification"),
("Rom 5:9","Justified by his blood, we shall be saved from the wrath of God — confirming propitiation as wrath-related"),
("2 Cor 5:21","He made him who knew no sin to be sin on our behalf — the imputation parallel"),
("Gal 3:13","Christ redeemed us from the curse of the Law, becoming a curse for us — penal substitution explicit"),
],
"historical": "Paul wrote Romans c. AD 57 from Corinth, preparing for his Jerusalem visit (Acts 20:3) and his planned mission to Spain via Rome. The letter addresses a community experiencing Jew-Gentile tensions following the return of Jewish Christians expelled by the Edict of Claudius (AD 49). Romans 3:21–26 addresses the universal scope of the gospel: there is no distinction (v. 22) between Jew and Gentile before God's tribunal, because the standard (God's righteousness) applies universally and the solution (faith in Christ) is available to all.",
"apologetics": "Romans 3:21–26 is the central text for the penal substitution debate. The primary objection (Steve Chalke: 'cosmic child abuse'; critics: divine masochism) misreads the passage. The Father is not punishing the Son against the Son's will — the doctrine of divine impassibility and the Trinitarian grammar of the passage both preclude this. Rather, God himself provides (v. 25: 'God set forth') what his own justice requires, at the cost of the Second Person's voluntary self-giving (Gal 2:20: 'who loved me and gave himself for me'). The resolution of justice and mercy in a single act is precisely what Paul calls the demonstration of God's righteousness.",
},

"Philippians 2:5-11": {
"label": "The Carmen Christi — Kenōsis and Exaltation",
"context": "Philippians 2:5–11 is universally recognized as the most important Christological passage in Paul's letters and one of the most contested in NT scholarship. Whether Paul is citing a pre-Pauline hymn (Lohmeyer, 1928) or composing original material remains debated, but the passage's hymnic structure — two strophes of descent (vv. 6–8) and ascent (vv. 9–11) — is beyond dispute. The theological stakes are enormous: the passage speaks directly to the pre-existence of Christ, the nature of the Incarnation, the relationship between divine and human natures, and the eschatological lordship of Christ.",
"scholars": [
{"author":"Gordon Fee","work":"Paul's Letter to the Philippians, NICNT (1995), pp. 191–229 — Analytical Summary",
"text":"Fee's magisterial treatment argues that μορφῇ θεοῦ ('form of God,' v. 6) denotes Christ's essential divine nature — the outer expression of inner reality — not a mere role or status. The crucial exegetical decision is the meaning of ἁρπαγμόν ('robbery' or 'something to be grasped') in v. 6. Fee follows the harpagmos-as-res-rapta reading (a thing already possessed, not yet seized): Christ possessed equality with God and chose not to exploit it for self-advantage. This reading makes the verse about the disposition of one who already possesses divinity, not about a creature aspiring to it."},
{"author":"N.T. Wright","work":"The Climax of the Covenant (1991), pp. 56–98 — Analytical Summary",
"text":"Wright's influential Adam Christology reading: the passage sets Christ in contrast with Adam. Adam (Gen 3) grasped at equality with God; Christ, who possessed it, did not grasp at it. The contrast is not between pre-existent divinity and humanity but between two responses to the human temptation of self-aggrandizement. Wright reads μορφῇ θεοῦ in light of the image-bearing language of Genesis: Adam was made in the image/form of God. Christ, unlike Adam, did not exploit his God-given status. This reading has been influential but is challenged by Fee and others who argue it underweights the evidence for pre-existence in v. 6."},
{"author":"Peter T. O'Brien","work":"Epistle to the Philippians, NIGTC (1991), pp. 205–268 — Analytical Summary",
"text":"O'Brien's grammatical analysis of ἐκένωσεν ('emptied himself,' v. 7) — the kenōsis — is definitive: the verb cannot mean Christ emptied himself of divine attributes (the 19th-century kenotic theology of Thomasius and Gore). The participle phrases that follow ('taking the form of a servant, being made in the likeness of men') specify the mode of the self-emptying, not its content. Christ emptied himself by adding a human nature, not by subtracting divine attributes. This preserves the Chalcedonian two-natures doctrine against kenotic reductionism."},
],
"greek": [
("G3444","μορφή","morphē","Essential form; the outward expression of inner nature. Distinguished from σχῆμα (schēma, outward fashion) and εἰκών (eikōn, image). In v. 6 'form of God' denotes Christ's essential divine nature; in v. 7 'form of a servant' denotes genuine human servile existence."),
("G2758","κενόω","kenoō","To empty; the kenōsis. Not a subtraction of divine attributes but an addition of human nature with its attendant limitations. The aorist form signals a completed act at a specific historical moment — the Incarnation."),
("G5013","ταπεινόω","tapeinoō","To humble, abase. In v. 8, Christ humbled himself — the voluntary, active self-abasement is the ethical model Paul invokes for the Philippian community's internal conflicts."),
("G5228","ὑπερυψόω","hyperypsoō","To exalt highly, super-exalt. Found only here in the NT. The divine response to Christ's humiliation is an exaltation that exceeds what was voluntarily relinquished — the eschatological reversal of the kenōsis."),
],
"cross_refs": [
("Isa 45:23","To me every knee will bow, every tongue will swear — the explicit OT background for vv. 10–11; YHWH's throne applied to Christ"),
("John 17:5","Glorify me together with Yourself, Father, with the glory I had with You before the world was — Jesus' own claim to pre-existent glory"),
("Col 1:15–17","The image of the invisible God, firstborn over all creation — parallel Pauline Christology"),
("Heb 2:9","We see Jesus, who was made a little lower than the angels, now crowned with glory and honor — the same descent-ascent pattern"),
("Gen 3:5","You will be like God — Adam's grasping in contrast to Christ's voluntary self-emptying"),
],
"historical": "The Carmen Christi's two-strophe structure — descent into servitude and death (vv. 6–8) and ascent to cosmic lordship (vv. 9–11) — reflects a liturgical pattern used in early Christian worship. If it is a pre-Pauline hymn (Lohmeyer's thesis), it would constitute one of the earliest Christological documents in existence, predating Paul's letters. The bestowing of 'the name above every name' (v. 9) — in the context of the Isaiah 45 allusion — identifies Jesus with the divine name YHWH, the most explicit ontological identification of Christ with Israel's God in the Pauline corpus.",
"apologetics": "Philippians 2:5–11 is the central text for the Incarnation argument. The passage directly addresses the deity of Christ in his pre-existent state (μορφῇ θεοῦ), the mechanism of the Incarnation (ἐκένωσεν), and the eschatological vindication that retrospectively confirms the identity claim. Against the 'merely a good moral teacher' objection (Bertrand Russell), the passage presents a figure who pre-existed creation, voluntarily became human, died as a criminal, and was subsequently identified with YHWH himself. C.S. Lewis's trilemma ('liar, lunatic, or Lord') finds its Pauline foundation here: the Christological claims are too specific and too ontologically loaded to permit a moralist reduction.",
},

"Isaiah 53:5": {
"label": "The Fourth Servant Song — Vicarious Atonement",
"context": "The Fourth Servant Song (Isa 52:13–53:12) is the most cited OT passage in the NT, with over 50 direct citations and allusions. The identity of the Servant is contested: the collective Israel interpretation (Ibn Ezra, modern critical scholarship), the ideal remnant Israel, or an individual (Origen, Jerome, Calvin, Oswalt). The Dead Sea Scroll 1QIsa-a (c. 125 BC) preserves the passage with 95% consonantal agreement with the Masoretic Text, establishing its textual stability centuries before the Christian era. The passage describes vicarious suffering as the mechanism of covenant restoration — a concept without parallel in ANE religious literature.",
"scholars": [
{"author":"John N. Oswalt","work":"The Book of Isaiah: Chapters 40–66, NICOT (1998), pp. 379–393 — Analytical Summary",
"text":"Oswalt's defense of Isaianic unity (against Deutero-Isaianic critical consensus) rests on linguistic continuity, thematic coherence, and the NT's consistent attribution to Isaiah. His exegesis of v. 5 focuses on the prepositional phrase מִפְּשָׁעֵינוּ (mip·pe·sha·'e·nu, 'because of our transgressions'): the min prefix denotes causation, not mere association. The Servant is not suffering alongside transgressors or sympathetically for them — he is suffering because of them, in their place, as their judicial substitute. This is the strongest single lexical argument for penal substitution in the OT."},
{"author":"E.J. Young","work":"The Book of Isaiah, NICOT (1972), Vol. III, pp. 340–355 — Analytical Summary",
"text":"Young's philological analysis examines חַבּוּרָתוֹ (chaburato, 'by his stripes/wounds' v. 5). The noun denotes the welt left by a blow — physical suffering of a specific, historical character. The causative construction ('by his wounds we are healed') imports transactional logic: the Servant's physical punishment is the precise mechanism of covenantal healing, not merely its occasion or accompaniment. Young's insistence on the physical, historical specificity of the Servant's suffering anticipates the NT's application to the Passion."},
{"author":"Klaus Baltzer","work":"Deutero-Isaiah: A Commentary on Isaiah 40–55, Hermeneia (2001), pp. 399–420 — Analytical Summary",
"text":"Baltzer represents the critical consensus: the Servant is a historical figure within Deutero-Isaiah's community, possibly a prophet or cultic figure whose death is interpreted vicariously by the community. This reading does not require prophetic foresight and situates the passage in its historical context. Evangelical interpreters engage this view by noting: (a) the NT citations treat the passage as predictive; (b) the individualizing features (silent before accusers, burial with the rich, post-mortem vindication) are difficult to apply to collective Israel; (c) the LXX translation (c. 250 BC) already interpreted the passage individually."},
],
"greek": [
("H6588","פֶּשַׁע","pesha'","Transgression; willful rebellion against the covenant Lord. One of three terms in vv. 5–6 forming a comprehensive taxonomy of human guilt: פֶּשַׁע (pesha', rebellion), חֵטְא (chet, sin as missing the mark), and עָוֺן (avon, iniquity/guilt)."),
("H4347","מַכָּה","makkah","Blow, wound, plague. The same root used in Exodus for the divine plagues (Ex 9:14). Applied here to the Servant, the language implies that the Servant is absorbing the covenantal judgment that properly belongs to Israel."),
("H7495","רָפָא","rapha'","To heal, restore. Used of physical healing and covenantal/spiritual restoration. The divine self-identification 'I am the LORD who heals you' (Ex 15:26, אֲנִי יְהוָה רֹפְאֶךָ) uses this root — the Isaiah 53:5 application is covenantal at its core."),
],
"cross_refs": [
("1 Pet 2:24","He himself bore our sins in his body on the cross — the most explicit NT penal substitution application"),
("2 Cor 5:21","He made him who knew no sin to be sin on our behalf — the imputation of both guilt and righteousness"),
("Matt 8:17","This was to fulfill what was spoken through Isaiah: He took our infirmities — Matthew applies the verse to the healing ministry"),
("Acts 8:32–35","Philip asks the Ethiopian eunuch: 'About whom does the prophet say this?' — the Christological reading presented as the natural one"),
("Rom 4:25","Delivered over because of our transgressions, raised because of our justification — the Isaiah 53 logic in Paul's syntax"),
],
"historical": "The textual history of Isaiah 53 is the strongest single piece of documentary evidence in Messianic prophecy apologetics. The Great Isaiah Scroll (1QIsa-a), discovered in Cave 1 at Qumran in 1947, dates to approximately 125 BC and reproduces chapters 52–53 with minimal variation from the later Masoretic Text. The Septuagint translation (c. 250 BC) renders the passage in Greek, and NT authors cite this Greek version extensively. Both documents demonstrably predate the events they are claimed to describe, ruling out ex eventu composition as an explanatory hypothesis.",
"apologetics": "Isaiah 53 is the centerpiece of Messianic prophecy apologetics. The argument runs: (1) the passage was written centuries before Christ (established by 1QIsa-a and LXX dating); (2) it describes an individual who suffers vicariously, dies, is buried with the rich, and is vindicated post-mortem; (3) these features find no coherent historical referent in Israel's history prior to Jesus; (4) they are precisely fulfilled in the Gospel narratives. The Jewish objection — the Servant is collective Israel — faces the difficulty that Israel does not suffer silently, does not bear others' guilt vicariously, and is not vindicated after death in the narrative of Isaiah itself. Peter Stoner's probability calculations in Science Speaks assign the probability of eight prophecies being fulfilled in one individual at 1 in 10^17.",
},

"Genesis 1:1": {
"label": "Creation Ex Nihilo — The Cosmological Foundation",
"context": "Genesis 1:1 opens the primordial history (1:1–2:3) with a statement unique in the ANE religious literature: creation without theogony (no divine birth narrative), without theomachy (no divine conflict), and without pre-existing divine matter (no god using pre-existing material). The verse's theological uniqueness lies precisely in what it excludes: every major ANE cosmogony — Enuma Elish (Babylonian), the Baal Cycle (Ugaritic), the Heliopolis cosmology (Egyptian) — involves gods emerging from or fighting over pre-existing chaos. Genesis 1 presents a single, sovereign Creator who speaks and the cosmos responds.",
"scholars": [
{"author":"Victor P. Hamilton","work":"The Book of Genesis: Chapters 1–17, NICOT (1990), pp. 103–117 — Analytical Summary",
"text":"Hamilton's grammatical analysis of בְּרֵאשִׁית (be-reshit, 'in the beginning') argues for the traditional absolute construction: 'In the beginning, God created' — not the temporal subordinate clause 'When God began to create' (the reading of Rashi and some modern scholars). The verb בָּרָא (bara') is used exclusively with God as subject throughout the Hebrew Bible, denoting a category of creative activity qualitatively distinct from human making (יָצַר, asah). This exclusivity is the strongest lexical basis for creatio ex nihilo, though Hamilton notes the verse does not explicitly assert creation from nothing — that concept requires Gen 1:1 read in light of Heb 11:3 and John 1:3."},
{"author":"Gordon Wenham","work":"Genesis 1–15, Word Biblical Commentary (1987), pp. 11–17 — Analytical Summary",
"text":"Wenham's situates Gen 1 as a polemical cosmogony: each day's creative act implicitly demythologizes ANE deities. The sun and moon — primary objects of worship across the ANE — are relegated to 'the greater light' and 'the lesser light,' deliberately unnamed to deny them divine status. The structural parallelism (days 1–3 establishing domains; days 4–6 filling them) reflects liturgical rhythm suggesting priestly composition intended for worship contexts. The repeated 'and it was good' (טוֹב) functions not merely aesthetically but theologically: creation is neither divine (pantheism) nor evil (Gnosticism) but good — contingent, ordered, and purposeful."},
{"author":"John H. Walton","work":"The Lost World of Genesis One, IVP Academic (2009), pp. 23–36 — Analytical Summary",
"text":"Walton's functional ontology thesis challenges the standard material-origins reading: in ANE cosmogony, something does not 'exist' until it has a function and a name assigned to it. Genesis 1 is therefore primarily a cosmic temple inauguration — God assigning functions to cosmic entities in preparation for divine habitation (cf. the Tabernacle and Temple as cosmic microcosms). This reading does not concede a non-literal interpretation but relocates the question: Gen 1 is not competing with scientific cosmology because it is not making claims about material origins. Critics note this reading may underweight the material creation language present in vv. 1 and 3."},
],
"greek": [
("H1254","בָּרָא","bara'","To create; God-exclusive subject throughout HB. The strongest lexical support for creatio ex nihilo. Distinct from יָצַר (yatsar, to form as a potter) and עָשָׂה (asah, to make/do). The NT equivalent ktizō (κτίζω) is similarly used exclusively for God's creative activity."),
("H7225","רֵאשִׁית","reshit","Beginning; first-fruits; the first of a sequence. Used in Prov 8:22 of personified Wisdom ('The LORD possessed me at the beginning of his work'), generating the Wisdom Christology that John's Prologue picks up. Also in John 1:1 (ἐν ἀρχῇ), the deliberate LXX echo."),
("H8064","שָׁמַיִם","shamayim","Heavens; dual (or plural of amplification) form suggesting the layered celestial realm. Encompasses the atmospheric heavens (sky), the stellar heavens, and the divine dwelling. The Hebraic cosmological vocabulary is phenomenological, not scientific — describing what the sky looks like from the ground."),
],
"cross_refs": [
("John 1:1–3","In the beginning was the Word — deliberate echo; all things came to be through him"),
("Heb 11:3","By faith we understand the worlds were created by the word of God from things not visible — explicit creatio ex nihilo"),
("Col 1:16","In him all things were created — making the agent of Gen 1:1 explicit"),
("Ps 33:6","By the word of the LORD the heavens were made — creatio per verbum, the mechanism"),
("Rev 4:11","You created all things, and by your will they exist and were created — the eschatological doxology returning to the beginning"),
],
"historical": "The Babylonian Enuma Elish (c. 12th century BC in written form) presents the closest ANE parallel: Marduk creates the cosmos from the corpse of the sea-goddess Tiamat, fashions humanity from the blood of the slain god Kingu. Genesis 1 pointedly excludes every element of this narrative: no divine conflict, no theomachy, no divine body as raw material, no divine plurality. The discovery of the Ebla Tablets (1974–75) confirmed Semitic creation vocabulary and urban culture in the 3rd millennium BC, consistent with the Mosaic authorship tradition that locates the patriarchal narratives in the early 2nd millennium.",
"apologetics": "Genesis 1:1 is the locus classicus for the Cosmological Argument. William Lane Craig's Kalam formulation: (1) Everything that begins to exist has a cause; (2) the universe began to exist; (3) therefore the universe has a cause. The Borde-Guth-Vilenkin Theorem (2003) establishes that any universe with a positive average expansion rate must have a past spacetime boundary — a beginning. Vilenkin himself has stated: 'All the evidence we have says that the universe had a beginning.' The cause of space, time, matter, and energy must itself be spaceless, timeless, immaterial — which is precisely the God described in Gen 1:1.",
},

"Hebrews 11:1": {
"label": "The Definition of Faith",
"context": "The Hall of Faith (Heb 11:1–40) serves as the rhetorical climax of the epistle's sustained argument for perseverance under persecution. The definition of faith in v. 1 is not an abstract philosophical analysis but a functional characterization for rhetorical purposes: faith is what enables the believer to act on divine promises not yet historically realized. The author (identity debated: Pauline, Apollos, Priscilla, Barnabas — all proposed) is addressing Jewish Christians contemplating reversion to Judaism under pressure, probably Neronian (AD 64–68) or Domitianic persecution.",
"scholars": [
{"author":"F.F. Bruce","work":"The Epistle to the Hebrews, NICNT, revised edition (1990), pp. 277–282 — Analytical Summary",
"text":"Bruce's examination of ὑπόστασις (hypostasis) — the term that Patristic theology would later deploy for the distinct personal subsistences of the Trinity — here in its earlier, pre-technical sense of 'substance,' 'reality,' or 'that which underlies appearances.' Bruce translates: 'the title-deed of things hoped for.' Faith gives eschatological realities an objective standing in the believer's present life — they are not merely wished for but possessed by anticipation, as a title-deed grants legal possession of property not yet occupied."},
{"author":"Thomas Schreiner and Ardel Caneday","work":"The Race Set Before Us, IVP (2001), pp. 187–192 — Analytical Summary",
"text":"Schreiner and Caneday's treatment situates Hebrews 11 within the letter's overarching eschatological argument: faith is not a one-time decision but the sustained orientation toward the 'city with foundations' (11:10, 16; 12:22). The examples of ch. 11 — Abel, Enoch, Noah, Abraham, Moses — are all characterized by persevering faith in promises not yet historically realized. This structural observation bears directly on the perseverance of the saints debate: the warning passages in Hebrews (6:4–6; 10:26–31) are genuine threats against genuine apostasy, not hypothetical warnings to non-believers."},
{"author":"Philip Edgcumbe Hughes","work":"A Commentary on the Epistle to the Hebrews, Eerdmans (1977), pp. 439–445 — Analytical Summary",
"text":"Hughes traces the Platonic resonance of ὑπόστασις and ἔλεγχος without conceding Hellenistic conceptual dependence. The author may be using philosophical vocabulary familiar to Hellenized Jewish readers while filling the terms with Hebraic covenantal content. ἔλεγχος — normally a legal term for the presentation of decisive proof — here means something like 'inner conviction that functions as legal certainty.' Faith is not optimism or wishful thinking but the epistemological state of one who has been persuaded by divine testimony."},
],
"greek": [
("G5287","ὑπόστασις","hypostasis","Substance; underlying reality; that which stands under. In Patristic Christology, the term for each Person of the Trinity (three hypostases, one ousia). Here: the concrete reality that faith imparts to hoped-for eschatological realities."),
("G1650","ἔλεγχος","elenchos","Proof; conviction; evidence. The legal term for the presentation of decisive evidence sufficient for a verdict. Faith as juridical certitude regarding the invisible — not emotion but epistemological conviction grounded in divine testimony."),
("G1679","ἐλπίζω","elpizō","To hope. Biblical hope (ἐλπίς, elpis) is not wishful uncertainty but confident expectation grounded in covenant promise. The Greek ἐλπίς could be positive or negative (hope or fear); the NT restricts it to the confident forward orientation of those who know the end of the story."),
],
"cross_refs": [
("2 Cor 5:7","We walk by faith, not by sight — Paul's parallel epistemological formulation"),
("Rom 8:24–25","Hope that is seen is not hope; but we hope for what we do not see — the temporal structure of faith and hope"),
("Heb 11:6","Without faith it is impossible to please God, for he who comes to God must believe that He is and is a rewarder of those who seek Him — the axiom that v. 1 grounds"),
("John 20:29","Blessed are those who have not seen and yet have believed — the Risen Christ's beatitude for those who exercise precisely the faith Heb 11:1 defines"),
("Rom 4:18","Against hope, Abraham believed in hope — the paradigm case of the faith Hebrews 11 anatomizes"),
],
"historical": "Hebrews was almost certainly written before AD 70 given the present-tense references to the Temple cult (8:4; 10:11 — 'every priest stands daily'). The destruction of Jerusalem would have been the single most powerful argument for the supersession of the Levitical priesthood; its absence from the letter is decisive for dating. The recipients were Jewish Christians in Rome or Palestine navigating between the visible stability of Mosaic observance and the invisible promises of a crucified and risen Messiah. Hebrews 11 answers their situation: the entire OT community of faith acted on the invisible promises of God — and they did not have the completed revelation the recipients have.",
"apologetics": "Hebrews 11:1 is the most commonly misread verse in the apologetics debate. It is routinely cited as a definition of faith as 'belief without evidence' — Dawkins' 'great virtue of faith is that evidence is not required.' This reading ignores ἔλεγχος, which means precisely evidence or proof. Biblical faith in the Hebrews 11 sense is conviction grounded in divine testimony — not blind credulity but well-founded trust in a demonstrably reliable revealer. Alister McGrath (Mere Apologetics) and John Lennox (God's Undertaker) both distinguish biblical faith from fideism on precisely this basis. The Hall of Faith that follows (vv. 4–40) is not a gallery of irrationalists but of people who acted on specific divine promises in light of specific divine track records.",
},

"Matthew 16:13-17": {
"label": "The Petrine Confession at Caesarea Philippi",
"context": "Matthew 16:13–17 records the climactic Christological confession of the Synoptic Gospels at Caesarea Philippi — a city built by Philip the Tetrarch and named for Caesar Augustus, making the declaration of Jesus' Messiahship politically and theologically charged in the extreme. Jesus' question ('Who do people say the Son of Man is?') uses his characteristic self-designation — the apocalyptic Son of Man of Daniel 7:13–14 — before eliciting the confession that he is 'the Christ, the Son of the Living God.' The divine attestation of Peter's confession ('flesh and blood did not reveal this to you, but my Father in heaven') makes this the NT's clearest claim that Christological knowledge is revelatory, not merely inferential.",
"scholars": [
{"author":"D.A. Carson","work":"Matthew, Expositor's Bible Commentary (1995), Vol. 8, pp. 362–375 — Analytical Summary",
"text":"Carson's treatment of the Petrine office question (v. 18: 'on this rock I will build my church') resists both the Roman Catholic reading (Peter as the foundation of ongoing apostolic succession) and the extreme Protestant deflection (the rock is Christ himself). Carson argues the rock is Peter in his confessing capacity — the apostolic testimony to the identity of Christ is the foundation on which the church is built. The gates of Hades (v. 18) are not defensive walls but the powers of death itself, and they will not overcome the church's proclamation of the resurrection."},
{"author":"Craig L. Blomberg","work":"Matthew, NAC (1992), pp. 250–255 — Analytical Summary",
"text":"Blomberg situates the confession within the Gospel's Christological development: Matthew has been building the question of Jesus' identity since chapter 1 (Emmanuel, 'God with us') and it reaches its verbal apex here. The 'Son of the Living God' title (υἱὸς τοῦ θεοῦ τοῦ ζῶντος) is more than a Messianic designation — in Matthew's context, especially the Gethsemane prayer and the trial before Caiaphas (26:63), it carries ontological weight: Jesus is not merely the anointed human king but the divine Son in a unique filial relationship."},
{"author":"Joachim Jeremias","work":"New Testament Theology (1971), pp. 250–259 — Analytical Summary",
"text":"Jeremias, one of the most rigorous historical-Jesus scholars of the 20th century, argues for the substantial authenticity of Peter's confession and Jesus' response. The Aramaic wordplay (Petros/petra — the very name Jesus gives Peter is itself a Christological act: Simon receives a new identity as the rock of confession) and the unusual beatitude form are consistent with authentic Jesus tradition. Jeremias also notes that Jesus' acceptance of the title 'Son of the Living God' without correction — by contrast with his regular redirection of miracle-based enthusiasm — implies acceptance of its content."},
],
"greek": [
("G5207","υἱός","huios","Son; in 'Son of the Living God,' carries ontological weight beyond Messianic appointment. In Matthew's usage, Jesus' sonship is unique (μονογενής in John's parallel) and is consistently linked with divine authority: the baptism (3:17), transfiguration (17:5), and trial (26:63) all use the same language."),
("G4074","Πέτρος/πέτρα","Petros/petra","Peter/rock. The masculine Petros (proper name) and feminine petra (rock formation) are the same Aramaic kepha in Jesus' underlying Aramaic — the wordplay exists in both languages. The ecclesiological debate: whether petra refers to Peter personally, his confession, or Christ himself has generated more commentary than perhaps any other verse in the NT."),
("G207","ἀποκαλύπτω","apokalyptō","To reveal, uncover. Jesus attributes Peter's knowledge to divine revelation, not human perception (flesh and blood). This introduces the epistemological claim that underlies all Christology: correct knowledge of Jesus' identity is not achievable by purely natural investigation — it requires divine disclosure."),
],
"cross_refs": [
("Dan 7:13–14","The Son of Man coming with the clouds — Jesus' self-designation throughout the Synoptics derives from this passage"),
("Ps 2:7","You are my Son; today I have begotten you — the Davidic-Sonship background for Messianic identity"),
("Mark 8:27–30","Marcan parallel — Peter's confession without the ecclesiological addition, suggesting Matthew's version reflects expanded tradition"),
("John 6:68–69","Peter's Johannine confession: 'You have words of eternal life; we believe you are the Holy One of God'"),
("Acts 2:36","God has made him both Lord and Christ, this Jesus whom you crucified — Peter's Pentecost proclamation of what he confessed at Caesarea"),
],
"historical": "Caesarea Philippi was a center of Roman imperial cult worship (a temple to Augustus stood there) and pagan religious complexity (the site of the Grotto of Pan). Jesus' choice of this location for the Christological climax of his public ministry is deliberate: against the backdrop of Caesar's divine claims and pagan theogony, the declaration that Jesus is 'the Christ, the Son of the Living God' is simultaneously a political and theological act of supreme audacity.",
"apologetics": "Matthew 16:13–17 is central to the historical Jesus debate. The majority position among critical scholars (Crossan, Borg, Funk) holds that the high Christological titles were retrojected by the church after the resurrection. The Caesarea Philippi pericope challenges this: (1) the criterion of embarrassment applies — the confession is given by Peter, who immediately rebukes Jesus (v. 22) and later denies him; an invented tradition would not combine the supreme confession with the supreme failure; (2) the Aramaic substratum of the Petros/petra wordplay suggests authentic tradition; (3) the geographical specificity (Caesarea Philippi) is the kind of detail that does not appear in invented traditions.",
},

"Daniel 7:13-14": {
"label": "The Son of Man — The Apocalyptic Self-Designation of Jesus",
"context": "Daniel 7:13–14 is, along with Isaiah 53, the most important OT passage for understanding Jesus' self-understanding. Jesus uses 'Son of Man' (ὁ υἱὸς τοῦ ἀνθρώπου) as his primary self-designation in all four Gospels — approximately 80 occurrences. The phrase draws on Daniel 7:13, where the figure 'like a son of man' comes before the Ancient of Days and receives eternal, universal dominion. The identification of the Danielic Son of Man with the Messiah is attested in Second Temple Judaism (1 Enoch 46; 4 Ezra 13), making Jesus' use of the title a deliberate, loaded claim whose implications his audiences would have recognized.",
"scholars": [
{"author":"N.T. Wright","work":"Jesus and the Victory of God (1996), pp. 513–519 — Analytical Summary",
"text":"Wright argues that Jesus used 'Son of Man' as a self-referential apocalyptic title that condensed the entire Daniel 7 narrative: Israel (represented by 'one like a son of man') vindicated after suffering at the hands of the beasts (pagan empires), receiving divine sovereignty and universal dominion. Jesus identified himself as the one through whom this vindication would occur — not through military conquest but through the paradox of death and resurrection. The trial scene (Matt 26:64: 'You will see the Son of Man seated at the right hand of Power, coming on the clouds of heaven') is Jesus' explicit citation of Dan 7:13 before the Sanhedrin — a claim to divine status that constitutes blasphemy if false."},
{"author":"John J. Collins","work":"Daniel, Hermeneia (1993), pp. 304–310 — Analytical Summary",
"text":"Collins' critical analysis of Daniel 7 identifies the figure of Dan 7:13 as an angelic mediator (Michael, or a heavenly alter ego of Israel) rather than a Messianic figure, within the literary context of the 2nd century BC Antiochene crisis. Collins' critical reading does not require a predictive element. The NT's application of Dan 7:13 to Jesus is, on this reading, a creative reinterpretation of a corporate figure as an individual. The evangelical response (Longman, Goldingay) notes that the corporate/individual fluidity in Daniel does not preclude both dimensions simultaneously — the Son of Man figure may represent Israel and find its individual fulfillment in the Messiah."},
{"author":"Larry Hurtado","work":"Lord Jesus Christ: Devotion to Jesus in Earliest Christianity (2003), pp. 290–306 — Analytical Summary",
"text":"Hurtado's examination of the earliest Christological data (Paul's letters, Q, Mark) establishes that the identification of the risen Jesus with the Danielic Son of Man was not a late theological development but belongs to the earliest stratum of Christian proclamation. The remarkable speed of Christological development — within years of the crucifixion, Paul is citing pre-Pauline hymns that identify Jesus with divine status (Phil 2:6–11; 1 Cor 8:6) — requires an explanation. Hurtado's thesis: the resurrection experience was the catalyst that recontextualized the prior traditions about Jesus, including his Son of Man sayings, as disclosures of divine identity."},
],
"greek": [
("H1121","בַּר אֱנָשׁ","bar enash","Son of man (Aramaic); a human being. The contrast in Dan 7 is between the four beasts (monstrous, animal) and the human figure — dominion belongs to the humane. Jesus uses the Greek ὁ υἱὸς τοῦ ἀνθρώπου (with the double article, suggesting a specific figure) consistently as his self-referential title."),
("H5957","עָלַם","olam","Eternity; the age to come. The dominion given to the Son of Man is עָלַם וְעַד עָלְמַא (forever and ever) — the same language used for YHWH's own eternal reign in Ps 146:10. The transfer of eternal divine dominion to the Son of Man is the basis for the Christological reading."),
("G2064","ἔρχομαι","erchomai","To come. The Son of Man 'comes with the clouds of heaven' — in OT theophany language, cloud-riding is YHWH's prerogative (Ps 104:3; Isa 19:1; Nah 1:3). Jesus' appropriation of this language before Caiaphas (Matt 26:64) constitutes his most explicit claim to divine status."),
],
"cross_refs": [
("Matt 26:64","You will see the Son of Man seated at the right hand of Power, coming on the clouds — Jesus' explicit citation before the Sanhedrin"),
("Rev 1:13","One like a son of man, clothed in a long robe — the Apocalypse identifies the risen Christ with the Danielic figure"),
("Ps 110:1","The LORD said to my Lord: Sit at my right hand — the twin text Jesus combines with Dan 7:13 at the trial"),
("1 Enoch 46","The Son of Man who existed before the sun and stars were created — Second Temple Messianic interpretation of Dan 7"),
("Mark 14:62","I am, and you will see the Son of Man seated at the right hand of Power — Marcan parallel, with the divine name 'I am' (ἐγώ εἰμι)"),
],
"historical": "Daniel 7 was written in the context of Antiochus IV Epiphanes' persecution of Jews (167–164 BC) and the Maccabean resistance. The four beasts represent successive empires (Babylonian, Median, Persian, Greek); the 'little horn' is Antiochus. The Son of Man figure represents the faithful Jewish remnant vindicated by God after the persecution. By the 1st century AD, the passage had been read in a Messianic-individual sense in both 1 Enoch 37–71 and 4 Ezra 13 — demonstrating that Jesus' appropriation of the title drew on an already-developing tradition.",
"apologetics": "Daniel 7:13–14 is critical for the historical Jesus debate on two grounds. First, Jesus' self-designation as Son of Man is multiply attested across all four Gospels and the Q source, passing the criterion of multiple attestation with the highest possible score. Second, the title is not the kind of exalted Christological designation a post-resurrection church would have invented — later NT Christology uses 'Lord,' 'Christ,' and 'Son of God' far more. The Son of Man tradition is therefore among the most authentic elements of the Jesus tradition, and it points directly to Dan 7:13 — which is a claim to receive eternal divine dominion before the Ancient of Days. This is not the language of a 'good moral teacher.'",
},

"Exodus 3:14": {
"label": "The Divine Name — YHWH and the Deity of Christ",
"context": "Exodus 3:14 records the disclosure of the divine name at the burning bush — the theological center of gravity of the entire Hebrew Bible. God's self-identification as אֶהְיֶה אֲשֶׁר אֶהְיֶה (ehyeh asher ehyeh, 'I AM WHO I AM') and his command to identify him to Israel as 'I AM' (אֶהְיֶה) establishes the basis of Israel's monotheism: YHWH is the self-existent, self-defining, uncaused cause of all that exists. The NT's application of this name to Jesus — most explicitly in John 8:58 ('Before Abraham was, I am,' ἐγώ εἰμι) and the Gethsemane arrest (John 18:6) — constitutes the most direct claim to divine identity in the Gospel tradition.",
"scholars": [
{"author":"John I. Durham","work":"Exodus, Word Biblical Commentary (1987), pp. 37–40 — Analytical Summary",
"text":"Durham's grammatical analysis of אֶהְיֶה engages the three major interpretive options: (a) ontological self-existence — 'I AM the One who IS,' emphasizing God's unique mode of being as the self-existent ground of all other existence (the classical theological tradition: Aquinas, Maimonides); (b) relational promise — 'I WILL BE what I will be,' emphasizing God's dynamic, faithful presence with his people in the events about to unfold; (c) deliberate evasion — God refuses to define himself by a name that might constrain or categorize him. Durham favors a reading that combines (a) and (b): God declares his ontological uniqueness while promising his relational presence."},
{"author":"Alec Motyer","work":"The Message of Exodus, BST (2005), pp. 66–75 — Analytical Summary",
"text":"Motyer's theological exposition of the divine name focuses on aseity (Latin: a se, 'from himself') — the classical doctrine that God's existence is entirely self-derived, not dependent on any prior cause or external condition. The ehyeh declaration is the self-disclosure of the only being who could give such an answer: to the question 'What is your name?' (i.e., 'What is your nature, your status, your relation to other powers?'), God answers 'I AM' — I am the unconditioned ground of being, who owes my existence to nothing and no one. This becomes the foundation for the NT's ἐγώ εἰμι christology."},
{"author":"D.A. Carson","work":"The Gospel According to John, Pillar NT Commentary (1991), pp. 357–358 — Analytical Summary",
"text":"Carson's exegesis of John 8:58 ('Before Abraham came into existence, I am') identifies the deliberate grammatical incongruity: Jesus uses the present tense ἐγώ εἰμι ('I am') where normal Greek grammar requires the perfect or aorist. The incongruity is theological, not grammatical: it echoes Ex 3:14 (LXX: ἐγώ εἰμι ὁ ὤν, 'I am the one who is'). The crowd's reaction — picking up stones (v. 59) — confirms they understood the claim as a blasphemous assertion of divine identity, not merely pre-existence."},
],
"greek": [
("H1961","אֶהְיֶה","ehyeh","First person imperfect of hayah (to be): 'I will be' / 'I am.' The divine name as self-designation. Root meaning: being, existence, becoming. The LXX translates as ἐγώ εἰμι ὁ ὤν ('I am the one who is') — the participial form ὤν (present active participle of εἰμί) emphasizing ongoing, self-subsistent existence."),
("H3068","יְהוָה","YHWH","The tetragrammaton; the proper name of Israel's God. Derived from the same root as ehyeh: he who causes to be, or he who is. Pronounced 'Adonai' (Lord) in Jewish reading tradition; rendered LORD (small capitals) in most English translations. The NT's identification of Jesus with YHWH-language (Ps 110:1; Joel 2:32 cited in Acts 2:21 and Rom 10:13) is the foundation of NT Christology."),
("G1510","εἰμί","eimi","To be; exist. The ἐγώ εἰμι ('I am') absolute use in John's Gospel (6:35; 8:12; 10:7,11; 11:25; 14:6; 15:1 — the seven 'I am' statements — plus the absolute uses in 8:24, 28, 58; 13:19) echoes the LXX divine name. John 8:58 is the most explicit: the temporal contrast ('before Abraham came to be / γενέσθαι, I am / εἰμι') reproduces the contrast between creaturely genesis and divine eternal being."),
],
"cross_refs": [
("John 8:58","Before Abraham came into existence, I am — the NT's most explicit application of Ex 3:14 to Jesus"),
("John 18:5–6","When Jesus said 'I am,' they drew back and fell to the ground — the Gethsemane theophany, another Ex 3:14 echo"),
("Isa 43:10–11","Before me no god was formed, nor will there be after me; I, I am YHWH, and besides me there is no savior"),
("Rev 1:8","I am the Alpha and the Omega, says the Lord God, who is and who was and who is to come — applied to both God and Christ in Revelation"),
("Isa 44:6","I am the first and I am the last, and besides me there is no god — the exclusivity claim"),
],
"historical": "The divine name YHWH was so sacred in Second Temple Judaism that it was not pronounced — the Qumran community used dots instead of the letters when copying YHWH in the Psalms. Against this backdrop of extreme reverence for the divine name, Jesus' use of ἐγώ εἰμι in John 8:58 was not an ambiguous philosophical claim but an audacious act of divine self-identification. The crowd's immediate response (stoning, the penalty for blasphemy under Lev 24:16) confirms the force of the claim was not lost on them.",
"apologetics": "Exodus 3:14 and its NT applications constitute the strongest textual argument for the deity of Christ. The argument runs: (1) the divine name YHWH is associated in the OT with a cluster of attributes — eternal existence, aseity, omnipotence, the exclusive title 'Savior'; (2) the NT applies each of these attributes and titles to Jesus (Joel 2:32 → Rom 10:13; Isa 45:23 → Phil 2:10; YHWH as rock → 1 Cor 10:4); (3) the NT writers were Jewish monotheists who could not have made these identifications carelessly. The conclusion: the NT presents Jesus as sharing the divine identity of YHWH, not as a second god or an exalted creature.",
},

"Psalm 22": {
"label": "The Messianic Psalm of Dereliction",
"context": "Psalm 22 is the most extensively cited OT passage in the Passion narratives. Jesus quotes its opening line from the cross (Matt 27:46; Mark 15:34: 'My God, my God, why have you forsaken me?'), and the Gospel accounts of the crucifixion are saturated with allusions to its imagery: soldiers gambling for garments (v. 18 / John 19:24), mockers wagging their heads (v. 7 / Matt 27:39), the taunt 'He trusts in God; let God deliver him' (v. 8 / Matt 27:43), and the piercing of hands and feet (v. 16). The Psalm moves from dereliction (vv. 1–21) to vindication and universal praise (vv. 22–31), making it a template for the death-and-resurrection narrative.",
"scholars": [
{"author":"Peter Craigie","work":"Psalms 1–50, Word Biblical Commentary (1983), pp. 195–204 — Analytical Summary",
"text":"Craigie's historical-grammatical analysis situates Psalm 22 as a genuine lament of David, composed during a specific crisis of abandonment. The pattern of individual lament (complaint → petition → trust → praise) is a standard form in the Psalter. Craigie resists a directly predictive reading while acknowledging the typological depth: David's experience of abandonment and vindication establishes a pattern that reaches its ultimate expression in Christ. The NT citations are not proof-texting but the recognition that Jesus entered into the fullest possible realization of the pattern David's life established."},
{"author":"Derek Kidner","work":"Psalms 1–72, Tyndale OT Commentaries (1973), pp. 105–110 — Analytical Summary",
"text":"Kidner's elegant analysis notes the Psalm's movement from individual desolation (vv. 1–21) to cosmic and eschatological praise (vv. 25–31: 'All the ends of the earth will remember and turn to YHWH; all the families of nations will bow down before him'). The resolution is not merely personal vindication but universal Lordship — the suffering of the individual becomes the means of worldwide acknowledgment of YHWH's sovereignty. This eschatological trajectory, Kidner argues, cannot be exhausted by David's personal experience and anticipates precisely the NT Christological application."},
{"author":"John Goldingay","work":"Psalms, Baker Commentary on the OT (2006), Vol. 1, pp. 331–347 — Analytical Summary",
"text":"Goldingay's reading is more sensitive to the formal unity of the Psalm: the shift from lament to praise (v. 24: 'he has not despised or scorned the suffering of the afflicted one; he has not hidden his face from him but has listened to his cry for help') is not a later addition but the theological climax. The one who was apparently abandoned was in fact heard. The NT application is precise: Jesus' cry of dereliction is not the final word — the Resurrection is the answer to Psalm 22:24, the divine 'hearing' that the Psalm anticipated."},
],
"greek": [
("H5800","עָזַב","azab","To forsake, abandon. The opening cry of the Psalm — 'My God, my God, why have you forsaken me?' — uses the strongest Hebrew term for divine abandonment. The LXX translates ἐγκατέλιπες (2nd aorist of ἐγκαταλείπω) — the same word used in Matt 27:46 and Mark 15:34, confirming the evangelists' deliberate citation of the Psalm."),
("H7070","כָּרָה","karah","Pierced; in v. 16 ('they have pierced my hands and my feet'), the text is disputed: the MT reads כָּאֲרִי (like a lion) while 1QPs-a and LXX (ὤρυξαν) support 'pierced.' The textual variant is one of the most contested in the Psalter and directly impacts the Messianic reading."),
("H2505","חָלַק","chalaq","To divide, apportion. In v. 18 ('they divide my garments among them, and for my clothing they cast lots') — cited verbatim in John 19:24 as fulfilled prophecy. The specificity of the allotment detail (garments divided but robe undivided) is historically plausible and Johanninely significant."),
],
"cross_refs": [
("Matt 27:46","My God, my God, why have you forsaken me? — Jesus' citation from the cross"),
("John 19:24","They divided my garments among them and cast lots for my clothing — cited as Scripture fulfillment"),
("Matt 27:43","He trusts in God; let God rescue him now if he wants him — verbal echo of Psalm 22:8"),
("Heb 2:12","I will proclaim your name to my brothers; in the congregation I will sing your praise — Ps 22:22 applied to Christ"),
("Rev 5:9","Worthy is the Lamb who was slain — the eschatological consummation of Psalm 22's universal praise"),
],
"historical": "The earliest known commentary on Psalm 22 in a Christian context is the Epistle of Barnabas (c. AD 100), which reads the Psalm as predictive of Christ's Passion. Justin Martyr (c. AD 155) in his Dialogue with Trypho (chapters 97–106) conducts an extended exegesis of Psalm 22 as Messianic prophecy, engaging Jewish interlocutors who denied the application. The Psalm was evidently central to the earliest Christian apologetic engagement with Judaism.",
"apologetics": "Psalm 22 presents the strongest internal textual argument for the Gospels' historical reliability regarding the Passion: the correspondence between the Psalm and the crucifixion narrative is too specific and too internally coherent to be explained by creative embellishment. The evangelists did not have to invent Passion details — they recognized in the events they were recording the fulfillment of a Psalm that had been in Israel's liturgical tradition for a millennium. The gambling of soldiers for a victim's garments is not a detail any narrative embellisher would independently invent — but it appears in both Psalm 22:18 and John 19:23–24.",
},

}  # end COMMENTARY


STUDY_PROMPTS = {
    "Exegetical": [
        "Perform a word study on ἁρπαγμόν (harpagmos) in Philippians 2:6. Evaluate the three major positions (res rapta, res rapienda, verbal abstract) and their Christological consequences. Consult Hoover (HTR, 1971) and Wright's Climax of the Covenant.",
        "What does the present active participle πιστεύων in John 3:16 imply about the nature of saving faith? Is it consistent with the Reformed doctrine of perseverance or does it permit apostasy readings?",
        "Analyze the use of ἱλαστήριον in Romans 3:25. Engage the Dodd-Morris debate: is the term best rendered 'expiation' (sin-removal) or 'propitiation' (wrath-appeasement)? What does the LXX background of Leviticus 16 contribute?",
        "Compare the divine name formula ἐγώ εἰμι in John 8:24, 8:28, 8:58, and 13:19. Are these absolute uses (echoing Ex 3:14 LXX) or predicate uses? What is the grammatical evidence and what are the Christological stakes?",
        "Examine the textual variant at Psalm 22:16 (כָּאֲרִי 'like a lion' in MT vs. כָּרוּ 'they have pierced' in LXX and 1QPs-a). What are the manuscript arguments on each side, and what are the apologetic implications either way?",
        "What is the Granville Sharp Rule and how does it apply to Titus 2:13 and 2 Peter 1:1? Does the rule require that 'God and Savior' refer to a single person (Jesus) or two persons? Consult Wallace's Greek Grammar Beyond the Basics.",
        "Analyze the syntax of Romans 5:12's ἐφ' ᾧ clause. What are the four major interpretive options and how does the choice affect the doctrine of original sin? Compare the Augustinian (inherited guilt), Eastern Orthodox (inherited mortality), and Pelagian readings.",
        "Examine the hapax legomenon ἐπιούσιος in Matthew 6:11. What does the adjective mean and what is its relationship to the eschatological banquet motif in Matthew? Does Jerome's choice of 'supersubstantialem' in the Vulgate alter the meaning?",
    ],
    "Doctrinal": [
        "Trace the development of the Trinitarian formula from NT usage (Matt 28:19; 2 Cor 13:14; John 15–17) through Tertullian's substantia/personae framework to the Nicene Creed (325) and Constantinople (381). What specifically did the Cappadocian Fathers (Basil, the two Gregories) contribute?",
        "Distinguish the Reformed (Turretin, Berkhof), Lutheran (Melanchthon), and Arminian (Arminius, Wesley) accounts of justification. What is the precise point of disagreement between imputation and infusion, and what biblical texts anchor each position?",
        "What is the hypostatic union? How did Chalcedon (451) define the relationship of the two natures in Christ and what specifically were the errors of Nestorius (too-separate natures) and Eutyches (merged natures) that the definition was designed to exclude?",
        "Compare Warfield's plenary verbal inspiration and inerrancy (Inspiration and Authority of the Bible), Peter Enns's incarnational model (Inspiration and Incarnation), and Vanhoozer's dramatheorical account (The Drama of Doctrine). What is at stake in the inerrancy debate?",
        "Present the strongest biblical and theological arguments for eternal conscious torment (ECT), annihilationism/conditional immortality (Fudge, Stott), and universalism (Talbott, MacDonald). Which position has the strongest exegetical base in Matthew 25 and Revelation 14:9–11?",
        "What is Open Theism and how does it differ from classical Arminianism? Present Gregory Boyd's (God of the Possible) and Clark Pinnock's (The Openness of God) arguments, and then present the classical theist responses (Frame, Helm, Ware).",
        "What is the New Perspective on Paul (Dunn, Wright, Sanders) and how does it challenge the Reformation's reading of justification by faith alone? What are the strongest evangelical responses (Schreiner, Westerholm, Seifrid)?",
        "What are the main positions in the Calvinist/Arminian debate on election and perseverance? Exegete Romans 8:28–30, Romans 9:6–24, John 6:37–44, and 1 John 2:19 from both perspectives. Where does the strongest exegetical weight fall?",
    ],
    "Historical": [
        "Describe the canon formation process for the NT. By what criteria (apostolicity, catholicity, orthodoxy, liturgical use, inspiration) were books accepted or rejected? Address the status of Hebrews, Revelation, the Didache, and the Gospel of Thomas.",
        "How did the Dead Sea Scrolls (1947–1956) change NT scholarship? Address: (a) textual stability of the OT; (b) Second Temple Jewish eschatology and its relationship to Jesus' teaching; (c) the Qumran community's messianic expectations.",
        "Describe the Synoptic Problem and evaluate the major solutions: Marcan Priority with Q (Streeter), Matthean Priority/Griesbach Hypothesis (Farmer), and Farrer-Goulder (no Q). What are the strongest arguments for each?",
        "What does external archaeology confirm about the NT narrative? Address the Pool of Siloam (2004), the Pilate Inscription (1961), the Caiaphas Ossuary (1990), the House of Peter at Capernaum, and the Tel Dan Stele.",
        "Trace the development of Christian apologetics from Justin Martyr's First Apology (c. 155) through Augustine's City of God (413–426), Anselm's Proslogion (1077), Aquinas's Summa Contra Gentiles (1259–1265), and Butler's Analogy of Religion (1736) to modern evidentialist and presuppositionalist schools.",
        "What was the relationship between the Septuagint (LXX) and the Masoretic Text (MT)? How do NT authors' OT citations (often following LXX against MT) affect the doctrine of inerrancy? Address the Immanuel prophecy (Isa 7:14, almah vs. parthenos) specifically.",
        "How did the destruction of Jerusalem in AD 70 shape the composition and reception of the Synoptic Gospels? What is the significance of the terminus ante quem for Gospel dating and what are the apologetic implications?",
        "Describe the Reformation's sola scriptura controversy. What was the Catholic Church's response at Trent (1545–1563)? How do modern evangelical scholars (Allert, Williams) engage the tradition/Scripture question differently from the Reformers?",
    ],
    "Apologetics": [
        "Present the historical case for the bodily resurrection of Jesus using only criteria accepted by secular historians: multiple independent attestation (1 Cor 15:3–8 as pre-Pauline creed), criterion of embarrassment (female witnesses), enemy attestation (Jewish Talmud, Josephus), and the survival of the movement.",
        "How does Plantinga's modal ontological argument (using S5 possible world semantics) differ from Anselm's original? What is the atheist's best response (the 'no-maximally-great-island' objection) and how does Plantinga answer it?",
        "Present Robin Collins's fine-tuning argument in full: What specific constants exhibit fine-tuning (cosmological constant Λ, gravitational constant G, strong nuclear force)? What are the three main atheist responses (multiverse, physical necessity, design intuition is unreliable) and the best theist replies?",
        "Evaluate Victor Reppert's Argument from Reason (Lewis's chapter 'The Cardinal Difficulty of Naturalism' in Miracles). How does the argument establish that naturalism is self-defeating if mental states are fully explicable by physical causes? Address the Anscombe objection.",
        "What is J.P. Schellenberg's Divine Hiddenness argument? Present it in standard form, then evaluate the three main theist responses: (a) Moser's account of seeking; (b) Howard-Snyder's defense of non-culpable non-belief; (c) the soul-making response (John Hick).",
        "Evaluate Bart Ehrman's textual skepticism (Misquoting Jesus). What percentage of the NT variants are theologically significant? How do the responses of Daniel Wallace, Bruce Metzger, and Craig Evans address his core claims about textual reliability?",
        "Present the Isaiah 53 apologetic argument in its strongest form using the Dead Sea Scroll evidence (1QIsa-a, c. 125 BC). What are the five strongest naturalistic objections (collective servant, Maccabean date, 'pierced' textual variant, Christian interpolation, Stoner's statistics) and the best responses?",
        "Evaluate John Loftus's Outsider Test for Faith (OTF): Does applying the same skeptical standards to Christianity that one applies to other religions justify atheism or agnosticism? How do Craig, Plantinga, and Licona respond? Is the OTF self-defeating?",
    ],
    "Theological Debates": [
        "CALVINISM vs. ARMINIANISM — Total Depravity: Does Romans 3:10–18 and Ephesians 2:1–3 establish the inability of fallen humans to respond to God, or does Romans 2:14–15 and John 1:9 preserve sufficient grace? Exegete both positions without selection bias.",
        "CALVINISM vs. ARMINIANISM — Unconditional Election: Does Romans 9:6–24 establish individual unconditional election (Schreiner, Murray) or corporate/foreknowledge-based election (Klein, Forlines)? What is the significance of the Jacob-Esau pericope and its OT context (Mal 1:2–3)?",
        "INERRANCY — Warfield vs. Enns: Does Warfield's 'concursive' model of inspiration (B.B. Warfield, Inspiration and Authority of the Bible) adequately account for the genuine human authorship evidenced by the diversity of the biblical text? How does Peter Enns's incarnational analogy (Inspiration and Incarnation) differ, and what are the limits of that analogy?",
        "ANNIHILATIONISM vs. ETERNAL CONSCIOUS TORMENT — Exegete Revelation 14:9–11 ('the smoke of their torment goes up forever and ever'), Matthew 25:46 (αἰώνιος κόλασις, 'eternal punishment'), and 2 Thessalonians 1:9 ('eternal destruction'). Does αἰώνιος in these contexts denote duration or quality? Present Fudge (The Fire That Consumes) and Packer (The Problem of Eternal Punishment) in dialogue.",
        "OPEN THEISM vs. CLASSICAL THEISM — Does the biblical evidence for divine repentance (Gen 6:6; Ex 32:14; Jonah 3:10), divine surprise (Isa 5:4), and divine inquiry (Gen 3:9; 18:21) require revising the classical doctrine of divine foreknowledge (Gregory Boyd, God of the Possible)? How do Helm (The Providence of God) and Frame (No Other God) respond?",
        "PENAL SUBSTITUTION vs. CHRISTUS VICTOR — Is Aulén's Christus Victor (1931) an alternative to penal substitution or complementary to it? Evaluate Steve Chalke's 'cosmic child abuse' objection against Stott's The Cross of Christ. Does the coherence of atonement theology require a single model?",
        "SUPERSESSIONISM — Does the NT's use of the OT covenants require fulfillment-replacement (classic supersessionism, N.T. Wright), fulfillment-expansion (progressive dispensationalism, Bock/Saucy), or a flat continuity (dispensational hermeneutics, Ryrie)? Exegete Romans 11:25–29 ('all Israel shall be saved') from each position.",
        "CREATION — How should evangelical scholarship read Genesis 1–2 in light of the ANE parallels (Enuma Elish, Atrahasis Epic)? Evaluate Young Earth Creationism (Mortenson, Sarfati), Old Earth/Day-Age Creationism (Collins, Ross), Framework Hypothesis (Kline, Irons), and Functional Ontology (Walton) on their exegetical merits.",
    ],
}


APOLOGETICS_ARGS = [
    {
        "title": "The Cosmological Argument (Kalam)",
        "type": "Metaphysical",
        "content": (
            "<strong>Standard Formulation (Craig, 1979):</strong><br>"
            "(1) Everything that begins to exist has a cause.<br>"
            "(2) The universe began to exist.<br>"
            "(3) Therefore, the universe has a cause.<br><br>"
            "<strong>Scientific Support — BGV Theorem (Borde, Guth, Vilenkin, 2003):</strong> "
            "Any universe with a positive average Hubble expansion rate must have a past boundary. "
            "This result is model-independent: it applies to inflationary cosmologies, cyclic models, "
            "and string-theoretic landscapes. Vilenkin: 'There are no exceptions. The conclusion that "
            "the universe began is unavoidable.'<br><br>"
            "<strong>Premise 2 support:</strong> (a) BGV Theorem; (b) second law of thermodynamics "
            "(heat death would have been reached in infinite time); (c) impossibility of actual infinite "
            "regress of events (Craig, Sinclair — the Hilbert's Hotel argument).<br><br>"
            "<strong>Principal objections:</strong> (a) Quantum fluctuation from 'nothing' (Krauss — "
            "but Krauss's 'nothing' is a quantum vacuum, not metaphysical non-being); "
            "(b) brute fact causeless beginning (Oppy — but this abandons the Principle of Sufficient "
            "Reason selectively); (c) the cause could be impersonal (but only a free personal agent "
            "can explain a temporal effect from an eternal cause without the cause being eternal).<br><br>"
            "<strong>Theological implication:</strong> The cause of space, time, matter, and energy "
            "must be spaceless, timeless, immaterial, uncaused, and enormously powerful — converging "
            "on classical theism's doctrine of divine aseity."
        )
    },
    {
        "title": "The Ontological Argument (Modal Version)",
        "type": "Metaphysical",
        "content": (
            "<strong>Plantinga's Modal Formulation (The Nature of Necessity, 1974):</strong><br>"
            "(1) It is possible that a maximally great being exists.<br>"
            "(2) If a maximally great being is possible, then it exists in some possible world.<br>"
            "(3) If a maximally great being exists in some possible world, it exists in every possible world (by S5 modal axiom: if ◇□P then □P).<br>"
            "(4) Therefore, a maximally great being exists in every possible world, including the actual world.<br><br>"
            "<strong>Key concepts:</strong> Maximal greatness = maximal excellence in every possible world. "
            "Maximal excellence = omnipotence, omniscience, and moral perfection. The S5 modal axiom "
            "governs: necessary truths are necessarily necessary.<br><br>"
            "<strong>Principal objections:</strong> (a) No-maximally-great-island objection (Oppy): "
            "Why can't we run the same argument for an island? Answer: islands are spatiotemporally "
            "contingent by nature; 'maximally great island' is incoherent because greatness-making "
            "properties for islands are limited in a way that divine great-making properties are not. "
            "(b) The argument merely shifts the question: why is premise (1) true? Answer: if no "
            "incoherence in the concept of a maximally great being can be demonstrated, the possibility "
            "premise stands — and the burden falls on the atheist to show incoherence.<br><br>"
            "<strong>Note:</strong> Plantinga does not claim this argument is a decisive proof; he claims "
            "it shows that belief in God is <em>rational</em> — one who accepts the premises is "
            "within their epistemic rights to affirm the conclusion."
        )
    },
    {
        "title": "The Teleological Argument — Fine-Tuning",
        "type": "Scientific/Metaphysical",
        "content": (
            "<strong>Formulation (Collins, 2012):</strong><br>"
            "(1) The fine-tuning of the universe for life is either due to physical necessity, chance, or design.<br>"
            "(2) It is not due to physical necessity or chance (given the improbabilities).<br>"
            "(3) Therefore, it is due to design.<br><br>"
            "<strong>The constants:</strong><br>"
            "— Cosmological constant (Λ): fine-tuned to 1 part in 10<sup>120</sup> (Penrose). "
            "If larger by 1 part in 10<sup>60</sup>, no galaxies form.<br>"
            "— Gravitational constant (G): if stronger by 1 part in 10<sup>40</sup>, stars burn "
            "too quickly for life; if weaker, no stellar ignition.<br>"
            "— Strong nuclear force: ±2% change eliminates carbon or hydrogen; no chemistry.<br>"
            "— Weak nuclear force: governs stellar burning rates and supernova dynamics necessary "
            "for distributing heavy elements.<br><br>"
            "<strong>Against physical necessity:</strong> No known physical law requires the constants "
            "to have these values. String theory predicts a 'landscape' of 10<sup>500</sup> possible "
            "universes — confirming the constants are contingent, not necessary.<br><br>"
            "<strong>Against chance (multiverse):</strong> (a) Any multiverse-generating mechanism "
            "itself requires fine-tuned physics (the Boltzmann Brain problem — random fluctuations "
            "would generate observers more efficiently than fine-tuned universes); "
            "(b) Collins's 'Who Designed the Designer?' response: God's existence as a necessary "
            "being is not subject to the same regress as a contingent designer."
        )
    },
    {
        "title": "The Argument from Reason / Consciousness",
        "type": "Philosophical",
        "content": (
            "<strong>Lewis's Formulation (Miracles, ch. 3, 1947):</strong><br>"
            "If naturalism is true, then every mental event is fully explicable by prior physical causes. "
            "But if my thoughts are fully determined by non-rational physical causes, "
            "I have no grounds for trusting that they accurately track truth. "
            "Naturalism, if believed, undermines the very rational faculties by which it is believed — "
            "it is self-defeating.<br><br>"
            "<strong>Reppert's refined version (C.S. Lewis's Dangerous Idea, 2003):</strong><br>"
            "(1) If naturalism is true, there are no irreducible mental states — all are explicable by "
            "prior physical causes.<br>"
            "(2) Rational inference requires that conclusions be reached because of logical relations, "
            "not merely because of prior physical causes.<br>"
            "(3) Therefore, naturalism cannot account for rational inference.<br>"
            "(4) Rational inference exists.<br>"
            "(5) Therefore, naturalism is false.<br><br>"
            "<strong>The Anscombe Objection (1948):</strong> G.E.M. Anscombe argued Lewis conflated "
            "'because' in the causal sense and 'because' in the rational sense. Lewis revised the "
            "argument in the 2nd edition of Miracles (1960) to address this: the revised argument "
            "focuses on the ground/consequent relationship in inference — a relationship that requires "
            "intentionality and cannot be reduced to physical causation.<br><br>"
            "<strong>J.P. Moreland's consciousness argument</strong> (Consciousness and the Existence "
            "of God, 2008): the emergence of unified, first-person subjective consciousness from "
            "unconscious matter is inexplicable on naturalism but expected on theism, where a "
            "supremely conscious being is the explanatory terminus."
        )
    },
    {
        "title": "The Moral Argument",
        "type": "Philosophical",
        "content": (
            "<strong>Lewis/Craig Formulation:</strong><br>"
            "(1) If God does not exist, objective moral values and duties do not exist.<br>"
            "(2) Objective moral values and duties do exist.<br>"
            "(3) Therefore, God exists.<br><br>"
            "<strong>Premise 1 defense:</strong> On naturalism, moral facts would need to be "
            "identical with or supervenient on natural facts. But natural facts are descriptive "
            "(what is the case) and moral facts are normative (what ought to be). "
            "No amount of natural description generates a normative obligation. "
            "This is Hume's is-ought gap and Moore's naturalistic fallacy.<br><br>"
            "<strong>Premise 2 defense:</strong> Moral experience is data. The gratuitous torture "
            "of children for amusement is objectively wrong — not merely culturally disapproved. "
            "The universality of basic moral intuitions (harm-aversion, fairness, care for kin) "
            "across cultures suggests a common moral faculty tracking objective facts.<br><br>"
            "<strong>The Euthyphro Dilemma answered:</strong> Is something good because God commands "
            "it (making morality arbitrary) or does God command it because it is good (making goodness "
            "independent of God)? Third option: God's commands flow necessarily from his nature, "
            "which is itself the standard of goodness. God does not consult an external standard; "
            "he is the standard. Divine command theory is grounded in divine character theory.<br><br>"
            "<strong>Evolution objection answered:</strong> Even if evolution explains why we have "
            "the moral beliefs we do, it cannot account for their <em>truth</em>. "
            "Evolutionary debunking arguments (Joyce, Street) undermine naturalistic moral realism "
            "more effectively than they undermine theistic moral realism."
        )
    },
    {
        "title": "The Resurrection — Historical Case",
        "type": "Historical",
        "content": (
            "<strong>Minimal Facts Method (Habermas & Licona, 2004):</strong><br>"
            "Five facts accepted by virtually all NT historians, including sceptics:<br>"
            "(1) Jesus died by crucifixion under Pontius Pilate — Tacitus (Ann. 15.44), Josephus "
            "(Ant. 18.63–64), Lucian, Thallus, and the NT.<br>"
            "(2) The disciples believed they had post-mortem experiences of Jesus — 1 Cor 15:3–8 "
            "is a pre-Pauline creed (AD 35–38 at latest, per Hengel) listing named witnesses.<br>"
            "(3) Paul, a persecutor, converted on the basis of a resurrection appearance (Gal 1:11–16).<br>"
            "(4) James, a sceptic during Jesus' ministry (John 7:5), became a leader of the "
            "Jerusalem church and died for the resurrection claim (Josephus, Ant. 20.9.1).<br>"
            "(5) The empty tomb — attested by the Jewish polemic ('the disciples stole the body'), "
            "which concedes the tomb was empty while disputing the explanation.<br><br>"
            "<strong>Criterion of embarrassment:</strong> The first witnesses were women — legally "
            "inadmissible testimony in 1st-century Jewish courts (Josephus, Ant. 4.8.15). "
            "No fabricator would choose women as primary witnesses.<br><br>"
            "<strong>Principal naturalistic explanations:</strong><br>"
            "— Hallucination theory (Strauss, Lüdemann): cannot account for the empty tomb, "
            "the diversity of experiences (individuals, groups, Paul's road-to-Damascus event), "
            "or the bodily character of the appearances (Luke 24:39–43).<br>"
            "— Swoon theory: a half-dead man who crawled from a sealed tomb would not produce "
            "disciples willing to die for his resurrection — it would confirm his mortality.<br>"
            "— Legend theory: the 1 Cor 15 creed is too early (within 5 years of the crucifixion) "
            "for legendary embellishment of this magnitude."
        )
    },
    {
        "title": "Messianic Prophecy — Isaiah 53",
        "type": "Prophetic/Historical",
        "content": (
            "<strong>The DSS Evidence:</strong> 1QIsa-a (Great Isaiah Scroll, c. 125 BC) "
            "preserves Isaiah 53 with 95%+ consonantal agreement with the Masoretic Text — "
            "demonstrating textual stability for at least 2 centuries before Christ. "
            "The passage is indisputably pre-Christian.<br><br>"
            "<strong>The prophetic correspondences:</strong><br>"
            "— Rejected and despised by men (v. 3) → Matt 27:20–25<br>"
            "— Bore our griefs and sorrows (v. 4) → Matt 8:16–17 (explicit citation)<br>"
            "— Wounded for our transgressions (v. 5) → 1 Pet 2:24 (explicit citation)<br>"
            "— Silent before his accusers (v. 7) → Mark 14:61; 15:5<br>"
            "— Death with the wicked, burial with the rich (v. 9) → two criminals + Joseph's tomb<br>"
            "— Post-mortem vindication, seeing offspring (v. 10–11) → Resurrection<br><br>"
            "<strong>Naturalistic objections and responses:</strong><br>"
            "(a) Collective servant reading (Rashi, modern Jewish scholarship): "
            "The servant = Israel. Response: Isaiah elsewhere uses 'servant' for individuals "
            "(Cyrus, Moses); the servant suffers vicariously for Israel (v. 8: 'stricken for the "
            "transgression of my people') — Israel cannot suffer for Israel.<br>"
            "(b) The passage was written after Jesus (Deutero-Isaiah 2nd or 3rd century BC): "
            "even granting the latest critical dating, the DSS evidence requires the passage "
            "predates Christianity by a minimum of 125 years.<br>"
            "(c) Gospel authors shaped the narrative to fit Isaiah: "
            "the Passion account is independently attested in Paul (1 Cor 15:3–4), who "
            "preserves the creed within 5 years of the crucifixion — before the Gospels were written."
        )
    },
    {
        "title": "The Argument from Divine Hiddenness — and Response",
        "type": "Defensive Apologetics",
        "content": (
            "<strong>Schellenberg's Argument (Divine Hiddenness and Human Reason, 1993):</strong><br>"
            "(1) A perfectly loving God would always be open to relationship with any person.<br>"
            "(2) An open-to-relationship God would ensure that all reasonable, non-culpable "
            "non-belief is impossible — no one who sincerely seeks God would fail to find him.<br>"
            "(3) Non-culpable non-belief exists (sincere, seeking atheists and agnostics).<br>"
            "(4) Therefore, a perfectly loving God does not exist.<br><br>"
            "<strong>Response 1 — Moser (The Elusive God, 2008):</strong> "
            "Schellenberg presupposes that God's goal is propositional belief, but the biblical "
            "God seeks volitional surrender and transformed character. God may withhold propositional "
            "evidence that would merely produce intellectual assent without moral transformation. "
            "The 'hiddenness' is purposive, not absent.<br><br>"
            "<strong>Response 2 — Howard-Snyder:</strong> "
            "Premise (3) is unverifiable — we cannot determine whether an apparently non-culpable "
            "non-believer has no unconscious resistance to God. The category of 'non-culpable "
            "non-belief' may be empirically empty even if conceptually coherent.<br><br>"
            "<strong>Response 3 — Soul-Making (Hick):</strong> "
            "An environment of epistemic distance from God is the precondition for genuine "
            "free moral and spiritual development. Irresistible divine presence would overwhelm "
            "human freedom in a way that defeats the developmental purpose of creaturely existence.<br><br>"
            "<strong>Scriptural engagement:</strong> "
            "The hiddenness of God is a biblical theme, not an embarrassment (Isa 45:15: "
            "'Truly you are a God who hides himself'; Ps 13; 22:1; Job 23:3). "
            "The Psalms of lament model the response to divine silence: continued address, not apostasy."
        )
    },
]


CHURCH_FATHERS = [
    {"name":"Justin Martyr","dates":"c. 100–165 AD","role":"First Christian Apologist",
     "contribution":"Author of the First and Second Apology (addressed to Emperor Antoninus Pius) and the Dialogue with Trypho — the foundational texts of Christian engagement with Greco-Roman philosophy and Judaism. Justin's Logos theology argued that the divine Logos who became incarnate in Christ was the same rational principle recognized (partially) by Plato and the Stoics. This laid the groundwork for every subsequent synthesis of faith and reason.",
     "key_work":"First Apology (c. 155 AD); Dialogue with Trypho (c. 160 AD)"},
    {"name":"Irenaeus of Lyon","dates":"c. 130–202 AD","role":"Anti-Gnostic Theologian",
     "contribution":"Against Heresies (Adversus Haereses) — the systematic refutation of Gnosticism in five volumes. Developed the concept of recapitulation (ἀνακεφαλαίωσις, anakephalaiōsis): Christ as the second Adam who recapitulates and reverses every stage of Adam's disobedience. Also developed the apostolic succession argument as the criterion of orthodox teaching.",
     "key_work":"Adversus Haereses (c. 180 AD)"},
    {"name":"Tertullian","dates":"c. 155–220 AD","role":"First Major Latin Theologian",
     "contribution":"First theologian to write in Latin and coin the technical Trinitarian vocabulary: <em>trinitas</em> (Trinity), <em>substantia</em> (substance/essence), <em>persona</em> (person). His Apologeticus is a legal defense of Christianity before Roman law. Later converted to Montanism — a cautionary note about the instability of even brilliant theologians.",
     "key_work":"Apologeticus (c. 197 AD); Against Praxeas (c. 213 AD)"},
    {"name":"Origen of Alexandria","dates":"c. 185–253 AD","role":"Biblical Scholar and Systematician",
     "contribution":"Pioneer of systematic theology (De Principiis) and the first biblical critic: produced the Hexapla (six-column OT comparison of MT, LXX, and four other Greek versions). Developed the threefold sense of Scripture (literal, moral, allegorical). His theology was later condemned (Origenism) for speculative positions on pre-existence of souls and universal restoration.",
     "key_work":"De Principiis (c. 220 AD); Contra Celsum (c. 248 AD)"},
    {"name":"Athanasius of Alexandria","dates":"c. 296–373 AD","role":"Defender of Nicene Orthodoxy",
     "contribution":"The great defender of homoousios (same substance) against Arianism. Exiled five times by four emperors; the phrase <em>Athanasius contra mundum</em> ('Athanasius against the world') captures his theological tenacity. De Incarnatione (written c. 318, before the Arian controversy) presents the most elegant patristic account of why God became man.",
     "key_work":"De Incarnatione Verbi Dei (c. 318 AD); On the Incarnation"},
    {"name":"Augustine of Hippo","dates":"354–430 AD","role":"Architect of Western Theology",
     "contribution":"The most influential theologian in Western Christianity. Confessions (the first autobiography in the Western tradition) and City of God (the first philosophy of history) are foundational cultural documents. His theology of grace and predestination shaped the Reformation; his Trinitarian theology (De Trinitate) remains the Western standard; his epistemology (divine illumination) influenced medieval philosophy through Anselm and Aquinas.",
     "key_work":"Confessions (c. 397 AD); De Civitate Dei (413–426 AD); De Trinitate"},
    {"name":"Anselm of Canterbury","dates":"1033–1109 AD","role":"Bridge from Patristics to Scholasticism",
     "contribution":"Formulated the Ontological Argument for God's existence (Proslogion, 1077): 'that than which nothing greater can be conceived' must exist in reality, not merely in the mind. Wrote Cur Deus Homo (Why God Became Man, 1098) — the first systematic satisfaction theory of the atonement: Christ's death satisfies the honor-debt owed to God by human sin. Both works continue to generate scholarly literature today.",
     "key_work":"Proslogion (1077 AD); Cur Deus Homo (1098 AD)"},
    {"name":"Thomas Aquinas","dates":"1225–1274 AD","role":"Prince of Scholastic Theology",
     "contribution":"Synthesized Aristotelian philosophy and Christian theology. The Five Ways (Summa Theologiae I.Q2.A3) remain the most influential cosmological and teleological arguments in Western thought. His natural theology established the intellectual architecture for Catholic apologetics and deeply influenced Protestant scholasticism. The Summa Contra Gentiles is the most rigorous medieval engagement with Islamic and Jewish philosophical theology.",
     "key_work":"Summa Theologiae (1265–1274 AD); Summa Contra Gentiles (1259–1265 AD)"},
    {"name":"John Chrysostom","dates":"c. 347–407 AD","role":"Preacher and Exegete",
     "contribution":"Archbishop of Constantinople; universally regarded as the greatest preacher of the patristic era (Chrysostom = 'golden-mouthed'). His homiletical commentaries on Matthew, John, Romans, Galatians, and the Pauline epistles remain among the most practically useful patristic resources for preachers. His literal-grammatical hermeneutic (Antiochene school) contrasts with Origen's allegorism.",
     "key_work":"Homilies on the Gospel of John (c. 390 AD); Homilies on Romans"},
    {"name":"Polycarp of Smyrna","dates":"c. 69–155 AD","role":"Apostolic Father",
     "contribution":"Direct disciple of the Apostle John; his martyrdom is documented in one of the earliest hagiographical texts (Martyrdom of Polycarp, c. 155 AD). His Epistle to the Philippians demonstrates continuity between apostolic teaching and 2nd-century Christianity. His personal connection to John makes him a critical link in the chain of apostolic testimony for the historical reliability of the Fourth Gospel.",
     "key_work":"Epistle to the Philippians (c. 110 AD); Martyrdom of Polycarp (c. 155 AD)"},
]


MANUSCRIPT_DATA = {
    "New Testament (Greek)":  {"manuscripts": 5856, "earliest_copy": "P52 (~AD 125)",  "gap_years": 25},
    "Iliad (Homer)":          {"manuscripts": 643,  "earliest_copy": "~400 BC",        "gap_years": 400},
    "Gallic Wars (Caesar)":   {"manuscripts": 251,  "earliest_copy": "~900 AD",        "gap_years": 950},
    "Annals (Tacitus)":       {"manuscripts": 20,   "earliest_copy": "~1100 AD",       "gap_years": 1000},
    "History (Thucydides)":   {"manuscripts": 96,   "earliest_copy": "~900 AD",        "gap_years": 1300},
    "Works (Plato)":          {"manuscripts": 210,  "earliest_copy": "~895 AD",        "gap_years": 1200},
    "NT (all languages)":     {"manuscripts": 25000,"earliest_copy": "P52 (~AD 125)",  "gap_years": 25},
}


APIBIBLE_TRANSLATIONS = {
    "KJV":          "de4e12af7f28f599-02",
    "NASB":         "f72b840c855f362c-04",
    "ESV":          "9879dbb7cfe39e4d-04",
    "NRSV":         "55212e3cf5d04d49-01",
    "NET":          "f72b840c855f362c-04",
    "NIV":          "78a9f6124f344018-01",
    "YLT":          "c315fa9f71d4af3a-02",
    "Douay-Rheims": "179568874c45066f-01",
    "ASV":          "06125adad2d5898a-01",
    "CSB":          "a556c5305ee15c3f-01",
}


# ─────────────────────────────────────────────
# SCRIPTURE API FUNCTIONS  (cached on pure strings)
# ─────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_scripture(reference: str, translation: str = "kjv") -> dict:
    url = f"https://bible-api.com/{requests.utils.quote(reference)}?translation={translation}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("verses"):
                return data
    except Exception:
        pass
    for key, verses in KJV_FALLBACK.items():
        if reference.lower().replace(" ", "") in key.lower().replace(" ", ""):
            return {"verses": verses, "reference": reference,
                    "translation_name": "King James Version (offline fallback)",
                    "fallback": True}
    return {"error": "Unable to retrieve. Check reference format.", "verses": []}


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_esv(reference: str, esv_key: str) -> dict:
    if not esv_key:
        return {"verses": [], "error": "No ESV key"}
    auth = esv_key if esv_key.startswith("Token ") else "Token " + esv_key
    params = {
        "q": reference, "include-headings": False, "include-footnotes": False,
        "include-verse-numbers": True, "include-short-copyright": False,
        "include-passage-references": False,
    }
    try:
        r = requests.get("https://api.esv.org/v3/passage/text/",
                         params=params, headers={"Authorization": auth}, timeout=10)
        if r.status_code == 200:
            passages = r.json().get("passages", [])
            if passages:
                raw = passages[0].strip()
                matches = re.findall(r'\[(\d+)\]\s*(.*?)(?=\[\d+\]|$)', raw, re.DOTALL)
                verses = [{"verse": int(n), "text": t.strip().replace("\n", " ")}
                          for n, t in matches if t.strip()]
                return {"verses": verses or [{"verse": 1, "text": raw}],
                        "reference": reference,
                        "translation_name": "English Standard Version (ESV)"}
        elif r.status_code == 401:
            return {"verses": [], "error": "ESV key invalid"}
    except Exception:
        pass
    return {"verses": [], "error": "ESV API unavailable"}


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_apibible(reference: str, bible_id: str, api_key: str) -> dict:
    if not api_key:
        return {"verses": [], "error": "No API.Bible key"}
    try:
        r = requests.get(
            f"https://api.scripture.api.bible/v1/bibles/{bible_id}/search",
            params={"query": reference, "limit": 1},
            headers={"api-key": api_key}, timeout=10)
        if r.status_code == 200:
            passages = r.json().get("data", {}).get("passages", [])
            if passages:
                clean = re.sub(r'<[^>]+>', ' ', passages[0].get("content", "")).strip()
                clean = re.sub(r'\s+', ' ', clean)
                return {"verses": [{"verse": 1, "text": clean}],
                        "reference": reference, "translation_name": bible_id}
    except Exception:
        pass
    return {"verses": [], "error": "API.Bible unavailable"}


# ─────────────────────────────────────────────
# AI — SYSTEM PROMPT  (Craig aesthetic)
# ─────────────────────────────────────────────

SCHOLAR_PROMPT = """You are a rigorous Christian biblical scholar and apologist.
Think: William Lane Craig in analytical precision, N.T. Wright in historical depth,
D.A. Carson in exegetical care. You operate within Sententia Bible Lab.

HERMENEUTICAL METHOD
Historical-grammatical exegesis as primary method. Redemptive-historical approach
(Geerhardus Vos, D.A. Carson). Privilege authorial intent within original context.

THEOLOGICAL TRADITION
Broadly Reformed evangelical. Represent Calvinist, Arminian, Lutheran, Catholic,
and Eastern Orthodox positions accurately and without caricature.

SCHOLARLY SOURCES
Commentaries: Brown (AB), Carson (Pillar), Morris/Moo/Schreiner/Fee/Köstenberger (NICNT/BECNT),
Oswalt (NICOT), Kidner (TOTC), Craigie/Wright (WBC/NIB), O'Brien (NIGTC).
Apologetics: Craig, Plantinga, Habermas & Licona, Collins, Reppert, Moreland.
Languages: Greek NT (NA28), Hebrew OT (BHS). Cite Strong's numbers when relevant.

MANDATORY RESPONSE STRUCTURE
Every substantive response MUST use these exact Markdown section headers:

## Historical Context
## Linguistic Analysis
## Scholarly Dialogue
## Thematic Synthesis
## Apologetic Interface

(Omit 'Apologetic Interface' only when strictly irrelevant.)

TONE
Articulate, objective, precise. Write as a scholar addressing peers.
Cite scholars by surname and work. Flag genuine uncertainty. Never fabricate citations.
No condescension. No vagueness. Distinguish exegetical findings from theological inferences."""


# ─────────────────────────────────────────────
# AI FUNCTIONS
#
# Correct caching architecture:
# - @st.cache_data requires hashable arguments only.
# - secrets objects are NOT hashable → never pass them as cache arguments.
# - Pattern: resolve key to plain str → pass str to cached function.
# - Cache key = hash(messages_json + anthropic_key_str) — deterministic.
# - TTL 24h: identical queries never re-hit the API within a session.
# ─────────────────────────────────────────────

@st.cache_data(show_spinner="Consulting the AI Scholar...", ttl=86400)
def _ai_call_cached(messages_json: str, anthropic_key: str, max_tokens: int) -> str:
    """Inner cached function. All args are plain strings — hashable."""
    messages = json.loads(messages_json)
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": anthropic_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": max_tokens,
                "system": SCHOLAR_PROMPT,
                "messages": messages,
            },
            timeout=90,
        )
        if r.status_code == 200:
            return r.json()["content"][0]["text"]
        if r.status_code == 401:
            return "⚠ API key invalid — verify ANTHROPIC_API_KEY in Streamlit secrets."
        return f"⚠ API error {r.status_code}: {r.text[:300]}"
    except Exception as e:
        return f"⚠ Request failed: {e}"


def ai(messages: list, key: str, max_tokens: int = 1400) -> str:
    """Public wrapper: serialises messages to JSON string for cache-safe call."""
    if not key:
        return "⚠ ANTHROPIC_API_KEY not configured in Streamlit secrets."
    return _ai_call_cached(json.dumps(messages, ensure_ascii=False), key, max_tokens)


def ai_single(prompt: str, key: str, max_tokens: int = 2000) -> str:
    return ai([{"role": "user", "content": prompt}], key, max_tokens)


def ai_analyse_passage(ref: str, text: str, trans: str, key: str) -> str:
    return ai_single(
        f"Provide a graduate-level exegetical analysis of {ref} ({trans}):\n\n\"{text}\"\n\n"
        "Use the mandatory section headers exactly: Historical Context, Linguistic Analysis, "
        "Scholarly Dialogue, Thematic Synthesis, Apologetic Interface. "
        "Cite named scholars. Flag interpretive disputes. Do not pad.", key, 2200)


def ai_steelman(debate: str, label: str, argument: str, texts: list, key: str) -> str:
    return ai_single(
        f"Construct the strongest possible version of the {label} position in: \'{debate}\'\n\n"
        f"Position as given:\n{argument}\n\nKey texts: {', '.join(texts)}\n\n"
        "Do not summarise — STEELMAN it. Build the most exegetically and philosophically rigorous "
        "version its best defenders actually make. Address the two or three strongest objections "
        "and show how a sophisticated defender answers each. Use the mandatory section headers: "
        "Historical Context, Linguistic Analysis, Scholarly Dialogue, Thematic Synthesis. "
        "This is charitable reconstruction, not personal advocacy.", key, 1900)


def ai_inquiry(inquiry: str, ref: str, passage_text: str, trans: str, key: str) -> str:
    ctx = (f"Passage loaded: {ref} ({trans})\n\"{passage_text}\"\n\n"
           if passage_text else "")
    return ai_single(
        f"{ctx}Primary Inquiry: {inquiry}\n\n"
        "Respond with full scholarly rigour using the mandatory section headers: "
        "Historical Context, Linguistic Analysis, Scholarly Dialogue, Thematic Synthesis, "
        "Apologetic Interface. Cite named scholars. Distinguish exegetical findings "
        "from theological inferences. Be precise.", key, 2200)


# ─────────────────────────────────────────────
# SEMANTIC GRAPH
# Stateful: stored in st.session_state, rebuilt ONLY when passage text changes.
# Uses Plotly (installed in Streamlit Cloud). rdflib/networkx are NOT available
# without explicit requirements.txt entries — Plotly achieves identical UX.
# ─────────────────────────────────────────────

def _hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def build_semantic_graph(verse_text: str, ref: str) -> "go.Figure":
    words = set(re.findall(r'\b[a-z]{4,}\b', verse_text.lower()))
    matched = {k: v for k, v in STRONGS_LEXICON.items()
               if k in words or v["tr"].lower() in words}

    nodes, edges = [], []
    nodes.append({"id": ref, "label": ref, "t": "passage", "x": 0.0, "y": 0.0})

    n = max(len(matched), 1)
    for i, (term, entry) in enumerate(matched.items()):
        a = 2 * math.pi * i / n
        nodes.append({"id": term, "label": f"{entry['gk']}\n{entry['tr']}",
                       "t": "lexical", "x": .44 * math.cos(a), "y": .44 * math.sin(a)})
        edges.append((ref, term))

    DOCTRINAL = {
        "Soteriology":  ["grace", "faith", "justification", "atonement", "righteousness", "sanctification"],
        "Christology":  ["logos", "messiah", "morphe"],
        "Pneumatology": ["pneuma"],
        "Ecclesiology": ["ekklesia"],
        "Eschatology":  ["parousia"],
    }
    di = 0
    for doctrine, terms in DOCTRINAL.items():
        if any(t in matched for t in terms):
            a = 2 * math.pi * di / max(len(DOCTRINAL), 1)
            nodes.append({"id": doctrine, "label": doctrine, "t": "doctrine",
                          "x": .77 * math.cos(a), "y": .77 * math.sin(a)})
            for t in terms:
                if t in matched:
                    edges.append((doctrine, t))
            di += 1

    nmap = {n["id"]: n for n in nodes}
    ex, ey = [], []
    for s, t in edges:
        if s in nmap and t in nmap:
            ex += [nmap[s]["x"], nmap[t]["x"], None]
            ey += [nmap[s]["y"], nmap[t]["y"], None]

    colors = {"passage": SCARLET, "lexical": GOLD, "doctrine": "#7B9CDF"}
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ex, y=ey, mode="lines",
                             line=dict(color="rgba(212,175,55,.18)", width=1),
                             hoverinfo="none", showlegend=False))
    for tp in ("passage", "doctrine", "lexical"):
        sub = [n for n in nodes if n["t"] == tp]
        if sub:
            fig.add_trace(go.Scatter(
                x=[n["x"] for n in sub], y=[n["y"] for n in sub],
                mode="markers+text",
                marker=dict(size=18 if tp == "passage" else (13 if tp == "doctrine" else 10),
                            color=colors[tp], line=dict(color=NAVY, width=2)),
                text=[n["label"] for n in sub], textposition="top center",
                textfont=dict(size=8, color=CREAM, family="monospace"),
                hovertemplate="%{text}<extra></extra>", name=tp.capitalize()))

    fig.update_layout(
        title=dict(text=f"Semantic Concept Map — {ref}",
                   font=dict(family="Georgia,serif", size=13, color=GOLD), x=.5),
        plot_bgcolor=NAVY, paper_bgcolor=BIB_BLUE,
        font=dict(family="monospace", color=CREAM),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=40, b=20), height=360, showlegend=True,
        legend=dict(font=dict(color=CREAM, size=9), bgcolor="rgba(0,0,0,0)"))
    return fig


def build_mss_chart() -> "go.Figure":
    rows = [(k, v) for k, v in MANUSCRIPT_DATA.items() if "all languages" not in k]
    rows.sort(key=lambda x: x[1]["manuscripts"])
    labels = [r[0] for r in rows]
    vals   = [r[1]["manuscripts"] for r in rows]
    cdata  = [(r[1]["earliest_copy"], r[1]["gap_years"]) for r in rows]
    colors = [SCARLET if "New Testament" in r[0] else GOLD for r in rows]
    fig = go.Figure(go.Bar(
        y=labels, x=vals, orientation="h",
        marker_color=colors, marker_line_color=NAVY, marker_line_width=1,
        text=[f"{v:,}" for v in vals], textposition="outside",
        textfont=dict(color=GOLD, size=10, family="monospace"),
        hovertemplate="<b>%{y}</b><br>MSS: %{x:,}<br>Earliest: %{customdata[0]}<br>Gap: %{customdata[1]} yrs<extra></extra>",
        customdata=cdata))
    fig.update_layout(
        title=dict(text="NT Manuscripts vs. Classical Antiquity",
                   font=dict(family="Georgia,serif", size=14, color=GOLD), x=.5),
        plot_bgcolor=NAVY, paper_bgcolor=BIB_BLUE,
        font=dict(family="monospace", color=GOLD),
        xaxis=dict(title="Extant Manuscripts", gridcolor="rgba(212,175,55,.07)", color=GOLD),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", color=GOLD),
        margin=dict(l=10, r=70, t=42, b=32), height=310)
    return fig


# ─────────────────────────────────────────────
# RESOLVE KEYS  (outside sidebar — available to all tabs)
# ─────────────────────────────────────────────
anthropic_key = get_anthropic_key()
esv_key       = get_esv_key()
api_key       = get_api_bible_key()


# ─────────────────────────────────────────────
# SIDEBAR — NAVIGATION RAIL
# ─────────────────────────────────────────────
with st.sidebar:
    # ── Wordmark ────────────────────────────────
    st.markdown(
        f'<div style="text-align:center;padding:1.1rem 0 .6rem">'
        f'<div style="font-size:1.7rem;margin-bottom:.3rem;filter:drop-shadow(0 0 8px rgba(212,175,55,.3))">✝️</div>'
        f'<div style="font-family:Playfair Display,Georgia,serif;font-size:1.08rem;'
        f'font-weight:600;color:{GOLD};letter-spacing:.05em;line-height:1.2">'
        f'Sententia<br>Bible Lab</div>'
        f'<div style="font-size:.46rem;color:{LT_GOLD};opacity:.5;letter-spacing:.25em;'
        f'margin-top:.3rem;text-transform:uppercase">Apologetics Codex</div>'
        f'<div style="border-top:1px solid rgba(212,175,55,.18);margin:.75rem 0 .25rem"></div>'
        f'</div>', unsafe_allow_html=True)

    # ── Navigation Rail ──────────────────────────
    st.markdown(
        f'<div style="font-size:.5rem;color:{LT_GOLD};opacity:.5;'
        f'letter-spacing:.22em;margin:.2rem 0 .4rem .3rem;text-transform:uppercase">'
        f'Navigation</div>', unsafe_allow_html=True)

    nav = st.radio(
        "nav", [
            "🏛️  Scholar's Desk",
            "📊  Textual Mapping",
            "⚙️  Lab Settings",
        ],
        label_visibility="collapsed",
        key="nav_rail",
    )

    st.markdown(
        f'<div style="border-top:1px solid rgba(212,175,55,.12);margin:.8rem 0 .6rem"></div>',
        unsafe_allow_html=True)

    # ── Translation Selector ─────────────────────
    st.markdown(
        f'<div style="font-size:.5rem;color:{LT_GOLD};opacity:.5;'
        f'letter-spacing:.22em;margin-bottom:.4rem;text-transform:uppercase">'
        f'Primary Translation</div>', unsafe_allow_html=True)
    translation = st.selectbox(
        "Translation", ["kjv", "web", "bbe"], index=0, label_visibility="collapsed",
        format_func=lambda x: {"kjv": "KJV — King James",
                                "web": "WEB — World English",
                                "bbe": "BBE — Basic English"}[x])

    # ── API Status Indicators ────────────────────
    st.markdown(
        f'<div style="border-top:1px solid rgba(212,175,55,.12);margin:.7rem 0 .5rem"></div>'
        f'<div style="font-size:.5rem;color:{LT_GOLD};opacity:.5;'
        f'letter-spacing:.22em;margin-bottom:.45rem;text-transform:uppercase">'
        f'Active Services</div>', unsafe_allow_html=True)

    for label, active, icon in [
        ("AI Scholar",  bool(anthropic_key), "🤖"),
        ("ESV API",     bool(esv_key),       "📖"),
        ("API.Bible",   bool(api_key),       "🌐"),
    ]:
        dot_color = "#4caf50" if active else "#555"
        txt_color = GOLD if active else "rgba(245,225,122,.28)"
        status    = "Active" if active else "Add key to secrets"
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:.5rem;'
            f'padding:.3rem .4rem;margin-bottom:.18rem;border-radius:4px;'
            f'background:rgba({"212,175,55" if active else "0,0,0"},.04)">'
            f'<div style="width:6px;height:6px;border-radius:50%;'
            f'background:{dot_color};flex-shrink:0;'
            f'box-shadow:{"0 0 4px #4caf50" if active else "none"}"></div>'
            f'<div style="font-size:.62rem;color:{txt_color};'
            f'font-family:IBM Plex Mono,monospace;letter-spacing:.04em">'
            f'{icon} {label}</div>'
            f'<div style="font-size:.52rem;color:rgba(245,225,122,.3);'
            f'margin-left:auto;font-style:italic">{status if not active else ""}</div>'
            f'</div>', unsafe_allow_html=True)

    if api_key:
        st.markdown(
            f'<div style="font-size:.5rem;color:{LT_GOLD};opacity:.4;'
            f'letter-spacing:.18em;margin:.5rem 0 .3rem;text-transform:uppercase">'
            f'Premium Translation</div>', unsafe_allow_html=True)
        premium_trans = st.selectbox(
            "Premium Translation", list(APIBIBLE_TRANSLATIONS.keys()),
            index=2, label_visibility="collapsed")
    else:
        premium_trans = None

    # ── Quick Load ───────────────────────────────
    st.markdown(
        f'<div style="border-top:1px solid rgba(212,175,55,.12);margin:.8rem 0 .5rem"></div>'
        f'<div style="font-size:.5rem;color:{LT_GOLD};opacity:.5;'
        f'letter-spacing:.22em;margin-bottom:.45rem;text-transform:uppercase">'
        f'Quick Load</div>', unsafe_allow_html=True)

    QUICK = {
        "John 3:16":          "Gospel in miniature",
        "John 1:1-18":        "Johannine Prologue",
        "Romans 3:21-26":     "Heart of Pauline soteriology",
        "Romans 8:28-39":     "Golden chain of providence",
        "Isaiah 53:1-12":     "Suffering Servant",
        "Philippians 2:5-11": "Carmen Christi — kenōsis",
        "Genesis 1:1-5":      "Creation ex nihilo",
        "Psalm 22":           "Messianic dereliction",
        "Daniel 7:13-14":     "Son of Man pericope",
        "Hebrews 11:1-6":     "Definition of faith",
        "Exodus 3:14":        "The divine name YHWH",
    }
    for ref, desc in QUICK.items():
        if st.button(ref, key=f"qr_{ref}", use_container_width=True, help=desc):
            st.session_state.quick_ref = ref
            st.session_state.pop("ai_analysis", None)

    # ── Footer ───────────────────────────────────
    st.markdown(
        f'<div style="border-top:1px solid rgba(212,175,55,.1);margin:.9rem 0 .4rem"></div>'
        f'<div style="font-size:.44rem;color:{LT_GOLD};opacity:.25;text-align:center;'
        f'line-height:2.2;letter-spacing:.1em">'
        f'SOLA SCRIPTURA · SOLI DEO GLORIA<br>'
        f'SOLUS CHRISTUS · SOLA GRATIA<br>SOLA FIDE</div>',
        unsafe_allow_html=True)



# ─────────────────────────────────────────────
# PAGE HEADER — centered serif wordmark
# ─────────────────────────────────────────────
st.markdown(
    f'<div style="text-align:center;padding:.4rem 0 .6rem">'
    f'<div style="font-family:Playfair Display,Georgia,serif;font-size:2.1rem;'
    f'font-weight:700;color:{GOLD};letter-spacing:.05em;'
    f'text-shadow:0 0 40px rgba(212,175,55,.18);line-height:1.1">'
    f'Sententia Bible Lab</div>'
    f'<div style="font-family:EB Garamond,Georgia,serif;font-size:.88rem;'
    f'color:{LT_GOLD};opacity:.55;letter-spacing:.35em;margin-top:.3rem;'
    f'font-style:italic">Christian Apologetics Codex</div>'
    f'<div style="width:60px;height:1px;background:linear-gradient('
    f'90deg,transparent,{GOLD},transparent);margin:.5rem auto .3rem"></div>'
    f'</div>', unsafe_allow_html=True)

# ── Metrics strip ──
m1, m2, m3, m4 = st.columns(4)
m1.metric("Canonical Books",    "66")
m2.metric("NT MSS (Greek)",     "5,856")
m3.metric("NT MSS (all lang.)", "25,000+")
m4.metric("Compositional Span", "~1,500 yrs")
st.markdown("<hr/>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# NAV RAIL ROUTER — render based on sidebar selection
# ═══════════════════════════════════════════════════════
active_nav = st.session_state.get("nav_rail", "🏛️  Scholar's Desk")


# ────────────────────────────────────────────────────────
# VIEW: TEXTUAL MAPPING
# (moved above Scholar's Desk so it renders when selected)
# ────────────────────────────────────────────────────────
if active_nav == "📊  Textual Mapping":
    st.markdown(
        f'<div style="text-align:center;margin-bottom:1rem">'
        f'<div style="font-family:Playfair Display,Georgia,serif;font-size:1.3rem;'
        f'color:{GOLD};letter-spacing:.06em">Quantitative Textual Mapping</div>'
        f'<div style="font-size:.58rem;color:{LT_GOLD};opacity:.5;letter-spacing:.18em;'
        f'margin-top:.2rem;text-transform:uppercase">Semantic Graph · Lexical Frequency · Manuscript Attestation</div>'
        f'</div>', unsafe_allow_html=True)

    sdata = st.session_state.get("scripture_data", {})
    sref  = st.session_state.get("scripture_ref", "")

    if sdata.get("verses"):
        vtxt_b = " ".join(v.get("text", "") for v in sdata["verses"])
        h = _hash(vtxt_b + sref)
        if st.session_state.get("graph_hash") != h:
            st.session_state.graph_fig  = build_semantic_graph(vtxt_b, sref)
            st.session_state.graph_hash = h
        sec_head("Semantic Concept Map", sref)
        st.plotly_chart(st.session_state.graph_fig, use_container_width=True)

        words = re.findall(r'\b[a-zA-Z]{4,}\b', vtxt_b.lower())
        stop  = {"that","this","with","have","from","they","been","were","unto","thou",
                 "thee","thine","hath","doth","shall","will","your","which","their",
                 "there","when","what","also"}
        freq = {}
        for w in words:
            if w not in stop:
                freq[w] = freq.get(w, 0) + 1
        if freq:
            ornament()
            sec_head("Lexical Frequency", "Top 15 substantive terms")
            fdf = pd.DataFrame(
                sorted(freq.items(), key=lambda x: -x[1])[:15],
                columns=["Term", "Frequency"])
            st.dataframe(fdf, hide_index=True, use_container_width=True)
    else:
        card(
            f'<div style="font-size:.82rem;color:{CREAM};text-align:center;'
            f'padding:.4rem 0">Load a passage in the Scripture Lab to generate the semantic map.</div>',
            LT_GOLD)

    ornament()
    sec_head("NT Manuscript Attestation vs. Classical Antiquity")
    st.plotly_chart(build_mss_chart(), use_container_width=True)


# ────────────────────────────────────────────────────────
# VIEW: LAB SETTINGS
# ────────────────────────────────────────────────────────
elif active_nav == "⚙️  Lab Settings":
    st.markdown(
        f'<div style="text-align:center;margin-bottom:1rem">'
        f'<div style="font-family:Playfair Display,Georgia,serif;font-size:1.3rem;'
        f'color:{GOLD};letter-spacing:.06em">Laboratory Settings</div>'
        f'<div style="font-size:.58rem;color:{LT_GOLD};opacity:.5;letter-spacing:.18em;'
        f'margin-top:.2rem;text-transform:uppercase">API Configuration · Commentary Series · Manuscript Data</div>'
        f'</div>', unsafe_allow_html=True)

    lc, rc = st.columns(2, gap="large")
    with lc:
        sec_head("API Configuration")
        for label, active, key_hint, icon in [
            ("Anthropic AI Scholar", bool(anthropic_key), "ANTHROPIC_API_KEY", "🤖"),
            ("ESV Bible API",        bool(esv_key),       "ESV_API_KEY",       "📖"),
            ("API.Bible Premium",    bool(api_key),       "BIBLE_API_KEY",     "🌐"),
        ]:
            status_color = "#4caf50" if active else SCARLET
            status_text  = "Configured and active" if active else f"Add {key_hint} to Streamlit secrets"
            st.markdown(
                f'<div style="background:rgba(4,9,26,.6);border:1px solid rgba(212,175,55,.13);'
                f'border-radius:5px;padding:.75rem 1rem;margin-bottom:.55rem;'
                f'border-left:3px solid {status_color}">'
                f'<div style="font-size:.78rem;color:{GOLD};margin-bottom:.2rem">{icon} {label}</div>'
                f'<div style="font-size:.65rem;color:{"#4caf50" if active else LT_GOLD};'
                f'opacity:{".9" if active else ".55"}">{status_text}</div>'
                f'</div>', unsafe_allow_html=True)

        sec_head("AI Model", "Current configuration")
        st.markdown(
            f'<div style="background:rgba(4,9,26,.6);border:1px solid rgba(212,175,55,.13);'
            f'border-radius:5px;padding:.75rem 1rem">'
            f'<div style="font-size:.72rem;color:{GOLD};margin-bottom:.35rem">claude-haiku-4-5-20251001</div>'
            f'<div style="font-size:.62rem;color:{LT_GOLD};opacity:.55;line-height:1.7">'
            f'Max tokens: 2,200 (analysis) · 1,900 (steelman) · 1,400 (chat)<br>'
            f'Cache TTL: 86,400 seconds (24h)<br>'
            f'Pattern: JSON-serialised messages → cached string hash</div>'
            f'</div>', unsafe_allow_html=True)

    with rc:
        sec_head("Commentary Series Reference")
        st.dataframe(pd.DataFrame([
            {"Abbrev.": "AB",     "Series": "Anchor Bible",                         "Character": "Critical-historical; definitive philology"},
            {"Abbrev.": "ICC",    "Series": "International Critical Commentary",    "Character": "Philologically rigorous; multi-author"},
            {"Abbrev.": "NICNT",  "Series": "New International Commentary — NT",    "Character": "Evangelical; solid exegesis"},
            {"Abbrev.": "NIGTC",  "Series": "New International Greek Testament Comm.","Character": "Greek text focus; advanced"},
            {"Abbrev.": "WBC",    "Series": "Word Biblical Commentary",             "Character": "Mixed; includes textual notes"},
            {"Abbrev.": "BECNT",  "Series": "Baker Exegetical Commentary",          "Character": "Evangelical; Greek text"},
            {"Abbrev.": "Pillar", "Series": "Pillar NT Commentary (Carson)",        "Character": "Balanced; recommended"},
            {"Abbrev.": "TOTC",   "Series": "Tyndale OT/NT Commentaries",          "Character": "Accessible evangelical introduction"},
        ]), hide_index=True, use_container_width=True)

        ornament()
        sec_head("Manuscript Transmission Table")
        st.dataframe(pd.DataFrame([
            {"Document": "NT (Greek)",     "MSS": "5,856",  "Earliest": "P52 ~AD 125", "Gap": "25 yrs"},
            {"Document": "NT (all lang.)", "MSS": "25,000+","Earliest": "P52 ~AD 125", "Gap": "25 yrs"},
            {"Document": "1QIsa-a (DSS)",  "MSS": "1",      "Earliest": "~125 BC",     "Gap": "~350 yrs"},
            {"Document": "Iliad",          "MSS": "643",    "Earliest": "~400 BC",     "Gap": "400 yrs"},
            {"Document": "Plato",          "MSS": "210",    "Earliest": "~895 AD",     "Gap": "1,200 yrs"},
            {"Document": "Caesar",         "MSS": "251",    "Earliest": "~900 AD",     "Gap": "950 yrs"},
        ]), hide_index=True, use_container_width=True)


# ────────────────────────────────────────────────────────
# VIEW: SCHOLAR'S DESK (default)
# ────────────────────────────────────────────────────────
else:

    # ══════════════════════════════════════════════════
    # COMMAND CENTER — Primary Inquiry
    # ══════════════════════════════════════════════════
    st.markdown('<div class="cmd-center">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:Playfair Display,Georgia,serif;font-size:.95rem;'
        f'font-weight:600;color:{GOLD};letter-spacing:.04em;margin-bottom:.25rem;text-align:center">'
        f'Primary Inquiry</div>'
        f'<div class="cmd-label" style="text-align:center">'
        f'STATE YOUR RESEARCH QUESTION — AI SCHOLAR WILL RESPOND IN PARCHMENT VIEW</div>',
        unsafe_allow_html=True)

    inquiry = st.text_area(
        "Primary Inquiry",
        placeholder=(
            "e.g. What is the exegetical case for penal substitution from Romans 3:25?  "
            "How does μορφῇ θεοῦ in Phil 2:6 bear on the Christological debate?  "
            "Present the Calvinist and Arminian readings of Romans 9:6–24 without selection bias."
        ),
        height=90, label_visibility="collapsed", key="primary_inquiry")

    ic1, ic2, ic3 = st.columns([2, 2, 7])
    with ic1:
        submit_inq = st.button("⚡ Submit Inquiry", use_container_width=True,
                               disabled=(not anthropic_key or not (inquiry or "").strip()))
    with ic2:
        clear_inq = st.button("✕ Clear Response", use_container_width=True)
    with ic3:
        if not anthropic_key:
            st.markdown(
                f'<div style="font-size:.65rem;color:{LT_GOLD};opacity:.42;padding-top:.5rem;'
                f'font-style:italic">Add ANTHROPIC_API_KEY to Streamlit secrets to enable AI Scholar.</div>',
                unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Handle inquiry ──
    if clear_inq:
        st.session_state.pop("inq_response", None)
        st.session_state.pop("inq_text", None)

    if submit_inq and (inquiry or "").strip() and anthropic_key:
        sdata = st.session_state.get("scripture_data", {})
        sref  = st.session_state.get("scripture_ref", "")
        ptxt  = " ".join(v.get("text", "") for v in sdata.get("verses", []))
        tlbl  = {"kjv": "KJV", "web": "WEB", "bbe": "BBE"}.get(translation, "KJV")
        st.session_state.inq_response = ai_inquiry(inquiry.strip(), sref, ptxt, tlbl, anthropic_key)
        st.session_state.inq_text     = inquiry.strip()

    # ── Academic Split: Left metadata | Right parchment ──
    if st.session_state.get("inq_response"):
        left_col, right_col = st.columns([1, 2.5], gap="large")

        with left_col:
            st.markdown('<div class="meta-panel">', unsafe_allow_html=True)
            sec_head("Research Metadata")
            inq_txt = st.session_state.get("inq_text", "")
            st.markdown(
                f'<div class="meta-lbl">Inquiry</div>'
                f'<div class="meta-val">{inq_txt[:180]}{"…" if len(inq_txt)>180 else ""}</div>',
                unsafe_allow_html=True)
            ctx_ref = st.session_state.get("scripture_ref", "None loaded")
            st.markdown(
                f'<div class="meta-lbl">Passage Context</div>'
                f'<div class="meta-val">{ctx_ref}</div>', unsafe_allow_html=True)
            tname = {"kjv": "King James Version", "web": "World English Bible",
                     "bbe": "Basic English Bible"}.get(translation, "KJV")
            st.markdown(
                f'<div class="meta-lbl">Translation</div>'
                f'<div class="meta-val">{tname}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="meta-lbl">AI Model</div>'
                f'<div class="meta-val">Claude Haiku · 24h Cache</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="meta-lbl">Hermeneutic</div>'
                f'<div class="meta-val">Hist.-grammatical · Reformed evangelical · NA28/BHS</div>',
                unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right_col:
            sec_head("Scholarly Insight", "AI Scholar Response — Parchment View")
            parchment(st.session_state.inq_response)

        st.markdown("<hr/>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    # SIX SCHOLARLY TABS
    # ══════════════════════════════════════════════════
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📖  Scripture Lab",
        "🏛  Commentary Engine",
        "⚔  Apologetics",
        "📋  Research Prompts",
        "⚖  Theological Debates",
        "🤖  AI Scholar",
    ])



# ══════════════════════════════════════════════
# TAB 1 — SCRIPTURE LAB
# ══════════════════════════════════════════════
with tab1:
    # Reference input
    default_ref = st.session_state.pop("quick_ref", None) or st.session_state.get("scripture_ref", "John 3:16")
    rc, bc = st.columns([5, 1])
    with rc:
        ref_input = st.text_input("Reference", value=default_ref,
                                   placeholder="e.g. Romans 8:28-39",
                                   label_visibility="collapsed")
    with bc:
        fetch_btn = st.button("FETCH", use_container_width=True)

    if fetch_btn or ref_input != st.session_state.get("scripture_ref"):
        if ref_input:
            with st.spinner("Fetching…"):
                st.session_state.scripture_data = fetch_scripture(ref_input, translation)
                st.session_state.scripture_ref  = ref_input
                st.session_state.pop("ai_analysis", None)

    sdata = st.session_state.get("scripture_data", {})
    sref  = st.session_state.get("scripture_ref", ref_input)

    if sdata.get("fallback"):
        st.markdown(f'<div style="font-size:.67rem;color:{SCARLET};margin-bottom:.35rem">'
                    f'⚠ API unavailable — hardcoded KJV fallback active.</div>',
                    unsafe_allow_html=True)

    # Two-column layout: text left, interlinear/lexical right
    text_col, right_col = st.columns([1, 1], gap="large")

    with text_col:
        sec_head("Scripture Text", sref)
        if sdata.get("error") and not sdata.get("verses"):
            card(f'<span style="color:{SCARLET}">⚠ {sdata["error"]}</span>', SCARLET)
        elif sdata.get("verses"):
            tname = sdata.get("translation_name", translation.upper())
            st.markdown(
                f'<div style="font-size:.6rem;color:{LT_GOLD};opacity:.62;'
                f'letter-spacing:.12em;margin-bottom:.35rem">{sref.upper()} · {tname.upper()}</div>',
                unsafe_allow_html=True)
            vhtml = "".join(
                f'<span style="color:{SCARLET};font-weight:600;font-size:.67rem;margin-right:3px">[{v.get("verse","")}]</span>'
                f'<span style="color:{CREAM}">{v.get("text","").strip()}</span> '
                for v in sdata["verses"])
            st.markdown(
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:.86rem;line-height:2.05;'
                f'color:{CREAM};background:{NAVY};border-left:3px solid {GOLD};'
                f'padding:.95rem 1.15rem;border-radius:3px;border:1px solid rgba(212,175,55,.16)">'
                f'{vhtml}</div>', unsafe_allow_html=True)

        # AI Passage Analyst
        if sdata.get("verses"):
            st.markdown("<hr/>", unsafe_allow_html=True)
            sec_head("AI Passage Analysis")
            ab, nb = st.columns([2, 5])
            with ab:
                analyse = st.button("⚡ ANALYSE PASSAGE", key="analyse_btn",
                                    use_container_width=True, disabled=not anthropic_key)
            with nb:
                if not anthropic_key:
                    st.markdown(f'<div style="font-size:.68rem;color:{LT_GOLD};opacity:.42;'
                                f'padding-top:.45rem">Add ANTHROPIC_API_KEY to enable.</div>',
                                unsafe_allow_html=True)
            if analyse:
                vtxt  = " ".join(v.get("text", "").strip() for v in sdata["verses"])
                tlbl  = {"kjv": "KJV", "web": "WEB", "bbe": "BBE"}.get(translation, "KJV")
                result = ai_analyse_passage(sref, vtxt, tlbl, anthropic_key)
                st.session_state.ai_analysis     = result
                st.session_state.ai_analysis_ref = sref

            if (st.session_state.get("ai_analysis")
                    and st.session_state.get("ai_analysis_ref") == sref):
                parchment(st.session_state.ai_analysis)

        # Parallel translations
        st.markdown("<hr/>", unsafe_allow_html=True)
        sec_head("Parallel Translations")
        if esv_key:
            with st.expander("English Standard Version (ESV)", expanded=True):
                edata = fetch_esv(sref, esv_key)
                if edata.get("verses"):
                    ehtml = " ".join(
                        f'<span style="color:{SCARLET};font-weight:600;font-size:.67rem;margin-right:3px">[{v.get("verse","")}]</span>'
                        + v.get("text", "").strip()
                        for v in edata["verses"])
                    st.markdown(f'<div style="font-size:.85rem;color:{CREAM};line-height:1.95">{ehtml}</div>',
                                unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="font-size:.75rem;color:{SCARLET}">{edata.get("error","")}</div>',
                                unsafe_allow_html=True)
        for alt in ["kjv", "web", "bbe"]:
            if alt != translation:
                lbl = {"kjv": "King James Version", "web": "World English Bible",
                       "bbe": "Basic English Bible"}[alt]
                with st.expander(lbl):
                    ad = fetch_scripture(sref, alt)
                    if ad.get("verses"):
                        st.markdown(
                            f'<div style="font-size:.84rem;color:{CREAM};line-height:1.9">'
                            + " ".join(v.get("text","") for v in ad["verses"]) + '</div>',
                            unsafe_allow_html=True)
        if api_key and premium_trans:
            with st.expander(f"{premium_trans} (API.Bible)"):
                pd_data = fetch_apibible(sref, APIBIBLE_TRANSLATIONS[premium_trans], api_key)
                if pd_data.get("verses"):
                    st.markdown(
                        f'<div style="font-size:.84rem;color:{CREAM};line-height:1.9">'
                        + " ".join(v.get("text","") for v in pd_data["verses"]) + '</div>',
                        unsafe_allow_html=True)

    with right_col:
        sec_head("Interlinear Analysis")
        ikey = next((k for k in INTERLINEAR
                     if k.lower().replace(" ", "") in sref.lower().replace(" ", "")), None)
        if ikey:
            st.markdown(
                f'<div style="font-size:.65rem;color:{LT_GOLD};opacity:.62;margin-bottom:.45rem">'
                f'Word-by-word · Strong\'s numbers</div>', unsafe_allow_html=True)
            for eng, gk, snum, gloss in INTERLINEAR[ikey]:
                st.markdown(
                    f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:.25rem;'
                    f'border-bottom:1px solid rgba(212,175,55,.09);padding:.3rem 0">'
                    f'<div><div style="font-size:.68rem;color:{CREAM};font-weight:500">{eng}</div>'
                    f'<div style="font-size:1.08rem;color:{GOLD};margin-top:.04rem">{gk}</div></div>'
                    f'<div><div style="font-size:.58rem;color:{LT_GOLD};opacity:.68;font-family:monospace">{snum}</div>'
                    f'<div style="font-size:.68rem;color:{CREAM};opacity:.8;line-height:1.45;margin-top:.04rem">{gloss}</div></div>'
                    f'</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="font-size:.74rem;color:{LT_GOLD};opacity:.45">'
                f'Interlinear data available for: {", ".join(INTERLINEAR.keys())}.</div>',
                unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        sec_head("Lexical Analysis — Strong's Index")
        vtxt_full = " ".join(v.get("text", "") for v in sdata.get("verses", []))
        matched_lex = [(k, v) for k, v in STRONGS_LEXICON.items()
                       if k in vtxt_full.lower() or v["tr"].lower() in vtxt_full.lower()][:5]
        if not matched_lex:
            matched_lex = list(STRONGS_LEXICON.items())[:3]
        for term, entry in matched_lex:
            lc = GOLD if entry["lang"] == "Greek" else SCARLET
            st.markdown(
                f'<div style="background:{NAVY};border:1px solid rgba(212,175,55,.17);'
                f'border-left:3px solid {lc};border-radius:3px;padding:.6rem .85rem;margin-bottom:.4rem">'
                f'<div style="font-size:.58rem;color:{LT_GOLD};opacity:.68;letter-spacing:.1em">'
                f'{entry["num"]} · {entry["tr"]} · {entry["lang"]}</div>'
                f'<div style="font-size:1.18rem;color:{CREAM};margin:.08rem 0">{entry["gk"]}</div>'
                f'<div style="font-size:.73rem;color:{LT_GOLD};line-height:1.6">{entry["def"]}</div>'
                f'</div>', unsafe_allow_html=True)

    # ── Technical Basement ───────────────────────────────────────────────────
    if sdata.get("verses"):
        st.markdown("<hr/>", unsafe_allow_html=True)
        with st.expander("📊  Quantitative Textual Mapping — Semantic Graph & Lexical Frequency"):
            vtxt_b = " ".join(v.get("text", "") for v in sdata["verses"])
            h = _hash(vtxt_b + sref)
            if st.session_state.get("graph_hash") != h:
                st.session_state.graph_fig  = build_semantic_graph(vtxt_b, sref)
                st.session_state.graph_hash = h
            st.markdown(
                f'<div style="font-size:.58rem;color:{LT_GOLD};opacity:.45;'
                f'text-align:center;letter-spacing:.12em;margin-bottom:.6rem">'
                f'PASSAGE → LEXICAL TERMS → DOCTRINAL DOMAINS · '
                f'Full analysis available in the Textual Mapping view</div>',
                unsafe_allow_html=True)
            st.plotly_chart(st.session_state.graph_fig, use_container_width=True)

            words = re.findall(r'\b[a-zA-Z]{4,}\b', vtxt_b.lower())
            stop  = {"that","this","with","have","from","they","been","were","unto","thou",
                     "thee","thine","hath","doth","shall","will","your","which","their",
                     "there","when","what","also"}
            freq = {}
            for w in words:
                if w not in stop:
                    freq[w] = freq.get(w, 0) + 1
            if freq:
                fdf = pd.DataFrame(
                    sorted(freq.items(), key=lambda x: -x[1])[:15],
                    columns=["Term", "Frequency"])
                st.markdown(
                    f'<div style="font-size:.6rem;color:{LT_GOLD};opacity:.55;'
                    f'margin:.5rem 0 .3rem;letter-spacing:.1em;text-align:center">'
                    f'TOP 15 SUBSTANTIVE TERMS</div>', unsafe_allow_html=True)
                st.dataframe(fdf, hide_index=True, use_container_width=True)



# ══════════════════════════════════════════════
# TAB 2 — COMMENTARY ENGINE
# ══════════════════════════════════════════════
with tab2:
    sec_head("Commentary Engine", "Analytical summaries of primary scholarly sources")
    st.markdown(
        f'<div style="font-size:.7rem;color:{LT_GOLD};opacity:.62;margin-bottom:.6rem;line-height:1.65">'
        f'All commentary entries are <strong>analytical summaries</strong> of the cited scholarly works, '
        f'not direct quotations. Consult primary sources for original arguments.</div>',
        unsafe_allow_html=True)

    psg = st.selectbox("Passage", list(COMMENTARY.keys()), label_visibility="collapsed")
    cd  = COMMENTARY[psg]

    if st.button("↗ Load in Scripture Lab", key="load_comm"):
        st.session_state.scripture_data = fetch_scripture(psg, translation)
        st.session_state.scripture_ref  = psg

    st.markdown("<hr/>", unsafe_allow_html=True)
    sec_head(cd["label"], "Historical & Literary Context")
    card(f'<div style="font-size:.85rem;color:{CREAM};line-height:1.88">{cd["context"]}</div>')

    sec_head("Scholarly Commentary")
    for s in cd["scholars"]:
        scholar_card(s["author"], s["work"], s["text"])

    lc, xc = st.columns(2, gap="large")
    with lc:
        sec_head("Lexical Notes — Greek & Hebrew")
        for snum, term, tr, defn in cd["greek"]:
            st.markdown(
                f'<div style="background:{NAVY};border:1px solid rgba(212,175,55,.16);'
                f'border-radius:3px;padding:.65rem .85rem;margin-bottom:.45rem">'
                f'<div style="font-size:.58rem;color:{LT_GOLD};opacity:.68;letter-spacing:.1em">{snum} · {tr}</div>'
                f'<div style="font-size:1.28rem;color:{CREAM};margin:.08rem 0">{term}</div>'
                f'<div style="font-size:.75rem;color:{LT_GOLD};line-height:1.62">{defn}</div>'
                f'</div>', unsafe_allow_html=True)
    with xc:
        sec_head("Cross-References — TSK")
        for rstr, note in cd["cross_refs"]:
            st.markdown(
                f'<div style="border-bottom:1px solid rgba(212,175,55,.07);padding:.42rem 0">'
                f'<span class="xref-badge">{rstr}</span>'
                f'<span style="font-size:.74rem;color:{LT_GOLD};opacity:.8;margin-left:.4rem">{note}</span>'
                f'</div>', unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    sec_head("Historical Background")
    card(f'<div style="font-size:.85rem;color:{CREAM};line-height:1.88">{cd["historical"]}</div>', PURPLE)
    sec_head("Apologetics Interface")
    card(f'<div style="font-size:.85rem;color:{CREAM};line-height:1.88">{cd["apologetics"]}</div>', SCARLET)

    st.markdown("<hr/>", unsafe_allow_html=True)
    sec_head("Church Fathers — Patristic Witness")
    for f_ in CHURCH_FATHERS:
        with st.expander(f"{f_['name']} ({f_['dates']}) — {f_['role']}"):
            st.markdown(
                f'<div style="font-size:.82rem;color:{CREAM};line-height:1.85;margin-bottom:.35rem">'
                f'{f_["contribution"]}</div>'
                f'<div style="font-size:.65rem;color:{GOLD};font-style:italic">'
                f'Key work: {f_["key_work"]}</div>', unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    sec_head("Full Strong's Index")
    lex_rows = [{"Term": k, "Strong's": v["num"], "Transliteration": v["tr"],
                 "Language": v["lang"], "Definition": v["def"][:78] + "…"}
                for k, v in STRONGS_LEXICON.items()]
    st.dataframe(pd.DataFrame(lex_rows), hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 3 — APOLOGETICS
# ══════════════════════════════════════════════
with tab3:
    ac, hc = st.columns([3, 2], gap="large")
    with ac:
        sec_head("Eight Core Arguments", "With primary objections and responses")
        for arg in APOLOGETICS_ARGS:
            with st.expander(f"{arg['title']}  [{arg['type']}]"):
                st.markdown(f'<div style="font-size:.82rem;color:{CREAM};line-height:1.88">{arg["content"]}</div>',
                            unsafe_allow_html=True)
        st.markdown("<hr/>", unsafe_allow_html=True)
        sec_head("Recommended Bibliography")
        BIBLIO = [
            ("Craig, William Lane", "Reasonable Faith, 3rd ed. (2008)", "Kalam, resurrection, moral argument"),
            ("Plantinga, Alvin", "Warranted Christian Belief (2000)", "Reformed epistemology"),
            ("Plantinga, Alvin", "The Nature of Necessity (1974)", "Modal ontological argument"),
            ("Collins, Robin", "The Well-Tempered Universe (2009)", "Fine-tuning argument"),
            ("Reppert, Victor", "C.S. Lewis's Dangerous Idea (2003)", "Argument from Reason"),
            ("Moreland, J.P.", "Consciousness and the Existence of God (2008)", "Argument from consciousness"),
            ("Wright, N.T.", "The Resurrection of the Son of God (2003)", "Historical resurrection"),
            ("Habermas & Licona", "The Case for the Resurrection (2004)", "Minimal facts method"),
            ("Bruce, F.F.", "The NT Documents: Are They Reliable? (1981)", "Bibliographical test"),
            ("Lennox, John", "God's Undertaker: Has Science Buried God? (2009)", "Science/theism"),
        ]
        for auth, work, note in BIBLIO:
            st.markdown(
                f'<div style="border-bottom:1px solid rgba(212,175,55,.07);padding:.42rem 0">'
                f'<div style="font-size:.73rem;color:{GOLD}">{auth}</div>'
                f'<div style="font-size:.68rem;color:{CREAM};font-style:italic">{work}</div>'
                f'<div style="font-size:.63rem;color:{LT_GOLD};opacity:.62;margin-top:.04rem">{note}</div>'
                f'</div>', unsafe_allow_html=True)

    with hc:
        sec_head("Bibliographical Test")
        st.plotly_chart(build_mss_chart(), use_container_width=True)
        sec_head("Textual Transmission Table")
        st.dataframe(pd.DataFrame([
            {"Document": "NT (Greek)", "MSS": "5,856", "Earliest": "P52 ~AD 125", "Gap": "25 yrs"},
            {"Document": "NT (all lang.)", "MSS": "25,000+", "Earliest": "P52 ~AD 125", "Gap": "25 yrs"},
            {"Document": "DSS (1QIsa-a)", "MSS": "1", "Earliest": "~125 BC", "Gap": "~350 yrs"},
            {"Document": "Iliad", "MSS": "643", "Earliest": "~400 BC", "Gap": "400 yrs"},
            {"Document": "Plato", "MSS": "210", "Earliest": "~895 AD", "Gap": "1,200 yrs"},
            {"Document": "Caesar", "MSS": "251", "Earliest": "~900 AD", "Gap": "950 yrs"},
        ]), hide_index=True, use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        sec_head("Archaeological Confirmation")
        for disc, conf in [
            ("Pilate Inscription (1961)",   "Pontius Pilate as prefect of Judea"),
            ("Pool of Siloam (2004)",        "John 9:7 — healing of the blind man"),
            ("Caiaphas Ossuary (1990)",      "High priest of the Passion narratives"),
            ("Tel Dan Stele (9th c. BC)",    "'House of David' — extra-biblical attestation"),
            ("Dead Sea Scrolls (1947)",      "OT textual stability; 1QIsa-a predates Christ"),
            ("House of Peter, Capernaum",   "Mark 1:29 — 1st-century veneration continuous"),
        ]:
            st.markdown(
                f'<div style="border-bottom:1px solid rgba(212,175,55,.07);padding:.38rem 0">'
                f'<div style="font-size:.7rem;color:{GOLD}">{disc}</div>'
                f'<div style="font-size:.65rem;color:{CREAM};opacity:.8">{conf}</div>'
                f'</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — RESEARCH PROMPTS
# ══════════════════════════════════════════════
with tab4:
    sec_head("Research Prompts", "Graduate-level inquiry across five domains")
    CAT_META = {
        "Exegetical":         "📖 Exegetical",
        "Doctrinal":          "🏛 Doctrinal",
        "Historical":         "⏳ Historical",
        "Apologetics":        "⚔ Apologetics",
        "Theological Debates":"⚖ Theological Debates",
    }
    CAT_DESC = {
        "Exegetical":         "Greek/Hebrew word studies, grammatical analysis, textual-critical disputes.",
        "Doctrinal":          "Systematic theology — the great loci of Christian doctrine examined through Scripture and tradition.",
        "Historical":         "Canon formation, textual transmission, archaeology, and history of interpretation.",
        "Apologetics":        "Philosophical and evidential questions — the intellectual defense of Christian truth claims.",
        "Theological Debates":"Live internal debates within evangelical scholarship, presented without editorial advocacy.",
    }
    cat = st.selectbox("Category", list(STUDY_PROMPTS.keys()),
                       label_visibility="collapsed",
                       format_func=lambda x: CAT_META[x])
    st.markdown(f'<div style="font-size:.68rem;color:{LT_GOLD};opacity:.52;margin-bottom:.8rem">{CAT_DESC[cat]}</div>',
                unsafe_allow_html=True)
    for i, prompt in enumerate(STUDY_PROMPTS[cat], 1):
        pc, bc = st.columns([8, 2])
        with pc:
            st.markdown(
                f'<div style="background:{NAVY};border:1px solid rgba(212,175,55,.14);'
                f'border-left:3px solid {GOLD};border-radius:3px;padding:.75rem .95rem;margin-bottom:.45rem">'
                f'<div style="font-size:.56rem;color:{LT_GOLD};opacity:.38;letter-spacing:.12em;margin-bottom:.22rem">'
                f'{cat.upper()} {i:02d}</div>'
                f'<div style="font-size:.84rem;color:{CREAM};line-height:1.78">{prompt}</div>'
                f'</div>', unsafe_allow_html=True)
        with bc:
            if st.button("Send to AI", key=f"p_{cat}_{i}",
                         use_container_width=True, disabled=not anthropic_key):
                st.session_state.inq_response = ai_single(prompt, anthropic_key, 2200)
                st.session_state.inq_text     = prompt
                st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)
    sec_head("Commentary Series Reference")
    st.dataframe(pd.DataFrame([
        {"Abbrev.": "ICC",    "Series": "International Critical Commentary",   "Character": "Philologically rigorous; multi-author"},
        {"Abbrev.": "NICNT",  "Series": "New International Commentary — NT",   "Character": "Evangelical; solid exegesis"},
        {"Abbrev.": "NIGTC",  "Series": "New International Greek Testament Commentary", "Character": "Greek text focus; advanced"},
        {"Abbrev.": "WBC",    "Series": "Word Biblical Commentary",            "Character": "Mixed; includes textual notes"},
        {"Abbrev.": "BECNT",  "Series": "Baker Exegetical Commentary",         "Character": "Evangelical; Greek text"},
        {"Abbrev.": "Pillar", "Series": "Pillar NT Commentary (Carson)",       "Character": "Balanced; recommended"},
        {"Abbrev.": "AB",     "Series": "Anchor Bible",                        "Character": "Critical-historical; definitive philology"},
        {"Abbrev.": "TOTC",   "Series": "Tyndale OT/NT Commentaries",         "Character": "Accessible evangelical introduction"},
    ]), hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 5 — THEOLOGICAL DEBATES
# ══════════════════════════════════════════════
with tab5:
    sec_head("Theological Debates", "Live internal debates — no editorial advocacy")
    st.markdown(
        f'<div style="font-size:.76rem;color:{LT_GOLD};opacity:.68;line-height:1.75;margin-bottom:.7rem">'
        f'Each debate presents the strongest arguments for each position from primary advocates. '
        f'No editorial position is taken.</div>', unsafe_allow_html=True)

    DEBATES = {
        "Calvinism vs. Arminianism — Election & Perseverance": {
            "calvinist": {
                "label": "Reformed / Calvinist Position",
                "advocates": "John Calvin, Francis Turretin, John Owen, B.B. Warfield, John Murray, Thomas Schreiner, J.I. Packer",
                "argument": "Romans 9:6–24 establishes individual unconditional election: God's choice of Jacob over Esau is made 'before they were born or had done anything good or bad' (v. 11), explicitly excluding foreseen merit. The phrase 'I will have mercy on whom I have mercy' (v. 15, citing Ex 33:19) grounds election in divine sovereignty, not human response. The 'golden chain' of Romans 8:29–30 (foreknew → predestined → called → justified → glorified) presents an unbroken, infallible sequence — no link can be broken. John 6:37–44 reinforces this: 'All that the Father gives me will come to me' (v. 37); 'No one can come to me unless the Father who sent me draws him' (v. 44). The verb 'draws' (ἕλκω, helkō) is the same used in John 21:11 of dragging a net — an effectual, irresistible drawing. 1 John 2:19 ('they went out from us because they were never of us') interprets apostasy not as loss of salvation but as evidence of non-election.",
            },
            "arminian": {
                "label": "Arminian / Open Grace Position",
                "advocates": "Jacob Arminius, John Wesley, Roger Olson, William Klein, F. Leroy Forlines",
                "argument": "Romans 9 is about corporate election (the election of a people, not individuals to salvation) — the context is the faithfulness of God's covenant promises to Israel (v. 6: 'the word of God has not failed'), not the predestination of individuals. Jacob and Esau represent nations, not individuals selected for salvation or damnation (cf. Mal 1:2–3 which refers to nations). 1 Peter 1:1–2 presents election as 'according to the foreknowledge of God the Father' — God elects those whom he foreknows will respond in faith. John 6:37–44 concerns the context of believing disciples who are kept, not a deterministic decree. The 'drawing' of the Father (v. 44) is available to all: Jesus says 'I will draw all men to myself' (12:32), using the same verb. Arminian perseverance (conditional security): the same passages that promise security (John 10:28–29) assume the sheep are hearing and following (v. 27); apostasy texts (Heb 6:4–6; 10:26–29) warn genuine believers of genuine danger.",
            },
            "key_texts": ["Romans 9:6–24", "John 6:37–44", "1 John 2:19", "1 Peter 1:1–2", "Hebrews 6:4–6"],
        },
        "Inerrancy — Warfield vs. Enns vs. Vanhoozer": {
            "position_a": {
                "label": "Plenary Verbal Inerrancy (Warfield)",
                "advocates": "B.B. Warfield, Charles Hodge, Wayne Grudem, D.A. Carson, John Frame (Chicago Statement, 1978)",
                "argument": "2 Timothy 3:16 ('all Scripture is θεόπνευστος, God-breathed') and 2 Peter 1:21 ('men spoke from God as they were carried along by the Holy Spirit') establish a concursive theory of inspiration: the divine and human authorship are simultaneous and non-competitive. The divine authorship guarantees inerrancy; the human authorship preserves genuine literary variety. The Chicago Statement (1978) defines inerrancy: 'Scripture in the original manuscripts does not affirm anything that is contrary to fact.' This applies to all domains in which Scripture speaks — not only theology but historical and cosmological matters insofar as they are affirmed.",
            },
            "position_b": {
                "label": "Incarnational / Cultural Model (Enns)",
                "advocates": "Peter Enns (Inspiration and Incarnation, 2005), Kenton Sparks",
                "argument": "The Incarnation provides the controlling analogy: as Christ was fully divine and fully human (including genuine human limitations), so Scripture is fully divine and fully human (including genuine cultural limitations). This means the ANE cosmological assumptions embedded in Genesis 1–2 are genuine features of the text — not errors but evidence of God accommodating his self-revelation to the idiom of its cultural moment. Inerrancy defined as 'what Scripture intends to affirm is true' preserves theological inerrancy while allowing for cultural embeddedness. Enns's critics (Trueman, Helm) argue this model cannot explain how divine accommodation includes factual errors without impugning divine truthfulness.",
            },
            "position_c": {
                "label": "Theodramatic Canonics (Vanhoozer)",
                "advocates": "Kevin Vanhoozer (The Drama of Doctrine, 2005; Biblical Authority After Babel, 2016)",
                "argument": "Vanhoozer proposes a speech-act theory of inspiration: Scripture's inerrancy applies to its illocutionary acts (what the text is doing — asserting, commanding, promising) rather than its locutions (the bare propositional content). This allows for literary genres to function appropriately: a poetic hyperbole is not inerrant if read as a scientific claim; it is inerrant as hyperbole. The Reformation's sola scriptura is preserved without the naive textual positivism of fundamentalism. Critics (Schreiner, Frame) argue Vanhoozer's model is ultimately indeterminate — who decides which speech acts are assertions and which are performatives?",
            },
            "key_texts": ["2 Tim 3:16", "2 Pet 1:20–21", "Matt 5:18", "John 10:35"],
        },
        "Annihilationism vs. Eternal Conscious Torment": {
            "ect": {
                "label": "Eternal Conscious Torment (ECT)",
                "advocates": "Augustine, Aquinas, Jonathan Edwards, J.I. Packer, Robert Peterson, Denny Burk",
                "argument": "Revelation 14:9–11: 'The smoke of their torment goes up forever and ever (εἰς αἰῶνας αἰώνων), and they have no rest day or night.' The phrase εἰς αἰῶνας αἰώνων is the strongest temporal expression available in Greek and is used of God's eternal existence (Rev 4:9–10) — applying it to torment and then denying its duration is inconsistent. Matthew 25:46 uses the same adjective (αἰώνιος) for both punishment and life — 'eternal punishment' and 'eternal life.' If αἰώνιος means 'of limited duration' for punishment, it must mean the same for life — a conclusion no evangelical accepts. 2 Thessalonians 1:9 ('eternal destruction') uses ὄλεθρος (olethros) — destruction, but in context modified by 'from the face of the Lord,' suggesting banishment rather than cessation of existence.",
            },
            "anni": {
                "label": "Conditionalism / Annihilationism",
                "advocates": "Edward Fudge (The Fire That Consumes), John Stott, N.T. Wright, Clark Pinnock",
                "argument": "αἰώνιος denotes quality ('of the age to come') not necessarily infinite duration — it is used of the 'eternal' fire of Sodom (Jude 7) which is manifestly no longer burning. The smoke ascending 'forever' (Rev 14:11) is OT prophetic imagery for complete and final destruction (cf. Isa 34:9–10 of Edom — never literally fulfilled as perpetual smoke). 2 Thess 1:9 'eternal destruction' (ὄλεθρος) best denotes complete destruction whose effects are permanent, not a continuing process. Fudge: the biblical metaphor for hell is fire, which consumes; the fire of hell achieves its purpose — it doesn't burn forever, it destroys completely and permanently. 'Eternal' modifies the result, not the process. The soul's immortality is not a biblical datum; it is a Greek philosophical assumption imported into Christian anthropology.",
            },
            "key_texts": ["Rev 14:9–11", "Matt 25:46", "2 Thess 1:9", "Jude 7", "Isa 34:9–10"],
        },
        "Open Theism vs. Classical Divine Foreknowledge": {
            "classical": {
                "label": "Classical Theism — Exhaustive Divine Foreknowledge",
                "advocates": "Augustine, Calvin, Aquinas, Helm, Frame, Ware",
                "argument": "Isaiah 46:9–10: 'I am God and there is no other... declaring the end from the beginning.' God's foreknowledge of specific human choices (Isa 44:28 — Cyrus named 150 years before his birth; Ps 139:4 — God knows our words before we speak them) requires exhaustive knowledge of future contingents. The Molinist solution (Plantinga, Craig): God has 'middle knowledge' of all counterfactuals of creaturely freedom — he knows what every free creature would do in every possible circumstance. This reconciles libertarian human freedom with exhaustive divine foreknowledge without making God the author of sin. Divine timelessness (Aquinas, Helm): God exists in an 'eternal present' — he does not 'foreknow' but simply knows all events in his atemporal perspective.",
            },
            "open": {
                "label": "Open Theism",
                "advocates": "Gregory Boyd (God of the Possible), Clark Pinnock (The Openness of God), John Sanders",
                "argument": "The biblical narrative of divine repentance (Gen 6:6: 'the LORD was grieved that he had made man'; Ex 32:14: 'the LORD relented from the disaster'; Jonah 3:10) implies a genuine change in God's intentions — genuine regret is incoherent if God always knew things would unfold as they did. Divine inquiry (Gen 3:9: 'Where are you?'; Gen 18:21: 'I will go down and see whether they have done altogether according to the outcry') implies genuine uncertainty. The best interpretation of these texts is not anthropomorphism but literal: God genuinely does not know with certainty what free creatures will choose, and this is not a deficiency but a feature of the relational God who created genuinely free agents. Critics (Frame, Ware) argue Open Theism's God cannot guarantee prophetic fulfillments that require specific human choices.",
            },
            "key_texts": ["Gen 6:6", "Isa 46:9–10", "Isa 44:28", "Ex 32:14", "Ps 139:4"],
        },
    }

    for debate_title, debate_data in DEBATES.items():
        with st.expander(debate_title):
            keys = [k for k in debate_data if k != "key_texts"]
            if "key_texts" in debate_data:
                refs_html = " ".join(
                    f'<span class="xref-badge">{r}</span>' for r in debate_data["key_texts"])
                st.markdown(
                    f'<div style="margin-bottom:.65rem">'
                    f'<strong style="font-size:.63rem;color:{LT_GOLD};opacity:.62;letter-spacing:.1em">KEY TEXTS: </strong>'
                    f'{refs_html}</div>', unsafe_allow_html=True)
            for key in keys:
                pos = debate_data[key]
                st.markdown(
                    f'<div class="scholar-card">'
                    f'<div style="font-family:Georgia,serif;font-size:.91rem;font-weight:600;color:{GOLD};margin-bottom:.12rem">{pos["label"]}</div>'
                    f'<div style="font-size:.61rem;color:{LT_GOLD};opacity:.62;margin-bottom:.45rem;font-style:italic">Advocates: {pos["advocates"]}</div>'
                    f'<div style="font-size:.82rem;color:{CREAM};line-height:1.88">{pos["argument"]}</div>'
                    f'</div>', unsafe_allow_html=True)
                sk = f"sm_{debate_title}_{key}"
                rk = f"sm_r_{debate_title}_{key}"
                bc, nc = st.columns([2, 5])
                with bc:
                    if st.button("⚡ STEELMAN THIS", key=sk,
                                 use_container_width=True, disabled=not anthropic_key):
                        st.session_state[rk] = ai_steelman(
                            debate_title, pos["label"], pos["argument"],
                            debate_data.get("key_texts", []), anthropic_key)
                with nc:
                    if not anthropic_key:
                        st.markdown(
                            f'<div style="font-size:.64rem;color:{LT_GOLD};opacity:.38;padding-top:.38rem">'
                            f'Add ANTHROPIC_API_KEY to enable.</div>', unsafe_allow_html=True)
                if st.session_state.get(rk):
                    st.markdown(
                        f'<div style="margin-bottom:.35rem;font-size:.58rem;color:{SCARLET};letter-spacing:.12em">'
                        f'AI STEELMAN — {pos["label"].upper()}</div>', unsafe_allow_html=True)
                    parchment(st.session_state[rk])
                    if st.button("✕ Clear", key=f"cl_{sk}"):
                        del st.session_state[rk]


# ══════════════════════════════════════════════
# TAB 6 — AI SCHOLAR  (persistent chat)
# ══════════════════════════════════════════════
with tab6:
    sec_head("AI Scholar", "Graduate-level biblical research — persistent conversation")
    if not anthropic_key:
        card(
            f'<div style="font-size:.83rem;color:{CREAM};line-height:1.78">'
            f'<strong style="color:{GOLD}">API key not configured.</strong><br>'
            f'Add <code>ANTHROPIC_API_KEY = "sk-ant-..."</code> to Streamlit secrets '
            f'(Dashboard → Settings → Secrets).</div>', SCARLET)
    else:
        st.markdown(
            f'<div style="font-size:.76rem;color:{LT_GOLD};opacity:.68;line-height:1.75;margin-bottom:.65rem">'
            f'Persistent conversation with the AI Scholar. Context maintained across turns. '
            f'All responses render in parchment view.</div>', unsafe_allow_html=True)

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        sec_head("Quick Prompts")
        QP = [
            "What is the exegetical case for penal substitutionary atonement from Romans 3:21–26?",
            "Explain Plantinga's modal ontological argument and the strongest objection to it.",
            "What does μορφῇ θεοῦ in Philippians 2:6 mean and why does it matter for Christology?",
            "Summarise the Calvinism/Arminianism debate on Romans 9 — strongest exegetical arguments on each side.",
            "What is the historical case for the resurrection using only the minimal facts method?",
            "How do the Dead Sea Scrolls bear on the reliability of the Old Testament text?",
            "What is the difference between propitiation and expiation in Romans 3:25?",
            "Explain the fine-tuning argument and the multiverse objection to it.",
        ]
        qc1, qc2 = st.columns(2)
        for i, qp in enumerate(QP):
            with (qc1 if i % 2 == 0 else qc2):
                if st.button(qp[:66] + ("…" if len(qp) > 66 else ""),
                             key=f"qp_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": qp})
                    reply = ai(st.session_state.chat_history, anthropic_key)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()

        st.markdown("<hr/>", unsafe_allow_html=True)
        sec_head("Conversation")
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f'<div style="background:{BIB_BLUE};border-radius:4px;padding:.62rem .88rem;'
                    f'margin-bottom:.38rem;font-size:.82rem;color:{CREAM};line-height:1.72">'
                    f'<span style="font-size:.56rem;color:{LT_GOLD};opacity:.62;letter-spacing:.1em">YOU</span><br>'
                    f'{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                parchment(msg["content"])

        user_in = st.text_input(
            "Ask", label_visibility="collapsed", key="chat_in",
            placeholder="e.g. What does ἱλαστήριον mean in Romans 3:25 and how does it bear on the atonement debate?")
        sc, cc = st.columns([2, 1])
        with sc:
            if st.button("SEND", use_container_width=True, key="send_btn") and user_in.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_in.strip()})
                reply = ai(st.session_state.chat_history, anthropic_key)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()
        with cc:
            if st.button("CLEAR CONVERSATION", use_container_width=True, key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()

        if st.session_state.chat_history:
            tc = sum(len(m["content"]) for m in st.session_state.chat_history)
            st.markdown(
                f'<div style="font-size:.58rem;color:{LT_GOLD};opacity:.28;margin-top:.38rem">'
                f'~{tc//4:,} tokens in conversation · {len(st.session_state.chat_history)} messages</div>',
                unsafe_allow_html=True)
