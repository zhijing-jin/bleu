from bleu import list_bleu

ref = ['it is a white cat .',
       'wow , this dog is huge .']
ref1 = ['This cat is white .',
        'wow , this is a huge dog .']
hyp = ['it is a white kitten .',
       'wowww , the dog is huge !']
hyp1 = ["it 's a white kitten .",
        'wow , this dog is huge !']
assert 34.99 == list_bleu([ref], hyp)
assert 34.99 == list_bleu(ref, hyp)

assert 57.91 == list_bleu([ref, ref1], hyp1)

from bleu import multi_list_bleu

assert [34.99, 53.28] == multi_list_bleu(ref, [hyp, hyp1])
assert [34.99, 57.91] == multi_list_bleu([ref, ref1], [hyp, hyp1])

# if you want to get files that saved the detokenized version of your input lists
bleus, ref_files, hyp_files = multi_list_bleu([ref, ref1], [hyp, hyp1],
                                              return_files=True)
print(ref_files)
['TMP_DIR/ref0.txt', 'TMP_DIR/ref1.txt']
print(hyp_files)
['TMP_DIR/hyp0.txt', 'TMP_DIR/hyp1.txt']
assert 39.76 == list_bleu([ref], hyp, detok=False)

# or if you want to test multiple hypotheses
assert [39.76, 47.47] == multi_list_bleu([ref, ref1], [hyp, hyp1], detok=False)

from bleu import file_bleu

hyp_file, hyp_file1 = hyp_files
assert 34.99 == file_bleu(ref_files, hyp_file)
assert 34.99 == file_bleu(ref_files[0], hyp_file)

from bleu import multi_file_bleu

hyp_file, hyp_file1 = hyp_files
bleus = multi_file_bleu(ref_files, [hyp_file, hyp_file1])
assert [34.99, 57.91] == multi_file_bleu(ref_files, [hyp_file, hyp_file1])
assert [34.99, 53.28] == multi_file_bleu(ref_files[0], [hyp_file, hyp_file1])

assert 34.99 == file_bleu(ref_files, hyp_file, verbose=True)
'''
[Info] Valid Reference Files: ['data/ref0.txt', 'data/ref1.txt']
[Info] Valid Hypothesis Files: ['data/hyp0.txt']
[Info] #lines in each file: 2
[cmd] perl detokenizer.perl -l en < data/ref0.txt > data/ref0.detok.txt 2>/dev/null
[cmd] perl detokenizer.perl -l en < data/ref1.txt > data/ref1.detok.txt 2>/dev/null
[cmd] perl detokenizer.perl -l en < data/hyp0.txt > data/hyp0.detok.txt 2>/dev/null
[cmd] perl multi-bleu-detok.perl data/ref0.detok.txt data/ref1.detok.txt < data/hyp0.detok.txt
2-ref bleu for data/hyp0.detok.txt: 34.99
'''

from bleu import detok_files

detok_ref_files = detok_files(ref_files, tmp_dir='./data',
                              file_prefix='ref_dtk', verbose=True)
'''
[cmd] perl ./TMP_DIR/detokenizer.perl -l en < data/ref0.txt > data/ref_dtk0.txt 2>/dev/null
[cmd] perl ./TMP_DIR/detokenizer.perl -l en < data/ref1.txt > data/ref_dtk1.txt 2>/dev/null
'''
assert ['./data/ref_dtk0.txt', './data/ref_dtk1.txt'] == detok_ref_files
