#!/usr/bin/env node
/**
 * OpenFilm Model Context Protocol (MCP) Server
 * Connects Antigravity and coding agents to OpenFilm CLI & Studio tools.
 */

const { exec, spawn } = require('child_process');
const readline = require('readline');
const fs = require('fs');
const path = require('path');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

function sendResponse(id, result) {
  const response = {
    jsonrpc: "2.0",
    id,
    result
  };
  process.stdout.write(JSON.stringify(response) + '\n');
}

function sendError(id, code, message, data) {
  const response = {
    jsonrpc: "2.0",
    id,
    error: {
      code,
      message,
      data
    }
  };
  process.stdout.write(JSON.stringify(response) + '\n');
}

function runCmd(command, cwd) {
  return new Promise((resolve) => {
    exec(command, { cwd: cwd || process.cwd(), maxBuffer: 10 * 1024 * 1024, shell: true }, (error, stdout, stderr) => {
      resolve({
        success: !error,
        code: error ? error.code : 0,
        stdout: stdout ? stdout.toString() : '',
        stderr: stderr ? stderr.toString() : ''
      });
    });
  });
}

const TOOLS = [
  {
    name: "openfilm_doctor",
    description: "Inspect the OpenFilm environment, checking Node.js, FFmpeg, ffprobe, and GPU hardware acceleration.",
    inputSchema: {
      type: "object",
      properties: {},
      required: []
    }
  },
  {
    name: "openfilm_open",
    description: "Launch or inspect OpenFilm Studio in the browser to interactively view, trim, color grade, or edit a film project.",
    inputSchema: {
      type: "object",
      properties: {
        projectDir: {
          type: "string",
          description: "Path to the project folder containing film.html (defaults to current directory)"
        }
      },
      required: []
    }
  },
  {
    name: "openfilm_look",
    description: "Generate a visual contact sheet and audio loudness waveform check of the film at specified timestamps or ranges.",
    inputSchema: {
      type: "object",
      properties: {
        target: {
          type: "string",
          description: "What to look at or range (e.g. '0-10' or '5' or 'film')"
        },
        projectDir: {
          type: "string",
          description: "Project directory path"
        }
      },
      required: []
    }
  },
  {
    name: "openfilm_render",
    description: "Render the OpenFilm project to MP4 using Chrome Headless and FFmpeg, saving output to '1.final content/'.",
    inputSchema: {
      type: "object",
      properties: {
        range: {
          type: "string",
          description: "Optional second range to render, e.g. '0-30'"
        },
        outputFile: {
          type: "string",
          description: "Custom output file path (defaults to 1.final content/)"
        },
        projectDir: {
          type: "string",
          description: "Project directory path"
        }
      },
      required: []
    }
  },
  {
    name: "openfilm_get",
    description: "Search or download free media (ambient sounds, music, voiceovers, sound effects) from OpenFilm's library.",
    inputSchema: {
      type: "object",
      properties: {
        what: {
          type: "string",
          description: "Media descriptor to fetch (e.g. 'rain ambience', 'cinematic drone', 'whoosh')"
        },
        projectDir: {
          type: "string",
          description: "Project directory path"
        }
      },
      required: ["what"]
    }
  },
  {
    name: "openfilm_scaffold",
    description: "Scaffold a new OpenFilm film.html and shot template with window.film frame(t) structure.",
    inputSchema: {
      type: "object",
      properties: {
        projectDir: {
          type: "string",
          description: "Target directory to create the project"
        },
        title: {
          type: "string",
          description: "Title of the film"
        },
        aspectRatio: {
          type: "string",
          description: "Aspect ratio ('9:16' vertical or '16:9' horizontal)"
        }
      },
      required: ["projectDir"]
    }
  }
];

const npxCmd = process.platform === 'win32' ? 'npx.cmd' : 'npx';

async function handleToolCall(name, args) {
  const cwd = args.projectDir ? path.resolve(args.projectDir) : process.cwd();

  if (name === "openfilm_doctor") {
    const res = await runCmd(`${npxCmd} -y openfilm@latest doctor`, cwd);
    return res.stdout || res.stderr || (res.success ? "Doctor check passed." : "Doctor check failed.");
  }

  if (name === "openfilm_open") {
    // Launch in background
    const proc = spawn(npxCmd, ["-y", "openfilm@latest", "open", cwd], {
      detached: true,
      stdio: "ignore",
      shell: true
    });
    proc.unref();
    return `OpenFilm Studio launched for project at: ${cwd}`;
  }

  if (name === "openfilm_look") {
    const arg = args.target ? `"${args.target}"` : "";
    const res = await runCmd(`${npxCmd} -y openfilm@latest look ${arg}`, cwd);
    return res.stdout || res.stderr || "Look complete.";
  }

  if (name === "openfilm_render") {
    const range = args.range ? `"${args.range}"` : "";
    const res = await runCmd(`${npxCmd} -y openfilm@latest render ${range}`, cwd);
    
    // Ensure render output is mirrored to 1.final content (or legacy final content) if needed
    const finalDir = fs.existsSync(path.join(cwd, "1.final content")) 
      ? path.join(cwd, "1.final content") 
      : (fs.existsSync(path.join(cwd, "final content")) ? path.join(cwd, "final content") : path.join(cwd, "1.final content"));
    if (!fs.existsSync(finalDir)) {
      try { fs.mkdirSync(finalDir, { recursive: true }); } catch (_) {}
    }
    if (fs.existsSync(finalDir)) {
      const files = fs.readdirSync(cwd).filter(f => f.endsWith(".mp4"));
      for (const f of files) {
        const dest = path.join(finalDir, f);
        if (!fs.existsSync(dest)) {
          try { fs.copyFileSync(path.join(cwd, f), dest); } catch (_) {}
        }
      }
    }
    return res.stdout || res.stderr || "Render finished.";
  }

  if (name === "openfilm_get") {
    const res = await runCmd(`${npxCmd} -y openfilm@latest get "${args.what}"`, cwd);
    return res.stdout || res.stderr || "Get completed.";
  }

  if (name === "openfilm_scaffold") {
    const isVertical = args.aspectRatio === "9:16";
    const width = isVertical ? 1080 : 1920;
    const height = isVertical ? 1920 : 1080;
    const filmHtmlPath = path.join(cwd, "film.html");
    const shotPath = path.join(cwd, "shot1.html");

    const filmHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=${width}, height=${height}">
  <title>${args.title || "OpenFilm Video"}</title>
  <style>
    body { margin: 0; background: #000; overflow: hidden; }
    section { position: absolute; inset: 0; }
    iframe { border: none; width: 100%; height: 100%; }
  </style>
</head>
<body>
  <section>
    <iframe src="shot1.html#t=0,5"></iframe>
  </section>
</body>
</html>`;

    const shotHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    body { margin: 0; background: #050508; color: #fff; font-family: sans-serif; display: grid; place-items: center; height: 100vh; }
    h1 { font-size: 5rem; margin: 0; text-align: center; }
  </style>
</head>
<body>
  <h1 id="headline">${args.title || "Scene 1"}</h1>
  <script>
    window.film = {
      frame(t) {
        const headline = document.getElementById("headline");
        const opacity = Math.min(1, t / 1.0);
        const scale = 1.0 + (t * 0.05);
        headline.style.opacity = opacity;
        headline.style.transform = "scale(" + scale + ")";
      }
    };
  </script>
</body>
</html>`;

    if (!fs.existsSync(cwd)) fs.mkdirSync(cwd, { recursive: true });
    fs.writeFileSync(filmHtmlPath, filmHtml, "utf-8");
    fs.writeFileSync(shotPath, shotHtml, "utf-8");
    return `Scaffolded OpenFilm project at ${cwd} (film.html, shot1.html, ${width}x${height}).`;
  }

  throw new Error(`Unknown tool: ${name}`);
}

rl.on('line', async (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;

  let message;
  try {
    message = JSON.parse(trimmed);
  } catch (err) {
    return;
  }

  const { id, method, params } = message;

  if (method === "initialize") {
    sendResponse(id, {
      protocolVersion: "2024-11-05",
      capabilities: {
        tools: {}
      },
      serverInfo: {
        name: "openfilm-mcp",
        version: "1.0.0"
      }
    });
    return;
  }

  if (method === "notifications/initialized") {
    // No-op for notification
    return;
  }

  if (method === "ping") {
    sendResponse(id, {});
    return;
  }

  if (method === "tools/list") {
    sendResponse(id, { tools: TOOLS });
    return;
  }

  if (method === "tools/call") {
    const { name, arguments: toolArgs } = params || {};
    try {
      const output = await handleToolCall(name, toolArgs || {});
      sendResponse(id, {
        content: [
          {
            type: "text",
            text: typeof output === 'string' ? output : JSON.stringify(output, null, 2)
          }
        ]
      });
    } catch (err) {
      sendResponse(id, {
        content: [
          {
            type: "text",
            text: `Error executing ${name}: ${err.message}`
          }
        ],
        isError: true
      });
    }
    return;
  }

  if (id !== undefined) {
    sendError(id, -32601, `Method not found: ${method}`);
  }
});
