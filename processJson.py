#coding:utf-8

import re, codecs, json

def mergeJson():
    f0 = codecs.open('rate_info', 'r', 'utf-8')
    lines = f0.readlines()
    f0.close()

    dur_info = {}
    for l in lines:
        l = l.strip().split('\t')
        dur_info[l[0]] = (l[1], l[2])

    f0 = open('Json/selected_lj_data.json', 'r')
    data = json.load(f0)
    f0.close()
    newdata = {}
    for key in data.keys():
        id = data[key]['utter_id']
        if id.startswith('140'):
            continue
        p, d = dur_info.get(id, (None, None))
        if not p:
            continue
        p = p.split(',')
        p_o = data[key]['phoneme'].split(' ')
        if len(p) != len(p_o):
            print(id)
            continue
        d = d.split(',')
        ol = data[key]['length_output']
        if int(d[-2]) > ol:
            print(id)
            continue
        d[-1] = str(ol)
        data[key]['index'] = ' '.join(d)
        newdata.update({key: data[key]})

    f = open('Json/lj_sent_data.json', 'w')
    json.dump(newdata, f, indent=4)
    f.close()


def combineJson():
    f0 = open('Json/emo_lj_sent_data.json', 'r')
    data1 = json.load(f0)
    f0.close()

    newdata = {}
    newdata.update(data1)

    f0 = open('Json/train_selected_emo_sent_data_5.json', 'r')
    data1 = json.load(f0)
    f0.close()
    for key in data1.keys():
        if key.endswith('2'):
            newdata.update({key[:-1] + '3': data1[key]})
            newdata.update({key[:-1] + '4': data1[key]})
            newdata.update({key[:-1] + '5': data1[key]})


    f0 = open('Json/emo_lj_sent_data_1.json', 'w')
    json.dump(newdata, f0, indent=4)
    f0.close()


def picksent():
    f0 = open('Json/emo_lj_sent_data.json', 'r')
    data1 = json.load(f0)
    f0.close()

    newdata = {}
    for key in data1.keys():
        id = data1[key]['utter_id']
        try:
            id = int(id)
        except:
            continue
        if id < 1300041 and id > 1300000 and not newdata.get(key, None):

            newdata.update({key: data1[key]})
    f0 = open('Json/emo_lj_sent_test.json', 'w')
    json.dump(newdata, f0, indent=4)
    f0.close()


def pickdata():
    f0 = open('Json/emo_lj_sent_data.json', 'r')
    data1 = json.load(f0)
    f0.close()

    newdata = {}
    for key in data1.keys():
        id = data1[key]['utter_id']
        if id.startswith('1'):
            newdata.update({key: data1[key]})


    f0 = open('Json/emo_sent_data_1.json', 'w')
    json.dump(newdata, f0, indent=4)
    f0.close()


if __name__ == "__main__":
    # mergeJson()
    # combineJson()
    # picksent()
    pickdata()
