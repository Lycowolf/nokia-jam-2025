from typing import Self

import pyxel

import game_state
import ui
from constants import BACKGROUND, MIDDLE_ROW
from screen import InvestigationScreen, StoryScreen, DeductionScreen, DeductionEndScreen, SmartText, Victory, Screen
from screen.game_over import GameOverScreen
from screen.transition import Transition
from .tools import build_scenario_graph, build_deduction_links
from misc_types import Way

"""
Spoilers:
This is an "escape room" scenario.

Year ago, Killian Gill killed his coworker Justin Moore by pushing him off the dam of a water power plant.
Two weeks ago, Killian ritually killed himself to became a poltergheist and get a revenge against the Detective.

Killian sent an SMS to the Detective with an invitation to a party at the plant. His plan is to kill the Detective
by pushing him off the dam, by crashing an elevator or by throwing him off the catwalks. He wants to make it look
like an accident to avoid exorcism. To do it, he waits until Detective is alone.

At the plant, Emily got in an argument with her coworker Mark and smashed his head against a generator cover,
accidentally killing him. She tried to make it look like a work accident.

Victor found dead Mark and went to alert Emily and others. When they were deciding what to do, Detective called 
and said he'll arrive shortly.

Detective is protected from cheap deaths by the (weaker) spirit of Justin Moore. As a hint to the player, Justin uses
">>text" and Killian uses ">text<" SMSes.

Hints Emily:
- she was assigned to work on different generator than she claims
- there's an indentation on the generator cover where the Marks's head hit it
- the body has a bruise at the back of the head
- Mark did prank her recently
"""

game_over_text = "You fall to your death\nKillian's ghost laughs"
lift_death_text = "The lift cable snaps\nEmergency brakes fail\n" + game_over_text
dam_death_text = "You walk over the dam\nA strong wind gust blows\n" + game_over_text
catwalks_death_text = "The iron structure breaks\nThe floor gives out\n" + game_over_text

def setup_scenario(skip_intro=False):
    screens = [
        InvestigationScreen('road',
                            "An asphalt road to the power plant, leads to the dam ←. Cars are parked here. A plant manager waits for me.",
                            left='dam arrival',
                            objects=[
                                ('Cars', "Employees are parking here."),
                                ("Your phone", """The invitation SMS reads:

                                    >Neil Ericsson, we are celebrating an anniversary of your successful victory against Killian Gill.
                                    You would be very welcome. Place and time follows.<"""),
                                ("Case folder", """You took your case folder with you. It contains the details of the previous case here:

                                     A man named Killian Gills lured his coworker Justin Moore to the dam and pushed him over the railings.
                                     He was jealous because Justin was younger but got promoted to be his boss."""),
                                ('Manager', """"Mr. Ericsson! You are here! Mark was found dead in the generator room!

                                        You have to help us, Mr. Ericsson!"

                                        Damn."""),
                            ]),
        # TODO: going down by the lift safely is a plot hole.
        InvestigationScreen('dam arrival',
                            "A concrete dam, hundred meters long. A lift ↓ leads to generator room. You parked your car on the road outside →.",
                            right='road', down="generator room",
                            objects=[
                                ('Lift', "A small cargo lift. The depth under it makes me uneasy."),
                                ('Dam', "It seemed smaller on the map. Iron railings on both sides."),
                                ('Manager', "\"Please, hurry! There's a lift directly to the generator room, lets use it.\""),
                            ]),
        InvestigationScreen('lift investigation',
                            "The lift to the surface ↑. It feels claustrophobic. Your phone beeps.",
                            down="generator room", up="lift crash",
                            objects=[("Phone", "You received an SMS:\n\n>>DON'T GO. DANGER.")]
                            ),
        InvestigationScreen('lift crash', lift_death_text),
        InvestigationScreen('generator room',
                            "Several employees fidget around four generators. A body is spread over one of them. Catwalks ↓ high above. A lift ↑ goes to the dam.",
                            down="catwalks", right="body", up="lift investigation", left="control room",
                            objects=[
                                ('This room', "The room is very large, but the amount of equipment and machinery make it feel almost cramped."),
                                ('Generators', """Four generators loudly turn flow of water to flow of electricity.
                                               Their turbines spin somewhere inside the dam wall, adding soft vibrations to the ambiance.
                                               
                                               Generators 1 to 3 were recently renovated, though the generator 3's cover is already visibly dented
                                               roughly at shoulder height. 
                                               
                                               Generator 4 is scratched and dented everywhere, still awaiting its new coat of paint."""),

                                ('Body',
                                 "A body lies next to the generator 3, next to an open cover. You can't see much detail from over here."),

                                ('Emily', """A wide-eyed, pale woman in her thirties stares at you, her hands shaking. She wears 
                                big earmuffs on her head. 
                                
                                "Hello Mr. Detective. I was doing the routine checks and measurements on the generator 4, when Victor came to me
                                and started shouting about Mark.
                                
                                No, I was focusing at work, I didn't see it happen. Sorry. Didn't hear either, we have to wear ear protection."
                                
                                She points at a wheeled rack full of test equipment nearby."""),

                                ('Victor', """A man in his twenties, sweaty and pale as death, wearing big earmuffs, looks you into the eyes.
                                
                                "Hi. I worked above, on the catwalks throughout the day, inspecting the ceiling and walls for cracks. 
                                When I climbed down to clean up before going home, I saw Mark there, dead, and immediately alerted everybody.
                                
                                No, I didn't hear anything odd, just the noise of our machines. I saw Emily talking to Victor several times,
                                waving hands, but that's just the part of our job. Also Sam, he was shouting at Mark 
                                about some problem I think."
                                 
                                He looks like he's fighting a panic attack."""),
                            ]),
        InvestigationScreen('body',
                            "The body of Mark lies on an generator, his shirt wrapped around an uncovered shaft. There's blood on his face.",
                            left="generator room",
                            objects=[
                                ("Generator shaft", "It looks like his shirt was caught on the spinning shaft, pulling "
                                                    "him in and smashing his head, hard against the steel. You have "
                                                    "no clue why would the machine started when he was working on it."),
                                ("Head", "There's a big head wound on his forehead, caused by smashing it against something hard. "
                                         "There's a bruise on the back and some hair is missing there."),
                                ("Shirt", "It's wrapped around the steel shaft, but it's a little loose."),
                            ]),
        InvestigationScreen('catwalks',
                            "A web of bridges and platforms spreads above the generators. You can't see well far ahead ↓. Your phone beeps.",
                            up="generator room", down="catwalks fall",
                            objects=[
                                ("Phone", "You received an SMS:\n\n>Important clue's ahead.<"),
                            ]),
        InvestigationScreen('catwalks fall', catwalks_death_text),
        InvestigationScreen('control room',
                            "A control room. You can see most of what's happening in the generator room. Two men are waiting. Manager office is ↓.",
                            right="generator room", down="office",
                            objects=[
                                ("Samuel", """A large man at least fifty years old looks at you through thick glasses, his shirt
                                stained with something dark.

                                "Good day Mr. Ericsson, I am the foreman of my team. I hope you'll help us again, just like the year ago.

                                I was working from the control room most of the time, but I went to the generator 
                                room several times to solve problems.

                                Yes, I had an argument with Victor, but I assure you, it was strictly professional.
                                 
                                I believe what happened was an accident, Victor was a little easygoing with the safety rules.
                                Yes, that's why I shouted at him. Tragically, it seems he didn't listen to me.

                                Why I didn't saw it happen? Well," he leans closer and whispers: "I fell asleep near the end
                                of the shift. Damn my age.

                                My shirt? Oh, well, you see, when I saw the body, I threw up and I haven't an opportunity
                                to change my clothing. This day is full of my failures it seems."

                                He seems really uncomfortable and embarrassed."""),

                                ("Manager", """An older but energetic woman with sad expression is looking at you.
                                
                                "Mr. Ericsson, the providence itself brought you here. I am really glad to see you, 
                                no matter why you are here. Do you have any progress yet? Can you eliminate any foul play?  
                                
                                Victor was quite popular with his coworkers, mainly for his practical jokes. Last time, 
                                he called Emily and convinced her the following day is an holiday. She learned it around 
                                noon and had to rush here in her pyjamas. I haven't seen anyone so red in my whole life."
                                
                                She smiles at the memory. "No, mr. detective, everyone was target of his jokes and we
                                all took it in good spirits. I don't believe anyone would kill Victor because a joke.
                                
                                I can't give you any useful information, I worked in my office, I am sorry. Please ask
                                my subordinates, they will surely help you."
                                
                                She looks sincerely saddened."""),
                            ]),
        InvestigationScreen('office',
                            "The plant manager's office. There are several documents lying on the desk.",
                            up="control room",
                            objects=[
                                ("Exits", "The only exit is the door you came in. There are no windows, "
                                          "only artificial lighting. How do people work here all day without going loopy?"),
                                ("Report from Samuel", "A report on Mark's performance. It points out his easygoing attitude, "
                                                    "but rates him \"satisfactory\" anyway."),
                                ("Work assignments", """Emily: routine maintenance of generator 3
                                
                                                    Mark: preparations for the planned grid load tests
                                
                                                    Samuel: foreman duties (check on him before shift end)
                                
                                                    Victor: inspection of generator room ceiling"""),
                                ("Letter from prison", """A notice from state prison. Killian Gill won't be returning
                                                       to work because he's commited suicide. 
                                                       
                                                       They ask if he's been a member of a gang or a cult, shouldn't 
                                                       they ask that before he's dead?""")
                            ]),

    ]
    graph = build_scenario_graph(screens)
    # HACK: replace death scenarios with confirmations
    inv_scr = graph["lift investigation"]
    from screen import ConfirmationScreen
    inv_scr.exits[Way.up] = ConfirmationScreen(inv_scr, GameOverScreen(lift_death_text), "Use the lift?")
    del graph["lift crash"]
    inv_scr = graph["catwalks"]
    inv_scr.exits[Way.up] = ConfirmationScreen(inv_scr, GameOverScreen(catwalks_death_text), "Go over the catwalks?")
    del graph["catwalks fall"]

    words = [
        "-----", "Emily", "Victor", "Samuel", "Mark", "the manager", "a ghost", "generator cover", "generator shaft",
        "head", "an accident", "did", "didn't", "generator 3", "generator 4", "the murderer",
        "ceiling inspection", "foreman duties", "grid tests", "looking away", "asleep", "beginning", "middle", "end",
        "was careless", "angered her", "angered him", "murdered", "smashed", "safe", "dangerous"
    ]

    # this must correspond with the content of `deductions` and the DeductionEndScreen.
    def select_end_screen(text: SmartText):
        decision = text.words[0]
        if text.words[0] != "-----":
            if decision == "stay and call help":
                solved = True
                for i in range(len(deductions) - 1):
                    if not deductions[i].solved:
                        solved = False
                if solved:
                    return Victory()
                else:
                    return GotAway()
            elif decision == "leave alone":
                return GameOverScreen(dam_death_text)
            elif decision == "leave with others":
                return GameOverScreen(lift_death_text)
        return deductions[-1]

    deductions = [
        DeductionScreen("""Throughout the day:
        
                                    The manager was working on administrative work. She didn't notice 
                                    Mark's death because she was isolated.
                                    
                                    Mark was working on {}. He died around the {} of the work day.
        
                                    Emily was working on {}. She {} notice Mark's death because she was {}.
                                    
                                    Victor was working on {}. He {} notice Mark's death because he was {}.
                                    
                                    Samuel was working on {}. He {} notice Mark's death because he was {}.""", words,
                        [
                            "grid tests", "end", "generator 3", "did", "the murderer", "ceiling inspection",
                            "looking away", "foreman duties", "didn't", "asleep"
                         ]),
        DeductionScreen("Mark was {} when his {} was caught by {} that {} his head against "
                        "the {} because he {}.", words,
                        # herring: an accident, his shirt, gen. shaft, smashed, gen. shaft, was careless
                        ["murdered", "head", "Emily", "smashed", "generator cover", "angered her"]),
        DeductionScreen("""Your phone beeps. You received an SMS:
        
                        >>Think carefully.
        
                        Supernatural events {} happen during my investigation. I received SMSes from {} on my phone.""",
                        ["-----", "did", "didn't", "Killian's ghost", "Justin's ghost", "two ghosts", "a prankster", "an unknown ghost"],
                        ["did", "two ghosts"]),
        DeductionEndScreen(""">You should hurry.<
                        
                        I will {}""",
                        ["-----", "leave alone", "leave with others", "stay and call help"],
                        select_end_screen)
    ]
    build_deduction_links(deductions)

    game_state.setup_game_state(screens, deductions)

    intro = StoryScreen(next_screen=graph['road'],
                        script=[ # TODO: be more cynical
                            "A year ago I solved a murder that happened at a small water power plant. An envious employee pushed his coworker off the dam.",
                            "They decided to invite me to a party to celebrate my skills. How nice!",
                            "It's a small plant, I think 20 people work there at most. It will be a cosy one.",
                            "Let's hope I won't attract any trouble."
                        ])
    intro.next = Transition(intro, intro.next, fade_label="Investigation")

    if skip_intro:
        return graph['entry']
    else:
        return intro

class GotAway(Screen):
    def update(self) -> Self:
        return self
    def draw(self):
        pyxel.cls(BACKGROUND)
        ui.draw_centered_text_row(MIDDLE_ROW - 1, "CASE UNSOLVED")
        ui.draw_centered_text_row(MIDDLE_ROW + 1, "you are safe")