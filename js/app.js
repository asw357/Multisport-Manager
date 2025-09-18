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
  authMsg.textContent = text;
  authMsg.className = ok ? "ok" : "error";
}

async function updateUI(session) {
  if (!session) {
    authSection.style.display = "block";
    appSection.style.display = "none";
    logoutBtn.style.display = "none";
    adminLink.style.display = "none";
    return;
  }
  authSection.style.display = "none";
  appSection.style.display = "block";
  logoutBtn.style.display = "inline-block";

  const user = session.user;
  welcome.textContent = `Welkom, ${user.email}`;

  // Admin check via admins table (op email)
  const { data: isAdmin, error: aErr } = await supabase
    .from("admins")
    .select("email")
    .eq("email", user.email)
    .maybeSingle();
  if (aErr) console.error("Admin check error:", aErr);
  adminLink.style.display = isAdmin ? "inline-block" : "none";

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
    countryInfo.textContent = country ? country.name : `Land #${profile.country_id}`;
    claimCountryBtn.style.display = "none";
  } else {
    countryInfo.textContent = "Nog geen land gekoppeld.";
    claimCountryBtn.style.display = "inline-block";
  }

  // Demo: toon edities
  const { data: eds, error: edErr } = await supabase
    .from("editions")
    .select("*")
    .order("start_datum", { ascending: true });

  editionsList.innerHTML = "";
  if (edErr) {
    console.error("Editions error:", edErr);
  } else if (eds) {
    eds.forEach(e => {
      const li = document.createElement("li");
      li.textContent = `${e.type}editie ${e.nummer} – ${e.locatie} (${e.jaar_fictief})`;
      editionsList.appendChild(li);
    });
  }
}

// Inloggen
authForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  authMsg.textContent = "";
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

// Registreren (email+password)
registerBtn.addEventListener("click", async () => {
  authMsg.textContent = "";
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  const { data, error } = await supabase.auth.signUp({ email, password });
  if (error) {
    console.error("SignUp error:", error);
    setMsg(error.message || "Registratie mislukt.");
  } else {
    setMsg("Registratie gestart — check je e-mail om te bevestigen.", true);
  }
});

// Magic link (handig om snel te testen)
magicBtn.addEventListener("click", async () => {
  authMsg.textContent = "";
  const email = document.getElementById("email").value.trim();
  if (!email) {
    setMsg("Vul een e-mail in om een magic link te sturen.");
    return;
  }
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: window.location.href // terug naar deze pagina
    }
  });
  if (error) {
    console.error("Magic link error:", error);
    setMsg(error.message || "Magic link verzenden mislukt.");
  } else {
    setMsg("Magic link verzonden — check je e-mail.", true);
  }
});

// Uitloggen
logoutBtn.addEventListener("click", async () => {
  await supabase.auth.signOut();
  await updateUI(null);
});

// Claim land via RPC
claimCountryBtn.addEventListener("click", async () => {
  const { data, error } = await supabase.rpc("claim_country");
  if (error) {
    console.error("claim_country error:", error);
    alert(error.message || "Claimen mislukt.");
    return;
  }
  countryInfo.textContent = data?.name ?? "Land toegekend";
  claimCountryBtn.style.display = "none";
});

// Sessiewijzigingen volgen
supabase.auth.onAuthStateChange((_event, session) => updateUI(session));

// Init
const { data: { session } } = await supabase.auth.getSession();
updateUI(session);
