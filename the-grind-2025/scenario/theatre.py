from screen import InvestigationScreen, StoryScreen, DeductionScreen
import game_state
from .tools import build_scenario_graph, build_deduction_links

def setup_test_scenario(skip_intro=False):

    screens = [
        InvestigationScreen('stage', "The main stage. There are two bodies in full costume and broken prop chandelier",
                            left='backstage', down='auditorium', right='lobby',
                            objects=[
                                ('Roland', 'The body of Carol Reyes, dressed in the full costume of the protagonist Orlando. There is a big bruise on his head,'
                                           ' and his neck is in unnatural position. A bloody sword is lying close to the body'),
                                ('Mador', 'The body of Johannes Meyer, dressed in the costume of Saracen warrior Mador. He has a stab wound in the '
                                          'abdomen, and there is lot of blood.'),
                                ('Bloody sword', 'Near Orlando\'s hand, there is an solid iron sword. Nearly half the blade is covered in blood.'
                                                 'It is still sticky on the underside.'),
                                ('Other sword', 'To the side of Mador lies another iron sword.'),
                            ]),
        InvestigationScreen('auditorium', '',
                            up='stage',
                            objects=[
                                ('Camera', 'Between the seats, there is a collapsed tripod with a video camera. The memory card is missing.')
                            ]),

        InvestigationScreen('prop storage', '',
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
                                                   'a big black came that would make Bram Stoker proud. 
                                                   
                                                   Under the clothes, there is a box with miscenaleous props - pistols, a bible, fake teeth, and
                                                   a bottle of fake blood. Unlike others, the bottle was stored haphazardly and blood residue has stained other props.
                                                   """),
                            ]),

        InvestigationScreen('lobby', '',
                            left='',
                            objects=[
                                ('Poster', 'A poster for upcoming premiere of Orlando Furioso. Photos of Reyes, Wagner and'
                                           'Diaz are displayed prominently as the main trio.'),
                                ('Older posters', 'Posters of many previous plays remain in the lobby. It seems this company favour the classics.'
                                                  'Dracula, Cleopatra, Oedipus Rex, and Le morte d\'Arthur are some of the recent ones.'),
                                ('Newspaper clippings',"""The unlucky play finally prepares for the first opening!
                                
                                The theatre world has just recovered after a tragic death of Daniel Rider, who suffered a tragic accident
                                on the night of the general rehearsal of the newest interpretation of Orlando Furioso. His indomitable
                                colleagues are not coved by hostile fate, and the renewed opening is expected in the upcoming days.
                                The replacement actor turned new main star, Carol Reyes, seems not too perturbed by the
                                rumors of the script being cursed.
                                
                                If any ghosts are interested in the play, I invite them to the grand opening. All the rest of you are
                                cordially invited too, of course.
                                
                                Reyes and his long-standing rivalry with Rider has long been known in the tabloid world, but
                                that reportedly never impacted their professional collaboration. < more juicy details on page 5 >"""),
                            ]),
    ]

    graph = build_scenario_graph(screens)

    intro = StoryScreen(next_screen=graph['1'],
                        script=[
                            "",

                        ])

    words = ["-----", ]
    deductions = [
        DeductionScreen("Victim was being drama queen in the {}", words, ["room center"]),


    ]
    build_deduction_links(deductions)

    game_state.setup_game_state(screens, deductions)

    if skip_intro:
        return graph['lobby']
    else:
        return intro



