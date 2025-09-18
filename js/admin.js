// /js/admin.js
import { supabase } from "./supabaseClient.js";

const guard = document.getElementById("guard");
const panel = document.getElementById("adminPanel");
const logoutBtn = document.getElementById("logoutBtn");

// Access guard
async function ensureAdmin() {
  const { data: { session } } = await supabase.auth.getSession();
  if (!session) {
    guard.innerHTML = `<p>Je bent niet ingelogd. <a href="index.html">Terug naar login</a></p>`;
    return false;
  }
  const user = session.user;

  // Admin check
  const { data: isAdmin, error } = await supabase
    .from("admins")
    .select("email")
    .eq("email", user.email)
    .maybeSingle();

  if (error) console.error("Admin check error:", error);

  if (!isAdmin) {
    guard.innerHTML = `<p>Geen toegang. <a href="index.html">Terug</a></p>`;
    return false;
  }

  guard.style.display = "none";
  panel.style.display = "block";
  return true;
}

logoutBtn.addEventListener("click", async () => {
  await supabase.auth.signOut();
  window.location.href = "index.html";
});

// Countries bulk add
const countriesText = document.getElementById("countriesText");
const countriesMsg = document.getElementById("countriesMsg");
document.getElementById("addCountriesBtn").addEventListener("click", async () => {
  const lines = countriesText.value.split("\n")
    .map(s => s.trim())
    .filter(s => s.length > 0);

  if (lines.length === 0) {
    countriesMsg.textContent = "Geen landen gevonden.";
    return;
  }

  const payload = lines.map(name => ({ name }));
  const { error } = await supabase
    .from("countries")
    .upsert(payload, { onConflict: "name", ignoreDuplicates: true });

  countriesMsg.textContent = error ? error.message : `Toegevoegd/overgeslagen: ${payload.length} records.`;
});

// Sports
document.getElementById("addSportBtn").addEventListener("click", async () => {
  const naam = document.getElementById("sportName").value.trim();
  const categorie = document.getElementById("sportSeason").value;
  const records_toepasbaar = document.getElementById("sportRecords").checked;

  if (!naam) return;

  const { error } = await supabase.from("sports").insert([{ naam, categorie, records_toepasbaar }]);
  document.getElementById("sportMsg").textContent = error ? error.message : "Sport opgeslagen.";
});

// Disciplines
document.getElementById("addDisciplineBtn").addEventListener("click", async () => {
  const sport_id = Number(document.getElementById("disciplineSportId").value);
  const naam = document.getElementById("disciplineName").value.trim();
  if (!sport_id || !naam) return;

  const { error } = await supabase.from("disciplines").insert([{ sport_id, naam }]);
  document.getElementById("disciplineMsg").textContent = error ? error.message : "Discipline opgeslagen.";
});

// Events
document.getElementById("addEventBtn").addEventListener("click", async () => {
  const discipline_id = Number(document.getElementById("eventDisciplineId").value);
  const naam = document.getElementById("eventName").value.trim();
  const geslacht = document.getElementById("eventGender").value;
  const formaat = document.getElementById("eventFormat").value.trim() || null;
  const record_type = document.getElementById("eventRecordType").value.trim() || "MR/NR/PR/CR";

  if (!discipline_id || !naam) return;

  const { error } = await supabase.from("events").insert([{ discipline_id, naam, geslacht, formaat, record_type }]);
  document.getElementById("eventMsg").textContent = error ? error.message : "Event opgeslagen.";
});

// Editions
document.getElementById("createEditionBtn").addEventListener("click", async () => {
  const type = document.getElementById("edType").value;
  const nummer = Number(document.getElementById("edNum").value);
  const locatie = document.getElementById("edLoc").value.trim();
  const jaar_fictief = Number(document.getElementById("edYear").value);
  const start_datum = document.getElementById("edStart").value;
  const eind_datum = document.getElementById("edEnd").value;

  const { error } = await supabase.from("editions").insert([
    { type, nummer, locatie, jaar_fictief, start_datum, eind_datum }
  ]);

  document.getElementById("editionMsg").textContent = error ? error.message : "Editie aangemaakt.";
});

// Link events to edition
document.getElementById("linkEventBtn").addEventListener("click", async () => {
  const editie_id = Number(document.getElementById("linkEdId").value);
  const event_id = Number(document.getElementById("linkEventId").value);
  const max_atleten_per_land = Number(document.getElementById("linkMax").value);
  const doorstroming = document.getElementById("linkFlow").value.trim() || null;

  const { error } = await supabase.from("editions_events").insert([
    { editie_id, event_id, max_atleten_per_land, doorstroming }
  ]);

  document.getElementById("linkMsg").textContent = error ? error.message : "Event gekoppeld.";
});

ensureAdmin();
