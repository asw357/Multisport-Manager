# Multisport Manager — Setup

## 1) Supabase
- Maak project aan en noteer **Project URL** + **Anon/Public Key**.
- Ga naar **Authentication → Email**:
  - Zet **Email/Password** aan.
  - (Optioneel) Zet **Email confirmations** uit om direct te kunnen inloggen.
  - Voeg je **Site URL / Redirect URL** toe (bijv. `https://<user>.github.io/multisport-manager/`).
- SQL Editor → voer `schema.sql` uit.

## 2) GitHub Pages
- Repo aanmaken, zet deze files in de root:
  - `index.html`, `admin.html`
  - `js/supabaseClient.js`, `js/app.js`, `js/admin.js`
  - `styles.css`, `404.html`, `.nojekyll`
  - `README.md`
- **Settings → Pages**: Deploy from `main` / root.

## 3) Config JS client
- In `js/supabaseClient.js`: vul jouw `SUPABASE_URL` en `ANON_KEY`.
- Test `index.html` via de Pages URL (niet via `file://`).

## 4) Admin
- Login/registreer met `wilcoboesveld12@hotmail.com`. Je ziet de **Admin**-link.
- In **Admin**:
  - `Landen (bulk toevoegen)` → één land per regel → **Toevoegen**.
  - `Sporten / Disciplines / Onderdelen` → bouw je sportendatabase op.
  - `Editie aanmaken` → jaar is niet nodig; data optioneel.
  - `Events koppelen aan editie`.

## 5) Speler
- Login met een spelersaccount → **Claim mijn land** (via RPC).
- Zie edities en koppelingen.

## Notities
- RLS staat aan (read openbaar; writes via admin-e-mail).
- `claim_country()` claimt atomair een vrij land.
- Je kunt later MP/tabellen, recordlogica en simulaties toevoegen.
