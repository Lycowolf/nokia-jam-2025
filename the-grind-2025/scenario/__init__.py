from . import tutorial, haunted_mansion, investigation_test, power_plant

cases = [
    ('Tutorial', tutorial.setup_scenario),
    ('Haunted mansion', haunted_mansion.setup_scenario),
    ('Deadly theatrics', investigation_test.setup_test_scenario),
    ('Power Plant', power_plant.setup_scenario)
]
