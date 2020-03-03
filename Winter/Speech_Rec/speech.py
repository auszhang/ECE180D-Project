import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=1024,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'en-us'),
    lm=os.path.join(model_path, 'en-us.lm.bin'),
    #dic=os.path.join(model_path, 'cmudict-en-us.dict')
    dic='words.dic'
)

count = 0
for phrase in speech:
    print(type(str(phrase)))
    print(str(phrase))
    

