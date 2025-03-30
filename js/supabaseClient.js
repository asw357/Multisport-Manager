// supabaseClient.js
const SUPABASE_URL = 'https://aqfgikfyymvigvexwhgp.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxZmdpa2Z5eW12aWd2ZXh3aGdwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMyNzM4MDcsImV4cCI6MjA1ODg0OTgwN30.YWeUkkpnpA19GU1Jpjebc6vGdoaIDSX7C6UQZW3ZTAA';

const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Zorg dat 'supabase' beschikbaar is in andere bestanden
window.supabase = supabaseClient;
