import game_state
from screen import InvestigationScreen, StoryScreen, DeductionScreen
from . import build_scenario_graph, build_deduction_links

def setup_scenario(skip_intro=False):
    screens = [
        InvestigationScreen('entry',
                            "Entrance hall of an old mansion. A distraught-looking policewoman waits for you.",
                            up='above stair',
                            objects=[
                                ('Policewoman',
                                 """ "Finally you are here! It's a real mystery you know? How could they die alone in 
                                 a locked room? Such stupid stunt!"
                                 
                                 "The observers are waiting for you on top of the stairs."""),
                                ('Stair', 'A creaky old stairway, just like from a Hollywood movie.'),
                                ('Dust', 'Things here are dusty, as expected in this kind of a mansion.'),
                            ]),
        InvestigationScreen('above stair',
                            "The policewoman led you into a run-down hallway, illuminated by a camping lantern. A man and a woman "
                            "with bags under their eyes are waiting in front of a closed door covered in police tape. "
                            "An ornate key sits in the keyhole.",
                            objects=[
                                ("Man", """The man is about fifty, his face pale.

                                                "Hello mr. detective! I am Peter Stone. The door was closed the whole night, we both stayed 
                                                awake the whole time, to make sure mr. Fowler, I mean the victim, wouldn't leave. 
                                                That was the bet you know.

                                                No, Jill was here with me the whole time.
                                                
                                                I didn't hear anything suspicious."

                                                He looks at the door with thousand-mile stare."""),
                                ("Woman", """The woman is younger, maybe twenty-five. Her eyes are red and her make-up marred by tears.

                                                "Good morning sir, I am Jill Palowski. We found Keith in there in the morning, we didn't move anything.

                                                Yes, he stayed there the whole night. He didn't believe in ghosts, the poor fool.
                                                
                                                We heard the house creaking, but that's all."

                                                She cleans her nose and wipes her eyes.
                                      """)
                            ],
                            down="entry", up="room"),
        InvestigationScreen('room',
                            "A small room. A body wrapped in a sleeping bag lies on the floor in a pool of blood, impaled by a spear."
                            "A medieval armor stands behind the door. There's a barred window on the opposite side of the room.",
                            objects=[
                                ("Body", "An expensively dressed man in his thirties. A spear was thrust into his heart, "
                                "its point protruding from the man's chest. He has no other wounds."),
                                ("Spear", "A medieval spear with a sharp metal point at one end. The other end is "
                                          "covered with rounded ornament."),
                                ("Blood", "A human blood. Starts to smell bad."),
                                ("Armor", "A suite of a medieval armor, complete with a helmet. It would look nice holding a spear. "),
                                ("Window", "Ornamental metal bars cover the window. They are completely rusted together, "
                                           "there's no opening it without power tools.")
                            ],
                            down="above stairs"),
    ]
    graph = build_scenario_graph(screens)

    words = [
        "-----", "victim", "policewoman", "ghost", "Peter", "Jill", "Keith", "Stone", "Palowski", "Fowler", "kill", "stay", "observe",
        "observers", "locked", "impaled", "front", "back", "called", "police", "made a bet", "night", "morning", "armor", "door"
    ]
    deductions = [
        DeductionScreen("{} {}, the victim, {} to {} in a haunted mansion through the {}", words, ["made a bet", "stay", "night"]),
        DeductionScreen("Mr. {} {} and Mrs. {} {} offered to {} the victim would {} until {}.", words,
                        ["Peter", "Stone", "Jill", "Palowski", "observe", "stay", "morning"]),
        DeductionScreen("They remained outside, {} the {} and waited until {}. After discovering the body, they {} the {}.", words,
                        ["locked", "door", "morning", "called", "police"]
                        ),
        DeductionScreen("The {} decided to kill the victim. They went and {} him from the {} with the {}.", words,
                        ["ghost", "impaled", "back", "spear"]),
    ]
    build_deduction_links(deductions)

    game_state.setup_game_state(screens, deductions)

    intro = StoryScreen(next_screen=graph['entry'],
                        script=[
                            """It was dark and stormy night, and I slept through it like a baby.
                            They called me at nine in the morning. The victim is a famous skeptic, but the police is clueless.
                            They invited me to a haunted mansion and I hope this ride will pay well...                             
                            """
                        ])

    if skip_intro:
        return graph['1']
    else:
        return intro