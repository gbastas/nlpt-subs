# nlpt-subs

To get accuracy measures of the ASR service for the different STT models tested on scenes 1&2 of 'Little Prince' run:
```
python get_wer_cer.py -t res/googleASR/transcription.out 
python get_wer_cer.py -t res/generic_LM/transcription.out
python get_wer_cer.py -t res/littleprince_specific_LM/transcription.out
```

