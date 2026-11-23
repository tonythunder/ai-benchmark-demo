from solution import build_waves


def test_places_newly_ready_tasks_in_the_next_wave():
    dependencies = {"ship": ["pack"], "pack": ["scan"], "scan": [], "log": []}
    assert build_waves(dependencies) == [["log", "scan"], ["pack"], ["ship"]]


def test_duplicate_and_shared_prerequisites():
    dependencies = {"z": ["core", "core"], "a": ["core"], "core": []}
    assert build_waves(dependencies) == [["core"], ["a", "z"]]


def test_cycles_fail_even_when_some_tasks_are_ready():
    assert build_waves({"x": ["y"], "y": ["x"], "ok": []}) is None
    assert build_waves({"self": ["self"]}) is None


def test_empty_schedule():
    assert build_waves({}) == []
