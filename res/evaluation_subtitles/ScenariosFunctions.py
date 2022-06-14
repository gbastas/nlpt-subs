import pysrt
import numpy as np

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