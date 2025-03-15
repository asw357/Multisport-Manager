const express = require('express');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(cors());

// Functie om JSON-bestanden te lezen
function readData(file) {
    try {
        return JSON.parse(fs.readFileSync(`./backend/data/${file}.json`, 'utf8'));
    } catch (error) {
        return [];
    }
}

// Functie om JSON-bestanden te schrijven
function writeData(file, data) {
    fs.writeFileSync(`./backend/data/${file}.json`, JSON.stringify(data, null, 2));
}

// API om te controleren of de server werkt
app.get('/', (req, res) => {
    res.send('Server is actief!');
});

// API om edities op te halen
app.get('/editions', (req, res) => {
    console.log("Edities opvragen...");
    res.json(readData('editions'));
});

// API om een nieuwe editie toe te voegen
app.post('/editions', (req, res) => {
    let editions = readData('editions');
    const newEdition = { id: editions.length + 1, name: req.body.name };
    editions.push(newEdition);
    writeData('editions', editions);
    res.status(201).json(newEdition);
});

// API om alle wedstrijden voor een editie op te halen
app.get('/schedule/:editionId', (req, res) => {
    let schedules = readData('schedule');
    let editionSchedule = schedules.filter(match => match.editionId == req.params.editionId);
    res.json(editionSchedule);
});

// API om een wedstrijd toe te voegen aan een editie
app.post('/schedule/:editionId', (req, res) => {
    let schedules = readData('schedule');
    const newMatch = {
        id: schedules.length + 1,
        editionId: parseInt(req.params.editionId),
        day: req.body.day,
        time: req.body.time,
        sport: req.body.sport,
        event: req.body.event,
        location: req.body.location
    };
    schedules.push(newMatch);
    writeData('schedule', schedules);
    res.status(201).json(newMatch);
});

// API om een wedstrijd te verwijderen
app.delete('/schedule/:matchId', (req, res) => {
    let schedules = readData('schedule');
    schedules = schedules.filter(match => match.id != req.params.matchId);
    writeData('schedule', schedules);
    res.json({ message: 'Wedstrijd verwijderd' });
});

// API om alle data te resetten
app.post('/reset', (req, res) => {
    writeData('users', []);
    writeData('athletes', []);
    writeData('results', []);
    writeData('mp', []);
    writeData('editions', []);
    writeData('schedule', []);
    res.json({ message: 'Alle data is gereset!' });
});

// Start de server en log de Replit URL
app.listen(PORT, () => {
    console.log(`Server draait op https://your-project.replit.app`);
});
