# Catbuild360 – Civil Engineer Gallery Website

Stack: HTML, CSS, JavaScript (frontend) · Node.js and Nodemailer · SQLite + SQL (`schema.sql`) · Python (`seed.py`).

## Run
1. `python3 seed.py`    – creates `db/catbuild.db` and `public/data.json`
2. `node --no-warnings server.js`  (Node 22.5+) → http://localhost:3000

Set `ADMIN_KEY=yourSecret` before starting. View enquiries with:
`curl -H "x-admin-key: yourSecret" localhost:3000/api/enquiries`

## Enquiry email

Run `npm install` from the `catgallery360` directory. For local use, create a `.env` next to `server.js` and add `GMAIL_APP_PASSWORD=your-app-password`. For a hosted site, set `GMAIL_APP_PASSWORD` as an environment secret on the Node host. The server sends new enquiry notifications to `mohamedanas7408@gmail.com`. The sender defaults to the same address, or you can set `GMAIL_USER` to the Gmail account that owns the app password.

Start or restart the server with `npm start` and open http://localhost:3000 for local testing. For deployment, serve the website through the Node process so `/api/enquiry` on the website's address reaches `server.js`.

Generate the app password in [Google Account settings](https://support.google.com/accounts/answer/185833) after enabling 2-Step Verification. Store it as a server secret. Enquiries are saved to SQLite before email is attempted. If email is disabled or delivery fails, the submission stays in SQLite.

## Edit content
Change the lists in `seed.py` (gallery titles, packages, specs) and re-run it. Add photos to `public/img/`.

Without Node, `public/index.html` can still be hosted statically (reads `data.json`), but the enquiry form needs the server.
