---
trigger: always_on
description: Automatic routing contract to OpenFilm for all video editing and video creation prompts.
---

# Automatic Video Editing & Creation Trigger: OpenFilm

Whenever a prompt arrives requesting:
- Video creation, generation, or production
- Video editing, cuts, pacing, transitions, trimming, or restyling
- Short videos, explainers, teasers, or cinematic motion sequences

The agent MUST automatically route the task through **OpenFilm**:

1. **Architecture & Standards:**
   - Use standard web pages with `film.html` and shot components implementing `window.film = { frame(t) { ... } }`.
   - Maintain frame-accurate determinism across all scenes.

2. **Tooling & MCP Integration:**
   - Execute workflows using the local **OpenFilm MCP Server** tools:
     - `openfilm_scaffold`: Generate `film.html` and shot layouts.
     - `openfilm_look`: Run frame audits, contact sheets, and loudness waveforms.
     - `openfilm_render`: Compile the film to MP4 via headless browser and FFmpeg.
     - `openfilm_open`: Launch OpenFilm Studio for collaborative timeline and color-grading adjustments.
     - `openfilm_get`: Pull royalty-free audio, foley, and visual elements.
   - Alternatively, invoke `npx -y openfilm@latest <command>`.

3. **Storage Rule:**
   - All rendered video outputs and exported MP4s must be saved into the `final content/` folder.
