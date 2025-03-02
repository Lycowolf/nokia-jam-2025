last_investigation = None
last_deduction = None

deduction_list = []
investigation_graph = None

case_menu = None

def register_case_menu(menu):
    global case_menu
    case_menu = menu

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

def deduction_progress(deduction):
    return [(d.correct(), d == deduction) for d in deduction_list]
