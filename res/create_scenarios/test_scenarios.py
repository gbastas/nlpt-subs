import ScenariosFunctions as scfun

file_path = 'scene12_take1.srt'

# example 1: contract distances and shrink durations
shifttime = {'mean': -1.0, 'std': 0.5}
durationtime = {'mean': 0.7, 'std': 0.2}

# # example 2: expand distances and dialate durations
# shifttime = {'mean': 1.0, 'std': 0.5}
# durationtime = {'mean': 1.3, 'std': 0.2}

scfun.modifyTime(file_path, shifttime=shifttime, durationtime=durationtime, durationfirst=True, srtfile_out='test_time.srt')

scfun.switchLines(file_path, switch_rate=5, randomness=1, srtfile_out='test_switch.srt')
