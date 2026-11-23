from collections import defaultdict


def build_waves(dependencies):
    dependents = defaultdict(list)
    remaining = {}
    for task, prerequisites in dependencies.items():
        distinct = set(prerequisites)
        remaining[task] = len(distinct)
        for prerequisite in distinct:
            dependents[prerequisite].append(task)

    wave = [task for task, count in remaining.items() if count == 0]
    schedule = []
    completed = 0
    while wave:
        schedule.append(sorted(wave))
        completed += len(wave)
        next_wave = []
        for task in wave:
            for dependent in dependents[task]:
                remaining[dependent] -= 1
                if remaining[dependent] == 0:
                    next_wave.append(dependent)
        wave = next_wave
    return schedule if completed == len(remaining) else None
