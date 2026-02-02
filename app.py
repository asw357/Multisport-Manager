import streamlit as st
import random
from supabase import create_client, Client

# 1. Database verbinding (stond er al)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# 2. HIER PLAATS JE DE GENERATOR (Nieuw)
def generate_local_athlete(country_name, gender="Man"):
    # Uitgebreide namenlijsten per cultuur (fictief maar passend)
    naming_data = {
        "Nederland": ["Lars van den Berg", "Thijs de Boer", "Sven Bakker", "Bram Visser"],
        "Bulgarije": ["Ivan Petrov", "Georgi Ivanov", "Stoyan Kolev", "Dimitar Bozhilov"],
        "Australië": ["Jack Thompson", "Riley Wilson", "Cooper Reid", "Lachlan Jones"],
        "Griekenland": ["Nikolaos Pappas", "Kostas Dimitriou", "Adonis Georgiou", "Yannis Angelos"],
        "Duitsland": ["Lukas Schmidt", "Max Müller", "Erik Wagner", "Finn Fischer"]
    }
    
    # Kies een naam op basis van het land, of een standaard als het land niet in de lijst staat
    name_list = naming_data.get(country_name, ["Alex Smith", "Sam Brown", "Jordan Taylor"])
    name = random.choice(name_list)
    
    # Skills genereren (0-100)
    # Dit is de basis, Admin kan dit later per sport onderdeel laten wegen
    skills = {
        "country_id": None, # Wordt ingevuld bij aanroep
        "name": name,
        "gender": gender,
        "age": random.randint(18, 25),
        "skill_speed": random.randint(45, 80),
        "skill_strength": random.randint(45, 80),
        "skill_stamina": random.randint(45, 80),
        "skill_technique": random.randint(45, 80),
        "skill_focus": random.randint(45, 80)
    }
    return skills

# 3. DE REST VAN JE CODE (Menu, Inschrijven, etc.)
st.set_page_config(page_title="Multi Sport Online PRO")
# ... de rest van de interface ...

import streamlit as st
import random
import time
from supabase import create_client, Client

# Verbinding
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- FUNCTIE: LAND TOEWIJZEN OP VOLGORDE ---
def claim_next_country(manager_name):
    # Zoek het land met de laagste registration_order dat geen manager heeft
    res = supabase.table("countries").select("*").is_("manager_id", "null").order("registration_order").limit(1).execute()
    
    if res.data:
        land = res.data[0]
        # Update land
        supabase.table("countries").update({"manager_id": manager_name, "is_active": True}).eq("id", land['id']).execute()
        return land
    return None

# --- INTERFACE ---
st.set_page_config(page_title="Multi Sport Online PRO", layout="wide")

menu = st.sidebar.radio("Navigatie", ["Inschrijven", "Manager Pagina", "Live Simulatie", "Admin Control"])

# --- INSCHRIJVEN ---
if menu == "Inschrijven":
    st.title("Inschrijven: Multi Sport Online")
    m_name = st.text_input("Kies je Manager Naam")
    
    if st.button("Start Carrière"):
        land = claim_next_country(m_name)
        if land:
            st.success(f"Welkom! Je bent Manager van {land['name']} (Plek {land['registration_order']})")
            # Check of je bij de eerste 8 zit voor Editie 1
            if land['registration_order'] <= 8:
                st.info("Je bent gekwalificeerd voor Zomer Editie 1!")
            else:
                st.warning("Je staat op de lijst voor Zomer Editie 2.")
        else:
            st.error("Alle 200+ landen zijn momenteel bezet.")

# --- MANAGER PAGINA ---
elif menu == "Manager Pagina":
    m_login = st.sidebar.text_input("Login")
    if m_login:
        land_res = supabase.table("countries").select("*").eq("manager_id", m_login).execute()
        if land_res.data:
            land = land_res.data[0]
            st.title(f"Hoofdkwartier: {land['name']}")
            
            # Tabbladen voor alles wat je wilde
            t1, t2, t3, t4 = st.tabs(["Atleten", "Training", "Scouting", "Historie"])
            with t1:
                st.write("Hier staan je atleten met hun skills en leeftijd.")
            with t3:
                st.write("Scout hier nieuwe talenten (Lijst van 5 of 10).")
        else:
            st.error("Manager niet gevonden.")

# --- ADMIN CONTROL ---
elif menu == "Admin Control":
    st.title("Admin: Beheer de Wereld")
    pw = st.text_input("Wachtwoord", type="password")
    if pw == "MultiSport2026!":
        st.subheader("Editie Instellingen")
        if st.button("Start Zomer Editie 1 (Nu)"):
            supabase.table("editions").update({"status": "lopend"}).eq("number", 1).execute()
            st.success("Editie 1 is nu LIVE!")
        
        st.subheader("Landen Beheer")
        # Hier kun je zien wie welk land heeft en mensen uitschrijven
        alle_landen = supabase.table("countries").select("registration_order, name, manager_id").order("registration_order").execute()
        st.table(alle_landen.data)
