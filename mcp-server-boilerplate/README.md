# mcp-server-boilerplate

A minimal Model Context Protocol (MCP) server template in TypeScript: one server, one real tool, wired for stdio transport.

## What it is

MCP is the emerging standard for exposing tools and resources to LLM clients (Claude Desktop, Claude Code, and any MCP-compatible agent) over a well-defined JSON-RPC protocol instead of a bespoke API per integration. This skeleton stands up the smallest server that's still real: it registers one tool with a typed input schema, validates the input, and returns a structured result.

## When to use it

- You want to expose an internal capability (a database query, an API call, a file operation) to an LLM client without building a custom plugin format.
- You're evaluating whether MCP fits a project and want the shortest path to "a client can actually call my tool."
- You need a clean starting point before adding real tools, auth, or multiple transports (stdio for local clients, HTTP/SSE for remote ones).

## The gotcha it solves

**Tool schemas that don't validate input silently produce malformed calls.** The most common first-pass mistake is registering a tool with a loose or missing input schema, which means:

- The client can send malformed arguments and the server just crashes or returns a confusing error.
- There's no single source of truth for what the tool expects, so the LLM client is more likely to call it wrong.

This skeleton defines the input schema with `zod` and validates every call before running any logic, so a bad call fails with a clear, structured error message instead of an unhandled exception deep in the tool implementation.

## How to run

This is an **illustrative skeleton**, not a published package.

```bash
npm install
npm run build
npm start
```

The server speaks MCP over stdio. To try it against a real client, point Claude Desktop's MCP config (or any MCP-compatible client) at the built entry point:

```json
{
  "mcpServers": {
    "cookbook-boilerplate": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-server-boilerplate/dist/server.js"]
    }
  }
}
```

## What's simplified here (not production-hardened)

- Single tool, stdio transport only — no HTTP/SSE transport, no OAuth.
- No logging/observability beyond stderr.
- No rate limiting — a real deployment behind a remote transport needs both auth and rate limits.
