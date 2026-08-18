# Devspace frontend

React/Vite client, extracted from Django templates without changing the DRF API.

```bash
cd ..
docker compose up --build

# in a second terminal
cd frontend
npm run dev
```

Vite proxies `/api` and `/media` to `http://localhost` (the Nginx port exposed by `docker compose`). The Django container itself is not published on port 8000, so that address will fail with `ECONNREFUSED`. Use `DEVSPACE_API_ORIGIN=http://host:port npm run dev` for another API origin. For a release build use `npm run build`; publish the resulting `dist/` through the web server with SPA fallback to `index.html`.

The current Django pages are intentionally left unchanged so the migration can be deployed without an API or backend change. Switch the web-server frontend entry point to `frontend/dist/` when ready.
