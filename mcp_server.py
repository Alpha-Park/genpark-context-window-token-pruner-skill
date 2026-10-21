"""MCP Server for Context Window Token Pruner.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import ContextWindowTokenPruner

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "prune_context",
                                "description": "Prune conversation history according to token budget while preserving pinned messages",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "messages": {"type": "array"},
                                        "max_tokens": {"type": "integer", "default": 1000}
                                    },
                                    "required": ["messages"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                res = ContextWindowTokenPruner.prune_context(
                    messages=args.get("messages", []),
                    max_tokens=args.get("max_tokens", 1000)
                )
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
