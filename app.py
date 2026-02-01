import streamlit as st
import random

# CONFIGURATIE & ADMIN CLAUSULE
st.set_page_config(page_title="Multi Sport Online", layout="wide")

# NOODCLAUSULE (Zoals afgesproken)
admin_note = "> **ADMIN NOTITIE:** De Admin heeft altijd het laatste woord bij technische fouten of onvoorziene situaties."

def main():
    st.title("🏆 Multi Sport Online")
    
    # SIDEBAR: Navigatie
    menu = ["Home", "Manager Dashboard", "Admin Paneel", "Reglement"]
    choice = st.sidebar.selectbox("Ga naar:", menu)

    if choice == "Home":
        st.subheader("Welkom bij de ultieme sport-simulatie")
        st.write("Kies je land, train je atleten en word de grootste sportnatie ter wereld.")
        st.info("De inschrijvingen voor Editie 1 zijn geopend!")

    elif choice == "Manager Dashboard":
        st.header("Manager Dashboard")
        land = st.text_input("Voer je landnaam in om in te loggen:")
        if land:
            st.success(f"Welkom Manager van {land}!")
            # Hier komen de atletenlijst en training-knoppen
            st.write("### Jouw Atleten")
            st.warning("De Admin moet de starters-atleten nog genereren voor dit land.")

    elif choice == "Admin Paneel":
        st.header("🕹️ Admin God-Mode")
        st.markdown(admin_note)
        
        password = st.text_input("Admin Wachtwoord:", type="password")
        if password == "admin123": # Verander dit later!
            st.write("### Controlekamer")
            if st.button("Genereer Starters-atleten voor actieve landen"):
                st.write("Bezig met genereren van 15 atleten per land...")
                # Hier komt de logica voor de random skills
            
            st.write("### MP & Bonus Beheer")
            goud_mp = st.number_input("MP voor Goud:", value=100)
            
            st.write("### Parcours & Weer")
            weer = st.selectbox("Huidig Weer:", ["Zonnig", "Bewolkt", "Regen"])

    elif choice == "Reglement":
        st.header("📜 Officiële Spelregels")
        st.write("""
        1. **Inschrijving:** Landen worden toegewezen op volgorde van aanmelding.
        2. **Gedrag:** Bij overtredingen kan de Admin MP-boetes of bans uitdelen.
        3. **Afwezigheid:** Na 14 dagen inactiviteit wordt een land vrijgegeven.
        4. **Bans:** Een ban duurt 4 volledige Edities.
        """)
        st.markdown(admin_note)

if __name__ == '__main__':
    main()
