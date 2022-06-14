import pysrt
import numpy as np
import matplotlib.pyplot as plt

def interval_intersection(x,y):
    s = max(x[0],y[0])
    e = min(x[1],y[1])
    return max( e-s , 0 )
# end interval_intersection

def interval_union(x,y):
    s = min(x[0],y[0])
    e = max(x[1],y[1])
    l = x[1]-x[0] + y[1]-y[0]
    return min( e-s , l )
# end interval_union

def subs_babatsikizer( spath, srtfile_out=None ):
    s = pysrt.open(spath)
    max_added_time = 1000
    min_inter_sub = 50
    if srtfile_out is None:
        srtfile_out = 'test.srt'
    for i in range(len( s )):
        added_time = max_added_time
        if i < len(s) - 1:
            added_time = min( max_added_time, s[i+1].start.ordinal - s[i].end.ordinal - min_inter_sub )
        s[i].end = pysrt.SubRipTime.from_ordinal( s[i].end.ordinal + added_time )
    s.save( srtfile_out , encoding='utf-8' )
# end subs_babatsikizer


def get_iou_stats( gpath , xpath ):
    # gpath: ground truth file path
    # xpath: new subtitles path
    # the assumption is that x includes text that already exist in g
    # 
    # load subtitles
    g = pysrt.open(gpath)
    x = pysrt.open(xpath)
    # keep texts
    gtext = []
    xtext = []
    # initialize ious
    ious = []
    for t in g:
        gtext.append( t.text )
    for t in x:
        xtext.append( t.text )
    # print(gtext)
    # print(xtext)
    ious = []
    coverage = []
    redundance = []
    all_idxs = []
    # for each subtitle text in g, find respective index in x
    for ig, t in enumerate(gtext):
        idxs = []
        for i, tt in enumerate( xtext ):
            if tt == t:
                idxs.append( i )
        # run iou for each found subtitle
        tmp_intersection = 0
        tmp_union = g[ig].end.ordinal - g[ig].start.ordinal
        i2 = [ g[ig].start.ordinal , g[ig].end.ordinal ]
        tmp_iou = 0
        tmp_coverage = 0
        tmp_redundance = 0
        # print('-------------------------------', ig)
        # print('gt: ', g[ig].start.ordinal, g[ig].end.ordinal)
        for i in idxs:
            i1 = [ x[i].start.ordinal , x[i].end.ordinal ]
            tmp_intersection += interval_intersection( i1, i2 )
            tmp_union += i2[1]-i2[0] - interval_intersection( i1, i2 )
            tmp_coverage += interval_intersection( i1, i2 )
            tmp_redundance += interval_intersection( i1, [0, i2[0]] ) + interval_intersection( i1, [i2[1], g[-1].end.ordinal] )
            # print('x: ', x[i].start.ordinal, x[i].end.ordinal)
        if tmp_union > 0:
            tmp_iou = tmp_intersection/tmp_union
        ious.append( tmp_iou )
        if i2[1]-i2[0] > 0:
            coverage.append( tmp_coverage/(i2[1]-i2[0]) )
            redundance.append( tmp_redundance/(i2[1]-i2[0]) )
        all_idxs.append( idxs )
    stats = {
        'iou': {
            'mean': np.mean(ious),
            'std': np.std(ious)
        },
        'coverage': {
            'mean': np.mean(coverage),
            'std': np.std(coverage)
        },
        'redundance': {
            'mean': np.mean(redundance),
            'std': np.std(redundance)
        }
    }
    subs_info = {
        'g': g,
        'x': x,
        'gtext': gtext,
        'xtext': xtext,
        'all_idxs': all_idxs
    }
    return ious, stats, subs_info
# end get_iou_stats



def modifyDuration(realsubs, durationtime=None):
    # durationtime: dictionary with mean and std percentage for changing subtitle duration
    if durationtime is None:
        durationtime = {'mean': 1, 'std': 0}
    for i, s in enumerate(realsubs):
        # original duration
        original_duration = s.end - s.start
        # modify duration
        t = np.random.normal( durationtime['mean'], durationtime['std'] )
        # check distance from next
        if i < len(realsubs)-1:
            max_allowed = realsubs[i+1].start - s.start
        else:
            max_allowed = pysrt.SubRipTime.from_ordinal(1000000)
        new_duration = min(t*original_duration.ordinal, max_allowed.ordinal)
        realsubs[i].end = pysrt.SubRipTime.from_ordinal(realsubs[i].start.ordinal + new_duration)
    return realsubs
# end modifyDuration

def modifyInterDistance(realsubs, shifttime=None):
    # shifttime: dictionary with mean and std time (secs) for shifting starting and ending times of each subtitle.
    if shifttime is None:
        shifttime = {'mean': 0, 'std': 0}
    # if negative mean, start from the beginning to the end
    # if positive mean, start from end to the beginning
    direction = 1
    start_idx = 0
    end_idx = len(realsubs)
    if shifttime['mean'] > 0:
        direction = -1
        start_idx = len(realsubs) - 1
        end_idx = -1
    for i in range(start_idx, end_idx, direction):
        t = np.random.normal( shifttime['mean'], shifttime['std'] )
        # check conflict with previous
        if i > 0:
            t = max( t , -(realsubs[i].start.ordinal-realsubs[i-1].end.ordinal)/1000 )
        else:
            t = max( t , -(realsubs[i].start.ordinal-0)/1000 )
        # check conflict with next
        if i < len(realsubs)-1:
            t = min( t , -(realsubs[i].end.ordinal-realsubs[i+1].start.ordinal)/1000 )
        realsubs[i].shift( seconds=t )
    return realsubs
# end modifyDuration

def modifyTime(srtfile_in, shifttime=None, durationtime=None, srtfile_out=None, durationfirst=True):
    # strfile_in: file path to input srt file
    # shifttime: dictionary with mean and std time (secs) for changing starting times between subtitles.
    if shifttime is None:
        shifttime = {'mean': 0, 'std': 0}
    # durationtime: dictionary with mean and std percentage for changing subtitle duration
    if durationtime is None:
        durationtime = {'mean': 1, 'std': 0}
    # srtfile_out: file path of output srt
    if srtfile_out is None:
        srtfile_out = 'test.srt'
    realsubs = pysrt.open( srtfile_in )
    if durationfirst:
        realsubs = modifyDuration(realsubs, durationtime=durationtime)
        realsubs = modifyInterDistance(realsubs, shifttime=shifttime)
    else:
        realsubs = modifyInterDistance(realsubs, shifttime=shifttime)
        realsubs = modifyDuration(realsubs, durationtime=durationtime)
    realsubs.save( srtfile_out , encoding='utf-8' )
# end modifyTime

def switchLines(srtfile_in, switch_rate=None, randomness=None, srtfile_out=None):
    # switch_rate: after how many subtitles to switch
    # randomness: +- how many subtitles from switch_rate
    # srtfile_out: file path of output srt
    if srtfile_out is None:
        srtfile_out = 'test.srt'
    realsubs = pysrt.open( srtfile_in )
    i = 0
    while i < len( realsubs )-1:
        t = int( np.ceil( np.random.normal( switch_rate, randomness ) ) )
        t = max(2, t)
        t = min(t, len( realsubs )-1 - i)
        if i+t > len(realsubs)-2:
            break
        tmp_text = realsubs[i+t].text
        realsubs[i+t].text = realsubs[i+t+1].text
        realsubs[i+t+1].text = tmp_text
        i += t
    realsubs.save( srtfile_out , encoding='utf-8' )
# end switchLines

def plot_time_diffs( gpath , xpath , fig_name='test.png', boxplot_fig_name=None, markers=None ):
    # load subtitles
    g = pysrt.open(gpath)
    x = pysrt.open(xpath)
    # keep texts
    gtext = []
    xtext = []
    # initialize ious
    ious = []
    for t in g:
        gtext.append( t.text )
    for t in x:
        xtext.append( t.text )
    # print(gtext)
    # print(xtext)
    start_x = []
    start_y = []
    end_x = []
    end_y = []
    # for each subtitle text in g, find respective index in x
    for ig, t in enumerate(gtext):
        idxs = []
        for i, tt in enumerate( xtext ):
            if tt == t:
                idxs.append( i )
        # run iou for each found subtitle
        # tmp_start = x[idxs[0]].start.ordinal
        tmp_start_diff = abs(x[idxs[0]].start.ordinal - g[ig].start.ordinal)
        # tmp_end = x[idxs[0]].end.ordinal
        tmp_end_diff = abs(x[idxs[0]].end.ordinal - g[ig].end.ordinal)
        for i in range(len(idxs)):
            # print('--------------------------------------------------')
            # print('len(x): ', len(x))
            # print('idxs: ', idxs)
            # print('ig - idxs[i]: ', ig, ' - ', idxs[i])
            # print('tmp_start_diff: ', tmp_start_diff)
            # print('x: ', x[idxs[i]])
            # print('g: ', g[ig])
            if abs(x[ idxs[i] ].start.ordinal - g[ig].start.ordinal) <= tmp_start_diff:
                # tmp_start = x[ idxs[i] ].start.ordinal
                tmp_start_diff = abs(x[ idxs[i] ].start.ordinal - g[ig].start.ordinal)
                # tmp_end = x[ idxs[i] ].end.ordinal
                tmp_end_diff = abs(x[ idxs[i] ].end.ordinal - g[ig].end.ordinal)
        start_x.append( g[ig].start.ordinal/1000 )
        start_y.append( tmp_start_diff/1000 )
        end_x.append( g[ig].end.ordinal/1000 )
        end_y.append( tmp_end_diff/1000 )
    plt.clf()
    plt.plot( start_x, start_y, 'bo' )
    plt.plot( end_x, end_y, 'rx' )
    if markers is not None:
        marker_keys = list(markers.keys())
        marker_values = list(markers.values())
        marker_y = np.max(start_y)
        for i in range(len(marker_keys)):
            plt.text( marker_values[i], marker_y, marker_keys[i] )
            plt.plot( [marker_values[i],marker_values[i]], [0,marker_y], 'k-' )
            marker_y *= 0.9
    plt.savefig(fig_name, dpi=300)
    if boxplot_fig_name is not None:
        plt.clf()
        plt.boxplot( [start_y, end_y] )
        plt.xticks([1, 2], ['start', 'end'])
        plt.savefig(boxplot_fig_name, dpi=300)
    start_y = np.array( start_y )
    end_y = np.array( end_y )
    start_y_no_outliers = start_y[start_y < 7.0]
    end_y_no_outliers = end_y[end_y < 7.0]
    return {
        'start':{
            'mean': np.mean( np.abs( start_y ) ),
            'std': np.std( np.abs( start_y ) ),
            'median': np.median( np.abs( start_y ) ),
        },
        'end':{
            'mean': np.mean( np.abs( end_y ) ),
            'std': np.std( np.abs( end_y ) ),
            'median': np.median( np.abs( end_y ) ),
        },
        'start_no_outliers':{
            'mean': np.mean( np.abs( start_y_no_outliers ) ),
            'std': np.std( np.abs( start_y_no_outliers ) ),
            'median': np.median( np.abs( start_y_no_outliers ) ),
        },
        'end_no_outliers':{
            'mean': np.mean( np.abs( end_y_no_outliers ) ),
            'std': np.std( np.abs( end_y_no_outliers ) ),
            'median': np.median( np.abs( end_y_no_outliers ) ),
        },
        'all': {
            'start': start_y,
            'end':  end_y,
            'start_no_outliers': start_y_no_outliers,
            'end_no_outliers':  end_y_no_outliers
        }
    }
# end plot_tim_diffs