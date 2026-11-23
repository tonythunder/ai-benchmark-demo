# Schedule dependency waves

Implement `build_waves(dependencies)`. The input maps each task ID (a string) to a list of prerequisite task IDs. Every prerequisite is also a key. Schedule all currently ready tasks together in one wave. Return a list of waves, each sorted lexicographically. A task unlocked by one wave can enter the next wave at the earliest. Treat duplicate prerequisites as one edge. Return `None` if any cycle prevents completion, including a self-cycle. Return `[]` for empty input.

Example. `build_waves({"ship": ["pack"], "pack": ["scan"], "scan": [], "log": []})` returns `[["log", "scan"], ["pack"], ["ship"]]`.
