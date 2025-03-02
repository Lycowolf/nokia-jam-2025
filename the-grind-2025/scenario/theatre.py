from screen import InvestigationScreen, StoryScreen, DeductionScreen
import game_state
from .tools import build_scenario_graph, build_deduction_links

def setup_scenario(skip_intro=False):

    screens = [
        InvestigationScreen('stage', "The main stage prepared for a play. There are two bodies in full costume, swords, and broken prop chandelier to the side.",
                            left='backstage', down='auditorium', right='lobby',
                            objects=[
                                ('Stage', 'The stage is set for epic sword fight scene. Set pieces are placed and the stage lights are still on.'),
                                ('Orlando', 'The body of Reyes, dressed in the full costume of the protagonist Orlando. There is a big bruise on his head,'
                                           'some lacerations, and his neck is in unnatural position. A bloody sword is lying close to the body'),
                                ('Mador', 'This body is Meyer, dressed in the costume of Saracen warrior Mador. He has a stab wound in the '
                                          'abdomen, and there is lot of blood.'),
                                ('Bloody sword', 'Near Orlando\'s hand, there is an solid iron sword. Nearly half the blade is covered in blood.'
                                                 'It is still sticky on the underside.'),
                                ('Other sword', 'To the side of Mador lies another iron sword.'),
                                ('Broken chandelier', 'On the side, there is an unreasonably massive and fancy prop chandelier. It is broken, but the rope'
                                                      'that was holding it seems intact.'
                                                      'It was moved when they discovered the body. One of the spokes is bent and there'
                                                      'are noticeable traces of impact. ')
                            ]),
        InvestigationScreen('backstage', 'The space behind the curtain. Not much props here, surprisingly. There are controls for operating the rigging.',
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

        InvestigationScreen('auditorium', 'An empty auditorium. No one in the seats. This place feels wrong when it is this empty.',
                            up='stage',
                            objects=[
                                ('Under the seats ...', 'Between the seats, there is a collapsed tripod with a video camera. The memory card is missing.')
                            ]),

        InvestigationScreen('prop storage', 'Prop storage room. All kings of theatre props are stored here. How can anyone find anything?',
                            right='backstage',
                            objects=[
                                ('Room', 'A respectable-sized room with big mess inside. Most accessed stuf is kept in order, but older props are just laying in heaps.'),
                                ('Sword cabinet', """The theater has impressive selection of prop swords. Medieval german swords,
                                                  Renaissance rapiers, even Turkish saber and some fantasy pieces straight out of Lord of the Rings.
                                                  All of them are the safety type, either collapsible or foam. Even full-force hit by those would not
                                                  cause serious hurt, but a bruise is still possible if care is not taken."""),
                                ('Old wooden chest', """There is an old chest. Inside are pieces of a knight costumes - chainmail armor, tabards,'
                                                     'and an unusually realistic crown. On the top, there are two leather sword sheathes. These are empty.
                                                     
                                                     The chest is covered in dust, but was opened recently."""),
                                ('Opened dresser', """One of the big dressers is partially open. Inside there is bunch of victorian clothing and, prominently,'
                                                   'a big black cape that would make Bram Stoker proud.
                                                   
                                                   Under the clothes, there is a box with miscellaneous props - pistols, a bible, fake teeth, and
                                                   a bottle of fake blood. Unlike others, the bottle was stored haphazardly and blood residue has stained other props.
                                                   """),
                            ]),

        InvestigationScreen('lobby', 'Theatre lobby. Standees and posters galore. An easy-going policeman is waiting for you.',
                            left='stage', right='corridor 1', up='bar',
                            objects=[
                                ('Poster', 'A poster for upcoming premiere of Orlando Furioso. Photos of Reyes(Orlando), Wagner(Modor) and'
                                           'Diaz(Angelica) are displayed prominently as the main trio.'),
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
                                that reportedly never impacted their professional collaboration. More juicy details on page 5."""),
                                ('Policeman', """Hello, Mr. Ericsson. Glad to have you here. It's those ghosts again, am I right?
                                We won't be able to do much investigating if they are. You can't exactly put cuffs on a spectre, right?
                                
                                Anyway the personnel is in the bar, anyone who was in this early. That jumpy young guy, Wright,
                                has found the body. He seems a talkative type, I figure he's trying to talk his way out of something.
                                But maybe not, if it were the ghosts then?  
                                """),
                            ]),
        InvestigationScreen('bar', 'Bar. The theatre personnel are gathered here.', down='lobby',
                            objects=[
                                ('Actor', """Norman Wagner. Does not look like a leading man.
                                    He looks tired - he is leaning on the bar.
                                    - is favoring one side, has a bruise on the chest
                                    - says he got it during practice yesterday, but no big deal
                                """),
                                ('Actress', """The main 
                                Felicity Diaz, a.k.a. Angelica. Totally done with this play
                                
                                - THe play is cursed and was never a good idea. Lots of problems. Better to cut losses and do something else.
                                - Rider was very hung on the Orlando role
                                - Rider and Reyes were very combative. They could shove it during the play, but practices were bad.
                                - Wagner was a weirdo who tended to visit the theater at night, for "atmosphere". More so after the accident
                                - I think Rider and Wagner were an item? That were the rumors anyway
                                - Regardless, Wagner took his death very badly 
                                 
                                """),
                                ('Theater technician',
                                 """Sam Wright, theatre technician. Young, nervous looking fellow. He looks he will start
                                 screaming at any moment.
                                 
                                 I just checked the rigging yesterday, before today\'s grand rehearsal. It was solid as solid can be.
                                 
                                 I told them to never touch the rigging, I told them many times. Do they listen? No.
                                 I know the controls seem not that hard, but it\'s dangerous anyway.
                                 
                                 Yes, it's only me who can do the rigging now. Rider, the last star, could do it himself.
                                 Had all hte permits, too/ The man could do anything, it seems. Stunts, tech, you name it. 
                                 Really bad we lost him, there is really not another like him.
                                 
                                 Do you know he was really looking forward to this role? He wanted it for years, they say.
                                 Seems like the play was his big project. He almost forced it to happen.
                                 Was very peculiar about it, too. Have you heard we almost didn't have an alternation for Orlando?
                                 He was super fussy about all the candidates, no one was good enough. Almost screamed at Reyes
                                 once, YOU SHALL NEVER HAVE IT, full on Uther with Excalibur, if you know what I mean. 
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
        InvestigationScreen('reyes_dressing_room', 'The dressing room of Carol Reyes, the main star. There is a bag on the floor.'
                                                   'Someone was changing here recently.',
                            down='corridor 1',
                            objects=[
                                ('Empty clothes rack', 'Empty costume rack in the dresser. It is labelled Orlando'),
                                ('Bag', 'A sports bag with a change of clothes.'),
                                ('Note', """'All right, I'll be there. Let's take a cam and record it, too. You will have easier time
                                with the head honcho if you can show him how much better Saracen I make."""),
                                ('Suspicious note', """In the trash, there is crumpled note. It is made by cutout letters from a newspaper,
                                                    movie kidnapper-style.
                                                    
                                                    Drop the role, YOU are NOT worthy of it. IF YOU do not, there will be CONSEQUENCES!!!
                                                    """),
                            ]),
        InvestigationScreen('meyer_dressing_room', 'A dressing room of Johannes Meyer. It is notably less spacious than the previous ones.'
                                                   'Someone was changing here recently.',
                            down='corridor 2',
                            objects=[
                                ('Empty clothes rack', 'Empty costume rack is standing in the room. It is labelled Modor'),
                                ('Rucksack', 'A rucksack with a change of clothes.'),
                                ('Note',  """'As I promised, we will go with you for the premiere. Norman can be an alter, he\'ll deal.
                                Come to the theater today at the evening, I want to go through the swordplay scene once more before the grand rehearsal.
                                C. """),
                            ]),
        InvestigationScreen('wagner_dressing_room', 'The dressing room of Norman Wagner. Feels like he never left.',
                            up='corridor 1',
                            objects=[
                                ('Room', 'This room seems used, like someone left in the middle of the work.'
                                         'Things are orderly, but not tidied.'),
                                ('Dresser', 'There is a big gap in the dresser. A whole costume rack is missing there.'),
                                ('Ornate knife', 'In the desk drawer, there is a fancy knife with an etched Wagner\'s name. It is very well cleaned.'),
                                ('Trash bin', 'Recently cleaned, there is bunch of crumpled papers and torn newspapers.'
                                              'On the bottom, there is a broken memory card'),
                            ]),
        InvestigationScreen('diaz_dressing_room', 'The dressing room of Felicity Diaz. Unusually subdued for a main female star.',
                            down='corridor 3',
                            objects=[
                                ('Room', 'This room is neat and tidy. Was it visited today at all?')
                            ]),
        InvestigationScreen('men_dressing_room', 'A common dressing room for less prominent male actors.', up='corridor 2'),
        InvestigationScreen('women_dressing_room', 'A common dressing room for less prominent female actors.', up='corridor 3'),
    ]

    graph = build_scenario_graph(screens)

    intro = StoryScreen(next_screen=graph['lobby'],
                        script=[
                            "More ghosts. Or so they say. The police were more that happy with my previous results. It seems they want seconds.",
                            "There are two dead at the metro theatre, just before opening the main event of the season.",
                            "And looks like I am the man to go there, remove the problem, wrap it in a neat bow ...",
                            "Change an inconvenient murder into a ghastly spectacle. No pun intended.",
                            "But it seems like I am the only one to take this seriously. Of course I'll go.",
                            "With what they pay me, I might even afford a ticket for the opening night.",
                        ])

    words = ["-----", 'Felicity', 'Diaz', 'Norman', 'Wagner', 'Johannes', 'Meyer', 'Carol', 'Reyes', 'Daniel', 'Rider', 'Sam', 'Wright',
             'theatre', 'practice', 'duel', 'swordplay scene', 'observed', 'killed', 'prohibited', 'mope', 'camera', 'chandelier',
             'rigging controls', 'rigging pulley',  'ghost', 'fall', 'death', 'head', 'chest', 'abdomen', 'leg', 'washed', 'swapped', 'prop sword',
             'real', 'knife', 'storage', 'memory card', 'fake blood', 'removed', 'accident', 'supervision']
    deductions = [
        DeductionScreen("In the evening before grand rehearsal, {} {} asked {} {} to meet at the {} in secret to {} the {}. ", words,
                        ['Carol', 'Reyes', 'Johannes', 'Meyer', 'theatre', 'practice', 'swordplay scene']),
        DeductionScreen("Unknowingly, they were {} by {} {} who was at the {} to {}.", words,
                        ['observed', 'Norman', 'Wagner', 'theatre', 'mope']),
        DeductionScreen("{} {} recorded the scene on {}. To get better recording, they practiced in full costume and"
                        "set up the props, including the big {}. They operated the {} despite being {} by {} {}.", words,
                        ['Carol', 'Reyes', 'camera', 'chandelier', 'rigging controls', 'prohibited', 'Sam', 'Wright']),
        DeductionScreen("During the {}, the {} of {} {} interfered with the {}, which caused the {} to {}. "
                        "It struck {} {} in the {}, causing his {}.", words,
                        ['practice', 'ghost', 'Daniel', 'Rider', 'rigging pulley', 'chandelier', 'fall', 'Carol', 'Reyes', 'head', 'death']),
        DeductionScreen("At that moment, {} {} ran to the {}. They confronted {} {}, altercation ensued, during which they drew {}."
                        "They were hit by {} in the {}, and their opponent was struct by {} in the {}. ", words,
                        ['Norman', 'Wagner', 'stage', 'Johannes', 'Meyer', 'knife', 'prop sword', 'chest', 'knife', 'abdomen']),
        DeductionScreen("After that, they wanted to {} their deed. They {} the murder weapon, {} each {} for a {} one from the {},"
                        " and placed {} on one to {} the change.", words,
                        ["hide", 'washed', 'swapped', 'prop sword', 'real', 'storage', 'fake blood', 'hide']),
        DeductionScreen("They also noticed the {}, shoved it aside, and {} the {}.", words,
                        ['camera', 'removed', 'memory card']),
        DeductionScreen("In the morning, {} {} discovered the bodies. At first, {} was suspected, because"
                        " {} were handled without {}.", words,
                        ['Sam', 'Wright', 'accident', 'rigging controls', 'supervision']),
        DeductionScreen("Summary: First victim was {} {}. They were killed with {} by {} {}.", words,
                        ['Carol', 'Reyes', 'chandelier', 'Daniel', 'Rider']),
        DeductionScreen("Summary: Second victim was {} {}. They were killed with {} by {} {}.", words,
                        ['Johannes', 'Meyer', 'knife', 'Norman', 'Wagner']),
        DeductionScreen('Supernatural {} involved. {} {} was a {}.',
                        ['-----', 'was', 'was not', 'The first', 'The second', 'killer', 'victim', 'poltergeist', 'normal human', 'phantom of the opera'],
                        ['was', 'The first', 'killer', 'poltergeist'])
    ]
    build_deduction_links(deductions)

    game_state.setup_game_state(screens, deductions)

    if skip_intro:
        return graph['lobby']
    else:
        return intro



