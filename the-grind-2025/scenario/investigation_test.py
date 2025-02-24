from screen import InvestigationScreen, Way, StoryScreen, DeductionScreen
import game_state

def setup_scenario(skip_intro=False):

    screens = [
        InvestigationScreen('1', "Foyer of a run-down, ratty theatre. There is a dead guy lying in a pool of blood.", right='2', objects=[
            ('Dead body', 'Body with multiple stab wounds. There is also a blunt wound on the head.'),
            ('Knife', 'A bloody knife is lying on the floor.'),
            ('Blood', 'There is a large red stain on the carpet. It is theatrical blood, not real one.'),
        ]),
        InvestigationScreen('2', "In the middle of the room lies a suspiciously clean carpet. " +
                                 "It was kind of that guy to die on washable floor and not here.",
                            left="1", right="3", up="A"),
        InvestigationScreen('3', "Storage closet. Someone must have been cleaning recently.", left='2', objects=[
            ('Empty bottle', 'Empty bottle of theatrical blood'),
            ('Broom', 'Slightly bloody broom is propped in the corner'),
            ('Comoda', 'Old, massive wooden comoda. A pile of glass shards was swept underneath'),
        ]),
        InvestigationScreen('A', "Staring towards the ceiling, I see a majestic but wounded chandelier. " +
                                 "Like everything here, it has seen better days.",
                            down='2', objects=[
            ('Chandelier', 'A large, glass chandelier. Probably heavy. Parts are missing or broken, and one of the spokes is bent.')
        ]),
    ]

    graph = build_scenario_graph(screens)

    intro = StoryScreen(next_screen=graph['1'],
                        script=[
                            "The lady was trouble. I knew it from the moment she entered my office.",
                            "No one enters my office without a very good reason.",
                            "Actually, no one enters my office at all. Maybe because the door is unmarked.",
                            "Or it might be the big \"KEEP OUT\" sign.",
                            "...",
                            "It feels I'm kinda losing my track here.",
                            "Let me start from the beginning.",
                            "My name is Niel Ericsson, and I am a private eye. My latest case looks a bit tricky.",
                            "It all began with a dead guy in a theatre lobby...",
                        ])

    words = ["foyer", "room center", "closet", "broom", "chandelier", "knife", "break", "conceal", "fall", "kill",
             "moved", "cleaned", "faked", "blood", "chest", "culprit", "victim"]
    deductions = [
        DeductionScreen("Victim was being drama queen in the {}", words, ["room center"]),
        DeductionScreen("This angered spirits. They caused the {} to {} and {} the victim.", words, ["chandelier", "fall", "kill"]),
        DeductionScreen("The {} wanted to {} it. They {} the victim and {} the scene.", words, ["culprit", "conceal", "moved", "cleaned"]),
        DeductionScreen("Then, they {} the {} wounds and added {}", words, ["faked", "knife", "blood"]),
    ]
    build_deduction_links(deductions)

    if skip_intro:
        return graph['1']
    else:
        return intro

def build_scenario_graph(screens):
    graph = {screen.name: screen for screen in screens}

    for screen in graph.values():
        for way in Way.all():
            out = screen.exits[way]
            if out:
                screen.exits[way] = graph.get(out, screen)

    game_state.last_investigation = screens[0]

    return graph

def build_deduction_links(deductions):
    for i, deduction in enumerate(deductions):
        deduction.prev = deductions[(i-1) % len(deductions)]
        deduction.next = deductions[(i+1) % len(deductions)]

    game_state.last_deduction = deductions[0]

    return deductions
