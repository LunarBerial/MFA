import os
import wave
import numpy as np
import shutil

if not os.path.exists('bad'):
    os.mkdir('bad')
count = 0
for origname in os.listdir('lj/'):
    print(origname)
    if not origname.endswith('wav'):
        continue
    w = wave.open('lj/' + origname)
    params = w.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    w_data = w.readframes(nframes)
    w_data = np.fromstring(w_data, dtype=np.short)
    w.close()
    w_data = w_data.tolist()
    if (max(w_data) >= 32766) or (min(w_data) <= -32765):
        print(max(w_data))
        count += 1
        shutil.move('lj/' + origname, 'bad/')

print(count)

from mxnet.gluon import loss
loss.L1Loss