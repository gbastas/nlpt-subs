# nlpt-subs

## Example Output Videos

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
## Alignment Evaluation

Go to "evaluation_iou_subtitles" folder and run

```
python run_results.py
```

System output and ground-truth srt files can be found in 
```
./res/{googleASR, genericLM, little_prince_specific_LM}/output.srt
```

Images can be found in
```
./evaluation_iou_subtitles/res
```
