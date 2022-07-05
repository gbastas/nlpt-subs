#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 07:25:47 2022

@author: max
"""

import SubtitlesEvaluation as se

# gpath = 'res/gt_scene12_take1.srt'
# gpath = 'res/gt_scene12_take2.srt'
# gpath = 'res/googleASR/output.srt'
# gpath = 'res/generic_LM_gb/output.srt'
# gpath = 'res/littleprince_specific_LM/output.srt'

spath = 'res/gt_scene12_take2.srt'
se.subs_babatsikizer( spath, srtfile_out='res/gt_babatsikised_scene12_take2.srt' )

gpath = 'res/gt_babatsikised_scene12_take2.srt'

markers = {
    'speech starts': 38,
    'error': 422,
    'repetition': 438,
    'scene change start': 753,
    'scene change end': 825
}

# googleASR
xpath = 'res/googleASR/output.srt'
ious_googleASR, stats_googleASR, subs_info_googleASR = se.get_iou_stats( gpath, xpath )
print('googleASR:', stats_googleASR)
time_delays_googleASR = se.plot_time_diffs( gpath , xpath , fig_name='res/googleASR_times.png', boxplot_fig_name='res/googleASR_box.png', markers=markers )
print('================= =================')
print('================= =================')
print('================= =================')
print('googleASR')
print('================= =================')
print('delays with outliers =================')
print('start: ', time_delays_googleASR['start'])
print('end: ', time_delays_googleASR['end'])
print('delays NO outliers =================')
print('start: ', time_delays_googleASR['start_no_outliers'])
print('end: ', time_delays_googleASR['end_no_outliers'])

# generic_LM_gb
xpath = 'res/generic_LM_gb/output.srt'
ious_generic_LM_gb, stats_generic_LM_gb, subs_info_generic_LM_gb = se.get_iou_stats( gpath, xpath )
print('generic_LM_gb:', stats_generic_LM_gb)
time_delays_generic_LM_gb = se.plot_time_diffs( gpath , xpath , fig_name='res/generic_LM_gb_times.png', boxplot_fig_name='res/generic_LM_gb_box.png', markers=markers )
print('================= =================')
print('================= =================')
print('================= =================')
print('generic_LM_gb')
print('================= =================')
print('delays with outliers =================')
print('start: ', time_delays_generic_LM_gb['start'])
print('end: ', time_delays_generic_LM_gb['end'])
print('delays NO outliers =================')
print('start: ', time_delays_generic_LM_gb['start_no_outliers'])
print('end: ', time_delays_generic_LM_gb['end_no_outliers'])

# littleprince_specific_LM
xpath = 'res/littleprince_specific_LM/output.srt'
ious_littleprince_specific_LM, stats_littleprince_specific_LM, subs_info_specific_LM = se.get_iou_stats( gpath, xpath )
print('littleprince_specific_LM:', stats_littleprince_specific_LM)
time_delays_littleprince_specific_LM = se.plot_time_diffs( gpath , xpath , fig_name='res/littleprince_specific_LM_times.png', boxplot_fig_name='res/littleprince_specific_LM_box.png', markers=markers )
print('================= =================')
print('================= =================')
print('================= =================')
print('littleprince_specific_LM')
print('================= =================')
print('delays with outliers =================')
print('start: ', time_delays_littleprince_specific_LM['start'])
print('end: ', time_delays_littleprince_specific_LM['end'])
print('delays NO outliers =================')
print('start: ', time_delays_littleprince_specific_LM['start_no_outliers'])
print('end: ', time_delays_littleprince_specific_LM['end_no_outliers'])

import matplotlib.pyplot as plt
plt.clf()
plt.boxplot( [time_delays_googleASR['all']['start'], time_delays_googleASR['all']['end'], time_delays_littleprince_specific_LM['all']['start'], time_delays_littleprince_specific_LM['all']['end']] )
plt.xticks([1, 2, 3, 4], ['google start', 'google end', 'spec. start', 'spec. end'])
plt.savefig('res/google_specific_box.png', dpi=300)

plt.clf()
plt.boxplot( [time_delays_googleASR['all']['start_no_outliers'], time_delays_googleASR['all']['end_no_outliers'], time_delays_littleprince_specific_LM['all']['start_no_outliers'], time_delays_littleprince_specific_LM['all']['end_no_outliers']] )
plt.xticks([1, 2, 3, 4], ['google start', 'google end', 'spec. start', 'spec. end'])
plt.savefig('res/google_specific_no_outliers_box.png', dpi=300)

# gpath = 'res/generic_LM_gb/output.srt'
# # googleASR
# xpath = 'res/littleprince_specific_LM/output.srt'
# ious_bs, stats_bs = se.get_iou_stats( gpath, xpath )
# print('bs:', stats_bs)