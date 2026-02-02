import streamlit as st
import random
from supabase import create_client, Client

# Verbinding maken
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- FUNCTIE: ATLEET GENERATOR ---
def generate_starter_team(country_id, country_name):
    names_db = {
        "Australië": ["Jack Thompson", "Cooper Reid", "Lachlan Jones", "Riley Wilson"],
        "Nederland": ["Jan de Vries", "Thijs Bakker", "Lars van Dijk", "Sven Postma"],
        "Duitsland": ["Lukas Schmidt", "Max Müller", "Erik Wagner", "Finn Fischer"]
    }
    local_names = names_db.get(country_name, ["John Smith", "Alex Brown", "Sam Wilson"])
    
    new_athletes = []
    for i in range(20):
        # Editie 1: Alleen mannen
        is_veteraan = i < 3 # Eerste 3 zijn leraren/matrozen
        age = random.randint(35, 45) if is_veteraan else random.randint(18, 28)
        
        athlete = {
            "country_id": country_id,
            "name": f"{random.choice(local_names)} ({i+1})",
            "gender": "Man",
            "age": age,
            "special_status": "veteraan" if is_veteraan else None,
            "skill_speed": random.randint(30, 60) if is_veteraan else random.randint(50, 85),
            "skill_technique": random.randint(70, 95) if is_veteraan else random.randint(40, 70),
            "skill_strength": random.randint(40, 80),
            "skill_stamina": random.randint(40, 80),
            "skill_focus": random.randint(50, 90)
        }
        new_athletes.append(athlete)
    supabase.table("athletes").insert(new_athletes).execute()

# --- INTERFACE ---
st.set_page_config(page_title="Multi Sport Online", layout="wide")

lang = st.sidebar.selectbox("Taal / Language", ["Nederlands", "English", "Deutsch", "Français"])
# (Vertalingen kunnen hier verder worden uitgebreid)

menu = st.sidebar.radio("Navigatie", ["Inschrijven", "Mijn Land", "Admin"])

# --- PAGINA: INSCHRIJVEN ---
if menu == "Inschrijven":
    st.title("🏅 Registreer je Land")
    manager_input = st.text_input("Manager Naam")
    
    if st.button("Start Carrière"):
        # Zoek eerstvolgende land
        res = supabase.table("countries").select("*").is_("manager_id", "null").order("registration_order").limit(1).execute()
        
        if res.data:
            land = res.data[0]
            supabase.table("countries").update({"manager_id": manager_name_input}).eq("id", land['id']).execute()
            
            # Genereer team
            generate_starter_team(land['id'], land['name'])
            
            st.success(f"Welkom! Je bent nu de manager van {land['name']}!")
            st.balloons()
        else:
            st.error("Alle landen zijn momenteel bezet.")

# --- PAGINA: DASHBOARD ---
elif menu == "Mijn Land":
    m_name = st.sidebar.text_input("Manager Naam Login")
    if m_name:
        res = supabase.table("countries").select("*").eq("manager_id", m_name).execute()
        if res.data:
            land = res.data[0]
            st.title(f"Dashboard: {land['name']}")
            st.metric("Management Punten", f"{land['mp']} MP")
            
            # Atleten tonen
            atleten_res = supabase.table("athletes").select("*").eq("country_id", land['id']).execute()
            if atleten_res.data:
                st.write("### Jouw Atleten")
                st.table(atleten_res.data)
        else:
            st.warning("Geen land gevonden voor deze manager.")

# --- PAGINA: ADMIN ---
elif menu == "Admin":
    st.title("🔒 Admin Panel")
    pw = st.text_input("Wachtwoord", type="password")
    if pw == "MultiSport2026!":
        st.success("Toegang verleend.")
        # Admin knoppen voor edities, etc.
        if st.button("Reset Alle Inschrijvingen (TESTING ONLY)"):
            supabase.table("countries").update({"manager_id": None, "is_active": False}).neq("id", 0).execute()
            st.warning("Alle landen zijn weer vrij.")
