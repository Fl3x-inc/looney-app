import streamlit as st
import random

st.set_page_config(layout="wide")
st.title("Looney Tunes Tool - FULL BUILD (Practical Version)")

# NOTE:
# This is a LARGE structured dataset example.
# Not literally every toon in the game (that would require API scraping),
# but built so you can EXTEND easily.

toons = [
    {"name":"Bugs Bunny","role":"Attacker","theme":"Hero","tags":["damage"]},
    {"name":"Daffy Duck","role":"Attacker","theme":"Villain","tags":["damage"]},
    {"name":"Marvin the Martian","role":"Attacker","theme":"Martian","tags":["damage"]},
    {"name":"Foghorn Leghorn","role":"Defender","theme":"Farm","tags":["tank"]},
    {"name":"Elmer Fudd","role":"Defender","theme":"Hunter","tags":["tank"]},
    {"name":"Tweety","role":"Support","theme":"Bird","tags":["heal"]},
    {"name":"Granny","role":"Support","theme":"City","tags":["heal"]},
    {"name":"Porky Pig","role":"Support","theme":"Farm","tags":["buff"]},
    {"name":"Sylvester","role":"Attacker","theme":"Hunter","tags":["damage"]},
    {"name":"Yosemite Sam","role":"Attacker","theme":"Outlaw","tags":["damage"]},
    {"name":"Road Runner","role":"Attacker","theme":"Speed","tags":["damage"]},
    {"name":"Wile E Coyote","role":"Attacker","theme":"Hunter","tags":["damage"]},
    {"name":"Pepe Le Pew","role":"Support","theme":"City","tags":["heal"]},
    {"name":"Lola Bunny","role":"Support","theme":"Hero","tags":["buff"]},
    {"name":"Taz","role":"Attacker","theme":"Wild","tags":["damage"]},
    {"name":"Speedy Gonzales","role":"Attacker","theme":"Speed","tags":["damage"]},
    {"name":"Gossamer","role":"Defender","theme":"Monster","tags":["tank"]},
]

names=[t["name"] for t in toons]
themes=sorted(list(set([t["theme"] for t in toons])))

# ---------- SMART TEAM ENGINE ----------
def score_team(team):
    score=0
    roles=[t["role"] for t in toons if t["name"] in team]

    if "Defender" in roles: score+=2
    if "Support" in roles: score+=2
    if roles.count("Attacker")>=2: score+=2

    return score

def build_best_team(pool):
    best=None
    best_score=-1

    for _ in range(50):
        sample=random.sample(pool, min(4,len(pool)))
        sc=score_team(sample)
        if sc>best_score:
            best_score=sc
            best=sample

    return best

mode=st.sidebar.selectbox("Mode",["War","Arena"])

# ---------- WAR ----------
if mode=="War":
    st.header("WAR")

    structure=st.selectbox("Structure",["Cannon (3)","Tower (4)","Central (6)","Ship (8)"])

    st.subheader("Enemy Team")
    enemy=[st.selectbox(f"Enemy {i+1}",names,key=f"w{i}") for i in range(4)]

    if st.button("Generate Attack Teams"):
        available=names.copy()

        for i in range(4):
            team=build_best_team(available)

            for t in team:
                if t in available:
                    available.remove(t)

            st.success(f"Attack {i+1}: {team}")

# ---------- ARENA ----------
if mode=="Arena":
    st.header("ARENA")

    selected_themes=st.multiselect("Themes",themes)
    pool=[t["name"] for t in toons if t["theme"] in selected_themes]

    st.write("Pool:",pool)

    defence=st.multiselect("Defence (4)",pool,max_selections=4)
    remaining=[t for t in pool if t not in defence]

    if st.button("Generate Arena Teams"):
        for i in range(2):
            team=build_best_team(remaining)

            for t in team:
                if t in remaining:
                    remaining.remove(t)

            st.success(f"Match {i+1}: {team}")

# ---------- GADGET PLACEHOLDER ----------
st.sidebar.markdown("### Gadgets (basic)")
st.sidebar.write("Basic placeholder system ready for V8 expansion")
