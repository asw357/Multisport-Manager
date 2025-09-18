// /js/app.js
import { supabase } from "./supabaseClient.js";

const authSection = document.getElementById("authSection");
const appSection = document.getElementById("appSection");
const authForm = document.getElementById("authForm");
const registerBtn = document.getElementById("registerBtn");
const magicBtn = document.getElementById("magicBtn");
const authMsg = document.getElementById("authMsg");
const logoutBtn = document.getElementById("logoutBtn");
const welcome = document.getElementById("welcome");
const adminLink = document.getElementById("adminLink");

const countryInfo = document.getElementById("countryInfo");
const claimCountryBtn = document.getElementById("claimCountryBtn");
const editionsList = document.getElementById("editionsList");

function setMsg(text, ok = false) {
  if (!authMsg) return;
  authMsg.textContent = text;
  authMsg.className = ok ? "ok" : "error";
}

async function isAdminRPC() {
  // Gebruik de serverfunctie i.p.v. SELECT op de admins-tabel
  const { data, error } = await supabase.rpc("is_current_user_admin");
  if (error) {
    console.warn("Admin RPC error:", error);
    return false;
  }
  return !!data;
}

async function updateUI(session) {
  if (!session) {
    authSection?.style && (authSection.style.display = "block");
    appSection?.style && (appSection.style.display = "none");
    logoutBtn?.style && (logoutBtn.style.display = "none");
    adminLink?.style && (adminLink.style.display = "none");
    return;
  }

  authSection?.style && (authSection.style.display = "none");
  appSection?.style && (appSection.style.display = "block");
  logoutBtn?.style && (logoutBtn.style.display = "inline-block");

  const user = session.user;
  if (welcome) welcome.textContent = `Welkom, ${user.email}`;

  // 🔐 Betrouwbare admin-check
  const isAdmin = await isAdminRPC();
  if (adminLink) adminLink.style.display = isAdmin ? "inline-block" : "none";

  // Profiel + land
  const { data: profile, error: pErr } = await supabase
    .from("profiles")
    .select("country_id")
    .eq("id", user.id)
    .maybeSingle();
  if (pErr) console.error("Profile fetch error:", pErr);

  if (profile?.country_id) {
    const { data: country, error: cErr } = await supabase
      .from("countries")
      .select("name")
      .eq("id", profile.country_id)
      .maybeSingle();
    if (cErr) console.error("Country fetch error:", cErr);
    if (countryInfo) countryInfo.textContent = country ? country.name : `Land #${profile.country_id}`;
    if (claimCountryBtn) claimCountryBtn.style.display = "none";
  } else {
    if (countryInfo) countryInfo.textContent = "Nog geen land gekoppeld.";
    if (claimCountryBtn) claimCountryBtn.style.display = "inline-block";
  }

  // Edities tonen
  const { data: eds, error: edErr } = await supabase
    .from("editions")
    .select("*")
    .order("editie_id", { ascending: true });

  if (editionsList) editionsList.innerHTML = "";
  if (edErr) {
    console.error("Editions error:", edErr);
  } else if (eds && editionsList) {
    eds.forEach(e => {
      const li = document.createElement("li");
      let text = `${e.type}editie ${e.nummer} – ${e.locatie}`;
      if (e.start_datum || e.eind_datum) {
        const s = e.start_datum ?? "?";
        const t = e.eind_datum ?? "?";
        text += ` (${s} – ${t})`;
      }
      li.textContent = text;
      editionsList.appendChild(li);
    });
  }
}

// Inloggen
if (authForm) {
  authForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    setMsg("", true);
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      console.error("Login error:", error);
      setMsg(error.message || "Inloggen mislukt.");
    } else {
      setMsg("Ingelogd.", true);
      await updateUI(data.session);
    }
  });
}

// Registreren
if (registerBtn) {
  registerBtn.addEventListener("click", async () => {
    setMsg("", true);
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    const { error } = await supabase.auth.signUp({ email, password });
    if (error) {
      console.error("SignUp error:", error);
      setMsg(error.message || "Registratie mislukt.");
    } else {
      setMsg("Registratie gestart — check je e-mail om te bevestigen.", true);
    }
  });
}

// Magic link
if (magicBtn) {
  magicBtn.addEventListener("click", async () => {
    setMsg("", true);
    const email = document.getElementById("email").value.trim();
    if (!email) {
      setMsg("Vul een e-mail in om een magic link te sturen.");
      return;
    }
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: window.location.href }
    });
    if (error) {
      console.error("Magic link error:", error);
      setMsg(error.message || "Magic link verzenden mislukt.");
    } else {
      setMsg("Magic link verzonden — check je e-mail.", true);
    }
  });
}

// Uitloggen
if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    await supabase.auth.signOut();
    await updateUI(null);
  });
}

// Claim land via RPC
if (claimCountryBtn) {
  claimCountryBtn.addEventListener("click", async () => {
    const { data, error } = await supabase.rpc("claim_country");
    if (error) {
      console.error("claim_country error:", error);
      alert(error.message || "Claimen mislukt. Tip: voeg eerst landen toe als admin.");
      return;
    }
    if (countryInfo) countryInfo.textContent = data?.name ?? "Land toegekend";
    claimCountryBtn.style.display = "none";
  });
}

// Sessiewijzigingen volgen
supabase.auth.onAuthStateChange((_event, session) => updateUI(session));

// Init
const { data: { session } } = await supabase.auth.getSession();
updateUI(session);
