

# for offline WER vealuation:
# python get_wer_cer.py -t res/googleASR/transcription.out 

import argparse
import jiwer

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test_file', type=str)
args = parser.parse_args()

# TestTest=$1


with open('gt_corpus', "r") as f:
    ground_truth = f.readline()

with open(args.test_file, "r") as f:
    hypothesis = f.readline()


print('ground_truth:', ground_truth[:50])
print('hypothesis:', hypothesis[:50])


wer = round(jiwer.wer(ground_truth, hypothesis),4) * 100
mer = round(jiwer.mer(ground_truth, hypothesis),4) * 100
wil = round(jiwer.wil(ground_truth, hypothesis),4) * 100
cer = round(jiwer.cer(ground_truth, hypothesis),4) * 100

print("wer", wer,'%')
print("mer", mer,'%')
print("wil", wil,'%')
print("cer", cer,'%')

# compute-wer --text --mode=present ark:$TestTest ark:test_corpus #">&" $HERE/wer || exit 1;

