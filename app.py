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
