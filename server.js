// Node server (Node 22+): static files, SQLite JSON API, and enquiry email
const http = require('http'), fs = require('fs'), path = require('path');
const { DatabaseSync } = require('node:sqlite');
const envFile = path.join(__dirname, '.env');
if (fs.existsSync(envFile)) process.loadEnvFile(envFile);
const enquiryEmail = 'mohamedanas7408@gmail.com';
const gmailUser = process.env.GMAIL_USER || enquiryEmail;
const gmailPassword = process.env.GMAIL_APP_PASSWORD?.replace(/\s/g, '');
const mailer = gmailPassword ? require('nodemailer').createTransport({
  service: 'gmail',
  auth: { user: gmailUser, pass: gmailPassword },
  connectionTimeout: 10000,
  socketTimeout: 15000
}) : null;
if (!mailer) console.warn('Enquiry email is disabled. Set GMAIL_APP_PASSWORD on the Node server.');
const db = new DatabaseSync(path.join(__dirname, 'db', 'catbuild.db'));
const PUB = path.join(__dirname, 'public'), PORT = process.env.PORT || 3000, ADMIN_KEY = process.env.ADMIN_KEY || 'change-me';
const MIME = { '.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.json':'application/json', '.jpg':'image/jpeg', '.png':'image/png', '.svg':'image/svg+xml' };
const send = (res, code, data) => { res.writeHead(code, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(data)); };
const parse = r => r.map(x => ({ ...x, ...(x.items ? { items: JSON.parse(x.items) } : {}) }));

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname === '/api/site' && req.method === 'GET')
    return send(res, 200, {
      gallery: db.prepare('SELECT category,title,image FROM gallery ORDER BY category,sort_order').all(),
      packages: parse(db.prepare('SELECT name,rate_per_sqft,image,items FROM packages').all()),
      specs: parse(db.prepare('SELECT section,items FROM specs').all()) });
  if (url.pathname === '/api/enquiry' && req.method === 'POST') {
    let body = ''; req.on('data', c => { body += c; if (body.length > 1e5) req.destroy(); });
    return req.on('end', async () => {
      let d;
      try {
        d = JSON.parse(body);
      } catch { return send(res, 400, { error: 'Bad request' }); }
      if (!d || typeof d !== 'object') return send(res, 400, { error: 'Bad request' });
      try {
        const name = String(d.name || '').trim().slice(0, 100), phone = String(d.phone || '').trim();
        if (!name || !/^[+\d][\d\s-]{7,14}$/.test(phone)) return send(res, 400, { error: 'Valid name and phone required' });
        const packageName = String(d.package || '').slice(0, 40);
        const message = String(d.message || '').slice(0, 1000);
        const saved = db.prepare('INSERT INTO enquiries(name,phone,package,message) VALUES(?,?,?,?)')
          .run(name, phone, packageName, message);
        if (mailer) {
          try {
            await mailer.sendMail({
              from: gmailUser,
              to: enquiryEmail,
              subject: `New catgallery360 enquiry #${saved.lastInsertRowid}`,
              text: `Name: ${name}\nPhone: ${phone}\nPackage: ${packageName || 'None selected'}\n\n${message}`
            });
          } catch (error) {
            console.error('Enquiry email failed for #' + saved.lastInsertRowid, error.code || 'SMTP error');
          }
        }
        return send(res, 201, { ok: true });
      } catch (error) {
        console.error('Unable to save enquiry', error.code || 'Database error');
        return send(res, 500, { error: 'Unable to save your enquiry. Please call 97519 88881.' });
      }
    });
  }
  if (url.pathname === '/api/enquiries') {   // admin: send header x-admin-key
    if (req.headers['x-admin-key'] !== ADMIN_KEY) return send(res, 401, { error: 'Unauthorized' });
    return send(res, 200, db.prepare('SELECT * FROM enquiries ORDER BY id DESC').all());
  }
  let file = path.normalize(path.join(PUB, url.pathname === '/' ? 'index.html' : decodeURIComponent(url.pathname)));
  if (!file.startsWith(PUB)) { res.writeHead(403); return res.end(); }
  fs.readFile(file, (e, buf) => {
    if (e) { res.writeHead(404); return res.end('Not found'); }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' }); res.end(buf);
  });
}).listen(PORT, () => console.log(`Catbuild360 running at http://localhost:${PORT}`));
