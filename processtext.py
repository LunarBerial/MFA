#coding: utf-8

import os, codecs, re

def gen_lexicon_and_lab():
    f0 = codecs.open('emo_pron', 'r', 'utf-8')
    f1 = codecs.open('lexicon.txt', 'a', 'utf-8')
    if not os.path.exists('emo_lab'):
        os.mkdir('emo_lab')

    for line in f0:
        line = line.strip().split('\t')
        if len(line) != 2:
            continue
        idx = line[0]
        line[1] = line[1].strip(';').split(';')
        for i, w in enumerate(line[1]):
            if re.search(r'pau\d', w):
                if i == len(line[1]) - 1:
                    line[1][i] = 'sil'
                else:
                    line[1][i] = 'sp'

            f1.write(w.replace(' ', '') + '\t' + w + '\n')

        f2 = codecs.open('./emo_lab/' + idx + '.lab', 'w', 'utf-8')
        f2.writelines(' '.join([l.replace(' ','') for l in line[1]]))
        f2.close()

    f1.close()
    f0.close()


if __name__ == "__main__":
    gen_lexicon_and_lab()
