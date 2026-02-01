import streamlit as st
from supabase import create_client, Client
import random

# DATABASE VERBINDING
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Multi Sport Online", layout="wide")

# ADMIN CLAUSULE
ADMIN_CLAUSE = "> **ADMIN NOTITIE:** De Admin heeft altijd het laatste woord bij technische fouten of onvoorziene situaties."

# --- HELPER FUNCTIES ---
def get_all_countries():
    return supabase.table("countries").select("*").order("registration_order").execute().data

def update_mp(country_id, new_balance):
    supabase.table("countries").update({"mp_balance": new_balance}).eq("id", country_id).execute()

def update_skill(athlete_id, skill_name, new_value):
    supabase.table("athletes").update({skill_name: new_value}).eq("id", athlete_id).execute()

# --- HOOFDAPP ---
def main():
    st.sidebar.title("🏆 Multi Sport Online")
    menu = ["🏠 Home", "📊 Manager Dashboard", "📡 Scouting & Transfer", "🕹️ Admin Paneel", "📜 Reglement"]
    choice = st.sidebar.radio("Navigatie", menu)

    if choice == "🏠 Home":
        st.header("Wereldoverzicht")
        landen = get_all_countries()
        for l in landen:
            st.write(f"📍 {l['name']} | MP: **{l['mp_balance']}**")
        st.info("Welkom bij de eerste editie van de Wereldspelen!")

    elif choice == "📊 Manager Dashboard":
        landen_lijst = get_all_countries()
        land_naam = st.selectbox("Log in als Land:", [l['name'] for l in landen_lijst])
        land_data = next(item for item in landen_lijst if item["name"] == land_naam)
        
        st.title(f"Dashboard: {land_naam}")
        st.metric("Landelijk Budget", f"{land_data['mp_balance']} MP")

        # ATLETENLIJST & TRAINING
        st.subheader("Jouw Team & Training")
        atleten_res = supabase.table("athletes").select("*").eq("country_id", land_data['id']).execute()
        atleten = atleten_res.data

        if not atleten:
            st.warning("Nog geen atleten gegenereerd voor dit land.")
        else:
            # Training Sectie
            with st.expander("🏋️ Snel-Trainen (25 MP per punt)"):
                atleet_keuze = st.selectbox("Kies atleet:", [a['name'] for a in atleten])
                gekozen_atleet = next(a for a in atleten if a['name'] == atleet_keuze)
                skill_keuze = st.selectbox("Skill:", ["skill_speed", "skill_strength", "skill_stamina", "skill_technique", "skill_focus"])
                
                if st.button("Bevestig Training"):
                    if land_data['mp_balance'] >= 25:
                        new_skill_val = gekozen_atleet[skill_keuze] + 1
                        update_skill(gekozen_atleet['id'], skill_keuze, new_skill_val)
                        update_mp(land_data['id'], land_data['mp_balance'] - 25)
                        st.success(f"{atleet_keuze} is verbeterd! Nieuwe waarde: {new_skill_val}")
                        st.rerun()
                    else:
                        st.error("Onvoldoende MP!")

            st.table(atleten)

    elif choice == "🕹️ Admin Paneel":
        st.header("Admin God-Mode")
        pw = st.text_input("Wachtwoord:", type="password")
        if pw == "admin123":
            st.success("Toegang geverifieerd")
            
            tab1, tab2, tab3 = st.tabs(["Landen & Atleten", "Editie Beheer", "Strafsysteem"])
            
            with tab1:
                if st.button("Genereer Starters (15 per land)"):
                    # Logica voor genereren (zie vorige code)
                    st.write("Bezig met genereren...")
            
            with tab2:
                st.subheader("Simulatie Instellingen")
                weer = st.selectbox("Weerbericht", ["Zonnig", "Regen", "Storm", "Hittegolf"])
                bonus = st.number_input("MP Bonus voor Goud", value=100)
                if st.button("Start Simulatie Editie"):
                    st.write("De simulatie-motor wordt opgestart...")

            with tab3:
                st.subheader("Sancties")
                st.selectbox("Land om te bannen:", [l['name'] for l in get_all_countries()])
                st.button("Ban voor 4 Edities")

    elif choice == "📜 Reglement":
        st.header("Spelregels")
        st.write("Hier staan alle regels over MP, bans en inactiviteit.")
        st.markdown(ADMIN_CLAUSE)

if __name__ == '__main__':
    main()
