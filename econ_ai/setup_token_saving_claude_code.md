---
title: "RTK + Caveman on Windows + Claude Code CLI — Install & Usage Guide"
description: "Reproducible setup guide for RTK (input-token reducer) and Caveman (output-token reducer) on Windows with Claude Code CLI."
os: "Windows 10/11 (x64)"
shell: "PowerShell 5.1+ and Git Bash"
audience: "Claude Code CLI users on Windows"
generated: "2026-06-15"
schema_version: "1.0"
tools:
  - id: rtk
    name: "Rust Token Killer"
    repo: "https://github.com/rtk-ai/rtk"
    reduces: "input-tokens"
    version_installed: "0.42.4"
    mechanism: "Claude Code PreToolUse(Bash) hook -> rtk hook claude"
  - id: caveman
    name: "Caveman"
    repo: "https://github.com/JuliusBrussee/caveman"
    reduces: "output-tokens"
    version_installed: "main (plugin: caveman@caveman)"
    mechanism: "Claude Code plugin marketplace (skills + SessionStart/UserPromptSubmit hooks via plugin manifest)"
dependencies:
  - "Claude Code CLI"
  - "Git for Windows (Git Bash)"
  - "Node.js >= 18 (Caveman stats/hooks only) — installed: v24.16.0"
config_dir: "C:\\Users\\<USER>\\.claude"
---

# RTK + Caveman on Windows + Claude Code CLI

Two complementary token-reduction tools for Claude Code:

| Tool    | Reduces            | How it works                                                              | Needs Node.js |
|---------|--------------------|--------------------------------------------------------------------------|---------------|
| RTK     | **Input** tokens   | Compresses/filters Bash command output before it reaches the model.      | No            |
| Caveman | **Output** tokens  | Switches the model into a terse "caveman" response style.                | Stats/hooks: yes |

They are independent and stack. Install order does not matter.

> Replace `<USER>` with your Windows username throughout (this machine: `KSuzuki`).

---

## 0. Prerequisites

```powershell
# Verify Claude Code CLI is installed
claude --version

# Verify Git Bash exists (Claude Code uses it as the Bash backend on Windows)
& "C:\Program Files\Git\bin\bash.exe" --version

# winget is used below to install Node.js (Caveman stats only)
winget --version
```

---

## 1. Install RTK (input-token reducer)

### 1.1 Download the Windows binary

```powershell
# Always resolve the latest release tag from the GitHub API
$rel = Invoke-RestMethod "https://api.github.com/repos/rtk-ai/rtk/releases/latest" -Headers @{ "User-Agent" = "pwsh" }
$asset = $rel.assets | Where-Object { $_.name -eq "rtk-x86_64-pc-windows-msvc.zip" }
"latest tag: $($rel.tag_name)"   # verified: v0.42.4

Invoke-WebRequest -Uri $asset.browser_download_url -OutFile "$env:TEMP\rtk.zip"
```

### 1.2 Extract and place on PATH

```powershell
# Recommended install location
$bin = "$env:USERPROFILE\.local\bin"
New-Item -ItemType Directory -Force -Path $bin | Out-Null

Expand-Archive -Path "$env:TEMP\rtk.zip" -DestinationPath "$env:TEMP\rtk-extracted" -Force
Copy-Item "$env:TEMP\rtk-extracted\rtk.exe" "$bin\rtk.exe" -Force

# Add to the *User* PATH so all shells (incl. Git Bash) see it
$userPath = [Environment]::GetEnvironmentVariable("Path","User")
if (($userPath -split ';' | Where-Object { $_.TrimEnd('\') -ieq $bin }).Count -eq 0) {
  [Environment]::SetEnvironmentVariable("Path", "$userPath;$bin", "User")
}
```

> Git Bash alternative (article method): add `export PATH="$HOME/.local/bin:$PATH"` to `~/.bash_profile`.
> Setting the **User PATH** (above) is more robust because it also covers PowerShell and fresh Git Bash sessions.

### 1.3 Verify the correct binary

```powershell
& "$env:USERPROFILE\.local\bin\rtk.exe" --version   # MUST print: rtk 0.42.4
```

> **Name collision warning:** Do **not** use `cargo install rtk` — it installs a different package
> ("Rust Type Kit"). Always confirm `rtk --version` prints `rtk X.Y.Z`.

### 1.4 Integrate with Claude Code

```powershell
# Preview first (writes nothing)
& "$env:USERPROFILE\.local\bin\rtk.exe" init -g --auto-patch --dry-run -v

# Apply: adds PreToolUse(Bash) hook to ~/.claude/settings.json,
# creates ~/.claude/RTK.md, appends @RTK.md to ~/.claude/CLAUDE.md.
& "$env:USERPROFILE\.local\bin\rtk.exe" init -g --auto-patch
```

Resulting `~/.claude/settings.json` hook block:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "rtk hook claude" } ] }
    ]
  }
}
```

Files created/modified by RTK:

| Path                                                | Action  |
|-----------------------------------------------------|---------|
| `C:\Users\<USER>\.local\bin\rtk.exe`                | created |
| `C:\Users\<USER>\.claude\settings.json`             | hook appended (backup: `settings.json.bak`) |
| `C:\Users\<USER>\.claude\RTK.md`                    | created |
| `C:\Users\<USER>\.claude\CLAUDE.md`                 | `@RTK.md` reference added |
| `C:\Users\<USER>\AppData\Roaming\rtk\filters.toml`  | created (filter template) |

---

## 2. Install Caveman (output-token reducer)

### 2.1 Install Node.js >= 18 (required for stats + hooks)

```powershell
winget install --id OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements --silent

# Refresh PATH in the current shell, then verify
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
node --version   # verified: v24.16.0
npx --version    # verified: 11.13.0
```

### 2.2 Install the Caveman plugin

```powershell
# Installs the Claude Code plugin (skills + agents) and registers the marketplace.
# Hooks (SessionStart / UserPromptSubmit) are handled by the plugin manifest — no manual settings.json hook needed.
npx -y github:JuliusBrussee/caveman -- --only claude
```

This runs, under the hood:

```text
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

Resulting `~/.claude/settings.json` additions:

```json
{
  "extraKnownMarketplaces": {
    "caveman": { "source": { "source": "github", "repo": "JuliusBrussee/caveman" } }
  },
  "enabledPlugins": { "caveman@caveman": true }
}
```

> **Post-install check:** `claude plugin install` may rewrite `settings.json` and can drop unrelated
> top-level keys (observed: `effortLevel` was removed). Diff against your backup and restore any lost keys:
> ```powershell
> Compare-Object (Get-Content "$HOME\.claude\settings.json.bak") (Get-Content "$HOME\.claude\settings.json")
> ```

Plugin skills installed (cache: `~/.claude/plugins/cache/caveman/...`):
`caveman`, `caveman-stats`, `caveman-commit`, `caveman-compress`, `caveman-review`, `caveman-help`, `cavecrew`.

---

## 3. Activate

```text
Restart Claude Code CLI so settings.json + plugins reload.
```

---

## 4. Usage

### 4.1 RTK — transparent, automatic

RTK works **automatically** once the hook is active. Every Bash command Claude runs is routed through
`rtk hook claude`, which compresses the output the model sees. You see the full output; the model sees the compressed one.

Meta commands (run these yourself or ask Claude to run them):

```bash
rtk gain              # Show token-savings analytics (cumulative)
rtk gain --history    # Per-command savings history
rtk discover          # Analyze past Claude Code history for missed savings opportunities
rtk proxy <cmd>       # Run a command WITHOUT filtering (debugging)
rtk --version         # Sanity check (expect: rtk 0.42.4)
```

Notes:
- No workflow change required; it is transparent.
- Highest impact on verbose commands: `cargo test`, `npm test`, `git status`, large `grep`/`ls` output, build logs.

### 4.2 Caveman — explicit mode toggle

Caveman changes the **response style** to a terse, compressed form while keeping technical accuracy
(code, error strings, API names stay verbatim; it auto-disables for security warnings and irreversible-action confirmations).

| Action                        | Command / phrase                          |
|-------------------------------|-------------------------------------------|
| Turn on (default level)       | `/caveman`  or say `caveman mode`         |
| Set intensity                 | `/caveman lite` \| `full` \| `ultra`       |
| Classical-Chinese variants    | `/caveman wenyan-lite` \| `wenyan-full` \| `wenyan-ultra` |
| Turn off                      | say `stop caveman` or `normal mode`       |
| Session stats                 | `/caveman-stats`                          |
| Compressed commit message     | `/caveman-commit`                         |
| Compressed code review        | `/caveman-review`                         |
| Compress a file's content     | `/caveman-compress <file>`                |
| Help                          | `/caveman-help`                           |

Intensity levels:

| Level   | Effect                                                                            |
|---------|-----------------------------------------------------------------------------------|
| `lite`  | Drop filler/hedging; keep full sentences + articles. Professional but tight.       |
| `full`  | Drop articles, fragments OK, short synonyms. Classic caveman (default).            |
| `ultra` | Abbreviate prose words (DB/auth/config). Never abbreviates code symbols/API names. |

`/caveman-stats` reports **per-session** only. Example output shape:

```text
Caveman Stats
──────────────────────────────
Turns:    442
Output tokens:        381,623
Est. without caveman: 1,090,351
Est. tokens saved:    708,728 (~65%)
```

### 4.3 Combined workflow

- RTK trims what Claude **reads** (command output).
- Caveman trims what Claude **writes** (responses).
- Best fit: long debugging / log-investigation / back-and-forth sessions (not bulk code generation).

---

## 5. Verify everything

```powershell
# RTK
& "$env:USERPROFILE\.local\bin\rtk.exe" --version           # rtk 0.42.4
& "$env:USERPROFILE\.local\bin\rtk.exe" gain                # should run (not "command not found")

# Node (Caveman dependency)
node --version                                              # v24.16.0+

# Caveman plugin enabled
(Get-Content "$HOME\.claude\settings.json" -Raw | ConvertFrom-Json).enabledPlugins
```

In Claude Code after restart: run `/caveman`, confirm replies become terse; run `rtk gain` to confirm RTK savings accrue.

---

## 6. Uninstall

```powershell
# Caveman
npx -y github:JuliusBrussee/caveman -- --uninstall

# RTK (remove hook + artifacts, then delete binary)
& "$env:USERPROFILE\.local\bin\rtk.exe" init -g --uninstall
Remove-Item "$env:USERPROFILE\.local\bin\rtk.exe"
# Optionally remove .local\bin from User PATH and delete ~/.claude/RTK.md, the @RTK.md line in CLAUDE.md,
# and C:\Users\<USER>\AppData\Roaming\rtk\
```

---

## 7. Troubleshooting

| Symptom                                             | Cause / Fix                                                                 |
|-----------------------------------------------------|----------------------------------------------------------------------------|
| `rtk gain` fails / wrong output                     | Wrong package installed via cargo. Reinstall the GitHub release binary.     |
| `rtk` not found inside Claude Code Bash hook        | `.local\bin` not on PATH. Re-run the User-PATH step (1.2) and restart.      |
| `rtk: Failed to resolve 'rg' via PATH`              | Harmless warning; RTK falls back to direct exec. Optionally install ripgrep.|
| `/caveman-stats` does nothing / Node errors         | Node.js missing or < 18. Install Node (2.1) and restart Claude Code.        |
| `effortLevel` (or other key) missing after install  | `claude plugin install` rewrote settings.json. Restore from `settings.json.bak`. |
| Caveman style won't turn off                         | Say `normal mode` or `stop caveman` explicitly.                            |
