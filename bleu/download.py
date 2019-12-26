import os
import tempfile

TMP_DIR = os.path.join(tempfile.gettempdir(), 'tmp_bleu')


def download_scripts(folder=TMP_DIR):
    files = [(os.path.join(folder, 'detokenizer.perl'),
              'https://raw.githubusercontent.com/moses-smt/mosesdecoder/master/scripts/tokenizer/detokenizer.perl'),
             (os.path.join(folder, 'multi-bleu-detok.perl'),
              'https://raw.githubusercontent.com/moses-smt/mosesdecoder/master/scripts/generic/multi-bleu-detok.perl'),
             (os.path.join(folder, 'multi-bleu.perl'),
              'https://raw.githubusercontent.com/moses-smt/mosesdecoder/master/scripts/generic/multi-bleu.perl'),
             ]
    if not os.path.isdir(folder):
        os.mkdir(folder)

    for fname, url in files:
        if not os.path.isfile(fname):
            from urllib.request import urlretrieve
            urlretrieve(url, fname)

    (detok_file, bleu_detok_file, bleu_file), _ = zip(*files)

    return detok_file, bleu_detok_file, bleu_file


DETOK_FILE, BLEU_DETOK_FILE, BLEU_FILE = download_scripts(TMP_DIR)
