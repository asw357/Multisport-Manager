import streamlit as st
import random
from supabase import create_client, Client

# Verbinding maken met Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- FUNCTIE: ATLEET GENERATOR ---
def generate_starter_team(country_id, country_name):
    # Simpele namenlijst (Later uit te breiden naar duizenden namen)
    names_db = {
        "Australië": ["Jack Thompson", "Cooper Reid", "Lachlan Jones", "Riley Wilson"],
        "Nederland": ["Jan de Vries", "Thijs Bakker", "Lars van Dijk", "Sven Postma"],
        "Duitsland": ["Lukas Schmidt", "Max Müller", "Erik Wagner", "Finn Fischer"]
    }
    local_names = names_db.get(country_name, ["John Smith", "Alex Brown", "Sam Wilson"])
    
    new_athletes = []
    for i in range(20):
        # Editie 1: Alleen mannen
        is_veteraan = i < 3  # De eerste 3 zijn 'leraren' of 'matrozen'
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
    
    # Stuur naar de database
    supabase.table("athletes").insert(new_athletes).execute()

# --- INTERFACE CONFIGURATIE ---
st.set_page_config(page_title="Multi Sport Online", layout="wide")

# Zijbalk voor taal en navigatie
lang = st.sidebar.selectbox("Taal / Language", ["Nederlands", "English", "Deutsch", "Français"])
menu = st.sidebar.radio("Navigatie", ["Inschrijven", "Mijn Land", "Admin"])

# --- PAGINA: INSCHRIJVEN ---
if menu == "Inschrijven":
    st.title("🏅 Registreer je Land")
    st.write("Schrijf je in als manager. Je krijgt automatisch het eerstvolgende land toegewezen.")
    
    # Hier zat de fout: de variabele naam moet overal hetzelfde zijn
    manager_input = st.text_input("Manager Naam")
    
    if st.button("Start Carrière"):
        if manager_input:
            # Zoek het eerstvolgende vrije land op registration_order
            res = supabase.table("countries").select("*").is_("manager_id", "null").order("registration_order").limit(1).execute()
            
            if res.data:
                land = res.data[0]
                # Update land met manager naam (hier is manager_input nu correct)
                supabase.table("countries").update({"manager_id": manager_input, "is_active": True}).eq("id", land['id']).execute()
                
                # Genereer team van 20 mannen
                generate_starter_team(land['id'], land['name'])
                
                st.success(f"Gefeliciteerd {manager_input}! Je bent nu de manager van {land['name']}!")
                st.balloons()
            else:
                st.error("Alle landen zijn momenteel bezet.")
        else:
            st.warning("Vul eerst een manager naam in.")

# --- PAGINA: DASHBOARD (MIJN LAND) ---
elif menu == "Mijn Land":
    st.title("🏛️ Land Management")
    m_login = st.sidebar.text_input("Log in met je Manager Naam")
    
    if m_login:
        res = supabase.table("countries").select("*").eq("manager_id", m_login).execute()
        if res.data:
            land = res.data[0]
            st.header(f"Land: {land['name']}")
            st.metric("Management Punten", f"{land['mp']} MP")
            
            # Laat de atleten zien
            atleten_res = supabase.table("athletes").select("*").eq("country_id", land['id']).execute()
            if atleten_res.data:
                st.subheader("Jouw Atleten (Mannen - Editie 1)")
                st.dataframe(atleten_res.data, use_container_width=True)
        else:
            st.error("Geen land gevonden voor deze manager.")

# --- PAGINA: ADMIN ---
elif menu == "Admin":
    st.title("🔒 Admin Controlekamer")
    pw = st.text_input("Wachtwoord", type="password")
    
    if pw == "MultiSport2026!":
        st.success("Toegang verleend.")
        
        st.subheader("Database Opschonen (Voor testen)")
        
        if st.button("❌ Wis alle atleten"):
            supabase.table("athletes").delete().neq("id", 0).execute()
            st.warning("Alle atleten zijn verwijderd uit de database.")
            
        if st.button("🔄 Maak alle landen weer vrij"):
            supabase.table("countries").update({"manager_id": None, "is_active": False}).neq("id", 0).execute()
            st.info("Alle managers zijn verwijderd. Landen zijn weer beschikbaar.")

        if st.button("🧨 VOLLEDIGE RESET (Atleten + Managers)"):
            supabase.table("athletes").delete().neq("id", 0).execute()
            supabase.table("countries").update({"manager_id": None, "is_active": False}).neq("id", 0).execute()
            st.error("Alles is gereset naar de start-situatie.")
