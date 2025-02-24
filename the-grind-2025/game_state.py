last_investigation = None
last_deduction = None

deduction_list = None
investigation_graph = None

def setup_game_state(investigations, deductions):
    global deduction_list, investigation_graph, last_investigation, last_deduction
    deduction_list = deductions
    investigation_graph = investigations
    last_investigation = investigation_graph[0]
    last_deduction = deductions[0]

def is_everything_solved():
    if not deduction_list:
        return False

    return all(deduction.correct() for deduction in deduction_list)