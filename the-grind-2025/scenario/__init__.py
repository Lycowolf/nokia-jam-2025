from . import tutorial, haunted_mansion, investigation_test, power_plant, theatre

cases = [
    ('Tutorial', tutorial.setup_scenario),
    ('Haunted mansion', haunted_mansion.setup_scenario),
    ('Deadly theatrics', theatre.setup_scenario),
    ('Power Plant', power_plant.setup_scenario)
]
