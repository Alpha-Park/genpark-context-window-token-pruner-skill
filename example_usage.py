"""Example usage for Context Window Token Pruner."""
from client import ContextWindowTokenPruner
import json

msgs = [
    {"role": "system", "content": "You are a professional Python engineer.", "priority": 10},
    {"role": "user", "content": "How do I implement binary search?", "priority": 1},
    {"role": "assistant", "content": "Here is the code...", "priority": 1},
    {"role": "user", "content": "Now add unit tests.", "priority": 5}
]

pruned = ContextWindowTokenPruner.prune_context(msgs, max_tokens=15)
print(json.dumps(pruned, indent=2))
