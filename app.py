import streamlit as st
from supabase import create_client, Client
import random

# Verbinding met de database
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Multi Sport Online", layout="wide")

# LIJSTEN VOOR RANDOM NAMEN (Skelet versie, breiden we later uit)
FIRST_NAMES = ["Lars", "Sanne", "Thijs", "Aniek", "Bram", "Jack", "Emma", "Marek", "Elena", "Jean", "Pierre", "Hans", "Ingrid"]
LAST_NAMES = ["de Jong", "Jansen", "Meijer", "Bakker", "Smit", "Thompson", "Müller", "Dubois", "Petrov", "Novak"]

def get_countries():
    response = supabase.table("countries").select("*").order("registration_order").execute()
    return response.data

def generate_athletes(country_id, amount=15):
    athletes_to_add = []
    for _ in range(amount):
        new_athlete = {
            "country_id": country_id,
            "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "gender": random.choice(["Mman", "Vrouw"]),
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
        for l in landen:
            st.write(f"- {l['name']} (MP: {l['mp_balance']})")

    elif choice == "Manager Dashboard":
        st.header("Manager Dashboard")
        land_naam = st.selectbox("Kies je land:", [l['name'] for l in get_countries()])
        
        # Haal de atleten op voor dit land
        land_data = supabase.table("countries").select("id").eq("name", land_naam).single().execute()
        atleten = supabase.table("athletes").select("*").eq("country_id", land_data.data['id']).execute()
        
        if not atleten.data:
            st.warning("Er zijn nog geen atleten voor dit land. Vraag de Admin om ze te genereren.")
        else:
            st.write(f"### Atleten van {land_naam}")
            st.table(atleten.data)

    elif choice == "Admin Paneel":
        st.header("🕹️ Admin Paneel")
        pw = st.text_input("Wachtwoord:", type="password")
        if pw == "admin123":
            st.success("Toegang verleend")
            
            if st.button("🚀 Genereer 15 Starters voor alle landen"):
                landen = get_countries()
                for l in landen:
                    # Check of ze al atleten hebben (om dubbelen te voorkomen)
                    check = supabase.table("athletes").select("id").eq("country_id", l['id']).execute()
                    if not check.data:
                        generate_athletes(l['id'])
                        st.write(f"✅ Atleten gemaakt voor {l['name']}")
                    else:
                        st.write(f"ℹ️ {l['name']} heeft al atleten.")
                st.balloons()

    elif choice == "Reglement":
        st.header("📜 Reglement")
        st.write("De Admin heeft altijd het laatste woord.")

if __name__ == '__main__':
    main()
