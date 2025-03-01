from .transition import Transition
from .search_menu import SearchMenuScreen

items = [
    ("Detective", """Niel Ericsson, a detective for hire.
        I'm an old-school guy in an old-school profession.
        My phone is so old it can take calls from beyond the veil.
        That's why I'm stuck taking ghost cases.
        
        Also, I don't like talking to living people. Can't you just text?
        """),
    ("Ghosts", """Ghosts or poltergeists are lingering spirits that hold a grudge.
        They are keen on doing harm to those who wronged them or anyone unlucky enough to be around.
        Basically, they are murderous assholes.
        
        Unlike human murderous assholes, they can do impossible feats.
        If we can eliminate possibility of human causes, it was probably a ghost.  
        """),
    ("When & where", """Present day. present time. 
        """),
]

def show_encyclopedia(prev_screen):
    lore_screen = SearchMenuScreen(prev_screen, items)
    return Transition(prev_screen, lore_screen, fade_label="Encyclopedia")