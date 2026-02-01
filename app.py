import streamlit as st
from supabase import create_client, Client
import random

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Multi Sport Online", layout="wide")

# --- GENERATOR LOGICA ---
def create_atleet(country_id, event_name):
    # Bepaal leeftijd op basis van onderdeel
    if "leraren" in event_name.lower() or "matrozen" in event_name.lower():
        age = random.randint(30, 45)
        # Leraren hebben vaak meer techniek en focus, minder snelheid
        skills = {
            "speed": random.randint(40, 60),
            "strength": random.randint(50, 70),
            "stamina": random.randint(50, 70),
            "technique": random.randint(65, 85),
            "focus": random.randint(70, 90)
        }
    else:
        age = random.randint(18, 25)
        skills = {k: random.randint(50, 70) for k in ["speed", "strength", "stamina", "technique", "focus"]}

    return {
        "country_id": country_id,
        "name": f"{random.choice(['Lars', 'Sanne', 'Thijs', 'Marek', 'Pierre'])} {random.choice(['Jansen', 'Smit', 'Müller', 'Dubois'])}",
        "gender": "Man", # Op basis van jouw lijst voor Editie 1
        "age": age,
        "skill_speed": skills["speed"],
        "skill_strength": skills["strength"],
        "skill_stamina": skills["stamina"],
        "skill_technique": skills["technique"],
        "skill_focus": skills["focus"]
    }

# --- UI ---
def main():
    st.sidebar.title("🏆 Multi Sport Online")
    choice = st.sidebar.radio("Menu", ["Home", "Manager Dashboard", "Admin Paneel"])

    if choice == "Home":
        st.header("Welkom bij de Wereldspelen")
        st.write("Kies een land in het Dashboard om te beginnen.")

    elif choice == "Manager Dashboard":
        landen = supabase.table("countries").select("*").execute().data
        land_naam = st.selectbox("Selecteer Land:", [l['name'] for l in landen])
        land = next(l for l in landen if l['name'] == land_naam)

        atleten = supabase.table("athletes").select("*").eq("country_id", land['id']).execute().data
        
        if not atleten:
            st.warning(f"Welkom Manager van {land_naam}! Je hebt nog geen actieve atleten.")
            if st.button("Claim Start-selectie voor Editie 1"):
                events = supabase.table("sports_events").select("*").execute().data
                nieuwe_atleten = []
                for e in events:
                    for _ in range(e['min_athletes_required']):
                        nieuwe_atleten.append(create_atleet(land['id'], e['event_name']))
                
                supabase.table("athletes").insert(nieuwe_atleten).execute()
                st.success("Je atleten zijn gearriveerd! Ververs de pagina.")
                st.rerun()
        else:
            st.subheader(f"Team {land_naam}")
            st.write(f"Budget: {land['mp_balance']} MP")
            st.table(atleten)

    elif choice == "Admin Paneel":
        pw = st.text_input("Wachtwoord", type="password")
        if pw == "admin123":
            st.write("### Beheer Onderdelen")
            # Hier kun je later onderdelen toevoegen/verwijderen
            if st.button("Reset alle data (Testen)"):
                supabase.table("athletes").delete().neq("id", 0).execute()
                st.rerun()

if __name__ == '__main__':
    main()
