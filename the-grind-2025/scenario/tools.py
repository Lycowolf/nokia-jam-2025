import game_state
from misc_types import Way

def build_scenario_graph(screens):
    graph = {screen.name: screen for screen in screens}

    for screen in graph.values():
        for way in Way.all():
            out = screen.exits[way]
            if out:
                if out in graph:
                    screen.exits[way] = graph.get(out)
                else:
                    print(f'ERROR: screen {screen.name} has exit to {out} which does not exist')
                    screen.exits[way] = screen

    game_state.last_investigation = screens[0]

    return graph

def build_deduction_links(deductions):
    for i, deduction in enumerate(deductions):
        deduction.prev = deductions[(i - 1) % len(deductions)]
        deduction.next = deductions[(i + 1) % len(deductions)]

    game_state.last_deduction = deductions[0]

    return deductions