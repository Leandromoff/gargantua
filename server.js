const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { exec } = require('child_process');
const express = require('express');
const session = require('express-session');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.use(session({
  secret: 'gargantua-secret',
  resave: false,
  saveUninitialized: false
}));

const USERS_FILE = path.join(__dirname, 'users.json');

function loadUsers() {
  const data = fs.readFileSync(USERS_FILE, 'utf-8');
  return JSON.parse(data);
}

function checkPassword(rawPassword, storedHash) {
  const parts = storedHash.split('$');
  if (parts.length !== 4) return false;
  const iterations = parseInt(parts[1], 10);
  const salt = parts[2];
  const hash = parts[3];
  const derived = crypto.pbkdf2Sync(rawPassword, salt, iterations, 32, 'sha256').toString('base64');
  return derived === hash;
}

function requireAuth(req, res, next) {
  if (req.session && req.session.user) {
    return next();
  }
  res.redirect('/login');
}

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const users = loadUsers();
  const user = users[username];
  if (user && checkPassword(password, user.password_hash)) {
    req.session.user = { username };
    return res.redirect('/dashboard');
  }
  res.send('Invalid credentials');
});

app.get('/logout', (req, res) => {
  req.session.destroy(() => {
    res.redirect('/login');
  });
});

app.get('/dashboard', requireAuth, (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

app.get('/api/user', requireAuth, (req, res) => {
  res.json({ username: req.session.user.username });
});

app.post('/api/ping', requireAuth, (req, res) => {
  const host = (req.body.host || '').trim();
  const count = req.body.count || '4';
  if (!host) return res.json({ success: false, error: 'Host requerido' });
  const cmd = `ping -c ${count} ${host}`;
  exec(cmd, { timeout: 30000 }, (err, stdout, stderr) => {
    if (err) {
      return res.json({ success: false, error: stderr || err.message });
    }
    res.json({ success: true, output: stdout });
  });
});

app.post('/api/traceroute', requireAuth, (req, res) => {
  const host = (req.body.host || '').trim();
  if (!host) return res.json({ success: false, error: 'Host requerido' });
  const cmd = `traceroute ${host}`;
  exec(cmd, { timeout: 60000 }, (err, stdout, stderr) => {
    if (err) {
      return res.json({ success: false, error: stderr || err.message });
    }
    res.json({ success: true, output: stdout });
  });
});

// TODO: implementar endpoints restantes (port scanner, nmap, dns lookup, etc.)

app.use(express.static(path.join(__dirname, 'public')));

app.listen(PORT, () => {
  console.log(`Gargantua Node server running on port ${PORT}`);
});
