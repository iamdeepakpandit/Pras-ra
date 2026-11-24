# OpenFilm Routing Rules

Whenever any request involves video creation, video editing, shorts production, motion design, or scene animation:
1. Automatically activate the **OpenFilm** engine.
2. Build compositions structured around `film.html` and deterministic `window.film = { frame(t) { ... } }` pages.
3. Use the OpenFilm MCP server tools (`openfilm_scaffold`, `openfilm_look`, `openfilm_render`, `openfilm_open`, `openfilm_get`) or `npx -y openfilm@latest`.
4. Ensure all final rendered outputs are saved into `final content/`.
