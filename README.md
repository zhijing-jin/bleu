# bleu (Python Package)
[![Pypi](https://img.shields.io/pypi/v/bleu.svg)](https://pypi.org/project/bleu)
[![Downloads](https://pepy.tech/badge/bleu)](https://pepy.tech/project/bleu)
[![Month_Downloads](https://pepy.tech/badge/bleu/month)](https://pepy.tech/project/bleu/month)

A Python Wrapper for the standard BLEU evaluation for Natural Language Generation (NLG). 
- GitHub project: [https://github.com/zhijing-jin/bleu](https://github.com/zhijing-jin/bleu).
- PyPI package: `pip install`[`bleu`](https://pypi.org/project/bleu/) 

## Installation
Requirement: Python 3

**Option 1: Install pip package**
```bash
pip install --upgrade bleu
```
**Option 2: Build from source**
```bash
pip install --upgrade git+git://github.com/zhijing-jin/bleu.git
```
## How to Run
The most standard way to calculate BLEU is by [Moses' script for detokenized BLEU](https://raw.githubusercontent.com/moses-smt/mosesdecoder/master/scripts/generic/multi-bleu-detok.perl). This package provides easy calls to it. 
#### Function 1: Calculate the BLEU for lists
If you want to check only one hypothesis (a list of sentences):
```python
>>> from bleu import list_bleu
>>> refs = [['it is a white cat .',
             'wow , this dog is huge .'],
            ['This cat is white .',
             'wow , this is a huge dog .']]
>>> hyp = ['it is a white kitten .',
            'wowww , the dog is huge !']
>>> hyp1 = ["it 's a white kitten .",
             'wow , this dog is huge !']
>>> list_bleu(refs, hyp)
34.99
>>> list_bleu(refs, hyp1)
57.91
```
If you want to check multiple hypothesis (several lists of sentences):
```python
>>> from bleu import multi_list_bleu
>>> multi_list_bleu(refs, [hyp, hyp1])
[34.99, 57.91]
# if you want to get files that saved the detokenized version of your input lists
>>> bleus, ref_files, hyp_files = multi_list_bleu(refs, [hyp, hyp1], return_files=True)
>>> ref_files
['TMP_DIR/ref0.txt', 'TMP_DIR/ref1.txt']
>>> hyp_files
['TMP_DIR/hyp0.txt', 'TMP_DIR/hyp1.txt']
```
`detok=False`: It is not advisable to use tokenized bleu (by [multi-bleu.perl](https://raw.githubusercontent.com/moses-smt/mosesdecoder/master/scripts/generic/multi-bleu.perl)), but if you want to call it, just use `detok=False`:
```python
>>> list_bleu(refs, hyp, detok=False)
39.76
# or if you want to test multiple hypotheses
>>> multi_list_bleu(refs, [hyp, hyp1], detok=False)
[39.76, 47.47]
```  
`verbose=True`: If there are unexpected errors, you might want to check the intermediate steps by `verbose=True`. 
 
#### Function 2: Calculate the BLEU for files
If you want to check only one hypothesis file:
```python
# if you already have the following files
>>> from bleu import file_bleu
>>> hyp_file = 'data/hyp0.txt'
>>> ref_files = ['data/ref0.txt', 'data/ref1.txt']
>>> file_bleu(ref_files, hyp_file)
34.99
```
If you want to check multiple hypothesis files:
```python
>>> from bleu import multi_file_bleu
>>> hyp_file1 = 'data/hyp1.txt'
>>> bleus, ref_files, hyp_files = multi_file_bleu(ref_files, [hyp_file, hyp_file1])
[34.99, 57.91]
```
`detok=True`: Set it if you want to calculate the (not recommended) tokenized bleu.

`verbose=True`: Set it if you want to inspect how the bleu calculations are made:
```python
>>> bleu = file_bleu(ref_files, hyp_file, verbose=True)
[Info] Valid Reference Files: ['data/ref0.txt', 'data/ref1.txt']
[Info] Valid Hypothesis Files: ['data/hyp0.txt']
[Info] #lines in each file: 2
[cmd] perl detokenizer.perl -l en < data/ref0.txt > data/ref0.detok.txt 2>/dev/null
[cmd] perl detokenizer.perl -l en < data/ref1.txt > data/ref1.detok.txt 2>/dev/null
[cmd] perl detokenizer.perl -l en < data/hyp0.txt > data/hyp0.detok.txt 2>/dev/null
[cmd] perl multi-bleu-detok.perl data/ref0.detok.txt data/ref1.detok.txt < data/hyp0.detok.txt
2-ref bleu for data/hyp0.detok.txt: 34.99
>>> bleu
34.99
```
#### Option 3: Detokenize files
```python
>>> detok_ref_files = detok_files(ref_files, tmp_dir='./data', file_prefix='ref_dtk', verbose=True)
[cmd] perl ./TMP_DIR/detokenizer.perl -l en < data/ref0.txt > data/ref_dtk0.txt 2>/dev/null
[cmd] perl ./TMP_DIR/detokenizer.perl -l en < data/ref1.txt > data/ref_dtk1.txt 2>/dev/null
>>> detok_ref_files
['data/ref_dtk0.txt', 'data/ref_dtk1.txt']
```
## In Case of Unexpected Outputs
Check the python file [bleu.py](bleu.py) and adapt it.

## Contact
If you have more questions, feel free to check out the common [Q&A](https://github.com/zhijing-jin/bleu/issues?utf8=%E2%9C%93&q=is%3Aissue), or raise a new GitHub issue.

In case of really urgent needs, contact the author [Zhijing Jin (Miss)](mailto:zhijing.jin@connect.hku.hk).
