# MFA
强制对齐工具
源地址：https://montreal-forced-aligner.readthedocs.io/en/latest/

注意事项：

所用的音频格式为 wav, 16bit, 采样率可以>= 16k

lexicon要提前准备好，音素和给出的不同的，英语也需要重新训练模型，因为triphone分布不同。

OOV词会对对齐产生较大影响，最好提前补充进lexicon。

工具会根据音频自动添加‘sp’静音，所以不用手动添加。

坑爹的是sp 和 sil 可能会连在一起出现（因为系统只认识sp这一个音素为静音段），用于训练的话，最好记得自己删干净。


