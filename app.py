"""
Sententia Bible Lab — Christian Apologetics Codex
==================================================
A graduate-level Biblical research workstation.
Tabs: Scripture Lab | Commentary Engine | Historical Context | Apologetics
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import re

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
# PALETTE
# ─────────────────────────────────────────────
NAVY          = "#0A1628"
BIBLICAL_BLUE = "#0038A8"
PURE_GOLD     = "#D4AF37"
LIGHT_GOLD    = "#F5E17A"
TYRIAN_PURPLE = "#66023C"
SCARLET       = "#B22222"
CREAM         = "#FFF8DC"

# ─────────────────────────────────────────────
# FONTS + CSS
# ─────────────────────────────────────────────
st.markdown(
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400&family=IBM+Plex+Mono:wght@300;400;600&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)

st.markdown(f"""
<style>
.stApp, [data-testid="stAppViewContainer"] {{
    background-color: {NAVY} !important;
}}
.stApp > header {{ background-color: {NAVY} !important; }}
[data-testid="block-container"] {{
    background-color: {NAVY} !important;
    padding-top: 1.2rem !important;
    max-width: 1400px !important;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(175deg, {NAVY} 0%, #0a1f50 100%) !important;
    border-right: 1px solid rgba(212,175,55,0.333) !important;
}}
[data-testid="stSidebar"] * {{ color: {PURE_GOLD} !important; }}
body, .stMarkdown, p, span, div {{
    font-family: 'IBM Plex Mono', 'Courier New', monospace;
    color: {CREAM};
}}
.stTabs [data-baseweb="tab-list"] {{
    background-color: {NAVY} !important;
    border-bottom: 1px solid rgba(212,175,55,0.2) !important;
    gap: 2px;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent !important;
    color: rgba(245,225,122,0.6) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.73rem !important;
    letter-spacing: 0.1em !important;
    padding: 8px 18px !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.15s ease !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {PURE_GOLD} !important;
    border-bottom: 2px solid rgba(212,175,55,0.4) !important;
}}
.stTabs [aria-selected="true"] {{
    color: {PURE_GOLD} !important;
    border-bottom: 2px solid {PURE_GOLD} !important;
    font-weight: 600 !important;
}}
.stTabs [data-baseweb="tab-panel"] {{
    background-color: {NAVY} !important;
    padding-top: 1.2rem !important;
}}
.stTextInput input {{
    background-color: rgba(0,56,168,0.533) !important;
    color: {CREAM} !important;
    border: 1px solid rgba(212,175,55,0.333) !important;
    border-radius: 3px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.88rem !important;
}}
.stTextInput input:focus {{
    border-color: {PURE_GOLD} !important;
    box-shadow: 0 0 6px rgba(212,175,55,0.2) !important;
}}
.stSelectbox > div > div {{
    background-color: rgba(0,56,168,0.533) !important;
    color: {CREAM} !important;
    border: 1px solid rgba(212,175,55,0.333) !important;
    font-family: 'IBM Plex Mono', monospace !important;
}}
.stButton > button {{
    background-color: {TYRIAN_PURPLE} !important;
    color: {PURE_GOLD} !important;
    border: 1px solid rgba(212,175,55,0.4) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    border-radius: 3px !important;
    transition: all 0.15s ease !important;
}}
.stButton > button:hover {{
    background-color: {PURE_GOLD} !important;
    color: {NAVY} !important;
}}
[data-testid="metric-container"] {{
    background-color: rgba(0,56,168,0.267) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 4px !important;
    padding: 0.6rem 0.9rem !important;
}}
[data-testid="metric-container"] label {{
    color: rgba(245,225,122,0.733) !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.1em !important;
}}
[data-testid="stMetricValue"] {{
    color: {PURE_GOLD} !important;
    font-size: 1.4rem !important;
    font-weight: 600 !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 3px !important;
}}
hr {{ border-color: rgba(212,175,55,0.133) !important; margin: 1.2rem 0 !important; }}
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {NAVY}; }}
::-webkit-scrollbar-thumb {{ background: rgba(212,175,55,0.267); border-radius: 2px; }}
.stExpander {{ border: 1px solid rgba(212,175,55,0.2) !important; border-radius: 4px !important; }}
.stExpander summary {{ color: {PURE_GOLD} !important; font-family: 'IBM Plex Mono', monospace !important; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# UTILITY RENDERERS
# ─────────────────────────────────────────────

def section_header(title: str, sub: str = ""):
    sub_html = f'<div style="font-size:0.68rem;color:rgba(245,225,122,0.533);letter-spacing:0.08em;margin-top:0.15rem;">{sub}</div>' if sub else ""
    st.markdown(f'''
        <div style="margin:1.2rem 0 0.7rem;">
            <div style="font-family:\'Playfair Display\',Georgia,serif;
                        font-size:1.1rem;font-weight:600;color:{PURE_GOLD};
                        letter-spacing:0.04em;line-height:1.2;">{title}</div>
            {sub_html}
            <div style="height:1px;background:linear-gradient(90deg,rgba(212,175,55,0.4),rgba(212,175,55,0));margin-top:0.4rem;"></div>
        </div>''', unsafe_allow_html=True)

def card(html: str, accent: str = PURE_GOLD):
    st.markdown(f'''
        <div style="background:{NAVY};border:1px solid {accent}33;border-left:3px solid {accent};
                    border-radius:4px;padding:1rem 1.25rem;margin-bottom:0.9rem;
                    box-shadow:0 2px 12px rgba(0,0,0,0.4);">{html}</div>''',
        unsafe_allow_html=True)

def quote_card(text: str, attribution: str, ref: str = ""):
    ref_html = f'<span style="color:rgba(245,225,122,0.467);font-size:0.72rem;"> — {ref}</span>' if ref else ""
    st.markdown(f'''
        <div style="background:linear-gradient(135deg,{NAVY},rgba(0,56,168,0.267));
                    border:1px solid rgba(212,175,55,0.267);border-left:4px solid {PURE_GOLD};
                    border-radius:4px;padding:1rem 1.3rem;margin-bottom:0.9rem;">
            <div style="font-family:\'Playfair Display\',Georgia,serif;font-style:italic;
                        font-size:0.93rem;color:{CREAM};line-height:1.85;margin-bottom:0.5rem;">
                "{text}"
            </div>
            <div style="font-size:0.72rem;color:{PURE_GOLD};letter-spacing:0.08em;">
                — {attribution}{ref_html}
            </div>
        </div>''', unsafe_allow_html=True)

def tag(text: str, color: str = TYRIAN_PURPLE):
    return f'<span style="display:inline-block;background:{color};color:{PURE_GOLD};font-size:0.68rem;padding:2px 9px;border-radius:2px;border:1px solid rgba(212,175,55,0.333);margin:2px;letter-spacing:0.06em;">{text}</span>'


# ─────────────────────────────────────────────
# DATA — COMMENTARY
# ─────────────────────────────────────────────

COMMENTARY = {
    "John 3:16": {
        "context": "The Nicodemus discourse (John 3:1–21) occurs at night — Johannine irony for spiritual darkness meeting divine light. The interlocutor is a Pharisee and ruler of the Jews (ἄρχων, archōn), making his nocturnal inquiry theologically loaded.",
        "scholars": [
            {
                "author": "Raymond E. Brown",
                "work": "The Gospel According to John (Anchor Bible, 1966), Vol. I, pp. 133–136",
                "text": "The Johannine 'world' (κόσμος) here is not a subset of humanity but the totality of the created order alienated from God. The aorist ἔδωκεν ('has given') signals a completed act of irreversible consequence — the Incarnation as the hinge of history. Brown situates this within realized eschatology: judgment is not deferred but operative in the act of believing or refusing to believe."
            },
            {
                "author": "D.A. Carson",
                "work": "The Gospel According to John (Pillar NT Commentary, 1991), pp. 204–206",
                "text": "Carson argues against universalism: 'God so loved the world' functions rhetorically to stress the vastness of divine condescension, not a guarantee of universal salvation. The μονογενής ('only-begotten' or 'unique') is best rendered as 'one and only Son,' distinguishing the second Person's filial relationship from adoptive sonship language elsewhere in John."
            },
            {
                "author": "Leon Morris",
                "work": "The Gospel According to John (NICNT, rev. 1995), p. 225",
                "text": "Morris underscores that John's ἵνα clause ('in order that') introduces purpose, not mere result: the Incarnation is a purposive act oriented toward eschatological rescue. The negative formulation ('should not perish') reflects the gravity of the default condition — perdition is the natural terminus without divine intervention."
            },
        ],
        "greek": [("G2889", "κόσμος", "kosmos", "The created order; in John, often the system of human existence organized in opposition to God."),
                  ("G3439", "μονογενής", "monogenēs", "Only-begotten; unique; technically 'of a single kind.' Patristic Christology anchors homoousios debates here."),
                  ("G622",  "ἀπόλλυμι", "apollymi", "To perish, be ruined utterly; the antithesis of eternal life in Johannine theology.")],
        "cross_refs": [("John 1:14", "The Word became flesh — the Incarnation premised in the Prologue"),
                       ("Rom 5:8", "God demonstrates His love in that while we were still sinners, Christ died"),
                       ("1 John 4:9", "By this the love of God was manifested — He sent His only-begotten Son"),
                       ("Gen 22:2", "Typological parallel: God commands Abraham to give his only son")],
        "historical": "The Nicodemus pericope reflects the Sitz im Leben of the Johannine community's debates with Pharisaic Judaism in the late 1st century. The night setting echoes Gethsemane and the Passion (John 13:30). Nicodemus reappears at John 7:50 and 19:39, his trajectory from darkness to public discipleship forming a narrative arc.",
        "apologetics": "The verse anchors the historical argument for Christianity: divine agency (God acted), historical particularity (gave His Son), and epistemic demand (believing). William Lane Craig's Kalam argument situates this as the revealed answer to why a personal Creator would interact with contingent beings."
    },
    "Romans 8:28": {
        "context": "Paul's eighth chapter constitutes the argumentative apex of Romans: having established justification by faith (ch. 1–5) and sanctification (ch. 6–8), Paul grounds assurance in divine sovereignty over suffering. Verse 28 opens the predestinarian sequence (vv. 28–30) — the 'golden chain' of Reformed theology.",
        "scholars": [
            {
                "author": "Thomas R. Schreiner",
                "work": "Romans (Baker Exegetical Commentary, 1998), pp. 449–453",
                "text": "Schreiner identifies the grammatical subject as 'God,' not 'the Spirit' or 'all things' — a divine passive that places cosmic sovereignty explicitly in Yahweh. 'Those who love God' echoes Deut. 6:5 (the Shema), anchoring Paul's pneumatology within OT covenant theology rather than Hellenistic fate categories."
            },
            {
                "author": "John Murray",
                "work": "The Epistle to the Romans (NICNT, 1959), Vol. I, pp. 312–315",
                "text": "Murray's exegesis of κατὰ πρόθεσιν ('according to purpose') emphasizes the pretemporal divine decree: God's 'working together' (συνεργεῖ) is not reactive but constitutive. Suffering is not outside the divine economy but is itself instrumentalized toward conformity to Christ (v. 29 — εἰκὼν, image)."
            },
            {
                "author": "Douglas Moo",
                "work": "The Letter to the Romans (NICNT, 2nd ed. 2018), pp. 537–541",
                "text": "Moo navigates the theodicy tension carefully: the promise is not that all things are good in themselves but that God deploys them toward a good end for the elect. The telic orientation toward glorification (v. 30) reveals that 'good' (ἀγαθόν) is eschatologically defined — it is the good of conformity to Christ, not temporal comfort."
            },
        ],
        "greek": [("G4903", "συνεργέω", "synergeo", "To work together with; divine concurrence in which God is the primary agent orchestrating secondary causes."),
                  ("G4286", "πρόθεσις", "prothesis", "Purpose; plan; pretemporal decree. Used of the showbread (Ex. 25:30 LXX) suggesting a sacred, purposeful arrangement."),
                  ("G2822", "κλητός", "klētos", "Called; in Paul, those effectually called in accordance with divine purpose, distinguished from the general call.")],
        "cross_refs": [("Gen 50:20", "Joseph: 'You meant evil, but God meant it for good' — the OT prototype"),
                       ("Eph 1:11", "Predestined according to the purpose of Him who works all things after the counsel of His will"),
                       ("Phil 1:12", "Paul's imprisonment has actually turned out for the progress of the gospel"),
                       ("Ps 119:91", "All things are Your servants — cosmic sovereignty over creation")],
        "historical": "Paul wrote Romans c. AD 57 from Corinth, prior to his Jerusalem visit (Acts 20:3). The letter addresses a community navigating Jew-Gentile tensions post the Edict of Claudius (AD 49), which had expelled Jews from Rome. Chapter 8 functions as the theological resolution to the suffering and ethnic tension explored in chapters 5–7.",
        "apologetics": "Romans 8:28 is the most consequential theodicy text in Christian scripture. Alvin Plantinga's Free Will Defense and John Hick's Soul-Making theodicy both engage this verse's logic: the compatibility of divine omnipotence, omniscience, and the presence of suffering. Reformed apologetics uses vv. 28–30 to argue that providence is not merely reactive but constitutively ordered."
    },
    "Isaiah 53:5": {
        "context": "The Fourth Servant Song (Isa. 52:13–53:12) constitutes the most cited OT passage in the NT (50+ citations/allusions). Deutero-Isaianic attribution is contested; Evangelical scholarship (Young, Oswalt) maintains Isaianic unity. The pericope presents vicarious suffering as the mechanism of covenant restoration — unprecedented in ANE religious literature.",
        "scholars": [
            {
                "author": "John N. Oswalt",
                "work": "The Book of Isaiah: Chapters 40–66 (NICOT, 1998), pp. 379–393",
                "text": "Oswalt defends the historical-grammatical sense of the Servant as an individual, not a collective. The penal substitutionary reading is warranted by the prepositional phrase מִפְּשָׁעֵינוּ (mip·pe·sha·'e·nu, 'because of our transgressions') — the min prefix denotes causation, not mere association. The Servant bears the guilt of others as judicial substitute."
            },
            {
                "author": "Walvoord & Zuck",
                "work": "Bible Knowledge Commentary (OT, 1985), pp. 1109–1111",
                "text": "The BKC identifies מוּסָר (musar, 'chastisement') as carrying both disciplinary and juridical connotations — it is the vocabulary of covenant curse (Lev. 26) applied to the Servant. The healings of Christ cited in Matt. 8:17 reflect the Matthean community's typological reading, while 1 Pet. 2:24 applies the verse explicitly to Christ's atoning work."
            },
            {
                "author": "E.J. Young",
                "work": "The Book of Isaiah (NICOT, 1972), Vol. III, pp. 340–355",
                "text": "Young's philological analysis of חַבּוּרָתוֹ (chaburato, 'by his stripes/wounds') emphasizes that the noun denotes the welt left by a blow — physical suffering that effects spiritual restoration. The causative relationship ('by his wounds we are healed') imports a transactional logic: the Servant's physical punishment is the precise mechanism of covenantal healing."
            },
        ],
        "greek": [("H6588", "פֶּשַׁע", "pesha'", "Transgression; willful rebellion against covenant Lord. Distinguished from חַטָּאת (sin) and עָוֺן (iniquity) — three terms in v. 5-6 forming a comprehensive taxonomy of human guilt."),
                  ("H4347", "מַכָּה", "makkah", "Blow, wound, plague. In the Exodus narrative, the term used for divine judgment. Applied here to the Servant as one who absorbs divine judgment."),
                  ("H7495", "רָפָא", "rapha'", "To heal, restore; used of physical and covenantal/spiritual restoration. El Shaddai is identified as 'the God who heals' (Ex. 15:26).")],
        "cross_refs": [("1 Pet 2:24", "He Himself bore our sins in His body on the cross — explicit NT application"),
                       ("2 Cor 5:21", "He made Him who knew no sin to be sin on our behalf — imputation"),
                       ("Matt 8:17", "This was to fulfill what was spoken through Isaiah: He took our infirmities"),
                       ("Rom 4:25", "Delivered over because of our transgressions, raised because of our justification")],
        "historical": "Isaiah 53 was found among the Dead Sea Scrolls (1QIsa-a, c. 125 BC) with over 95% consonantal agreement with the Masoretic Text — confirming textual stability. The Septuagint (LXX, c. 250 BC) renders the passage in Greek, used by NT authors writing before the destruction of Jerusalem (AD 70). The text thus predates Christianity by centuries, making it the strongest prophetic argument in Christian apologetics.",
        "apologetics": "Isaiah 53 is the centerpiece of Messianic prophecy apologetics. Josh McDowell's Evidence That Demands a Verdict and Lee Strobel's The Case for Christ both cite the Dead Sea Scroll evidence for pre-Christian textual integrity. The mathematical probability argument (Stoner's Science Speaks) assigns astronomical odds against accidental fulfillment of the Isaiah 53 cluster in one individual."
    },
    "Genesis 1:1": {
        "context": "The Toledoth formula ('In the beginning') opens the primordial history (Gen. 1:1–2:3), the P-source's structured cosmogony in critical scholarship. Evangelical hermeneutics treats it as straightforward historical narrative. The verse's theological uniqueness lies in what it excludes: dualism, emanationism, and the divine conflict motifs ubiquitous in ANE cosmogonies (Enuma Elish, Baal Cycle).",
        "scholars": [
            {
                "author": "Victor P. Hamilton",
                "work": "The Book of Genesis: Chapters 1–17 (NICOT, 1990), pp. 103–117",
                "text": "Hamilton's grammatical analysis of בְּרֵאשִׁית (be-reshit) argues against the temporal absolute ('In the beginning of God's creating') and for the traditional absolute reading: 'In the beginning, God created.' The verb בָּרָא (bara') is used exclusively with God as subject in the Hebrew Bible — denoting divine creative activity qualitatively distinct from human making (יָצַר, asah)."
            },
            {
                "author": "Gordon Wenham",
                "work": "Genesis 1–15 (Word Biblical Commentary, 1987), pp. 11–17",
                "text": "Wenham situates Gen. 1 as a polemical cosmogony: each creative act implicitly demythologizes ANE deities. The sun and moon, worshipped across the ancient Near East, are reduced to 'the greater light' and 'the lesser light' — unnamed to deny divine status. The structural parallelism (days 1–3 establishing form; 4–6 filling) reflects liturgical rhythm, suggesting priestly composition for worship contexts."
            },
            {
                "author": "John H. Walton",
                "work": "The Lost World of Genesis One (IVP Academic, 2009), pp. 23–36",
                "text": "Walton's functional ontology thesis: in ANE cosmogony, something does not 'exist' until it has a function and a name. Genesis 1 is thus a cosmic temple inauguration — God is not describing material origins but assigning functions to cosmic entities in preparation for divine habitation. This reading resolves the apparent conflict with scientific cosmogony without conceding a non-literal reading."
            },
        ],
        "greek": [("H1254", "בָּרָא", "bara'", "To create; used exclusively with God as subject. Denotes creation that is not dependent on pre-existing material — the strongest biblical support for creatio ex nihilo."),
                  ("H7225", "רֵאשִׁית", "reshit", "Beginning; first-fruits; that which is first in a sequence. Used in Prov. 8:22 of personified Wisdom, generating Christological readings (cf. Col. 1:15)."),
                  ("H8064", "שָׁמַיִם", "shamayim", "Heavens; dual form suggesting the expansive, layered celestial realm. Includes the atmospheric heavens, the stellar heavens, and the divine abode.")],
        "cross_refs": [("John 1:1", "In the beginning was the Word — Johannine Prologue echoes Gen. 1:1 deliberately"),
                       ("Heb 11:3", "By faith we understand that the worlds were framed by the word of God"),
                       ("Col 1:16", "In Him all things were created, in heaven and on earth"),
                       ("Ps 33:6", "By the word of the LORD the heavens were made — creatio per verbum")],
        "historical": "The Babylonian Enuma Elish (c. 12th century BC) presents the closest ANE parallel: Marduk creates the cosmos from the corpse of the sea-goddess Tiamat. Genesis 1 pointedly avoids theogony (origin of gods), divine conflict, and polytheistic cosmology. The discovery of the Ebla Tablets (1974–75) confirmed the patriarchal period's cultural milieu and the antiquity of Semitic creation vocabulary.",
        "apologetics": "Genesis 1:1 is the locus classicus for the Cosmological Argument. William Lane Craig's contemporary formulation of the Kalam: (1) Everything that begins to exist has a cause; (2) The universe began to exist; (3) Therefore, the universe has a cause. The BGV Theorem (Borde, Guth, Vilenkin, 2003) demonstrates that any universe with a positive average expansion rate must have a beginning — scientific convergence with the theological claim of v. 1."
    },
    "Hebrews 11:1": {
        "context": "The Hall of Faith (Heb. 11:1–40) serves as the rhetorical climax of the epistle's exhortation to perseverance. The author (unknown; Pauline, Apollos, Priscilla, or Barnabas have been proposed) is addressing Jewish Christians contemplating reversion to Judaism under persecution. The definition of faith in v. 1 is not exhaustive theology but a functional description for the rhetorical purpose of sustaining the argument.",
        "scholars": [
            {
                "author": "F.F. Bruce",
                "work": "The Epistle to the Hebrews (NICNT, rev. 1990), pp. 277–282",
                "text": "Bruce examines ὑπόστασις (hypostasis): in classical Greek it means 'substance' or 'reality underlying appearances.' In Patristic theology, it became the term for the distinct personal subsistences of the Trinity (three hypostases, one ousia). Applied to faith, it suggests that faith gives eschatological realities an objective status in the believer's life — 'the title-deed of things hoped for.'"
            },
            {
                "author": "Thomas Schreiner & Ardel Caneday",
                "work": "The Race Set Before Us (IVP, 2001), pp. 187–192",
                "text": "Schreiner and Caneday argue that Hebrews 11 presents faith as the persevering orientation toward the eschatological city (11:10, 16; 12:22) — not a one-time decision but a sustained posture. The ἔλεγχος ('conviction' or 'evidence') of things not seen imports the language of juridical demonstration: faith is the means by which the not-yet-visible is held as certain."
            },
            {
                "author": "Philip Edgcumbe Hughes",
                "work": "A Commentary on the Epistle to the Hebrews (Eerdmans, 1977), pp. 439–445",
                "text": "Hughes traces the Platonic resonance of the verse without conceding Hellenistic dependence: the author may be using familiar philosophical vocabulary to communicate with Hellenized Jewish readers while filling the terms with Hebraic covenantal content. Hypostasis as 'substance' reflects OT trust in divine promissory reliability (Ps. 119:49–50), not Platonic idealism."
            },
        ],
        "greek": [("G5287", "ὑπόστασις", "hypostasis", "Substance; that which stands under; reality. In Patristic Christology, the term for each Person of the Trinity. Here: faith as the ground of eschatological confidence."),
                  ("G1650", "ἔλεγχος", "elenchos", "Proof; conviction; evidence. Legal term for the presentation of decisive evidence. Faith as juridical certitude regarding the invisible."),
                  ("G1679", "ἐλπίζω", "elpizō", "To hope; biblical hope (elpis) is not wishful uncertainty but confident expectation grounded in covenant promise.")],
        "cross_refs": [("2 Cor 5:7", "We walk by faith, not by sight — Pauline epistemological parallel"),
                       ("Rom 8:24", "Hope that is seen is not hope; but we hope for what we do not see"),
                       ("Heb 11:6", "Without faith it is impossible to please God — the axiom this verse grounds"),
                       ("John 20:29", "Blessed are those who did not see and yet believed")],
        "historical": "Hebrews was likely written prior to AD 70 given the present-tense temple references (8:4; 10:11). The recipients were Jewish Christians in Rome or Palestine facing probable Neronian (AD 64–68) or Domitianic persecution. The epistle's sophisticated Greek (the most literary in the NT) suggests a Hellenized Jewish author writing to educated converts considering return to Mosaic observance as a survival strategy.",
        "apologetics": "Hebrews 11:1 is often misread as fideism (belief without evidence). Properly understood, ἔλεγχος ('conviction' / 'evidence') refutes this: faith in the biblical sense is conviction grounded in testimony and historical evidence. Alister McGrath's Mere Apologetics and John Lennox's God's Undertaker both distinguish biblical faith from blind belief, grounding it in the reliability of divine testimony — precisely the argument Hebrews 11 makes through its historical survey."
    },
}

STRONGS_LEXICON = {
    "grace":      {"num": "G5485", "gk": "χάρις", "tr": "charis",   "def": "Unmerited divine favor; gift freely bestowed apart from works. Root: χαίρω (chairō) — to rejoice."},
    "faith":      {"num": "G4102", "gk": "πίστις", "tr": "pistis",   "def": "Conviction of truth; reliance upon Christ for salvation. Root: πείθω (peithō) — to persuade."},
    "logos":      {"num": "G3056", "gk": "λόγος",  "tr": "logos",    "def": "Word; divine rational principle; second Person in Johannine theology. Root: λέγω (legō) — to speak."},
    "agape":      {"num": "G26",   "gk": "ἀγάπη",  "tr": "agapē",   "def": "Self-sacrificial, unconditional love; highest form of divine love. Root: ἀγαπάω (agapaō) — to love."},
    "covenant":   {"num": "H1285", "gk": "בְּרִית", "tr": "berith",  "def": "Binding agreement between parties; backbone of redemptive history. Root: בָּרָה (bara) — to cut."},
    "shalom":     {"num": "H7965", "gk": "שָׁלוֹם", "tr": "shalom", "def": "Completeness, wholeness, peace; holistic well-being and right relationship. Root: שָׁלֵם (shalem) — to be complete."},
    "messiah":    {"num": "H4899", "gk": "מָשִׁיחַ","tr": "mashiach","def": "Anointed One; divinely commissioned deliverer; fulfilled in Jesus. Root: מָשַׁח (mashach) — to anoint."},
    "ekklesia":   {"num": "G1577", "gk": "ἐκκλησία","tr": "ekklēsia","def": "Assembly of called-out ones; the Church as covenant community. Root: ἐκ + καλέω — out of + to call."},
    "pneuma":     {"num": "G4151", "gk": "πνεῦμα",  "tr": "pneuma",  "def": "Spirit; wind; breath. Used of the Holy Spirit and human spirit. Root: πνέω (pneō) — to blow."},
    "sozo":       {"num": "G4982", "gk": "σῴζω",    "tr": "sōzō",    "def": "To save, rescue, preserve from destruction; used of physical healing and spiritual salvation."},
    "dikaiosyne": {"num": "G1343", "gk": "δικαιοσύνη","tr": "dikaiosynē","def": "Righteousness; conformity to the divine standard; in Paul, the status declared by God in justification."},
    "apokalypsis":{"num": "G602",  "gk": "ἀποκάλυψις","tr": "apokalypsis","def": "Unveiling; revelation; disclosure of that which was hidden. The genre title of the final NT book."},
}

STUDY_PROMPTS = {
    "Doctrinal": [
        "What is the biblical basis for the doctrine of penal substitutionary atonement, and how do scholars like John Stott and Henri Blocher defend it against critics?",
        "Trace the development of Trinitarian theology from the NT texts through Nicaea (325 AD). What were the Arian claims and how did Athanasius refute them?",
        "How does Paul distinguish δικαίωσις (justification) from ἁγιασμός (sanctification) in Romans 3–8? What are the Lutheran and Reformed differences on this question?",
        "What is the Johannine conception of eternal life (ζωὴ αἰώνιος)? Does it refer primarily to duration or quality of existence? Examine John 17:3.",
        "Explain the biblical covenants (Noahic, Abrahamic, Mosaic, Davidic, New) and how Covenant Theology and Dispensationalism read their relationship.",
        "What is the hypostatic union and where does Scripture ground it? How did Chalcedon (451 AD) resolve the Nestorian and Eutychian errors?",
        "How does the book of Job function as a theodicy? Compare the three friends' arguments with God's answer from the whirlwind (Job 38–41).",
        "What is the New Perspective on Paul (Dunn, Wright) and how does it challenge the Reformation reading of justification by faith alone?",
    ],
    "Historical": [
        "Describe the Sitz im Leben of Paul's letter to the Romans. Who were its recipients, what was their social situation, and how does this shape the letter's argument?",
        "What was the canon formation process for the NT? By what criteria (apostolicity, catholicity, orthodoxy, liturgical use) were books included or excluded?",
        "Compare the Synoptic Problem — the Marcan Priority hypothesis, the Two-Source Theory, and Matthean Priority (Griesbach). What are the strongest arguments for each?",
        "How did the Dead Sea Scrolls (1947) change our understanding of Second Temple Judaism and NT textual transmission?",
        "Describe the relationship between the Septuagint (LXX) and the Masoretic Text (MT). How do NT authors' OT citations reveal their Bible?",
        "What does archaeology confirm about the biblical narrative? Discuss the Pool of Siloam, the Pilate Inscription, and the Tel Dan Stele.",
        "How did the destruction of Jerusalem (AD 70) shape the development of early Christianity and the composition of the Gospels?",
        "Describe the Reformation debate over sola scriptura. What was the Catholic response at Trent and how do modern evangelical scholars answer it?",
    ],
    "Apologetics": [
        "Present the historical case for the resurrection of Jesus using only criteria accepted by critical historians (enemy attestation, multiple independent sources, criterion of embarrassment).",
        "How does the Kalam Cosmological Argument (Craig) interface with the BGV Theorem (Borde, Guth, Vilenkin, 2003)? What does a universe with a beginning imply theologically?",
        "Evaluate the Outsider Test for Faith (John Loftus). How do Christian philosophers respond to the charge that religious belief is culturally determined?",
        "What is the evidential problem of evil (Rowe) and what are the best Christian responses — Plantinga's Free Will Defense, Hick's Soul-Making, and skeptical theism?",
        "Make the case that the NT documents are reliable historical sources using F.F. Bruce's bibliographical test, internal evidence, and external corroboration.",
        "How does the Isaiah 53 Dead Sea Scroll evidence (1QIsa-a) constitute a prophetic argument for the Messiahship of Jesus? What are the naturalistic objections?",
        "Evaluate the Moral Argument for God's existence (Lewis, Craig). Is the grounding of objective morality in divine nature question-begging?",
        "How do Christian philosophers respond to the divine hiddenness argument (Schellenberg)? Is divine absence evidence against theism?",
    ],
    "Exegetical": [
        "Perform a word study on the Greek ἀγαπάω vs. φιλέω in John 21:15–17. Does the distinction carry theological weight or is it Johannine stylistic variation?",
        "What is the Granville Sharp Rule and how does it support the deity of Christ in Titus 2:13 and 2 Peter 1:1?",
        "Analyze the chiastic structure of John 1:1–18 (the Prologue). What theological emphases does the structure reveal?",
        "What does ἐφ' ᾧ mean in Romans 5:12 and how does the translation choice affect the doctrine of original sin? Compare Augustinian and Eastern Orthodox readings.",
        "Examine the hapax legomenon ἐπιούσιος in Matthew 6:11 (the Lord's Prayer). What does 'daily bread' mean in light of the eschatological context?",
        "How should the participle in Ephesians 5:18 ('be filled with the Spirit') be interpreted grammatically? What does the present passive imperative imply?",
        "Analyze the use of the OT in Matthew 2:15 ('Out of Egypt I called My son'). Is this typology, allegory, or prediction? Compare conservative and critical readings.",
        "What is the background of the 'principalities and powers' (ἀρχαί καὶ ἐξουσίαι) in Ephesians 6:12? How do Walter Wink and Clinton Arnold differ?",
    ],
}

CHURCH_FATHERS = [
    {"name": "Athanasius of Alexandria", "dates": "c. 296–373 AD", "contribution": "De Incarnatione; defender of Nicene orthodoxy against Arianism. 'He became what we are that we might become what He is.'", "key_work": "De Incarnatione Verbi Dei (c. 318 AD)"},
    {"name": "Augustine of Hippo", "dates": "354–430 AD", "contribution": "Confessions, City of God, On the Trinity. Foundational for Western theology on grace, predestination, and the just war theory.", "key_work": "De Civitate Dei (413–426 AD)"},
    {"name": "John Chrysostom", "dates": "c. 347–407 AD", "contribution": "Archbishop of Constantinople; greatest preacher of the patristic era. Homiletical commentaries on Matthew, John, Romans, Galatians.", "key_work": "Homilies on the Gospel of John (c. 390 AD)"},
    {"name": "Origen of Alexandria", "dates": "c. 185–253 AD", "contribution": "Pioneer of systematic theology and biblical criticism. Developed allegorical hermeneutics; produced the Hexapla (six-column OT comparison).", "key_work": "De Principiis (c. 220 AD)"},
    {"name": "Tertullian", "dates": "c. 155–220 AD", "contribution": "First major Latin theologian; coined 'Trinity' (Trinitas) and 'substance/persons' framework. Later joined the Montanist movement.", "key_work": "Apologeticus (c. 197 AD)"},
    {"name": "Irenaeus of Lyon", "dates": "c. 130–202 AD", "contribution": "Against Heresies — refutation of Gnosticism. Developed the concept of recapitulation (ἀνακεφαλαίωσις): Christ restoring what Adam lost.", "key_work": "Adversus Haereses (c. 180 AD)"},
]

MANUSCRIPT_DATA = {
    "New Testament (Greek)":     {"manuscripts": 5856, "earliest_copy": "P52 (~AD 125)", "gap_years": 25},
    "Iliad (Homer)":             {"manuscripts": 643,  "earliest_copy": "~400 BC",       "gap_years": 400},
    "Gallic Wars (Caesar)":      {"manuscripts": 251,  "earliest_copy": "~900 AD",        "gap_years": 950},
    "Annals (Tacitus)":          {"manuscripts": 20,   "earliest_copy": "~1100 AD",       "gap_years": 1000},
    "History (Thucydides)":      {"manuscripts": 96,   "earliest_copy": "~900 AD",        "gap_years": 1300},
    "Works (Plato)":             {"manuscripts": 210,  "earliest_copy": "~895 AD",        "gap_years": 1200},
}


# ─────────────────────────────────────────────
# API
# ─────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_scripture(reference: str, translation: str = "kjv") -> dict:
    url = f"https://bible-api.com/{requests.utils.quote(reference)}?translation={translation}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {"error": "Unable to retrieve. Check reference and connectivity.", "verses": []}


# ─────────────────────────────────────────────
# CHART
# ─────────────────────────────────────────────

def build_manuscript_chart():
    GOLD = "#D4AF37"; SCAR = "#B22222"; NVY = "#0A1628"; BLUE = "#0038A8"
    df = pd.DataFrame([
        {"Work": k, "Manuscripts": v["manuscripts"],
         "Earliest": v["earliest_copy"], "Gap": v["gap_years"]}
        for k, v in MANUSCRIPT_DATA.items()
    ]).sort_values("Manuscripts", ascending=True)

    colors = [SCAR if "New Testament" in w else GOLD for w in df["Work"]]
    fig = go.Figure(go.Bar(
        y=df["Work"], x=df["Manuscripts"], orientation="h",
        marker_color=colors, marker_line_color=NVY, marker_line_width=1,
        text=[f"{v:,}" for v in df["Manuscripts"]],
        textposition="outside", textfont=dict(color=GOLD, size=10, family="monospace"),
        hovertemplate="<b>%{y}</b><br>Manuscripts: %{x:,}<br>Earliest: %{customdata[0]}<br>Compositional gap: %{customdata[1]} yrs<extra></extra>",
        customdata=list(zip(df["Earliest"], df["Gap"])),
    ))
    fig.update_layout(
        title={"text": "Manuscript Attestation: NT vs. Classical Antiquity",
               "font": {"family": "serif", "size": 17, "color": GOLD}, "x": 0.5},
        plot_bgcolor=NVY, paper_bgcolor=BLUE,
        font={"family": "monospace", "color": GOLD},
        xaxis={"title": "Extant Manuscripts", "gridcolor": "rgba(212,175,55,0.10)",
               "color": GOLD, "tickfont": {"size": 10}},
        yaxis={"gridcolor": "rgba(0,0,0,0)", "color": GOLD, "tickfont": {"size": 10}},
        margin={"l": 10, "r": 90, "t": 55, "b": 40}, height=360,
    )
    return fig


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown(f"""
        <div style="text-align:center;padding:1.2rem 0 0.6rem">
            <div style="font-size:1.8rem;margin-bottom:0.3rem">✝️</div>
            <div style="font-family:'Playfair Display',Georgia,serif;
                        font-size:1.35rem;font-weight:600;color:{PURE_GOLD};
                        letter-spacing:0.06em;line-height:1.2;">
                Sententia Bible Lab
            </div>
            <div style="font-size:0.58rem;color:rgba(245,225,122,0.533);letter-spacing:0.2em;margin-top:0.3rem">
                CHRISTIAN APOLOGETICS CODEX
            </div>
        </div>
        <div style="height:1px;background:linear-gradient(90deg,rgba(212,175,55,0),rgba(212,175,55,0.4),rgba(212,175,55,0));margin:0.3rem 0 1rem;"></div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:0.65rem;color:rgba(245,225,122,0.6);letter-spacing:0.15em;margin-bottom:0.4rem">📖 TRANSLATION</div>', unsafe_allow_html=True)
    translation = st.selectbox("Translation", ["kjv", "web", "bbe"], index=0,
                                label_visibility="collapsed",
                                format_func=lambda x: {"kjv": "King James (KJV)",
                                                        "web": "World English (WEB)",
                                                        "bbe": "Basic English (BBE)"}[x])

    st.markdown('<hr/>', unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:0.65rem;color:rgba(245,225,122,0.6);letter-spacing:0.15em;margin-bottom:0.6rem">QUICK LOAD — CANONICAL PASSAGES</div>', unsafe_allow_html=True)
    QUICK_REFS = {
        "John 3:16": "The Gospel in miniature",
        "Romans 8:28-39": "The golden chain of salvation",
        "Isaiah 53:1-12": "The Suffering Servant",
        "Genesis 1:1-5": "Creation ex nihilo",
        "Hebrews 11:1-6": "The definition of faith",
        "Psalm 22": "The Messianic Psalm of dereliction",
        "John 1:1-18": "The Johannine Prologue",
        "Philippians 2:5-11": "The Carmen Christi / kenōsis",
        "Romans 3:21-26": "The heart of Pauline soteriology",
        "Revelation 1:1-8": "The Apocalyptic opening",
    }
    for ref, desc in QUICK_REFS.items():
        if st.button(ref, key=f"qr_{ref}", use_container_width=True, help=desc):
            st.session_state.quick_load_ref = ref
            st.session_state.quick_load_translation = translation

    st.markdown('<hr/>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.58rem;color:rgba(245,225,122,0.267);text-align:center;line-height:1.8;">Sola Scriptura · Soli Deo Gloria<br>Solus Christus · Sola Gratia · Sola Fide</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown(f"""
    <div style="text-align:center;padding:0.8rem 0 0.4rem">
        <div style="font-family:'Playfair Display',Georgia,serif;
                    font-size:2.4rem;font-weight:600;color:{PURE_GOLD};
                    letter-spacing:0.05em;line-height:1.1;
                    text-shadow:0 0 30px rgba(212,175,55,0.267);">
            Sententia Bible Lab
        </div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;
                    color:rgba(245,225,122,0.533);letter-spacing:0.2em;margin-top:0.3rem;">
            CHRISTIAN APOLOGETICS CODEX · GRADUATE RESEARCH WORKSTATION
        </div>
    </div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Canonical Books", "66")
with c2: st.metric("NT Manuscripts", "5,856")
with c3: st.metric("Translations", "3,000+")
with c4: st.metric("Compositional Span", "~1,500 yrs")

st.markdown('<hr/>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "Scripture Lab",
    "Commentary Engine",
    "Historical & Apologetics",
    "Research Prompts",
])


# ══════════════════════════════════════════════
# TAB 1 — SCRIPTURE LAB
# ══════════════════════════════════════════════
with tab1:
    # Handle quick-load from sidebar
    if "quick_load_ref" in st.session_state:
        ref_default = st.session_state.pop("quick_load_ref")
        trans_default = st.session_state.pop("quick_load_translation", translation)
    else:
        ref_default = st.session_state.get("scripture_ref", "John 3:16")
        trans_default = translation

    col_ref, col_btn = st.columns([5, 1])
    with col_ref:
        ref_input = st.text_input(
            "Reference", value=ref_default,
            placeholder="e.g. Romans 8:28-39, Isaiah 53, Psalm 23",
            label_visibility="collapsed",
        )
    with col_btn:
        fetch_btn = st.button("FETCH", use_container_width=True)

    if "scripture_data" not in st.session_state or fetch_btn or ref_input != st.session_state.get("scripture_ref"):
        if ref_input:
            with st.spinner("Fetching passage..."):
                st.session_state.scripture_data = fetch_scripture(ref_input, trans_default)
                st.session_state.scripture_ref  = ref_input

    sdata = st.session_state.get("scripture_data", {})
    sref  = st.session_state.get("scripture_ref", ref_input)

    col_text, col_analysis = st.columns([1, 1], gap="large")

    # ── Left: Scripture Text ──
    with col_text:
        section_header("Scripture Text", sref)

        if sdata.get("error") and not sdata.get("verses"):
            card(f'<span style="color:{SCARLET}">⚠ {sdata["error"]}</span>', SCARLET)
        elif sdata.get("verses"):
            verses = sdata["verses"]
            ref_label = sdata.get("reference", sref)
            trans_name = sdata.get("translation_name", trans_default.upper())

            st.markdown(f'''
                <div style="font-size:0.65rem;color:rgba(245,225,122,0.533);letter-spacing:0.12em;
                            margin-bottom:0.6rem;">{ref_label.upper()} · {trans_name.upper()}</div>
            ''', unsafe_allow_html=True)

            verse_html = ""
            for v in verses:
                num  = v.get("verse", "")
                text = v.get("text", "").strip()
                verse_html += f'''<span style="color:{SCARLET};font-weight:600;font-size:0.72rem;
                    margin-right:4px;">[{num}]</span><span style="color:{CREAM};line-height:2;">{text}</span> '''

            st.markdown(f'''
                <div style="font-family:'IBM Plex Mono',monospace;font-size:0.88rem;
                            line-height:2;color:{CREAM};background:{NAVY};
                            border-left:3px solid {PURE_GOLD};padding:1rem 1.2rem;
                            border-radius:3px;border:1px solid rgba(212,175,55,0.133);">
                    {verse_html}
                </div>''', unsafe_allow_html=True)

            # Parallel translations
            st.markdown('<hr/>', unsafe_allow_html=True)
            section_header("Parallel Translations")
            for alt_trans in ["kjv", "web", "bbe"]:
                if alt_trans != trans_default:
                    alt_label = {"kjv":"KJV","web":"WEB","bbe":"BBE"}[alt_trans]
                    with st.expander(f"{alt_label} — {sref}"):
                        with st.spinner(f"Loading {alt_label}..."):
                            alt_data = fetch_scripture(sref, alt_trans)
                        if alt_data.get("verses"):
                            alt_text = " ".join(v.get("text","").strip() for v in alt_data["verses"])
                            st.markdown(f'<div style="font-size:0.84rem;color:{CREAM};line-height:1.9;">{alt_text}</div>',
                                        unsafe_allow_html=True)

    # ── Right: Analysis Panel ──
    with col_analysis:
        # Strong's Lexical Analysis
        section_header("Lexical Analysis // Strong's")
        text_lower = " ".join(v.get("text","") for v in sdata.get("verses",[])).lower()
        matched = [(k, v) for k, v in STRONGS_LEXICON.items() if k in text_lower or k in sref.lower()]

        if matched:
            for term, entry in matched[:5]:
                st.markdown(f'''
                    <div style="background:rgba(0,56,168,0.2);border:1px solid rgba(212,175,55,0.2);
                                border-left:3px solid {PURE_GOLD};border-radius:3px;
                                padding:0.75rem 1rem;margin-bottom:0.6rem;">
                        <div style="font-size:0.65rem;color:rgba(245,225,122,0.6);letter-spacing:0.1em;">
                            {entry["num"]} · {entry["tr"]}
                        </div>
                        <div style="font-size:1.3rem;color:{CREAM};margin:0.2rem 0;">{entry["gk"]}</div>
                        <div style="font-size:0.78rem;color:{LIGHT_GOLD};line-height:1.7;">{entry["def"]}</div>
                    </div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="font-size:0.78rem;color:rgba(245,225,122,0.4);">Load a passage containing tracked theological terms to activate lexical analysis.</div>',
                        unsafe_allow_html=True)

        st.markdown('<hr/>', unsafe_allow_html=True)

        # Cross-references
        section_header("Cross-References // TSK")
        TSK_REFS = {
            "John 3:16":      [("John 1:14","Incarnation in the Prologue"),("Rom 5:8","God demonstrates love at the cross"),("1 John 4:9","Love manifested in the sending"),("Gen 22:2","Typological: Abraham's only son")],
            "Romans 8:28":    [("Gen 50:20","Joseph: evil turned to good by divine purpose"),("Eph 1:11","Predestined per the counsel of His will"),("Phil 1:12","Imprisonment advancing the gospel"),("Ps 119:91","All things serve the Creator")],
            "Isaiah 53:5":    [("1 Pet 2:24","He bore our sins in His body"),("2 Cor 5:21","Made sin who knew no sin — imputation"),("Matt 8:17","Fulfillment in the healing ministry"),("Rom 4:25","Delivered for our transgressions")],
            "Genesis 1:1":    [("John 1:1","In the beginning was the Word"),("Heb 11:3","Worlds framed by the word of God"),("Col 1:16","All things created in Him"),("Ps 33:6","Heavens made by the LORD's word")],
            "Hebrews 11:1":   [("2 Cor 5:7","Walk by faith, not by sight"),("Rom 8:24","Hope that is seen is not hope"),("Heb 11:6","Without faith impossible to please God"),("John 20:29","Blessed who believe without seeing")],
        }
        canonical_key = next((k for k in TSK_REFS if k.lower() in sref.lower()), None)
        refs_to_show = TSK_REFS.get(canonical_key, [])

        if refs_to_show:
            for ref_v, desc in refs_to_show:
                st.markdown(f'''
                    <div style="display:flex;align-items:baseline;gap:0.7rem;margin-bottom:0.4rem;">
                        <span style="background:{TYRIAN_PURPLE};color:{PURE_GOLD};font-size:0.68rem;
                                     padding:2px 9px;border-radius:2px;white-space:nowrap;
                                     border:1px solid rgba(212,175,55,0.267);">{ref_v}</span>
                        <span style="font-size:0.78rem;color:rgba(245,225,122,0.6);">{desc}</span>
                    </div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="font-size:0.78rem;color:rgba(245,225,122,0.4);">Cross-reference data available for the five key passages in Commentary Engine.</div>',
                        unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 — COMMENTARY ENGINE
# ══════════════════════════════════════════════
with tab2:
    section_header("Commentary Engine", "Scholarly patristic, Reformation, and contemporary sources")

    passage_select = st.selectbox(
        "Select Passage",
        list(COMMENTARY.keys()),
        label_visibility="collapsed",
        format_func=lambda x: x,
    )
    data = COMMENTARY[passage_select]

    # Auto-load the passage in session state
    if st.button(f"↗ Load {passage_select} in Scripture Lab", key="load_from_commentary"):
        st.session_state.scripture_data = fetch_scripture(passage_select, translation)
        st.session_state.scripture_ref  = passage_select

    st.markdown('<hr/>', unsafe_allow_html=True)

    # ── Context ──
    section_header("Historical & Literary Context")
    card(f'<div style="font-size:0.88rem;color:{CREAM};line-height:1.85;">{data["context"]}</div>')

    # ── Scholar Commentaries ──
    section_header("Scholarly Commentary")
    for sch in data["scholars"]:
        st.markdown(f'''
            <div style="background:linear-gradient(135deg,{NAVY},rgba(0,56,168,0.133));
                        border:1px solid rgba(212,175,55,0.2);border-left:4px solid {PURE_GOLD};
                        border-radius:4px;padding:1.1rem 1.3rem;margin-bottom:1rem;">
                <div style="font-family:'Playfair Display',Georgia,serif;
                            font-size:1rem;font-weight:600;color:{PURE_GOLD};margin-bottom:0.2rem;">
                    {sch["author"]}
                </div>
                <div style="font-size:0.65rem;color:rgba(245,225,122,0.533);letter-spacing:0.06em;
                            margin-bottom:0.7rem;font-style:italic;">{sch["work"]}</div>
                <div style="font-size:0.86rem;color:{CREAM};line-height:1.88;">{sch["text"]}</div>
            </div>''', unsafe_allow_html=True)

    col_lex, col_xref = st.columns(2, gap="large")

    # ── Greek/Hebrew Lexicon ──
    with col_lex:
        section_header("Lexical Notes // Greek & Hebrew")
        for strongs_num, term, transliteration, definition in data["greek"]:
            st.markdown(f'''
                <div style="background:{NAVY};border:1px solid rgba(212,175,55,0.133);border-radius:3px;
                            padding:0.8rem 1rem;margin-bottom:0.6rem;">
                    <div style="font-size:0.62rem;color:rgba(245,225,122,0.533);letter-spacing:0.1em;">
                        {strongs_num} · {transliteration}
                    </div>
                    <div style="font-size:1.4rem;color:{CREAM};margin:0.2rem 0;">{term}</div>
                    <div style="font-size:0.78rem;color:{LIGHT_GOLD};line-height:1.7;">{definition}</div>
                </div>''', unsafe_allow_html=True)

    # ── Cross-References ──
    with col_xref:
        section_header("Cross-References // Treasury of Scripture Knowledge")
        for ref_str, note in data["cross_refs"]:
            st.markdown(f'''
                <div style="border-bottom:1px solid rgba(212,175,55,0.094);padding:0.6rem 0;">
                    <div style="display:flex;gap:0.8rem;align-items:baseline;">
                        <span style="background:{TYRIAN_PURPLE};color:{PURE_GOLD};font-size:0.68rem;
                                     padding:2px 9px;border-radius:2px;white-space:nowrap;
                                     border:1px solid rgba(212,175,55,0.267);">{ref_str}</span>
                        <span style="font-size:0.8rem;color:rgba(245,225,122,0.8);">{note}</span>
                    </div>
                </div>''', unsafe_allow_html=True)

    st.markdown('<hr/>', unsafe_allow_html=True)

    # ── Historical Background ──
    section_header("Historical Background & Sitz im Leben")
    card(f'<div style="font-size:0.87rem;color:{CREAM};line-height:1.85;">{data["historical"]}</div>', TYRIAN_PURPLE)

    # ── Apologetics Connection ──
    section_header("Apologetics Interface")
    card(f'<div style="font-size:0.87rem;color:{CREAM};line-height:1.85;">{data["apologetics"]}</div>', SCARLET)

    st.markdown('<hr/>', unsafe_allow_html=True)

    # ── Church Fathers ──
    section_header("Church Fathers // Patristic Witness")
    st.markdown(f'<div style="font-size:0.72rem;color:rgba(245,225,122,0.533);margin-bottom:0.8rem;">Formative voices in the interpretive tradition preceding the Reformation.</div>', unsafe_allow_html=True)
    for father in CHURCH_FATHERS:
        with st.expander(f"{father['name']} ({father['dates']})"):
            st.markdown(f'''
                <div style="font-size:0.84rem;color:{CREAM};line-height:1.8;margin-bottom:0.5rem;">
                    {father["contribution"]}
                </div>
                <div style="font-size:0.68rem;color:rgba(212,175,55,0.6);font-style:italic;">
                    Key work: {father["key_work"]}
                </div>''', unsafe_allow_html=True)

    # ── Lexical Distribution Table ──
    st.markdown('<hr/>', unsafe_allow_html=True)
    section_header("Lexical Distribution Table // Full Strong's Index")
    lex_df = pd.DataFrame([
        {"Term": k, "Strong's": v["num"], "Transliteration": v["tr"],
         "Language": "Greek" if v["num"].startswith("G") else "Hebrew",
         "Definition (abbreviated)": v["def"][:70] + "…"}
        for k, v in STRONGS_LEXICON.items()
    ])
    st.dataframe(lex_df, width="stretch", hide_index=True, column_config={
        "Term":                   st.column_config.TextColumn("TERM",           width=90),
        "Strong's":               st.column_config.TextColumn("STRONG'S",       width=80),
        "Transliteration":        st.column_config.TextColumn("TRANSLITERATION",width=130),
        "Language":               st.column_config.TextColumn("LANG",            width=65),
        "Definition (abbreviated)":st.column_config.TextColumn("DEFINITION"),
    })


# ══════════════════════════════════════════════
# TAB 3 — HISTORICAL & APOLOGETICS
# ══════════════════════════════════════════════
with tab3:
    col_hist, col_apo = st.columns([1, 1], gap="large")

    with col_hist:
        section_header("Bibliographical Test", "Manuscript attestation compared with classical antiquity")
        st.markdown(f'<div style="font-size:0.78rem;color:rgba(245,225,122,0.6);margin-bottom:0.8rem;">F.F. Bruce\'s bibliographical criterion: the NT possesses a documentary foundation orders of magnitude superior to any other ancient document. Scarlet = NT.</div>', unsafe_allow_html=True)
        st.plotly_chart(build_manuscript_chart(), width="stretch")

        section_header("Textual Transmission")
        transmission_data = [
            {"Document": "New Testament (Greek)", "Manuscripts": "5,856", "Earliest": "P52 (~AD 125)", "Gap": "25 years", "Languages": "25,000+"},
            {"Document": "Dead Sea Scrolls (Isaiah)", "Manuscripts": "1QIsa-a", "Earliest": "~125 BC", "Gap": "350 yrs from composition", "Languages": "Hebrew"},
            {"Document": "Septuagint (LXX)", "Manuscripts": "500+", "Earliest": "~250 BC", "Gap": "N/A — translation", "Languages": "Greek"},
            {"Document": "Iliad (Homer)", "Manuscripts": "643", "Earliest": "~400 BC", "Gap": "400 years", "Languages": "Greek"},
            {"Document": "Works (Plato)", "Manuscripts": "210", "Earliest": "~895 AD", "Gap": "1,200 years", "Languages": "Greek"},
        ]
        st.dataframe(pd.DataFrame(transmission_data), width="stretch", hide_index=True)

        section_header("Archaeological Confirmation")
        arch_data = [
            {"Discovery": "Pilate Inscription (1961)", "Location": "Caesarea Maritima", "Confirms": "Pontius Pilate as prefect of Judea"},
            {"Discovery": "Pool of Siloam (2004)", "Location": "Jerusalem", "Confirms": "John 9:7 — healing of the blind man"},
            {"Discovery": "Tel Dan Stele (9th c. BC)", "Location": "Dan, Israel", "Confirms": "Extra-biblical attestation of 'House of David'"},
            {"Discovery": "Dead Sea Scrolls (1947)", "Location": "Qumran caves", "Confirms": "OT textual stability; Second Temple eschatology"},
            {"Discovery": "Ebla Tablets (1974)", "Location": "Tell Mardikh, Syria", "Confirms": "Patriarchal names, Sodom/Gomorrah, Canaanite culture"},
            {"Discovery": "House of Peter (Capernaum)", "Location": "Capernaum", "Confirms": "Mark 1:29 — Peter's house; continuous veneration from 1st c."},
            {"Discovery": "James Ossuary", "Location": "Jerusalem (provenance)", "Confirms": "Inscription: 'James, son of Joseph, brother of Jesus'"},
        ]
        st.dataframe(pd.DataFrame(arch_data), width="stretch", hide_index=True)

    with col_apo:
        section_header("Apologetics Framework", "Primary arguments for the truth of Christianity")

        apo_sections = [
            ("The Cosmological Argument", f"""
                <strong style="color:{PURE_GOLD}">Kalam Formulation (Craig, 1979):</strong><br>
                (1) Everything that begins to exist has a cause.<br>
                (2) The universe began to exist.<br>
                (3) Therefore, the universe has a cause.<br><br>
                <strong style="color:{PURE_GOLD}">Scientific Support:</strong> The BGV Theorem (Borde, Guth, Vilenkin, 2003) demonstrates that any universe with a positive average Hubble expansion must have a past boundary — a beginning. This result is independent of quantum gravity considerations and applies to all inflationary models.<br><br>
                <strong style="color:{PURE_GOLD}">Theological implication:</strong> The cause of space, time, matter, and energy must itself be spaceless, timeless, immaterial, and enormously powerful — a description consistent with classical theism's doctrine of divine aseity.
            """),
            ("The Resurrection: Historical Case", f"""
                <strong style="color:{PURE_GOLD}">The Minimal Facts Method (Habermas & Licona):</strong><br>
                Five facts granted by virtually all NT scholars, including skeptics:<br>
                (1) Jesus died by crucifixion under Pontius Pilate (Tacitus, Josephus, Lucian).<br>
                (2) The tomb was found empty on the third day.<br>
                (3) The disciples had real experiences they believed were of the risen Jesus.<br>
                (4) This transformed them — willing to die for the claim.<br>
                (5) Paul and James, former opponents, converted on resurrection claims.<br><br>
                <strong style="color:{PURE_GOLD}">Criterion of embarrassment:</strong> The first witnesses were women — whose testimony was inadmissible in 1st-century Jewish courts. No one inventing a resurrection story in that milieu would have made women the primary witnesses.
            """),
            ("Messianic Prophecy (Isaiah 53)", f"""
                <strong style="color:{PURE_GOLD}">Prophetic Argument:</strong><br>
                Isaiah 53 predates Christianity by a minimum of 200 years (Dead Sea Scroll 1QIsa-a, c. 125 BC). The passage describes:<br>
                — Suffering and rejection (v. 3)<br>
                — Vicarious suffering for others (v. 5)<br>
                — Silent before accusers (v. 7)<br>
                — Death and burial with the rich (v. 9)<br>
                — Post-mortem vindication (v. 11)<br><br>
                <strong style="color:{PURE_GOLD}">Peter Stoner's probability analysis</strong> (<em>Science Speaks</em>) assigns the probability of one individual fulfilling 8 Messianic prophecies accidentally at 1 in 10<sup>17</sup>. Isaiah 53 alone contains multiple independent data points.
            """),
            ("The Moral Argument", f"""
                <strong style="color:{PURE_GOLD}">Lewis / Craig Formulation:</strong><br>
                (1) If God does not exist, objective moral values and duties do not exist.<br>
                (2) Objective moral values and duties do exist.<br>
                (3) Therefore, God exists.<br><br>
                <strong style="color:{PURE_GOLD}">C.S. Lewis (Mere Christianity, 1952):</strong> The existence of a universal moral law — which humans consistently recognize even when they violate it — points to a Moral Lawgiver. The naturalistic alternatives (evolution, social contract) cannot ground genuine moral <em>obligation</em>, only moral <em>preference</em>.<br><br>
                <strong style="color:{PURE_GOLD}">Grounding objection answered:</strong> Divine command theory is not arbitrary if God's commands flow necessarily from His nature (Euthyphro Dilemma resolved by identifying God's nature as the standard, not His commands).
            """),
        ]

        for title, content in apo_sections:
            with st.expander(title):
                st.markdown(f'<div style="font-size:0.84rem;color:{CREAM};line-height:1.88;">{content}</div>',
                            unsafe_allow_html=True)

        st.markdown('<hr/>', unsafe_allow_html=True)

        section_header("Recommended Bibliography")
        biblio = [
            ("William Lane Craig", "Reasonable Faith (3rd ed., 2008)", "Systematic Christian apologetics — Kalam, resurrection, moral argument"),
            ("F.F. Bruce", "The New Testament Documents: Are They Reliable? (6th ed., 1981)", "Bibliographical test and historical reliability"),
            ("N.T. Wright", "The Resurrection of the Son of God (2003)", "Historical case for the bodily resurrection — 800 pages"),
            ("Gary Habermas & Michael Licona", "The Case for the Resurrection of Jesus (2004)", "Minimal facts method — scholarly apparatus"),
            ("Alvin Plantinga", "Warranted Christian Belief (2000)", "Epistemological grounding of religious belief"),
            ("John N. Oswalt", "The Book of Isaiah: Chapters 40–66 (NICOT, 1998)", "Conservative exegesis of the Servant Songs"),
            ("Raymond E. Brown", "The Gospel According to John (Anchor Bible, 1966)", "Critical commentary — historical-grammatical method"),
            ("D.A. Carson", "The Gospel According to John (Pillar NT Commentary, 1991)", "Evangelical commentary with philological depth"),
            ("Thomas R. Schreiner", "Romans (Baker Exegetical Commentary, 1998)", "Calvinist soteriology rigorously exegeted"),
            ("Gleason Archer", "Encyclopedia of Bible Difficulties (1982)", "Systematic treatment of apparent contradictions"),
        ]
        for author, work, note in biblio:
            st.markdown(f'''
                <div style="border-bottom:1px solid rgba(212,175,55,0.094);padding:0.55rem 0;">
                    <div style="font-size:0.78rem;color:{PURE_GOLD};">{author}</div>
                    <div style="font-size:0.73rem;color:{CREAM};font-style:italic;">{work}</div>
                    <div style="font-size:0.68rem;color:rgba(245,225,122,0.533);margin-top:0.15rem;">{note}</div>
                </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — RESEARCH PROMPTS
# ══════════════════════════════════════════════
with tab4:
    section_header("Research Prompts", "Curated questions for rigorous biblical and theological study")
    st.markdown(f'''
        <div style="font-size:0.82rem;color:rgba(245,225,122,0.733);line-height:1.8;margin-bottom:1.2rem;">
        These prompts are designed for graduate-level engagement. Each question opens a line of inquiry
        that requires engagement with primary sources, original languages, and scholarly secondary literature.
        Use them with commentaries, lexicons, or in dialogue with a theological supervisor.
        </div>''', unsafe_allow_html=True)

    prompt_category = st.selectbox(
        "Category",
        list(STUDY_PROMPTS.keys()),
        label_visibility="collapsed",
        format_func=lambda x: f"{'📖' if x=='Exegetical' else '🏛️' if x=='Doctrinal' else '⏳' if x=='Historical' else '⚔️'} {x}",
    )

    prompts = STUDY_PROMPTS[prompt_category]
    category_descriptions = {
        "Doctrinal":   "Systematic and dogmatic theology — the great loci of Christian doctrine examined through Scripture and tradition.",
        "Historical":  "Historical-critical questions — canon, textual criticism, Sitz im Leben, and the development of Christian thought.",
        "Apologetics": "Philosophical and evidential questions — the intellectual defense of Christian truth claims.",
        "Exegetical":  "Greek and Hebrew textual analysis — grammar, syntax, word studies, and interpretive disputes.",
    }
    st.markdown(f'<div style="font-size:0.72rem;color:rgba(245,225,122,0.533);margin-bottom:1.2rem;">{category_descriptions[prompt_category]}</div>',
                unsafe_allow_html=True)

    for i, prompt in enumerate(prompts, 1):
        st.markdown(f'''
            <div style="background:{NAVY};border:1px solid rgba(212,175,55,0.2);border-left:3px solid {PURE_GOLD};
                        border-radius:4px;padding:1rem 1.2rem;margin-bottom:0.75rem;
                        box-shadow:0 1px 8px rgba(0,0,0,0.3);">
                <div style="font-size:0.6rem;color:rgba(245,225,122,0.4);letter-spacing:0.12em;
                            margin-bottom:0.4rem;">{prompt_category.upper()} INQUIRY {i:02d}</div>
                <div style="font-size:0.88rem;color:{CREAM};line-height:1.8;">{prompt}</div>
            </div>''', unsafe_allow_html=True)

    st.markdown('<hr/>', unsafe_allow_html=True)
    section_header("Study Methodology")
    methodology = [
        ("1. Exegesis before Eisegesis", f"Begin always with the text itself — the original Hebrew (OT) or Greek (NT). Identify the grammatical form of key verbs (tense, voice, mood), the syntactic structure, and the immediate context. Resources: <em>A Greek Grammar of the New Testament</em> (Blass-Debrunner-Funk); <em>Biblical Hebrew: A Text and Workbook</em> (Kittel-Hoffer-Wright)."),
        ("2. Historical-Grammatical Method", f"Determine the author's intended meaning within the original historical and cultural context. Consult the Sitz im Leben: Who wrote it? To whom? Under what circumstances? What was the rhetorical purpose? The meaning of a text cannot exceed what its original author could have intended to communicate."),
        ("3. Theological Analysis", f"Having established exegesis, locate the passage within the broader redemptive-historical narrative (Geerhardus Vos, <em>Biblical Theology</em>). What earlier texts does this passage develop, fulfill, or allude to? How does it contribute to the progressive unfolding of the covenant of grace?"),
        ("4. Engage the Tradition", f"Consult the patristic commentaries (Ante-Nicene Fathers, NPNF series), the Reformers (Calvin's Commentaries, Luther's Works), and contemporary critical scholarship (ICC, NICNT, NIGTC, WBC series). Theologically responsible exegesis is always communal — it takes place in dialogue with the 2,000-year interpretive tradition."),
        ("5. Apologetics Integration", f"Where relevant, connect textual findings to the broader apologetic project: Does this passage bear on the evidential question? Does it advance or complicate the theological claims being defended? Resources: Craig's <em>Reasonable Faith</em>; Plantinga's <em>Warranted Christian Belief</em>."),
    ]
    for title, content in methodology:
        with st.expander(title):
            st.markdown(f'<div style="font-size:0.84rem;color:{CREAM};line-height:1.88;">{content}</div>',
                        unsafe_allow_html=True)

    st.markdown('<hr/>', unsafe_allow_html=True)
    section_header("Key Commentaries by Book")
    commentary_guide = [
        ("Genesis",       "Wenham (WBC) · Hamilton (NICOT) · Walton (NIVAC) · Keil & Delitzsch (classic)"),
        ("Psalms",        "Kidner (TOTC) · Goldingay (Baker) · Mowinckel (form-critical) · Spurgeon (Treasury)"),
        ("Isaiah",        "Oswalt (NICOT, 2 vols.) · Young (NICOT, 3 vols.) · Motyer (IVP) · Childs (OTL)"),
        ("Matthew",       "Carson (EBC) · France (NIGTC) · Davies & Allison (ICC, 3 vols.) · Keener"),
        ("John",          "Brown (AB, 2 vols.) · Carson (Pillar) · Morris (NICNT) · Barrett · Köstenberger"),
        ("Romans",        "Moo (NICNT) · Schreiner (BECNT) · Murray (NICNT) · Cranfield (ICC, 2 vols.) · Dunn"),
        ("Galatians",     "Moo (BECNT) · Longenecker (WBC) · Bruce (NIGTC) · Martyn (AB)"),
        ("Ephesians",     "Lincoln (WBC) · Hoehner (Baker) · O'Brien (Pillar) · Arnold (ZECNT)"),
        ("Hebrews",       "Bruce (NICNT) · Hughes (Eerdmans) · Ellingworth (NIGTC) · Lane (WBC, 2 vols.)"),
        ("Revelation",    "Beale (NIGTC) · Aune (WBC, 3 vols.) · Mounce (NICNT) · Bauckham (theology)"),
    ]
    rows = [{"Book": b, "Recommended Commentaries": c} for b, c in commentary_guide]
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True,
                 column_config={"Book": st.column_config.TextColumn("BOOK", width=100),
                                "Recommended Commentaries": st.column_config.TextColumn("RECOMMENDED COMMENTARIES")})
