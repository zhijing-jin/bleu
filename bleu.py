'''
author = Zhijing Jin (zhijing.jin@connect.hku.hk)
date = Aug 24, 2019

How to Run:

python bleu.py \
-refs data/ref0.txt data/ref1.txt -hyps data/hyp0.txt
'''
from __future__ import print_function, division

import os
import json
import argparse

try:
    import efficiency
except ImportError:
    os.system('pip install git+git://github.com/zhijing-jin/efficiency.git')


def files2bleu(hyp_files, ref_files, temp_file='tmp.txt', concise=True,
               verbose=False):
    '''
    This is to get the average BLEU for hyp among ref0, ref1, ref2, ...
    :param hyp_files: a list of filenames for hypothesis
    :param ref_files: a list of filenames for references
    :return: print a bleu score
    '''
    from efficiency.function import shell

    ref_files, hyp_files = \
        check_files(ref_files, hyp_files, verbose=verbose)

    ref_concat = ' '.join(ref_files)
    outputs = []

    for hyp in hyp_files:
        cmd = 'perl multi-bleu-detok.perl {refs} < {hyp} '.format(
            refs=ref_concat, hyp=hyp, output=temp_file)
        if verbose:
            print('[cmd]', cmd)
        stdout, stderr = shell(cmd)

        if stdout.startswith('Illegal division by zero'):
            output = -1
        else:
            num = stdout.split(',')[0].replace('BLEU = ', '')
            output = float(num)
        outputs += [output]

        if verbose:
            print('{}-ref bleu for {}: {}'.format(len(ref_files), hyp, output))
    return outputs


def check_files(ref_files, hyp_files, verbose=False):
    # Step 1. Check whether all files exist
    valid_refs = [f for f in ref_files if os.path.isfile(f)]
    valid_hyps = [f for f in hyp_files if os.path.isfile(f)]
    if verbose:
        print('[Info] Valid Reference Files: {}'.format(str(valid_refs)))
        print('[Info] Valid Hypothesis Files: {}'.format(str(valid_hyps)))

    # Step 2. Check whether all files has the same num of lines
    num_lines = []
    files = valid_refs + valid_hyps
    for file in files:
        with open(file) as f:
            lines = [line.strip() for line in f]
            num_lines += [len(lines)]
    if len(set(num_lines)) != 1:
        print("[Error] file length different!")
        print("list(zip(files, num_lines)):", list(zip(files, num_lines)))
        import pdb
        pdb.set_trace()
        # assert False

    if verbose:
        print("[Info] #lines in each file: {}".format(num_lines[0]))

    # Step 3. detokenization
    valid_refs = detok_file(valid_refs, verbose=verbose)
    valid_hyps = detok_file(valid_hyps, verbose=verbose)

    return valid_refs, valid_hyps


def detok_file(files, verbose=False):
    '''
    This is to detokenize all files
    :param files: a list of filenames
    :return: a list of files after detokenization
    '''
    for file_ix, file in enumerate(files):
        if file.endswith('.detok'):
            continue
        detok_name = file + '.detok'
        cmd = 'perl detokenizer.perl -l en < {} > {} 2>/dev/null'.format(
            file, detok_name)
        if verbose:
            print('[cmd]', cmd)
        os.system(cmd)
        files[file_ix] = detok_name
    return files


def lists2files(refs, hyps, tmp_dir='./data'):
    def _list2file(sents, file):
        writeout = '\n'.join(sents) + '\n'
        with open(file, 'w') as f:
            f.write(writeout)

    ref_files = [os.path.join(tmp_dir, 'ref{}.txt'.format(ref_ix))
                 for ref_ix, _ in enumerate(refs)]
    hyp_files = [os.path.join(tmp_dir, 'hyp{}.txt'.format(hyp_ix))
                 for hyp_ix, _ in enumerate(hyps)]

    _ = [_list2file(*item) for item in zip(refs, ref_files)]
    _ = [_list2file(*item) for item in zip(hyps, hyp_files)]
    return ref_files, hyp_files


def lists2bleu(refs, hyps, tmp_dir='./data', verbose=False, return_files=False):
    ref_files, hyp_files = lists2files(refs, hyps, tmp_dir=tmp_dir)
    temp_file = os.path.join(tmp_dir, 'tmp.txt')

    bleus = files2bleu(hyp_files=hyp_files, ref_files=ref_files,
                       temp_file=temp_file, verbose=verbose)
    if return_files:
        return bleus, ref_files, hyp_files
    else:
        return bleus


def test():
    refs = [['it is a white cat .',
             'wow , this dog is huge .'],
            ['This cat is white .',
             'wow , this is a huge dog .']]
    hyps = [['it is a white kitten .',
             'wowww , the dog is huge !']]

    bleus = lists2bleu(refs, hyps, verbose=True)


def download_scripts():
    files = [('detokenizer.perl',
              'https://raw.githubusercontent.com/moses-smt/mosesdecoder/master/scripts/tokenizer/detokenizer.perl'),
             ('multi-bleu-detok.perl',
              'https://raw.githubusercontent.com/moses-smt/mosesdecoder/master/scripts/generic/multi-bleu-detok.perl'),
             ('multi-bleu.perl',
              'https://raw.githubusercontent.com/moses-smt/mosesdecoder/master/scripts/generic/multi-bleu.perl'),
             ]
    for fname, url in files:
        if not os.path.isfile(fname):
            os.system('curl -o {fname} {url}'.format(fname=fname, url=url))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-refs', default=['data/ref0.txt', 'data/ref1.txt'],
                        nargs='+', type=str,
                        help='a list of filenames for reference files, separated by space')
    parser.add_argument('-hyps', default=['data/hyp0.txt'], nargs='+', type=str,
                        help='a list of filenames for hypothesis files, separated by space')
    parser.add_argument('-data_dir', default='', type=str,
                        help='directory to save temporary outputs')
    parser.add_argument('-verbose', action='store_true',
                        help='whether to allow printing out logs')

    args = parser.parse_args()

    download_scripts()

    args.data_dir = args.data_dir if args.data_dir else \
        args.hyps[0].rsplit('/')[0]
    args.temp_file = os.path.join(args.data_dir, 'tmp.txt')
    if args.verbose:
        print(json.dumps(vars(args), indent=4, sort_keys=True))

    ref_files = args.refs
    hyp_files = args.hyps

    outputs = files2bleu(hyp_files, ref_files, verbose=args.verbose,
                         temp_file=args.temp_file)
    print("All BLEUs:", outputs)


if __name__ == "__main__":
    main()
