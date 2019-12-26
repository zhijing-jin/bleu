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

from .download import TMP_DIR, DETOK_FILE, BLEU_DETOK_FILE, BLEU_FILE


def file_bleu(ref_files, hyp_file, detok=True, verbose=False):
    bleus = multi_file_bleu(ref_files, [hyp_file], detok=detok, verbose=verbose)
    return bleus[0]


def multi_file_bleu(ref_files, hyp_files, detok=True, verbose=False):
    '''
    This is to get the average BLEU for hyp among ref0, ref1, ref2, ...
    :param hyp_files: a list of filenames for hypothesis
    :param ref_files: a list of filenames for references
    :return: print a bleu score
    '''
    from efficiency.function import shell

    ref_files, hyp_files = \
        preprocess_files(ref_files, hyp_files, verbose=verbose)

    outputs = []
    script = BLEU_DETOK_FILE if detok else BLEU_FILE

    for hyp in hyp_files:
        cmd = 'perl {script} {refs} < {hyp} '.format(
            script=script,refs=' '.join(ref_files), hyp=hyp)
        if verbose: print('[cmd]', cmd)
        stdout, stderr = shell(cmd)

        bleu_prefix = 'BLEU = '

        if verbose and not stdout.startswith(bleu_prefix):
            print(stdout)

        if bleu_prefix in stdout:
            num = stdout.split(bleu_prefix, 1)[-1].split(',')[0]
            output = float(num)
        else:
            # if stdout.startswith('Illegal division by zero'):
            output = -1

        outputs += [output]

        if verbose:
            print('{}-ref bleu for {}: {}'.format(len(ref_files), hyp, output))
    return outputs


def list_bleu(refs, hyp, detok=True, tmp_dir=TMP_DIR, verbose=False, return_files=False):
    ref_files, hyp_files = lists2files(refs, [hyp], tmp_dir=tmp_dir)

    bleus = multi_file_bleu(ref_files=ref_files, hyp_files=hyp_files,
                            detok=detok, verbose=verbose)
    bleu = bleus[0]
    hyp_file = hyp_files[0]
    if return_files:
        return bleu, ref_files, hyp_file
    else:
        return bleu

def multi_list_bleu(refs, hyps, detok=True, tmp_dir=TMP_DIR, verbose=False, return_files=False):
    ref_files, hyp_files = lists2files(refs, hyps, tmp_dir=tmp_dir)

    bleus = multi_file_bleu(ref_files=ref_files, hyp_files=hyp_files,
                            detok=detok, verbose=verbose)
    if return_files:
        return bleus, ref_files, hyp_files
    else:
        return bleus

def lists2files(refs, hyps, tmp_dir=TMP_DIR):
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


def preprocess_files(ref_files, hyp_files, verbose=False):
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
        raise RuntimeError("[Error] File lengths are different! list(zip(files, num_lines)): {}".format(list(zip(files, num_lines))))

    if verbose:
        print("[Info] #lines in each file: {}".format(num_lines[0]))

    # Step 3. detokenization
    valid_refs = detok_files(valid_refs, tmp_dir=TMP_DIR, file_prefix='ref_dtk', verbose=verbose)
    valid_hyps = detok_files(valid_hyps, tmp_dir=TMP_DIR, file_prefix='hyp_dtk', verbose=verbose)

    return valid_refs, valid_hyps


def detok_files(files_in, tmp_dir=TMP_DIR, file_prefix='detok', verbose=False):
    '''
    This is to detokenize all files
    :param files: a list of filenames
    :return: a list of files after detokenization
    '''
    files_out = []
    if not os.path.isdir(tmp_dir): os.mkdir(tmp_dir)
    for ix, f_in in enumerate(files_in):
        f_out = os.path.join(tmp_dir, '{}{}.txt'.format(file_prefix, ix))
        files_out.append(f_out)

        cmd = 'perl {DETOK_FILE} -l en < {f_in} > {f_out} 2>/dev/null'.format(
            DETOK_FILE=DETOK_FILE, f_in=f_in, f_out=f_out)
        if verbose: print('[cmd]', cmd)
        os.system(cmd)
    return files_out


def main(args=None):
    refs = [['it is a white cat .',
             'wow , this dog is huge .'],
            ['This cat is white .',
             'wow , this is a huge dog .']]
    hyp = ['it is a white kitten .',
             'wowww , the dog is huge !']
    hyp2 = ["it 's a white kitten .",
             'wow , this dog is huge !']
    import pdb;pdb.set_trace()
    bleus, ref_files, hyp_files  = multi_list_bleu(refs, [hyp, hyp2], detok=True, verbose=True, return_files=True)
    bleu = list_bleu(refs, hyp, detok=True, verbose=False)


    bleus = multi_file_bleu(ref_files, hyp_files, detok=True, verbose=True)
    bleu = file_bleu(ref_files, hyp_files[0], detok=True, verbose=True)

    if args is not None:
        if args.verbose:
            print(json.dumps(vars(args), indent=4, sort_keys=True))

        outputs = multi_file_bleu(args.refs, args.hyps, verbose=args.verbose)
        print("All BLEUs:", outputs)


if __name__ == "__main__":
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
    main(args)
