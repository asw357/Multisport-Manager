import streamlit as st
from supabase import create_client, Client
import random

# DATABASE VERBINDING
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Multi Sport Online", layout="wide")

# --- FUNCTIES VOOR DE LOGICA ---

def get_free_countries():
    # Haal landen op die nog geen manager hebben
    res = supabase.table("countries").select("*").is_("manager_id", "NULL").execute()
    return res.data

def create_atleet(country_id, event_name):
    # Check of het een leraar of matroos is
    is_special = "leraren" in event_name.lower() or "matrozen" in event_name.lower()
    
    if is_special:
        age = random.randint(32, 48)
        # Leraren/Matrozen: Focus en Techniek zijn top, Snelheid minder
        skills = {
            "speed": random.randint(35, 55),
            "strength": random.randint(50, 70),
            "stamina": random.randint(45, 65),
            "technique": random.randint(70, 90),
            "focus": random.randint(75, 95)
        }
    else:
        age = random.randint(18, 26)
        skills = {k: random.randint(50, 72) for k in ["speed", "strength", "stamina", "technique", "focus"]}

    return {
        "country_id": country_id,
        "name": f"{random.choice(['Lars', 'Sanne', 'Thijs', 'Marek', 'Pierre', 'Jack', 'Hans'])} {random.choice(['Jansen', 'Smit', 'Müller', 'Dubois', 'Thompson'])}",
        "gender": "Man",
        "age": age,
        "skill_speed": skills["speed"],
        "skill_strength": skills["strength"],
        "skill_stamina": skills["stamina"],
        "skill_technique": skills["technique"],
        "skill_focus": skills["focus"],
        "is_special_heritage": is_special # Deze markering zorgt dat ze buiten de limieten vallen
    }

# --- INTERFACE ---

def main():
    st.sidebar.title("🏆 Multi Sport Online")
    menu = ["🏠 Home / Inschrijven", "📊 Manager Dashboard", "🕹️ Admin Paneel"]
    choice = st.sidebar.radio("Ga naar:", menu)

    if choice == "🏠 Home / Inschrijven":
        st.header("Schrijf je in voor de Game")
        vrije_landen = get_free_countries()
        
        if not vrije_landen:
            st.warning("Alle landen zijn momenteel bezet.")
        else:
            gekozen_land_naam = st.selectbox("Kies een land om te managen:", [l['name'] for l in vrije_landen])
            user_id = st.text_input("Verzin een Manager-naam (bijv. Manager_NL):")
            
            if st.button("Claim dit Land & Ontvang Start-atleten"):
                if user_id:
                    # 1. Update het land met de manager naam
                    land = next(l for l in vrije_landen if l['name'] == gekozen_land_naam)
                    supabase.table("countries").update({"manager_id": user_id, "is_active": True}).eq("id", land['id']).execute()
                    
                    # 2. Genereer de atleten op basis van de sport_events tabel
                    events = supabase.table("sports_events").select("*").execute().data
                    atleten_lijst = []
                    for e in events:
                        for _ in range(e['min_athletes_required']):
                            atleten_lijst.append(create_atleet(land['id'], e['event_name']))
                    
                    supabase.table("athletes").insert(atleten_lijst).execute()
                    st.success(f"Gefeliciteerd! Je bent nu de manager van {gekozen_land_naam}. Ga naar het Dashboard.")
                else:
                    st.error("Vul eerst een Manager-naam in.")

    elif choice == "📊 Manager Dashboard":
        st.header("Manager Dashboard")
        # Alleen actieve landen tonen
        actieve_landen = supabase.table("countries").select("*").eq("is_active", True).execute().data
        
        if not actieve_landen:
            st.info("Er zijn nog geen actieve managers. Schrijf je eerst in via de Home pagina.")
        else:
            mijn_land_naam = st.selectbox("Bekijk dashboard van:", [l['name'] for l in actieve_landen])
            land_data = next(l for l in actieve_landen if l['name'] == mijn_land_naam)
            
            st.subheader(f"Land: {land_data['name']} (Manager: {land_data['manager_id']})")
            st.write(f"Budget: **{land_data['mp_balance']} MP**")
            
            atleten = supabase.table("athletes").select("*").eq("country_id", land_data['id']).execute().data
            
            # Tabel tonen met een extra kolom voor Special Heritage
            st.write("### Jouw Team")
            st.table(atleten)

    elif choice == "🕹️ Admin Paneel":
        pw = st.text_input("Admin Wachtwoord", type="password")
        if pw == "admin123":
            st.write("### Database Beheer")
            if st.button("⚠️ RESET GAME (Wis alle managers en atleten)"):
                supabase.table("athletes").delete().neq("id", 0).execute()
                supabase.table("countries").update({"manager_id": None, "is_active": False, "mp_balance": 1000}).neq("id", 0).execute()
                st.success("De game is gereset.")
                st.rerun()

if __name__ == '__main__':
    main()
