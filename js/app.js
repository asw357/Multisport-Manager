import { supabase } from "./supabaseClient.js";

const authSection = document.getElementById("authSection");
const appSection = document.getElementById("appSection");
const authForm = document.getElementById("authForm");
const registerBtn = document.getElementById("registerBtn");
const authMsg = document.getElementById("authMsg");
const logoutBtn = document.getElementById("logoutBtn");
const welcome = document.getElementById("welcome");
const adminLink = document.getElementById("adminLink");

const countryInfo = document.getElementById("countryInfo");
const claimCountryBtn = document.getElementById("claimCountryBtn");
const editionsList = document.getElementById("editionsList");

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
  const { data: isAdmin } = await supabase
    .from("admins")
    .select("email")
    .eq("email", user.email)
    .maybeSingle();

  if (isAdmin) adminLink.style.display = "inline-block";
  else adminLink.style.display = "none";

  // Profiel + land
  const { data: profile } = await supabase
    .from("profiles")
    .select("country_id")
    .eq("id", user.id)
    .maybeSingle();

  if (profile?.country_id) {
    const { data: country } = await supabase
      .from("countries")
      .select("name")
      .eq("id", profile.country_id)
      .maybeSingle();
    countryInfo.textContent = country ? country.name : `Land #${profile.country_id}`;
    claimCountryBtn.style.display = "none";
  } else {
    countryInfo.textContent = "Nog geen land gekoppeld.";
    claimCountryBtn.style.display = "inline-block";
  }

  // Kleine demo: toon edities
  const { data: eds, error: edErr } = await supabase
    .from("editions")
    .select("*")
    .order("start_datum", { ascending: true });

  editionsList.innerHTML = "";
  if (!edErr && eds) {
    eds.forEach(e => {
      const li = document.createElement("li");
      li.textContent = `${e.type}editie ${e.nummer} – ${e.locatie} (${e.jaar_fictief})`;
      editionsList.appendChild(li);
    });
  }
}

authForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  authMsg.textContent = "";
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) {
    authMsg.textContent = error.message;
  } else {
    await updateUI(data.session);
  }
});

registerBtn.addEventListener("click", async () => {
  authMsg.textContent = "";
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  const { data, error } = await supabase.auth.signUp({ email, password });
  authMsg.textContent = error ? error.message : "Check je e-mail om te bevestigen.";
});

logoutBtn.addEventListener("click", async () => {
  await supabase.auth.signOut();
  await updateUI(null);
});

// Claim land via RPC
claimCountryBtn.addEventListener("click", async () => {
  const { data, error } = await supabase.rpc("claim_country");
  if (error) {
    alert(error.message);
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
