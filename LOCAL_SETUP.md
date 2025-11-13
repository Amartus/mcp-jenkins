# AxelBrace Local Setup Guide

This document provides setup instructions for using the **mcp-jenkins** fork with AxelBrace's internal Jenkins infrastructure.

## Overview

This is a fork of [lanbaoshen/mcp-jenkins](https://github.com/lanbaoshen/mcp-jenkins) customized for AxelBrace development workflows. The MCP Jenkins server bridges Jenkins with AI language models (Claude, GitHub Copilot) following Anthropic's MCP specification.

**Repository**: https://github.com/Amartus/mcp-jenkins.git

---

## Quick Start: VS Code Copilot Chat Integration

### 1. Prerequisites
- VS Code with GitHub Copilot Chat
- Valid Jenkins credentials for `jenkins-test-axelbrace.tools-nbrace.com`
- `.vscode/mcp.json` configuration file (template provided below)

### 2. Configuration Setup

Add the following configuration to your `.vscode/mcp.json` file:

```jsonc
{
  "inputs": [
    {
      "type": "promptString",
      "id": "jenkins-token",
      "description": "Jenkins Token to read API",
      "password": true
    }
  ],
  "servers": {
    "mcp-jenkins": {
      "command": "uvx",
      "args": [
        "git+https://github.com/Amartus/mcp-jenkins.git",
        "--jenkins-url=<your-jenkins-url>",
        "--jenkins-username=<your-username>",
        "--jenkins-password=${input:jenkins-token}"
      ]
    }
  }
}
```

### 3. First-Time Setup

1. **Start VS Code** with your workspace
2. **Open Copilot Chat** (Ctrl+Shift+I or Cmd+Shift+I)
3. **MCP Server will prompt** for your Jenkins token on first use
4. **Enter your Jenkins API token** when prompted
   - Get your token from: `https://jenkins-test-axelbrace.tools-nbrace.com/me/configure`
   - Scroll to "API Token" section and generate a new token if needed

### 4. Verify Connection

In Copilot Chat, try:
```
@mcp-jenkins Get all jobs
```

You should see a list of available Jenkins jobs.

---

## Configuration Details

### Environment & Credentials

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Jenkins URL** | `<your-jenkins-url>` | Replace with your Jenkins server URL |
| **Username** | `<your-username>` | Your Jenkins username |
| **Authentication** | Jenkins API Token | Stored securely via `${input:jenkins-token}` |

### Authentication Methods

#### Option A: Interactive Input (Recommended)
Use `${input:jenkins-token}` - VS Code will prompt you once, then cache the token for the session.

**Pros**: Secure, no hardcoded credentials
**Cons**: Requires manual input per session

#### Option B: Environment Variable
```jsonc
"mcp-jenkins": {
  "command": "uvx",
  "args": [
    "git+https://github.com/Amartus/mcp-jenkins.git",
    "--jenkins-url=<your-jenkins-url>",
    "--jenkins-username=<your-username>",
    "--jenkins-password=${env:JENKINS_TOKEN}"
  ]
}
```

Then set: `export JENKINS_TOKEN=your_token`

**Pros**: No prompting needed
**Cons**: Less secure if token is in shell history

#### Option C: .env File (Local Only)
Create `.env` in your workspace root:
```
JENKINS_TOKEN=your_api_token
JENKINS_USERNAME=your_username
```

Load via your terminal: `source .env`

---

## Available Tools

This release adds the following tools. For the full base toolset, see the README's Available Tools section: [README.md](README.md#available-tools).

| Tool | Purpose | Example |
|------|---------|---------|
| `save_build_artifact` | Download and save a build artifact directly to disk (optimized for large files) | "Save artifact eks_logs_951.zip from job X build 42 to /tmp/eks_logs_951.zip" |
| `get_all_views` | List all Jenkins views | "List all views" |
| `get_jobs_per_view` | List jobs belonging to a specific view | "Show jobs in view 'All'" |

For the base list of all tools provided by this MCP server, see [README.md](README.md#available-tools).

---

## Troubleshooting

### Issue: "Connection refused" or "Unable to reach Jenkins"
**Cause**: Jenkins URL is unreachable or credentials are invalid.

**Solution**:
1. Verify Jenkins URL: Replace `<your-jenkins-url>` with your actual Jenkins server URL
2. Check VPN connection if accessing internal Jenkins
3. Verify username and API token are correct (replace `<your-username>` with your actual username)
4. Test directly: `curl -u your-username:token https://your-jenkins-url/api/json`

### Issue: "Authentication failed"
**Cause**: Invalid credentials or expired token.

**Solution**:
1. Generate a new API token: https://jenkins-test-axelbrace.tools-nbrace.com/me/configure
2. Update your `.vscode/mcp.json` with the new token
3. Restart VS Code

### Issue: "No tools available" or MCP server not connecting
**Cause**: Configuration error or incorrect git URL.

**Solution**:
1. Verify `mcp.json` syntax (must be valid JSON)
2. Check `uvx` is installed: `which uvx` or `pip show uv`
3. Verify placeholders are replaced:
   - Replace `<your-jenkins-url>` with your actual Jenkins URL
   - Replace `<your-username>` with your Jenkins username
4. Test manually:
   ```bash
   uvx git+https://github.com/Amartus/mcp-jenkins.git \
     --jenkins-url=https://your-jenkins-url \
     --jenkins-username=your_username \
     --jenkins-password=YOUR_TOKEN
   ```

### Issue: "Permission denied" for specific jobs
**Cause**: Your Jenkins user doesn't have access to those jobs.

**Solution**:
1. Check your Jenkins user permissions: https://jenkins-test-axelbrace.tools-nbrace.com/me/configure
2. Request access from Jenkins administrator
3. Contact: [jenkins-admins@amartus.com]

---
