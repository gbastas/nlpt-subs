# nlpt-subs

## Example Outout Videos

https://youtu.be/UN-ByxZxgok

## Get Recognition Accuracy (Experiment 1)

Dependencies:
```
pip install jiwer
```

To get accuracy measures of the ASR service for the different STT models tested on scenes 1&2 of 'Little Prince' run:
```
python get_wer_cer.py -t res/{googleASR, genericLM, little_prince_specific_LM}/transcription.out 
```
## Alignment Evaluation (TODO: Max)

NOTE: synched srt files can be found in 
```
./res/{googleASR, genericLM, little_prince_specific_LM}/output.srt
```
