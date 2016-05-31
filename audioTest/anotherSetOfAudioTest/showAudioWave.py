# -*- coding: utf-8 -*-
import pyaudio
import pylab
import numpy

### RECORD AUDIO FROM MICROPHONE ###
rate=44100
soundcard=1 #CUSTOMIZE THIS!!! 自定义
p=pyaudio.PyAudio()
strm=p.open(format=pyaudio.paInt16,channels=1,rate=rate,\
                        input_device_index=soundcard,input=True)
strm.read(1024) #prime the sound card this way
print type(strm.read(1024))
pcm=numpy.fromstring(strm.read(1024), dtype=numpy.int16) # 将字符串转化为INT数组
print type(pcm)
### DO THE FFT ANALYSIS ###
fft=numpy.fft.fft(pcm)
fftr=10*numpy.log10(abs(fft.real))[:len(pcm)/2] # 实部
ffti=10*numpy.log10(abs(fft.imag))[:len(pcm)/2] # 虚部
fftb=10*numpy.log10(numpy.sqrt(fft.imag**2+fft.real**2))[:len(pcm)/2] # 实数和虚数部分相加
freq=numpy.fft.fftfreq(numpy.arange(len(pcm)).shape[-1])[:len(pcm)/2] # 频率
freq=freq*rate/1000 #make the frequency scale #单位换算HZ——KHZ

### GRAPH THIS STUFF ###
pylab.subplot(411)
pylab.title("Original Data")
pylab.grid()
pylab.plot(numpy.arange(len(pcm))/float(rate)*1000,pcm,'r-',alpha=1)
pylab.xlabel("Time (milliseconds)")
pylab.ylabel("Amplitude")
pylab.subplot(412)
pylab.title("Real FFT")
pylab.xlabel("Frequency (kHz)")
pylab.ylabel("Power")
pylab.grid()
pylab.plot(freq,fftr,'b-',alpha=1)
pylab.subplot(413)
pylab.title("Imaginary FFT")
pylab.xlabel("Frequency (kHz)")
pylab.ylabel("Power")
pylab.grid()
pylab.plot(freq,ffti,'g-',alpha=1)
pylab.subplot(414)
pylab.title("Real+Imaginary FFT")
pylab.xlabel("Frequency (kHz)")
pylab.ylabel("Power")
pylab.grid()
pylab.plot(freq,fftb,'k-',alpha=1)
pylab.show()