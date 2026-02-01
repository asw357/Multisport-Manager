import streamlit as st
from supabase import create_client, Client
import random

# Verbinding met de database
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Multi Sport Online", layout="wide")

# UITGEBREIDERE NAMENLIJST (Voor meer variatie)
FIRST_NAMES = ["Lars", "Sanne", "Thijs", "Aniek", "Bram", "Jack", "Emma", "Marek", "Elena", "Jean", "Pierre", "Hans", "Ingrid", "Luca", "Sophie", "Boris", "Nina"]
LAST_NAMES = ["de Jong", "Jansen", "Meijer", "Bakker", "Smit", "Thompson", "Müller", "Dubois", "Petrov", "Novak", "Garcia", "Silva", "Ferrari"]

def get_countries():
    response = supabase.table("countries").select("*").order("registration_order").execute()
    return response.data

def generate_athletes(country_id, amount=15):
    athletes_to_add = []
    for _ in range(amount):
        new_athlete = {
            "country_id": country_id,
            "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "gender": random.choice(["Man", "Vrouw"]), # FIX: Mman is nu Man
            "skill_speed": random.randint(50, 70),
            "skill_strength": random.randint(50, 70),
            "skill_stamina": random.randint(50, 70),
            "skill_technique": random.randint(50, 70),
            "skill_focus": random.randint(50, 70)
        }
        athletes_to_add.append(new_athlete)
    
    supabase.table("athletes").insert(athletes_to_add).execute()

def main():
    st.title("🏆 Multi Sport Online")
    
    menu = ["Home", "Manager Dashboard", "Admin Paneel", "Reglement"]
    choice = st.sidebar.selectbox("Ga naar:", menu)

    if choice == "Home":
        st.subheader("Landen Overzicht")
        landen = get_countries()
        col1, col2 = st.columns(2)
        for i, l in enumerate(landen):
            with (col1 if i % 2 == 0 else col2):
                st.info(f"**{l['name']}** | MP: {l['mp_balance']}")

    elif choice == "Manager Dashboard":
        st.header("Manager Dashboard")
        landen_lijst = get_countries()
        land_naam = st.selectbox("Kies je land:", [l['name'] for l in landen_lijst])
        
        # Haal data op
        land_data = next(item for item in landen_lijst if item["name"] == land_naam)
        atleten = supabase.table("athletes").select("*").eq("country_id", land_data['id']).execute()
        
        if not atleten.data:
            st.warning("Er zijn nog geen atleten voor dit land.")
        else:
            st.write(f"### Atleten van {land_naam}")
            # We maken de tabel mooier door de ID-kolommen te verbergen
            display_df = []
            for a in atleten.data:
                display_df.append({
                    "Naam": a['name'],
                    "Geslacht": a['gender'],
                    "Snelheid": a['skill_speed'],
                    "Kracht": a['skill_strength'],
                    "Uithouding": a['skill_stamina'],
                    "Techniek": a['skill_technique'],
                    "Focus": a['skill_focus']
                })
            st.table(display_df)

    elif choice == "Admin Paneel":
        st.header("🕹️ Admin Paneel")
        pw = st.text_input("Wachtwoord:", type="password")
        if pw == "admin123":
            st.success("Toegang verleend")
            
            # Knoppen voor Admin acties
            if st.button("🚀 Genereer Starters voor nieuwe landen"):
                landen = get_countries()
                for l in landen:
                    check = supabase.table("athletes").select("id").eq("country_id", l['id']).execute()
                    if not check.data:
                        generate_athletes(l['id'])
                        st.write(f"✅ Atleten gemaakt voor {l['name']}")
                st.balloons()
            
            if st.button("🗑️ Reset alle atleten (LET OP!)"):
                # Voor jou om te testen: dit gooit de atleten tabel leeg
                supabase.table("athletes").delete().neq("id", 0).execute()
                st.warning("Alle atleten zijn verwijderd uit de database.")

    elif choice == "Reglement":
        st.header("📜 Reglement")
        st.markdown("> **ADMIN NOTITIE:** De Admin heeft altijd het laatste woord bij technische fouten of onvoorziene situaties.")

if __name__ == '__main__':
    main()
