import ScenariosFunctions as scfun
import os

foldername = 'srt_scenarios'

if not os.path.exists(foldername):
    os.makedirs(foldername)

file_path = 'scene12_take1.srt'

# scenario 1: contract distances and shrink durations
shifttime = {'mean': -1.0, 'std': 0.5}
durationtime = {'mean': 0.7, 'std': 0.2}
scfun.modifyTime(file_path, shifttime=shifttime, durationtime=durationtime, durationfirst=True, srtfile_out=foldername + os.sep + 'shrink_time_1.srt')

# scenario 2: contract distances and shrink durations
shifttime = {'mean': -2.0, 'std': 0.5}
durationtime = {'mean': 0.5, 'std': 0.2}
scfun.modifyTime(file_path, shifttime=shifttime, durationtime=durationtime, durationfirst=True, srtfile_out=foldername + os.sep + 'shrink_time_2.srt')

# scenario 3: expand distances and dialate durations
shifttime = {'mean': 1.0, 'std': 0.5}
durationtime = {'mean': 1.3, 'std': 0.2}
scfun.modifyTime(file_path, shifttime=shifttime, durationtime=durationtime, durationfirst=True, srtfile_out=foldername + os.sep + 'expand_time_1.srt')

# scenario 4: expand distances and dialate durations
shifttime = {'mean': 2.0, 'std': 0.5}
durationtime = {'mean': 1.5, 'std': 0.2}
scfun.modifyTime(file_path, shifttime=shifttime, durationtime=durationtime, durationfirst=True, srtfile_out=foldername + os.sep + 'expand_time_2.srt')

# scenario 5: perturb distances and dialate durations
shifttime = {'mean': 0.0, 'std': 0.5}
durationtime = {'mean': 1.0, 'std': 0.2}
scfun.modifyTime(file_path, shifttime=shifttime, durationtime=durationtime, durationfirst=True, srtfile_out=foldername + os.sep + 'perturb_time_1.srt')

# scenario 6: perturb distances and dialate durations
shifttime = {'mean': 0.0, 'std': 1.0}
durationtime = {'mean': 1.0, 'std': 0.5}
scfun.modifyTime(file_path, shifttime=shifttime, durationtime=durationtime, durationfirst=True, srtfile_out=foldername + os.sep + 'perturb_time_2.srt')

# scenario 7: switch 10
scfun.switchLines(file_path, switch_rate=10, randomness=2, srtfile_out=foldername + os.sep + 'switch_10.srt')

# scenario 8: switch 5
scfun.switchLines(file_path, switch_rate=5, randomness=1, srtfile_out=foldername + os.sep + 'switch_5.srt')

# scenario 9: perturb and switch 10
scfun.switchLines(foldername + os.sep + 'perturb_time_2.srt', switch_rate=10, randomness=2, srtfile_out=foldername + os.sep + 'switch_10_peturb_2.srt')

# scenario 10: perturb and switch 5
scfun.switchLines(foldername + os.sep + 'perturb_time_2.srt', switch_rate=5, randomness=1, srtfile_out=foldername + os.sep + 'switch_5_perturb_2.srt')
