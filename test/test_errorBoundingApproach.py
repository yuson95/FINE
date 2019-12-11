import pandas as pd

def test_errorBoundingApproach(minimal_test_esM):
    '''
    Get the minimal test system, and check if the Error-Bounding-Approach works for it
    '''

    # modify the minimal LP and change it to a MILP
    esM = minimal_test_esM

    # get the components with capacity variables
    electrolyzers = esM.getComponent('Electrolyzers')
    pressureTank = esM.getComponent('Pressure tank')

    # set binary variables and define bigM
    electrolyzers.hasIsBuiltBinaryVariable = True
    pressureTank.hasIsBuiltBinaryVariable = True

    electrolyzers.investIfBuilt = pd.Series(2e5, index = esM.locations)
    pressureTank.investIfBuilt = pd.Series(1e5, index = esM.locations)

    electrolyzers.bigM = 30e4
    pressureTank.bigM = 30e6

    # optimize with 2 Stage Approach
    esM.optimizeErrorBoundingApproach(relaxed=True, solver = 'glpk', numberOfTypicalPeriods=2, numberOfTimeStepsPerPeriod=1)

    # get gap
    gap=esM.gap

    assert gap > 0.1078 and gap < 0.1079