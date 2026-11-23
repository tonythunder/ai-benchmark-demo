from solution import manifest_delta


def test_classifies_all_three_changes():
    assert manifest_delta({"a": "x", "b": "y"}, {"a": "z", "c": "y"}) == {
        "added": ["c"], "removed": ["b"], "changed": ["a"]
    }


def test_case_and_sort_order_are_preserved():
    assert manifest_delta({"x": "1", "X": "1"}, {"Z": "2", "a/b": "3"}) == {
        "added": ["Z", "a/b"], "removed": ["X", "x"], "changed": []
    }


def test_keeps_all_keys_when_no_change():
    assert manifest_delta({"x": "1"}, {"x": "1"}) == {
        "added": [], "removed": [], "changed": []
    }


def test_sorted_changes_without_mutating_the_input():
    before, after = {"z": "1", "a": "2"}, {"z": "3", "a": "4"}
    assert manifest_delta(before, after)["changed"] == ["a", "z"]
    assert before == {"z": "1", "a": "2"} and after == {"z": "3", "a": "4"}
