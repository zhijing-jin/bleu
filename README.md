A Python Wrapper for the standard BLEU evaluation for Natural Language Generation (NLG).

## How to Run
#### Option 1: Use the `lists2bleu()` or `files2bleu()` function.
```python
>>> from bleu import lists2bleu, files2bleu
>>> refs = [['it is a white cat .',
             'wow , this dog is huge .'],
            ['This cat is white .',
             'wow , this is a huge dog .']]
>>> hyps = [['it is a white kitten .',
             'wowww , the dog is huge !']]
>>> bleus = lists2bleu(refs, hyps, verbose=False)
>>> bleus[0]
34.99

# or if you have them in files
>>> hyp_files = ['data/hyp0.txt']
>>> ref_files = ['data/ref0.txt', 'data/ref1.txt']
>>> temp_file = 'data/tmp.txt' # temp_file is to save temporary outputs
>>> files2bleu(hyp_files, ref_files,
               temp_file=temp_file, verbose=True)

[Info] Valid Reference Files: ['data/ref0.txt', 'data/ref1.txt']
[Info] Valid Hypothesis Files: ['data/hyp0.txt']
[Info] #lines in each file: 2
[cmd] perl detokenizer.perl -l en < data/ref0.txt > data/ref0.detok.txt 2>/dev/null
[cmd] perl detokenizer.perl -l en < data/ref1.txt > data/ref1.detok.txt 2>/dev/null
[cmd] perl detokenizer.perl -l en < data/hyp0.txt > data/hyp0.detok.txt 2>/dev/null
[cmd] perl multi-bleu-detok.perl data/ref0.detok.txt data/ref1.detok.txt < data/hyp0.detok.txt
2-ref bleu for data/hyp0.detok.txt: 34.99
[34.99]
```
#### Option 2:  Call the python file [get_bleu.py](bleu.py)
```bash
python get_bleu.py \
-refs data/ref0.txt data/ref1.txt -hyps data/hyp0.txt
```

If you want to directly call get_bleu in your code, just adapt [get_bleu.py](bleu.py) into your code.

Check the `python get_bleu.py --help` if you have any questions.
