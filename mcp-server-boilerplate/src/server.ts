/**
 * server.ts — illustrative skeleton: a minimal MCP server with one validated tool.
 *
 * Not production-hardened. Single tool, stdio transport only, no auth.
 * Registers `echo_upper`, a trivial tool, so the wiring (schema -> validation
 * -> handler -> structured result) is fully visible in ~50 lines.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

const EchoUpperInput = z.object({
  text: z.string().min(1, "text must not be empty"),
});

const server = new Server(
  { name: "cookbook-mcp-boilerplate", version: "0.1.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "echo_upper",
      description: "Returns the input text uppercased. Illustrative tool only.",
      inputSchema: {
        type: "object",
        properties: {
          text: { type: "string", description: "Text to uppercase" },
        },
        required: ["text"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name !== "echo_upper") {
    throw new Error(`Unknown tool: ${request.params.name}`);
  }

  // Validate before touching business logic — bad input fails here with a
  // clear message instead of crashing deeper in the handler.
  const parsed = EchoUpperInput.safeParse(request.params.arguments);
  if (!parsed.success) {
    return {
      isError: true,
      content: [{ type: "text", text: `Invalid arguments: ${parsed.error.message}` }],
    };
  }

  const result = parsed.data.text.toUpperCase();
  return {
    content: [{ type: "text", text: result }],
  };
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("cookbook-mcp-boilerplate running on stdio");
}

main().catch((err) => {
  console.error("Fatal error starting MCP server:", err);
  process.exit(1);
});
