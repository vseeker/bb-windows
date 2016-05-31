# coding=utf-8

# NOTE: this example requires PyAudio because it uses the Microphone class

import PyBaiduYuyin as pby

# obtain audio from the microphone
r = pby.Recognizer()
with pby.Microphone() as source:
    # 监听一秒钟用于设定相关阈值
    r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
    print("Say something!")
    audio = r.listen(source)


# for testing purposes, we're just using the default API key
# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY", show_all=True)`
# instead of `r.recognize_google(audio, show_all=True)`
print "trying to recognize ... "
print("Speech Recognition results:")
resultTmp = r.recognize(audio)
# print resultTmp[u'alternative'], type(resultTmp[u'alternative'])
print "{0}".format(resultTmp.encode('utf-8'))
# print "{0}".format(resultTmp) # 测试该句的转格式能不能用


