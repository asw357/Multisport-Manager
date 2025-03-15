const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(cors());

// Functie om JSON-bestanden te lezen
function readData(file) {
    return JSON.parse(fs.readFileSync(`./backend/data/${file}.json`, 'utf8'));
}

// Functie om JSON-bestanden te schrijven
function writeData(file, data) {
    fs.writeFileSync(`./backend/data/${file}.json`, JSON.stringify(data, null, 2));
}

// API om gebruikers te laden
app.get('/users', (req, res) => {
    res.json(readData('users'));
});

// API om atleten te laden
app.get('/athletes', (req, res) => {
    res.json(readData('athletes'));
});

// API om resultaten te laden
app.get('/results', (req, res) => {
    res.json(readData('results'));
});

// API om medal points te laden
app.get('/mp', (req, res) => {
    res.json(readData('mp'));
});

// API om landen te laden
app.get('/countries', (req, res) => {
    res.json(readData('countries'));
});

// API om een nieuwe gebruiker toe te voegen
app.post('/users', (req, res) => {
    let users = readData('users');
    users.push(req.body);
    writeData('users', users);
    res.status(201).json({ message: 'Gebruiker toegevoegd' });
});

// API om een atleet bij te werken
app.put('/athletes/:id', (req, res) => {
    let athletes = readData('athletes');
    let index = athletes.findIndex(a => a.id === req.params.id);
    if (index !== -1) {
        athletes[index] = req.body;
        writeData('athletes', athletes);
        res.json({ message: 'Atleet bijgewerkt' });
    } else {
        res.status(404).json({ error: 'Atleet niet gevonden' });
    }
});

// API om een wedstrijdresultaat toe te voegen
app.post('/results', (req, res) => {
    let results = readData('results');
    results.push(req.body);
    writeData('results', results);
    res.status(201).json({ message: 'Resultaat toegevoegd' });
});

// API om medal points bij te werken
app.put('/mp/:userId', (req, res) => {
    let mp = readData('mp');
    let index = mp.findIndex(m => m.userId === req.params.userId);
    if (index !== -1) {
        mp[index].points = req.body.points;
        writeData('mp', mp);
        res.json({ message: 'Medal Points bijgewerkt' });
    } else {
        res.status(404).json({ error: 'Gebruiker niet gevonden' });
    }
});

// API om alle data te resetten
app.post('/reset', (req, res) => {
    writeData('users', []);
    writeData('athletes', []);
    writeData('results', []);
    writeData('mp', []);
    res.json({ message: 'Alle data is gereset!' });
});

app.listen(PORT, () => {
    console.log(`Server draait op http://localhost:${PORT}`);
});
