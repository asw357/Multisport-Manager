import streamlit as st
from supabase import create_client, Client

# Verbinding met jouw database
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- TAALINSTELLINGEN ---
lang = st.sidebar.selectbox("Taal / Language", ["Nederlands", "English", "Deutsch", "Français"])
texts = {
    "Nederlands": {"welcome": "Welkom bij Multi Sport Online", "register": "Inschrijven", "dash": "Manager Dashboard"},
    "English": {"welcome": "Welcome to Multi Sport Online", "register": "Register", "dash": "Manager Dashboard"}
}

st.title(texts[lang]["welcome"])

menu = st.sidebar.radio("Menu", [texts[lang]["register"], texts[lang]["dash"], "Admin"])

# --- INSCHRIJVEN (BLIND OP VOLGORDE) ---
if menu == texts[lang]["register"]:
    st.header("Nieuwe Manager Registratie")
    manager_name = st.text_input("Kies een Manager Naam")
    
    if st.button("Claim je land"):
        # Zoek het eerstvolgende vrije land op registration_order
        res = supabase.table("countries").select("*").is_("manager_id", "NULL").order("registration_order").limit(1).execute()
        
        if res.data:
            land = res.data[0]
            supabase.table("countries").update({"manager_id": manager_name, "is_active": True}).eq("id", land['id']).execute()
            st.success(f"Gefeliciteerd! Je bent de manager van: {land['name']}")
            st.info("Je krijgt nu je starters atleten voor de huidige editie...")
        else:
            st.error("Alle landen zijn momenteel bezet.")

# --- DASHBOARD ---
elif menu == texts[lang]["dash"]:
    name = st.text_input("Voer je manager naam in")
    if name:
        land_res = supabase.table("countries").select("*").eq("manager_id", name).execute()
        if land_res.data:
            land = land_res.data[0]
            st.subheader(f"Land: {land['name']} 🇳🇱") # Vlag wordt dynamisch
            st.write(f"Management Punten (MP): {land['mp']}")
            
            # Hier komen de tabbladen voor Training, Scouting, etc.
            tab1, tab2, tab3 = st.tabs(["Mijn Atleten", "Training", "Scouting"])
            with tab1:
                st.write("Lijst met atleten verschijnt hier...")
        else:
            st.error("Manager niet gevonden.")

# --- ADMIN PANEEL ---
elif menu == "Admin":
    st.header("Admin Controlekamer")
    pwd = st.text_input("Wachtwoord", type="password")
    if pwd == "jouw_geheime_code":
        st.write("Hier kun je edities starten, weer aanpassen en MP bonussen beheren.")
        import random

def generate_starter_team(country_id, country_name):
    # Namenlijstjes per land (als voorbeeld, dit breiden we uit)
    names_db = {
        "Australië": ["Jack Thompson", "Cooper Reid", "Lachlan Jones"],
        "Bulgarije": ["Ivan Petrov", "Georgi Ivanov", "Stoyan Koleve"],
        "Griekenland": ["Nikolaos Pappas", "Kostas Dimitriou", "Adonis Georgiou"],
        "Duitsland": ["Lukas Schmidt", "Max Müller", "Erik Wagner"],
        "Nederland": ["Jan de Vries", "Thijs Bakker", "Lars van Dijk"]
    }
    
    # Pak namen van het land, of algemene namen als het land niet in de lijst staat
    local_names = names_db.get(country_name, ["John Doe", "Alex Smith", "Sam Brown"])
    
    athletes = []
    
    # Maak 20 starters-atleten aan
    for i in range(20):
        name = random.choice(local_names) + f" {random.randint(1,99)}" # Tijdelijk uniek maken
        
        # Editie 1: Alleen mannen
        gender = "Man"
        
        # Leeftijd en Skills
        if i < 3: # De 'veteranen' (Leraren/Matrozen)
            age = random.randint(35, 45)
            status = "veteraan"
            skill_tech = random.randint(70, 90) # Veteranen zijn technisch beter
            skill_speed = random.randint(40, 60)
        else:
            age = random.randint(18, 28)
            status = None
            skill_tech = random.randint(40, 70)
            skill_speed = random.randint(50, 85)

        athlete_data = {
            "country_id": country_id,
            "name": name,
            "gender": gender,
            "age": age,
            "special_status": status,
            "skill_speed": skill_speed,
            "skill_strength": random.randint(40, 85),
            "skill_stamina": random.randint(40, 85),
            "skill_technique": skill_tech,
            "skill_focus": random.randint(40, 85)
        }
        athletes.append(athlete_data)
    
    # Stuur de atleten naar de database
    supabase.table("athletes").insert(athletes).execute()
