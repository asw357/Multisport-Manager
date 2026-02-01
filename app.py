import streamlit as st
from supabase import create_client, Client

# Verbinding maken met Supabase (De Kluis)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Multi Sport Online", layout="wide")

def get_countries():
    # Haal de landen op uit de database
    response = supabase.table("countries").select("*").order("registration_order").execute()
    return response.data

def main():
    st.title("🏆 Multi Sport Online")
    
    menu = ["Home", "Manager Dashboard", "Admin Paneel", "Reglement"]
    choice = st.sidebar.selectbox("Ga naar:", menu)

    if choice == "Home":
        st.subheader("Welkom bij de ultieme sport-simulatie")
        st.write("Deelnemende landen in Editie 1:")
        
        # Laat de landen uit de database zien
        landen = get_countries()
        for l in landen:
            st.write(f"- {l['name']} (MP: **{l['mp_balance']}**)")

    elif choice == "Admin Paneel":
        st.header("🕹️ Admin Paneel")
        pw = st.text_input("Wachtwoord:", type="password")
        if pw == "admin123":
            st.success("Ingelogd als Admin")
            # Hier voegen we later de knoppen toe voor atleten genereren

    elif choice == "Reglement":
        st.header("📜 Reglement")
        st.write("1. Geen transfers. 2. 4 edities ban bij overtreding.")

if __name__ == '__main__':
    main()
