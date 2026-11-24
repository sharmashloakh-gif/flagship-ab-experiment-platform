import hashlib

def assign_variant(user_id: str, experiment_key: str, variants: dict[str, int]) -> str:
    """Deterministically assigns a user to a variant based on percentage weights summing to 100."""
    if sum(variants.values()) != 100:
        raise ValueError("Variant weights must sum to 100")
    digest = hashlib.sha256(f"{experiment_key}:{user_id}".encode()).hexdigest()
    bucket = int(digest[:8], 16) % 100
    cumulative = 0
    for variant_name, weight in variants.items():
        cumulative += weight
        if bucket < cumulative:
            return variant_name
    return list(variants.keys())[-1]

if __name__ == "__main__":
    weights = {"control": 50, "new_checkout_ui": 30, "one_click_pay": 20}
    counts = {k: 0 for k in weights}
    for uid in range(1000):
        v = assign_variant(f"user_{uid}", "checkout_v2", weights)
        counts[v] += 1
    print("1000-user rollout distribution:", counts)
