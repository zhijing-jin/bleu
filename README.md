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
[34.99]

# or if you have them in files
>>> hyp_files = ...
>>> ref_files = ...
>>> temp_file = ...
>>> files2bleu(hyp_files, ref_files, 
    temp_file=temp_file, verbose=False)
    # temp_file is to save temporary outputs
```
#### Option 2:  Call the python file [get_bleu.py](bleu.py)
```bash
python get_bleu.py \
-refs data/ref0.txt data/ref1.txt -hyps data/hyp0.txt
```

If you want to directly call get_bleu in your code, just adapt [get_bleu.py](bleu.py) into your code.

Check the `python get_bleu.py --help` if you have any questions.