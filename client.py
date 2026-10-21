"""Context Window Token Pruner.
100% Python Standard Library.
"""

class ContextWindowTokenPruner:
    """Priority-weighted context window token pruner & FIFO eviction engine."""

    @staticmethod
    def estimate_tokens(text: str) -> int:
        return max(1, len(text.split()))

    @classmethod
    def prune_context(cls, messages: list, max_tokens: int = 1000) -> dict:
        pinned_messages = [m for m in messages if m.get("priority", 1) >= 10]
        evictable_messages = [m for m in messages if m.get("priority", 1) < 10]

        pinned_tokens = sum(cls.estimate_tokens(m.get("content", "")) for m in pinned_messages)
        remaining_budget = max(0, max_tokens - pinned_tokens)

        kept_evictable = []
        current_tokens = 0

        for m in reversed(evictable_messages):
            t_cnt = cls.estimate_tokens(m.get("content", ""))
            if current_tokens + t_cnt <= remaining_budget:
                kept_evictable.insert(0, m)
                current_tokens += t_cnt
            else:
                break

        pruned_count = len(evictable_messages) - len(kept_evictable)
        final_messages = pinned_messages + kept_evictable
        total_tokens = sum(cls.estimate_tokens(m.get("content", "")) for m in final_messages)

        return {
            "pruned_messages_count": pruned_count,
            "kept_messages_count": len(final_messages),
            "total_tokens": total_tokens,
            "messages": final_messages
        }
