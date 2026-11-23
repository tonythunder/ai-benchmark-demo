def manifest_delta(old, new):
    old_paths, new_paths = old.keys(), new.keys()
    return {
        "added": sorted(new_paths - old_paths),
        "removed": sorted(old_paths - new_paths),
        "changed": sorted(path for path in old_paths & new_paths if old[path] != new[path]),
    }
