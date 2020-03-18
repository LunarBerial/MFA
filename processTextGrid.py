#coding:utf-8

import re, codecs, os

# 分析TextGrid， 提取音素，时程信息对。
def extract_dur_info(labfile):
    f0 = codecs.open(labfile, 'r', 'utf-8')
    lines = [l.strip() for l in f0.readlines()]
    f0.close()

    idx_1 = lines.index('item [1]:')
    idx_2 = lines.index('item [2]:')
    list_1 = []
    for i, l in enumerate(lines[idx_1 + 6:idx_2]):
        if i % 4 == 3:
            p = l.split('"')[-2]
            t0 = lines[idx_1 + i + 4].split('=')[1][1:]
            t1 = lines[idx_1 + i + 5].split('=')[1][1:]

            list_1.append((p, t0, t1))
    list_2 = []
    for i, l in enumerate(lines[idx_2+ 6:]):
        if i % 4 == 3:
            p = l.split('"')[-2]
            t0 = lines[idx_2 + i + 4].split('=')[1][1:]
            t1 = lines[idx_2 + i + 5].split('=')[1][1:]
            list_2.append((p, t0, t1))

    return list_1, list_2


# 由TeXGrid中提取的两个list，去除冗余项，得到（phoneme， duration）对列表
def align_phonemes(list_1:list, list_2:list):
    full_phoneme_string = ''.join([a[0] for a in list_1])
    dur_list = []
    flag = True
    for i, l in enumerate(list_2):
        if i == 0 and l[0] == 'sil':
            dur_list.append((l[0], l[2]))
        elif i == 0 and l[0] != 'sil':
            if float(l[2]) > 0.03:
                dur_list.append(('sil', 0.03))
                dur_list.append((l[0], l[2]))
                full_phoneme_string = full_phoneme_string[len(l[0]):]
            else:
                flag = False
                print('no space for sil')
                break
        else:
            p = l[0]
            t = l[2]
            if p == '':
                if i == len(list_2) -1 and list_2[i - 1][0] == 'sil':
                    p_d, _ = dur_list[-1]
                    dur_list[-1] = (p_d, t)
                elif i == len(list_2) -1 and list_2[i - 1][0] == 'sp':
                    dur_list.append(('sil', t))
            elif full_phoneme_string.startswith(p):
                if p == 'sp' and list_2[i + 1][0] == 's' and not full_phoneme_string.startswith('sps'):
                    t_deta = (float(t) + float(l[1])) / 2
                    p_d, _ = dur_list[-1]
                    dur_list[-1] = (p_d, t_deta)
                else:
                    dur_list.append((p, t))
                    full_phoneme_string = full_phoneme_string[len(p):]
            elif p == 'sp':
                t_deta = (float(t) + float(l[1]))/ 2
                p_d, _ = dur_list[-1]
                dur_list[-1] = (p_d, t_deta)
            else:
                print('alignment failed')
                flag = False
                break
    if dur_list and dur_list[-1][0] != 'sil':
        if len(dur_list) < 2:
            return dur_list, False
        t0 = float(dur_list[-2][-1])
        t1 = float(dur_list[-1][-1])
        if t1 - t0 > 0.06:
            p, _ = dur_list[-1]
            dur_list[-1] = (p, t1 - 0.06)
            dur_list.append(('sil', t1))
        else:
            flag = False
            print('do not has space for sil')

    return dur_list, flag

# time和frame number转换，返回累加结果
def calculate_rate(dur_list:list):
    for i, d in enumerate(dur_list):
        p, t = d
        t = float(t)
        t = round(t * 1000 / 5)
        dur_list[i] = (p, str(t))

    return dur_list


def gen_rate_info():
    f = codecs.open('rate_info_emo', 'w', 'utf-8')
    for lab in os.listdir('result/emo_lab/emo_lab'):
        # print(lab)
        list_1, list_2 = extract_dur_info('result/emo_lab/emo_lab/'+lab)

        dur_list, flag = align_phonemes(list_1, list_2)
        if not flag:
            print(lab)
            continue

        f.writelines(lab.split('.')[0] + '\t' + ','.join([d[0] for d in dur_list]))
        dur_list = calculate_rate(dur_list)
        f.writelines('\t' + ','.join([d[1] for d in dur_list]) + '\n')

    f.close()


def checksp():
    for labfile in os.listdir('lab'):
        if not labfile.endswith('lab'):
            continue
        f = codecs.open('lab/' + labfile, 'r', 'utf-8')
        phoneme = f.readlines()[0].strip().split(' ')
        # print(labfile, phoneme)
        for p in phoneme:
            if p.startswith('sp') and not p == 'sp':
                print(labfile, p)
                break
        f.close()


if __name__ == "__main__":
    gen_rate_info()
    # checksp()