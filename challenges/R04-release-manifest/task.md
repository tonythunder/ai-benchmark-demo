# Diff release manifests

Implement `manifest_delta(old, new)`. Each manifest maps a case-sensitive POSIX relative path string to a digest string. Return a dictionary with keys `added`, `removed` and `changed`, each containing a lexicographically sorted list of paths. A path is changed if it exists in both inputs with different digest strings. Paths are already normalized. Do not infer moves when two paths have the same digest. Do not mutate the inputs.

Example. `manifest_delta({"a":"x","b":"y"}, {"a":"z","c":"y"})` returns `{"added":["c"], "removed":["b"], "changed":["a"]}`.
