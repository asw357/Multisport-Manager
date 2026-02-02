import streamlit as st
import random
import pandas as pd
from supabase import create_client, Client

# --- SETUP ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- MEERTALIGHEID DICTIONARY ---
dict = {
    "Nederlands": {"welcome": "Welkom Coach", "train": "Training", "scout": "Scouten", "tactics": "Tactiek", "dash": "Dashboard"},
    "English": {"welcome": "Welcome Coach", "train": "Training", "scout": "Scouting", "tactics": "Tactics", "dash": "Dashboard"},
    "Deutsch": {"welcome": "Willkommen Coach", "train": "Training", "scout": "Scouting", "tactics": "Taktik", "dash": "Dashboard"},
    "Français": {"welcome": "Bienvenue Coach", "train": "Entraînement", "scout": "Recrutement", "tactics": "Tactique", "dash": "Tableau de bord"}
}

# --- FUNCTIES ---
def get_athlete_data(land_id):
    return supabase.table("athletes").select("*").eq("country_id", land_id).execute().data

# --- INTERFACE ---
st.set_page_config(page_title="Multi Sport Online PRO", layout="wide")
lang = st.sidebar.selectbox("Language", ["Nederlands", "English", "Deutsch", "Français"])
t = dict[lang]

menu = st.sidebar.radio("Navigatie", [t["dash"], t["train"], t["scout"], t["tactics"], "Simulatie", "Admin"])

# Gebruiker inloggen (Simpel voor nu via sidebar)
m_name = st.sidebar.text_input("Manager Naam Login")
land_data = None
if m_name:
    res = supabase.table("countries").select("*").eq("manager_id", m_name).execute()
    if res.data: land_data = res.data[0]

# --- 1. DASHBOARD ---
if menu == t["dash"]:
    if not land_data:
        st.title("Inschrijven")
        new_name = st.text_input("Kies een Manager Naam")
        if st.button("Claim Land"):
            # Land claim logica (zie vorige code)
            st.success("Land geclaimd! Log in via de zijbalk.")
    else:
        st.title(f"{t['dash']}: {land_data['name']}")
        st.metric("Budget", f"{land_data['mp']} MP")
        atleten = get_athlete_data(land_data['id'])
        st.dataframe(pd.DataFrame(atleten))

# --- 2. TRAINING (Gedetailleerd) ---
elif menu == t["train"] and land_data:
    st.title(t["train"])
    atleten = get_athlete_data(land_data['id'])
    a_keuze = st.selectbox("Selecteer Atleet", [a['name'] for a in atleten])
    t_type = st.radio("Type Training", ["Licht (10 MP, +1 skill)", "Intensief (50 MP, +4 skill)", "Specialistisch (100 MP, +10 skill)"])
    
    if st.button("Start Training"):
        # Hier de logica voor kosten en skill-update...
        st.success(f"Training voltooid voor {a_keuze}!")

# --- 3. SCOUTING (Keuzelijst van 5) ---
elif menu == t["scout"] and land_data:
    st.title(t["scout"])
    if st.button("Genereer Scouting Lijst (50 MP)"):
        st.session_state.scout_list = [
            {"name": f"Talent {i}", "speed": random.randint(50, 90), "strength": random.randint(50, 90)} 
            for i in range(5)
        ]
    
    if "scout_list" in st.session_state:
        for i, talent in enumerate(st.session_state.scout_list):
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{talent['name']}** - Snelheid: {talent['speed']}, Kracht: {talent['strength']}")
            if col2.button(f"Contracteer #{i}", key=f"scout_{i}"):
                # Toevoegen aan database en MP aftrekken
                st.success(f"{talent['name']} is nu onderdeel van je team!")

# --- 4. TACTIEK & INSCHRIJVEN ---
elif menu == t["tactics"] and land_data:
    st.title("Onderdeel Inschrijving & Tactiek")
    events = supabase.table("sports_events").select("*").execute().data
    event_keuze = st.selectbox("Kies Onderdeel", [e['event_name'] for e in events])
    atleten = get_athlete_data(land_data['id'])
    a_keuze = st.selectbox("Kies Atleet voor dit onderdeel", [a['name'] for a in atleten])
    
    # Tactiek opties zoals besproken
    tactiek = st.selectbox("Kies Tactiek", ["Behoudende Start (Veilig)", "Explosieve Start (Risico op vals)", "Kopgroep volgen", "Alles-of-niets"])
    
    if st.button("Bevestig Inschrijving"):
        # Opslaan in event_registrations
        st.success(f"{a_keuze} ingeschreven voor {event_keuze} met tactiek: {tactiek}")

# --- 5. ADMIN (Weging aanpassen) ---
elif menu == "Admin":
    st.title("Admin: Sport-Weging")
    events = supabase.table("sports_events").select("*").execute().data
    e_select = st.selectbox("Kies Sport om weging aan te passen", [e['event_name'] for e in events])
    
    st.write("Bepaal hoe zwaar skills meetellen (Totaal moet 1.0 zijn)")
    w_speed = st.slider("Weging Snelheid", 0.0, 1.0, 0.5)
    w_strength = st.slider("Weging Kracht", 0.0, 1.0, 0.5)
    
    if st.button("Sla Weging Op"):
        # Update skill_weights tabel
        st.success("Weging bijgewerkt voor de simulatie-motor.")
