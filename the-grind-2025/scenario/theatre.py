from screen import InvestigationScreen, StoryScreen, DeductionScreen
import game_state
from .tools import build_scenario_graph, build_deduction_links

def setup_scenario(skip_intro=False):

    screens = [
        InvestigationScreen('stage', "The main stage. There are two bodies in full costume and broken prop chandelier",
                            left='backstage', down='auditorium', right='lobby',
                            objects=[
                                ('Roland', 'The body of Carol Reyes, dressed in the full costume of the protagonist Orlando. There is a big bruise on his head,'
                                           'some lacerations, and his neck is in unnatural position. A bloody sword is lying close to the body'),
                                ('Mador', 'The body of Johannes Meyer, dressed in the costume of Saracen warrior Mador. He has a stab wound in the '
                                          'abdomen, and there is lot of blood.'),
                                ('Bloody sword', 'Near Orlando\'s hand, there is an solid iron sword. Nearly half the blade is covered in blood.'
                                                 'It is still sticky on the underside.'),
                                ('Other sword', 'To the side of Mador lies another iron sword.'),
                                ('Broken chandelier', 'On the side, there is an unreasonably massive and fancy prop chandelier. It is broken, but the rope'
                                                      'that was holding it seems intact.'
                                                      'It was moved when they discovered the body. One of the spokes is bent and there'
                                                      'are noticeable traces of impact. ')
                            ]),
        InvestigationScreen('backstage', 'Backstage',
                            right='stage', left='prop storage',
                            objects=[
                                ('Rigging controls',
                                 'Manual controls for the rigging. The main hanged prop is set to upper position,'
                                 'and the controls are properly locked.'),
                                ('Note on the controls',
                                 """There is a note stuck on the control console.
                                 
                                 Use of rigging is FORBIDDEN without authorized supervision!
                                 Seriously, hands off when I am not there!
                                Sam, the technician
                                 """),
                                ('Pulley', 'Motorized pulley for the rigging. Something has failed and it has released all the rope.'
                                           'The safety brake failed to engage. This has probably caused the tragedy on the stage.'
                                           'It seems like improbable string of failures.'),
                            ]),

        InvestigationScreen('auditorium', 'Empty auditorium',
                            up='stage',
                            objects=[
                                ('Camera', 'Between the seats, there is a collapsed tripod with a video camera. The memory card is missing.')
                            ]),

        InvestigationScreen('prop storage', 'Prop storage room',
                            right='backstage',
                            objects=[
                                ('Room', 'A respectable-sized room with big mess inside. Most accessed stuf is kept in order, but older props are just laying in heaps.'),
                                ('Sword cabinet', 'The theater has impressive selection of prop swords. Medieval german swords, '
                                                  'Renaissance rapiers, even Turkish saber and some fantasy pieces straight out of Lord of the Rings.'
                                                  'All of them are the safety type, either collapsible or foam.'),
                                ('Old wooden chest', """There is an old chest. Inside are pieces of a knight costumes - chainmail armor, tabards,'
                                                     'and an unusually realistic crown. On the top, there are two leather sword sheathes. These are empty.
                                                     
                                                     The chest is covered in dust, but was opened recently."""),
                                ('Opened dresser', """One of the big dressers is partially open. Inside there is bunch of victorian clothing and, prominently,'
                                                   'a big black cape that would make Bram Stoker proud.
                                                   
                                                   Under the clothes, there is a box with miscellaneous props - pistols, a bible, fake teeth, and
                                                   a bottle of fake blood. Unlike others, the bottle was stored haphazardly and blood residue has stained other props.
                                                   """),
                            ]),

        InvestigationScreen('lobby', 'Lobby',
                            left='stage', right='corridor 1', up='bar',
                            objects=[
                                ('Poster', 'A poster for upcoming premiere of Orlando Furioso. Photos of Reyes, Wagner and'
                                           'Diaz are displayed prominently as the main trio.'),
                                ('Older posters', 'Posters of many previous plays remain in the lobby. It seems this company favours the classics.'
                                                  'Dracula, Cleopatra, Oedipus Rex, and Le morte d\'Arthur are some of the recent ones.'),
                                ('Newspaper clippings',"""The unlucky play finally prepares for the first opening!
                                
                                The theatre world has just recovered after a tragic death of Daniel Rider, who suffered a tragic accident
                                on the night of the general rehearsal of the newest interpretation of Orlando Furioso. His indomitable
                                colleagues are not cowed by hostile fate, and the renewed opening is expected in the upcoming days.
                                The replacement actor turned new main star, Carol Reyes, seems not too perturbed by the
                                rumors of the script being cursed.
                                
                                If any ghosts are interested in the play, I invite them to the grand opening. All the rest of you are
                                cordially invited too, of course.
                                
                                Reyes and his long-standing rivalry with Rider has long been known in the tabloid world, but
                                that reportedly never impacted their professional collaboration. < more juicy details on page 5 >"""),
                                ('Police', ''),

                            ]),
        InvestigationScreen('bar', 'Bar. The actors who discovered the mess are there.', down='lobby',
                            objects=[
                                ('actor', 'Norman Wagner, our killer of opportunity'),
                                ('actress', 'Felicity Diaz, a.k.a. Angelica. Done with this play'),
                                ('theater technician',
                                 """Sam Wright, theatre technician. Young, nervous looking fellow. He looks he will start
                                 screaming at any moment.
                                 
                                 I just checked the rigging yesterday, before today\'s grand rehearsal. It was solid as solid can be.
                                 
                                 I told them to never touch the rigging, I told them many times. Do they listen? No.
                                 I know the controls are not that hard to figure out, but it\'s dangerous anyway.
                                 """),
                            ]),
        InvestigationScreen('corridor 1', 'Non-public part of the theater. Here are dressing rooms for main stars.'
                            '\n             ↑ Reyes ↓ Wagner',
                            up='reyes_dressing_room', down='wagner_dressing_room', left='lobby', right='corridor 2',
                            ),
        InvestigationScreen('corridor 2', 'Non-public part of the theater. Here are dressing rooms for less main stars.'
                            '\n      ↑ Meyer, ↓ Men',
                            up='meyer_dressing_room', down='men_dressing_room', left='corridor 1', right='corridor 3',
                            ),
        InvestigationScreen('corridor 3', 'Non-public part of the theater. Here are dressing rooms for actresses.'
                            '\n             ↑ Diaz, ↓ Women',
                            up='diaz_dressing_room', down='women_dressing_room', left='corridor 2',
                            ),
        InvestigationScreen('reyes_dressing_room', '',
                            down='corridor 1',
                            objects=[
                                ('', ''),
                            ]),
        InvestigationScreen('meyer_dressing_room', '',
                            down='corridor 2',
                            objects=[
                                ('Note',  """'As I promised, we will go with you for the premiere. Norman can be an alter, he\'ll deal.
                                Come to the theater today at the evening, I want to go through the swordplay scene once more before the grand rehearsal.
                                C. """),

                                ('', ''),
                            ]),
        InvestigationScreen('wagner_dressing_room', '',
                            up='corridor 1',
                            objects=[
                                ('Ornate knife', 'Fancy knife with a name etched. It is very well cleaned.'),
                                ('Trash bin', 'Recently cleaned, there is bunch of crumpled papers. On the bottom, there is a cracked memory card'),
                            ]),
        InvestigationScreen('diaz_dressing_room', '', down='corridor 3',),
        InvestigationScreen('men_dressing_room', 'A common dressing room for less prominent male actors.', up='corridor 2'),
        InvestigationScreen('women_dressing_room', 'A common dressing room for less prominent female actors.', up='corridor 3'),

    ]

    graph = build_scenario_graph(screens)

    intro = StoryScreen(next_screen=graph['lobby'],
                        script=[
                            "More ghosts. Or so they say.",
                            "There are two dead at the metro theatre, just before opening the main event of the season.",
                            "With what they pay me, I might even afford a ticket for the thing.",
                        ])

    words = ["-----", ]
    deductions = [
        DeductionScreen("Victim was being drama queen in the {}", words, ["room center"]),
        DeductionScreen("Victim was being drama queen in the {}", words, ["room center"]),
        DeductionScreen("Victim was being drama queen in the {}", words, ["room center"]),


    ]
    build_deduction_links(deductions)

    game_state.setup_game_state(screens, deductions)

    if skip_intro:
        return graph['lobby']
    else:
        return intro



