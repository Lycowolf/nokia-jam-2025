import game_state
from screen import InvestigationScreen, StoryScreen, DeductionScreen
from screen.transition import Transition
from .tools import build_scenario_graph, build_deduction_links

def setup_scenario(skip_intro=False):
    screens = [
        InvestigationScreen('entry',
                            "Entrance hall of an old mansion. A distraught-looking policewoman waits for you.",
                            up='hallway',
                            objects=[
                                ('Policewoman',
                                 """ "Finally you are here! It's a real mystery you know? How could they die alone in 
                                 a locked room? Such stupid stunt!"
                                 
                                 "The observers are waiting for you on top of the stairs. We unsealed the door about a hour ago."""),
                                ('Stair', 'A creaky old stairway, just like in a Hollywood movie.'),
                                ('Dust', 'Things here are dusty, as expected in this kind of a mansion.'),
                            ]),
        InvestigationScreen('hallway',
                            "The policewoman led you into a run-down hallway, illuminated by a camping lantern.",
                            down='entry', up='above stair'),
        InvestigationScreen('above stair',
                            "A man and a woman with bags under their eyes are waiting in front of a closed door. "
                            "An ornate key sits in the keyhole.",
                            objects=[
                                ("Man", """The man is about fifty, his face pale.

                                                "Hello mr. detective! I am Peter Stone. The door was closed and sealed the whole night, we both stayed 
                                                awake the whole time, to make sure Mr. Fowler, I mean the victim, wouldn't leave. 
                                                That was the bet you know.

                                                No, Jill was here with me the whole time.
                                                
                                                I didn't hear anything suspicious."

                                                He looks at the door with thousand-mile stare."""),
                                ("Woman", """The woman is younger, maybe twenty-five. Her eyes are red and her make-up marred by tears.

                                                "Good morning sir, I am Jill Palowski. Keith wouldn't respond to us in the morning,
                                                not even pick up his phone, so we called the police.
                                                
                                                Yes, he stayed there the whole night. He didn't believe in ghosts, the poor fool.
                                                
                                                We didn't move anything. The policewomen here cut the seals.
                                                
                                                We heard the house creaking, but that's all."

                                                She cleans her nose and wipes her eyes.
                                      """),
                                ("Door", """Big, solid wooden door. Probably older that you are. Strips of paper were sealing it, now cut apart."""),
                                ("Lock and key", """A massive, antique key of finely wrought metal in a matching lock. It won't be opening quietly.""")
                            ],
                            down="hallway", up="room"),
        InvestigationScreen('room',
                            "A small room. A medieval armor stands behind the door. There's a body on the floor, and a small window on the other side.",
                            objects=[
                                ("Door", """Big, solid wooden door. Probably older that you are."""),
                                ("Armor", "A suite of a medieval armor, complete with a helmet. It would look nice holding a spear. "),
                                ("Body", "Sure looks dead. You can't see much from the doorway, you need to step closer. "),
                            ],
                            down="above stair", right='body'),
        InvestigationScreen('body',"""A body wrapped in a sleeping bag lies on the floor in a pool of blood, impaled by a spear.""",
                            objects=[
                                ("Body",
                                 "An expensively dressed man in his thirties. A spear was thrust into his heart, "
                                 "its point protruding from the man's chest. He has no other wounds."),
                                ("Spear", "A medieval spear with a sharp metal point at one end. The other end is "
                                          "covered with rounded ornament."),
                                ("Blood", "A human blood. Starts to smell bad."),
                            ],
                            left='room', right='window'),
        InvestigationScreen('window', """There's a barred window on the opposite side of the room.""",
                            objects=[
                                ("Window",
                                 "Ornamental metal bars cover the window. They are completely rusted together, "
                                 "there's no opening it without power tools."),
                                ("Other exits",
                                 "Beside the door and the window, there is no plausible entry to the room."),
                            ], left='body'),
    ]
    graph = build_scenario_graph(screens)

    words = [
        "-----", "victim", "policewoman", "ghost", "Peter Stone", "Jill Palowski", "Keith Fowler", "kill", "stay", "observers",
        "locked", "impaled", "front", "back", "called", "police", "made a bet", "night", "morning", "armor", "door", "key", "spear",
        "could", "couldn't", "waited outside", "went inside", "never saw"
    ]
    deductions = [
        DeductionScreen("{}, the victim, {} to {} in a haunted mansion through the {}.", words,
                        ["Keith Fowler", "made a bet", "stay", "night"]),
        DeductionScreen("Mr. {} and Mrs. {} offered to act as {}, making sure the victim would {} until {}.", words,
                        ["Peter Stone", "Jill Palowski", "observers", "stay", "morning"]),
        DeductionScreen("They remained outside, {} the {} and waited until {}. After discovering the body, they {} the {}.", words,
                        ["locked", "door", "morning", "called", "police"]
                        ),
        DeductionScreen("""Jill {} commit the murder because she {} the room during the night.
        
        Peter {} commit the murder because he {} the room during the night.
        
        The policewoman {} commit the murder because she {} the room during the night.""",
                        words,
                        ["couldn't", "waited outside", "couldn't", "waited outside", "couldn't", "never saw",]),
        DeductionScreen("The {} killed the victim. They went and {} him from the {} with the {}.", words,
                        ["ghost", "impaled", "back", "spear"]),
    ]
    build_deduction_links(deductions)

    game_state.setup_game_state(screens, deductions)

    intro = StoryScreen(next_screen=graph['entry'],
                        script=[
                            "It was dark and stormy night, and I slept through it like a baby.",
                            "They called me at nine in the morning. The famous skeptic departed and police that arrived"
                            "on the scene is clueless.",
                            "Looks like I am visiting a haunted mansion. I hope this ride will pay well..."
                        ])
    intro.next = Transition(intro, intro.next, fade_label="Investigation")

    if skip_intro:
        return graph['entry']
    else:
        return intro