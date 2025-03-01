import game_state
from screen import InvestigationScreen, StoryScreen, DeductionScreen
from .tools import build_scenario_graph, build_deduction_links

def setup_scenario():
    screens = [
        InvestigationScreen("1",
                            "Use arrows to move between screens. Glyphs in lower-right corner show possible exits.",
                            right="2"),
        InvestigationScreen("2",
                            "This is Investigation mode. You explore crime scene, observe, and theorize what happened.",
                            left="1", right="3"),
        InvestigationScreen("3",
                            "Press Space to examine objects on the screen. Then, Space to select objects, Z to return here.",
                            objects=[
                                ("Room", "One of tutorial rooms. On the wall, there are signs with control hints."),
                                ("Space - select", "Sign that says: 'Press space to select'"),
                                ("Z - exit", "Label with hint: 'Press Z to exit search menu'"),
                            ],
                            left="2", right="4"),
        InvestigationScreen("4",
                            "Press A to switch to Deduction mode.",
                            objects=[
                                ("Note", "You can only switch to deduction from the screen with arrows, not from menu like this."),
                                ("Chalk writing", "Scribbles on the wall: End of the tutorial is in Deduction mode"),
                            ],
                            left="3", down="5"),
        InvestigationScreen("5",
                            "Hint: correct words for second deduction screen are 'choose', 'guess', 'selection'",
                            up="4"),
    ]
    graph = build_scenario_graph(screens)

    deductions = [
        DeductionScreen("This is Deduction mode. Use ← or → to switch {}, press A to return to Investigation mode.", ["screens"], ["screens"]),
        DeductionScreen("Use ↑ and ↓ to {} keyword slot. Use Space to {} keyword. You can change your {} without limit.",
                        ['choose', 'selection', 'guess'], ["choose", "guess", "selection"]),
        DeductionScreen("When you guess all the words on a screen correctly, the screen is {}.", ['-----', 'locked'], ["locked"]),
        DeductionScreen("The indicator on the bottom shows which {} are already solved. This one is.", ["screens"], ["screens"]),
        DeductionScreen("When all the screens are solved, you {}!", ["-----", "win", "lose"], ["win"]),
    ]
    build_deduction_links(deductions)

    game_state.setup_game_state(screens, deductions)

    return graph['1']