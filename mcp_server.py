import sys
import json
from client import PageReplacementSimulator

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-page-replacement-lru-clock-lfu-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "simulate_page_replacement",
                    "description": "Simulate virtual memory page replacement algorithms (LRU / Clock)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "reference_string": {"type": "array", "items": {"type": "integer"}},
                            "num_frames": {"type": "integer", "default": 3},
                            "algorithm": {"type": "string", "enum": ["lru", "clock"], "default": "lru"}
                        },
                        "required": ["reference_string"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "simulate_page_replacement":
            frames = args.get("num_frames", 3)
            sim = PageReplacementSimulator(num_frames=frames)
            refs = args.get("reference_string", [])
            algo = args.get("algorithm", "lru")
            data = sim.lru(refs) if algo == "lru" else sim.clock(refs)
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
