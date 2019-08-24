A Python Wrapper for the standard BLEU evaluation for Natural Language Generation (NLG).

## How to Run
```bash
python get_bleu.py \
-refs data/ref0.txt data/ref1.txt -hyps data/hyp0.txt
```

If you want to directly call get_bleu in your code, just adapt [get_bleu.py](./get_bleu.py) into your code.

Check the `python get_bleu.py --help` if you have any questions.