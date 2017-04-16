import numpy as np
import scipy as sp
import stf


def blank_artifact(method='quad'):
    """
    This function requires the latency cursors to be set. It corrects the 
    artifact located between the cursors based on the method specified by the 
    user. 
    
    :: Params ::
    
    method = ['zero', 'linear', 'quad']
        -'zero' replaces the artefact with zeros
        
        -'linear' replaces the artifact wtih a line connecting the two points at 
        either end
        
        -'quad' performs a quadratic interpolation to infer the data
    
    :: Output ::
    
    A new window with the blanked data
    """

def multi_baseline():
    """
    This function requires baseline cursors to be set at the first baseline 
    point, and latency cursors to be set at the second baseline point. It will 
    return a new window with the region between the cursers, proportionally
    baselined. 
    i.e. it takes the difference between the first and second baseline, and 
    then baselines every point with a weighted subtraction
    """