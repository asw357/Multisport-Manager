import streamlit as st
import random
import time
from supabase import create_client, Client

# Database verbinding
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- ENGINE: ATLEET GENERATOR ---
def create_athlete(country_id, name=None, gender="Man"):
    if not name:
        names = ["Lukas", "Erik", "Marc", "Sven", "Johan", "Alex", "Finn", "Pietro"]
        surnames = ["de Groot", "Schmidt", "Smith", "Bakker", "Müller", "Jones"]
        name = f"{random.choice(names)} {random.choice(surnames)}"
    
    athlete = {
        "country_id": country_id,
        "name": name,
        "gender": gender,
        "age": random.randint(18, 25),
        "skill_speed": random.randint(40, 75),
        "skill_strength": random.randint(40, 75),
        "skill_stamina": random.randint(40, 75),
        "skill_technique": random.randint(40, 75),
        "skill_focus": random.randint(40, 75)
    }
    return athlete

# --- INTERFACE ---
st.set_page_config(page_title="Multi Sport Online", layout="wide")
st.sidebar.title("🏅 Multi Sport Online")

menu = st.sidebar.radio("Menu", ["Inschrijven", "Manager Dashboard", "Scouting & Training", "Simulatie", "Admin"])

# --- MODULE 1: INSCHRIJVEN ---
if menu == "Inschrijven":
    st.title("Start je Olympische Avontuur")
    m_name = st.text_input("Naam van de Manager")
    if st.button("Claim Land"):
        res = supabase.table("countries").select("*").is_("manager_id", "null").order("registration_order").limit(1).execute()
        if res.data:
            land = res.data[0]
            supabase.table("countries").update({"manager_id": m_name}).eq("id", land['id']).execute()
            # Maak eerste 15 atleten
            start_team = [create_athlete(land['id']) for _ in range(15)]
            supabase.table("athletes").insert(start_team).execute()
            st.success(f"Welkom {m_name}! Je bent de manager van {land['name']}. Je hebt 15 atleten gekregen.")
        else:
            st.error("Geen landen beschikbaar.")

# --- MODULE 2: DASHBOARD & TRAINING ---
elif menu == "Manager Dashboard" or menu == "Scouting & Training":
    m_login = st.sidebar.text_input("Login (Manager Naam)")
    if m_login:
        land_res = supabase.table("countries").select("*").eq("manager_id", m_login).execute()
        if land_res.data:
            land = land_res.data[0]
            st.title(f"Dashboard: {land['name']}")
            
            col1, col2 = st.columns(2)
            col1.metric("Management Punten", f"{land['mp']} MP")
            col2.metric("Medailles", f"🥇 {land['gold']} | 🥈 {land['silver']} | 🥉 {land['bronze']}")

            if menu == "Manager Dashboard":
                st.subheader("Jouw Team")
                atleten = supabase.table("athletes").select("*").eq("country_id", land['id']).execute()
                st.dataframe(atleten.data)
            
            else: # Scouting & Training
                tab1, tab2 = st.tabs(["🏋️ Training", "🔎 Scouting"])
                with tab1:
                    st.write("Verbeter je atleten voor 50 MP per sessie.")
                    atleten = supabase.table("athletes").select("*").eq("country_id", land['id']).execute()
                    atleet_namen = {a['name']: a['id'] for a in atleten.data}
                    keuze = st.selectbox("Kies atleet", list(atleet_namen.keys()))
                    skill = st.selectbox("Welke skill trainen?", ["Speed", "Strength", "Stamina", "Technique", "Focus"])
                    if st.button("Trainen"):
                        if land['mp'] >= 50:
                            # Update skill
                            col_name = f"skill_{skill.lower()}"
                            current_skill = next(a[col_name] for a in atleten.data if a['name'] == keuze)
                            supabase.table("athletes").update({col_name: current_skill + random.randint(1, 3)}).eq("id", atleet_namen[keuze]).execute()
                            supabase.table("countries").update({"mp": land['mp'] - 50}).eq("id", land['id']).execute()
                            st.success(f"{keuze} is verbeterd!")
                            st.rerun()
                with tab2:
                    st.write("Scout een nieuwe atleet voor 200 MP.")
                    if st.button("Scout Nieuw Talent"):
                        if land['mp'] >= 200:
                            nieuw = create_athlete(land['id'])
                            supabase.table("athletes").insert(nieuw).execute()
                            supabase.table("countries").update({"mp": land['mp'] - 200}).eq("id", land['id']).execute()
                            st.balloons()
                            st.success(f"Nieuwe atleet gescout: {nieuw['name']}")

# --- MODULE 3: SIMULATIE ---
elif menu == "Simulatie":
    st.title("Live Verslag & Resultaten")
    st.info("Hier zie je de wedstrijden zodra de Admin de editie start.")
    # In een echte simulatie rekenen we hier de tijden uit op basis van skills
    if st.button("Simuleer 100m Sprint (Demo)"):
        with st.status("Wedstrijd bezig...", expanded=True) as status:
            st.write("Atleten maken zich klaar...")
            time.sleep(2)
            st.write("BANG! Ze zijn weg!")
            time.sleep(3)
            st.write("De laatste meters...")
            results = [
                {"Land": "Australië", "Tijd": "9.88s", "Rank": 1},
                {"Land": "Nederland", "Tijd": "9.95s", "Rank": 2},
                {"Land": "Griekenland", "Tijd": "10.02s", "Rank": 3}
            ]
            st.table(results)
            status.update(label="Wedstrijd Voltooid!", state="complete")

# --- MODULE 4: ADMIN ---
elif menu == "Admin":
    st.title("Beheer")
    if st.text_input("Admin Wachtwoord", type="password") == "MultiSport2026!":
        if st.button("🧨 RESET GAME (Wis alles)"):
            supabase.table("athletes").delete().neq("id", 0).execute()
            supabase.table("countries").update({"manager_id": None, "mp": 1000, "gold":0, "silver":0, "bronze":0}).neq("id", 0).execute()
            st.error("Systeem gereset.")
