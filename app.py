import streamlit as st
import random
import time
import pandas as pd
from supabase import create_client, Client

# --- SETUP & VERBINDING ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def get_land_by_manager(name):
    res = supabase.table("countries").select("*").eq("manager_id", name).execute()
    return res.data[0] if res.data else None

def generate_random_athlete(country_id):
    namen = ["Lukas", "Liam", "Sven", "Mateo", "Finn", "Arthur", "Lars", "Noah"]
    achternamen = ["Bakker", "Visser", "Schmidt", "Smith", "Dubois", "Petrov"]
    return {
        "country_id": country_id,
        "name": f"{random.choice(namen)} {random.choice(achternamen)}",
        "age": random.randint(18, 28),
        "skill_speed": random.randint(40, 75),
        "skill_strength": random.randint(40, 75),
        "skill_stamina": random.randint(40, 75),
        "skill_technique": random.randint(40, 75),
        "skill_focus": random.randint(40, 75)
    }

# --- INTERFACE ---
st.set_page_config(page_title="Multi Sport Online - Master", layout="wide")
st.sidebar.title("🏅 Multi Sport Online")
menu = st.sidebar.radio("Navigatie", ["🏠 Home / Inschrijven", "🏛️ Mijn Land", "🏋️ Training & Scouting", "🏟️ Simulatie", "🔒 Admin"])

# --- PAGINA: INSCHRIJVEN ---
if menu == "🏠 Home / Inschrijven":
    st.title("Welkom bij Multi Sport Online")
    st.write("Stap in de schoenen van een bondscoach en leid je land naar Olympisch goud.")
    m_name = st.text_input("Voer een Manager Naam in om te starten")
    if st.button("Start je Carrière"):
        if m_name:
            vrij_land = supabase.table("countries").select("*").is_("manager_id", "null").order("registration_order").limit(1).execute()
            if vrij_land.data:
                land = vrij_land.data[0]
                supabase.table("countries").update({"manager_id": m_name, "is_active": True}).eq("id", land['id']).execute()
                # Maak direct 15 starters-atleten
                team = [generate_random_athlete(land['id']) for _ in range(15)]
                supabase.table("athletes").insert(team).execute()
                st.success(f"Gefeliciteerd {m_name}! Je bent de manager van {land['name']}.")
                st.balloons()
            else: st.error("Geen landen meer beschikbaar.")

# --- PAGINA: MIJN LAND ---
elif menu == "🏛️ Mijn Land":
    m_login = st.sidebar.text_input("Manager Login")
    land = get_land_by_manager(m_login)
    if land:
        st.title(f"Dashboard: {land['name']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Management Punten", f"{land['mp']} MP")
        c2.metric("Goud 🥇", land['gold'])
        c3.metric("Zilver/Brons 🥈🥉", f"{land['silver']} / {land['bronze']}")
        
        st.subheader("Jouw Selectie")
        atleten = supabase.table("athletes").select("*").eq("country_id", land['id']).execute()
        st.dataframe(pd.DataFrame(atleten.data).drop(columns=['country_id', 'id']))

# --- PAGINA: TRAINING & SCOUTING ---
elif menu == "🏋️ Training & Scouting":
    m_login = st.sidebar.text_input("Manager Login")
    land = get_land_by_manager(m_login)
    if land:
        st.title("Ontwikkeling & Scouting")
        t1, t2 = st.tabs(["🏋️ Atleet Trainen (50 MP)", "🔎 Nieuw Talent Scouten (200 MP)"])
        
        with t1:
            atleten = supabase.table("athletes").select("*").eq("country_id", land['id']).execute()
            if atleten.data:
                a_keuze = st.selectbox("Kies atleet", [a['name'] for a in atleten.data])
                skill_keuze = st.selectbox("Train Skill", ["Speed", "Strength", "Stamina", "Technique", "Focus"])
                if st.button("Start Training"):
                    if land['mp'] >= 50:
                        target = next(a for a in atleten.data if a['name'] == a_keuze)
                        col = f"skill_{skill_keuze.lower()}"
                        supabase.table("athletes").update({col: target[col] + random.randint(2, 5)}).eq("id", target['id']).execute()
                        supabase.table("countries").update({"mp": land['mp'] - 50}).eq("id", land['id']).execute()
                        st.success(f"{a_keuze} is beter geworden in {skill_keuze}!")
                        st.rerun()
        with t2:
            if st.button("Scout een Atleet"):
                if land['mp'] >= 200:
                    nieuw = generate_random_athlete(land['id'])
                    supabase.table("athletes").insert(nieuw).execute()
                    supabase.table("countries").update({"mp": land['mp'] - 200}).eq("id", land['id']).execute()
                    st.success(f"Nieuw talent gescout: {nieuw['name']}!")
                    st.balloons()

# --- PAGINA: SIMULATIE ---
elif menu == "🏟️ Simulatie":
    st.title("Olympisch Stadion - Live")
    event = st.selectbox("Kies een onderdeel voor de demonstratie", ["100m Sprint", "Marathon", "Gewichtheffen"])
    if st.button("Start Wedstrijd Simulatie"):
        with st.status("Deelnemers maken zich klaar...", expanded=True) as status:
            time.sleep(1)
            st.write("Startschot klinkt! 🔫")
            # De simulatie-motor: berekent score op basis van skills + geluk
            deelnemers = supabase.table("athletes").select("*, countries(name)").limit(8).execute()
            if deelnemers.data:
                results = []
                for d in deelnemers.data:
                    score = (d['skill_speed'] * 0.7) + (d['skill_focus'] * 0.3) + random.randint(-5, 5)
                    results.append({"Land": d['countries']['name'], "Atleet": d['name'], "Score": round(score, 2)})
                
                df_res = pd.DataFrame(results).sort_values(by="Score", ascending=False).reset_index(drop=True)
                df_res.index += 1
                st.table(df_res)
                status.update(label="Wedstrijd afgelopen!", state="complete")
                st.success(f"Goud gaat naar {df_res.iloc[0]['Land']}!")

# --- PAGINA: ADMIN ---
elif menu == "🔒 Admin":
    st.title("Admin Panel")
    if st.text_input("Wachtwoord", type="password") == "MultiSport2026!":
        if st.button("🧨 VOLLEDIGE RESET"):
            supabase.table("athletes").delete().neq("id", 0).execute()
            supabase.table("countries").update({"manager_id": None, "mp": 1000, "gold":0, "silver":0, "bronze":0, "is_active":False}).neq("id", 0).execute()
            st.error("Systeem volledig gereset naar 0.")
