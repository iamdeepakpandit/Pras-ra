---
name: openfilm
description: Make videos as web pages with OpenFilm. Use when the user asks for a video, motion graphics, an animation, a launch film, an explainer, a music video, to edit, cut, check or render a film (film.html and pages with window.film), or to open OpenFilm or its Studio.
---

# OpenFilm

OpenFilm turns any coding agent into an AI video agent with visual editors to change anything it makes.

## Core Architecture
- **A Film is a Function of Time:** Given `t`, it draws that moment deterministically.
- **Root File:** `film.html` containing tracks of clips (`<section><iframe src="shot.html#t=0,4"></iframe></section>`).
- **Shot Architecture:** Each shot is a standard web page implementing:
  ```javascript
  window.film = {
    frame(t) { /* draw the complete picture at t seconds */ }
  };
  ```
- **Rendering & Checking:** No heavy framework dependencies; uses headless browser + FFmpeg.

## CLI Commands
- `npx -y openfilm@latest open [folder]` — Start or open a project in Studio.
- `npx -y openfilm@latest look [what] [t | a-b]` — Check and draw contact sheet with audio/loudness audit.
- `npx -y openfilm@latest render [a-b]` — Render to MP4 beside `film.html` (mirrored to `final content/`).
- `npx -y openfilm@latest get [what]` — Fetch media from local footage, free libraries, or AI providers.
- `npx -y openfilm@latest skills` — List skills installed for this film.
- `npx -y openfilm@latest doctor` — Diagnose environment readiness (Node, FFmpeg, Chrome).
