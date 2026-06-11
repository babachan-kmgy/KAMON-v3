import time
import json
import os
import bisect

# 方法A: 実行中のスクリプトの位置からリポジトリルートを特定
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)

d = os.path.join(repo_root, "api_v3", "data", "surname")
vm = json.load(open(os.path.join(d, "variant_map_v3.json"), encoding="utf-8"))
fd = {item["stable_id"]: item for item in json.load(open(os.path.join(d, "surname_full_v3.json"), encoding="utf-8"))}

vml = [(k.lower(), v) for k, v in vm.items() if v in fd]

# Current optimized loop
def search_opt(q_lower):
    results = []
    for v_lower, sid in vml:
        if v_lower == q_lower:
            results.append((0, fd[sid]))
        elif v_lower.startswith(q_lower):
            results.append((1, fd[sid]))
        elif q_lower in v_lower:
            results.append((2, fd[sid]))
    return results

# New bisect + partial search
vml_sorted = sorted(vml, key=lambda x: x[0])
vml_keys = [x[0] for x in vml_sorted]

def search_bisect(q_lower):
    results = []
    
    # 1. Binary search for exact & prefix matches (O(log N + M))
    start_idx = bisect.bisect_left(vml_keys, q_lower)
    for i in range(start_idx, len(vml_sorted)):
        v_lower, sid = vml_sorted[i]
        if v_lower == q_lower:
            results.append((0, fd[sid]))
        elif v_lower.startswith(q_lower):
            results.append((1, fd[sid]))
        else:
            break
            
    # 2. Scanning for partial matches (O(N))
    # We only scan if we need to find partial matches.
    # To avoid duplicate results, we keep track of found sids.
    found_sids = {item["stable_id"] for score, item in results}
    for v_lower, sid in vml_sorted:
        if sid not in found_sids and q_lower in v_lower:
            results.append((2, fd[sid]))
            
    return results

# Benchmark
t0 = time.time()
for _ in range(50):
    search_opt("佐藤")
# 読み出しや検索処理
opt_time = time.time() - t0
print(f"Current Opt: {opt_time:.4f}s")

t0 = time.time()
for _ in range(50):
    search_bisect("佐藤")
bisect_time = time.time() - t0
print(f"Bisect Opt: {bisect_time:.4f}s")
print(f"Speedup: {opt_time / bisect_time:.2f}x")
