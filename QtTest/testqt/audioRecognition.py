# coding=utf-8

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    # 监听一秒钟用于设定相关阈值
    r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
    print("Say something!")
    audio = r.listen(source)


try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY", show_all=True)`
    # instead of `r.recognize_google(audio, show_all=True)`
    print "trying to recognize ... "
    from pprint import pprint
    print("Google Speech Recognition results:")
    resultTmp = r.recognize_google(audio,show_all=True)
    # print resultTmp[u'alternative'], type(resultTmp[u'alternative'])
    counter = 0
    for el in resultTmp[u'alternative']:
        for ell in el:
            if ell == 'confidence': # 可信度
                print ell,el[ell]
            elif counter < 2:
                print el[ell]
            else:
                break
        counter += 1

                # pprint(r.recognize_google(audio,show_all=True)) # pretty-print the recognition result
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

