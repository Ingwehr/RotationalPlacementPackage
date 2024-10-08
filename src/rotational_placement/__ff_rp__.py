import numpy as np

def ffRotationalPlacement(a: int, b: int, max_radius: int, step_size: int, exp) -> None: 
    '''
    DESCRIPTION
    -----------
    mathematically derives the approximate amount of seeds within a given radius (maxRadius) and collects data with a specified interval (stepSize) between data points 
    
    PARAMETERS
    ----------
    a: int
        numerator of input
    b: int
        denominator of input
    maxRadius: int
        termination point for interval
    stepSize: int
        interval between data points, resolution of data
    exp: Experiment
        instance of Experiment, data will be added to this instance
    
    RETURNS
    -------
    dataDict: dict[list[float]]
        dict with radii and corresponding efficacies in two separate lists
    '''

    def __add_segment__(a: int, b: int, segments: list[dict[str,float]]):
        '''
        DESCRIPTION
        -----------
        returns the next coming segment using cool math

        PARAMETERS
        ----------
        a: int
            numerator of input
        b: int
            denominator of input
        segments: list[dict[str,float]]
            list of previously added segments
        maxRadius: int
            termination point for experiment

        RETURNS
        -------
        segment: dict[str,float]
            the next segment to be appended to segments 
        '''
        
        number_of_arcs = 1

        arc_angle = 2 * np.pi * ((number_of_arcs * a / b) % 1)

        if arc_angle > np.pi: 
            arc_angle = 2 * np.pi - arc_angle

        while arc_angle > 2 * np.arcsin(1 / segments[-1]['segmentRadius']):
            number_of_arcs += 1
            arc_angle = 2 * np.pi * ((number_of_arcs * a / b) % 1)
            if arc_angle > np.pi: 
                arcAngle = 2 * np.pi - arc_angle

        segment_radius = 2 / np.sin(arc_angle)
        arc_quotient = ((segment_radius + 1)**2-(segment_radius - 1)**2 + (segment_radius * np.sin(np.pi / number_of_arcs))**2) / ((2 * segment_radius * np.sin(np.pi / number_of_arcs)) * (segment_radius + 1))
        arc_span = np.arccos(arc_quotient) + np.pi/2
        seeds_per_arc = round(arc_span / (2 * arcAngle))

        segment = {'numberOfArcs':number_of_arcs,
                   'arcAngle':arcAngle,
                   'segmentRadius':segment_radius,
                   'arcQuotient':arc_quotient,
                   'arcSpan':arc_span,
                   'seedsPerArc':seeds_per_arc,
                   'segmentEfficacy':seeds_per_arc * number_of_arcs}

        return segment

    def __truncate_segment__(current_segment: dict[str,float], previous_segment: dict[str,float], current_radius: int): 
        '''
        DESCRIPTION
        -----------
        calculates teh amount of seeds in a part of a segment and returns that number 

        PARAMETERS
        ----------
        currentSegment: dict[str,float]
            the segment being truncated
        previousSegment: dict[str,float]
            the segment before the one being truncated
        currentRadius: int
            where currentSegment is being "cut off"
        '''
        '''
        R_old (previousSegmentRadius): 
        R_new (currentSegmentRadius): 
        R_max (currentRadius):
        '''

        reduction_angle = 2 * np.arcsin(previous_segment['segmentRadius'] / current_segment['segmentRadius'])
        truncation_angle = 2 * np.arcsin(current_radius / current_segment['segmentRadius'])

        truncated_seeds = round((truncation_angle - reduction_angle) / (2 * current_segment['arcAngle']))
        
        return truncated_seeds

    radiusEventHorizon = 1 / np.sin(np.pi / b)

    #construct list of segments
    #the first segment has fewer properties than the ones that are added
    segments = [{'segment_radius':2,'segment_efficacy':1}]

    if max_radius < radiusEventHorizon: 
        while segments[-1]['segment_radius'] < max_radius: 
            segments.append(__add_segment__(a,b,segments))
    else: 
        while segments[-1]['segment_radius'] < radiusEventHorizon: 
            segments.append(__add_segment__(a,b,segments))
        
        #create segment from radiusEventHorizon to maxRadius with spokes 
        segment = {'number_of_arcs': b,
                   'arc_angle': 0,
                   'segment_radius': max_radius,
                   'arc_quotient': ((max_radius + 1)**2-(max_radius - 1)**2 + (max_radius * np.sin(np.pi / max_radius))**2) / ((2 * max_radius * np.sin(np.pi / max_radius)) * (max_radius + 1)),
                   'arc_span': max_radius,
                   'seeds_per_arc': (max_radius - segments[-1]['segmentRadius']) / 2}
        
        segments.append(segment)
    
    #collect data 
    dataDict = {'radius':[], 'efficacy':[]}

    for current_radius in range(2,max_radius,step_size): 
    
        for i,segment in enumerate(segments):
    
            if segment['segmentRadius'] > current_radius: 
                efficacy = 0
                for segment in segments[:i]: 
                    efficacy += segment['segmentEfficacy']
                efficacy += __truncate_segment__(segments[i],segments[i-1],current_radius)
                break
    
        dataDict['radius'].append(current_radius)
        dataDict['efficacy'].append(efficacy)
    
    return dataDict
