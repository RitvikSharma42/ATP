#!/usr/bin/env python
# coding: utf-8

# In[17]:


# Imports of necessary libraries

# Data manipulation and linear algebra computation
import pandas as pd
import numpy as np
# File management
import os,glob
# DL and related libraries
from transformers import WhisperConfig
import torch
import whisperx
from transformers import WhisperForConditionalGeneration
from datasets import load_dataset
# For Live audio recording
import sounddevice as sdrec
from scipy.io.wavfile import write
import wavio as wv
# For phonetic similarity etc.
from fastDamerauLevenshtein import damerauLevenshtein
from Levenshtein import distance,hamming,jaro_winkler,median,median_improve,seqratio,editops,ratio,jaro
from abydos.phonetic import *


# In[11]:


sd=SoundD()
metap=Metaphone()
snx=Soundex()
import gc

device = "cuda"
batch_size = 16 # reduce if low on GPU mem
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)
model = whisperx.load_model("large-v2", device, compute_type=compute_type,language="en")


# In[12]:


def check_encoding(w1,w2):
    if sd.encode(w1)==sd.encode(w2):
        return w2
    else:
        return None
def get_soundex(word):
    token = word.upper()
    soundex = ""
    soundex += token[0]
    dictionary = {"BFPV": "1", "CGJKQSXZ":"2", "DT":"3", "L":"4", "MN":"5", "R":"6", "AEIOUHWY":".","1234567890":""}
    for char in token[1:]:
        for key in dictionary.keys():
            if char in key:
                code = dictionary[key]
                if code != soundex[-1]:
                    soundex += code
    soundex = soundex.replace(".", "")
    soundex = soundex[:4].ljust(4, "0")
    return soundex
def transcribe_audio_file(ap,language="en"):
    audio_path=ap
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=batch_size)
    return result["segments"][0]["text"]
def pre_proc(pred):
    pred=pred.replace(" ", "")
    pred=pred.replace("(", "")
    pred=pred.replace(")", "")
    pred=pred.replace(",", "")
    return pred


# In[13]:


def get_matches(l,w):
    fin=[]
    sflag=0
    d1={a:distance(a,w)+hamming(a,w) for a in l["name"]}
    d2={a:ratio(a,w)+jaro_winkler(a,w) for a in l["name"]}
    one=min(d1.values())
    two=max(d2.values())
    rest=[[i for i in d1.keys() if d1[i]==one],[j for j in d2.keys() if d2[j]==two]]
    lst_soundD,lst_soundex,lst_mep,lst_dl=[],[],[],[]
    uno=snx.encode(w)
    dos=sd.encode(w)
    tres=metap.encode(w)
    lst_soundex.append([j for j in l[l.Soundex==uno].name])
    lst_soundD.append([j for j in l[l.SoundD==int(dos)].name])
    lst_mep.append([j for j in l[l.Metaphone==tres].name])
    dc={j:damerauLevenshtein(j,w.upper(),similarity=True) for j in df1["name"]}
    lst_dl=[i for i in dc.keys() if dc[i]==max(dc.values())]
    for i in lst_soundex[0]:
        i=i.upper()
        if i in lst_soundD[0] or i in lst_mep[0] or i in lst_dl:
            if i not in fin:
                fin.append(i)
                sflag=1
    if fin==[]:
        fin=lst_dl
    if len(fin)>2 and fin==lst_dl:
        fintemp=[]
        dictionary = {"BFPV": "1", "CGJKQSXZ":"2", "DT":"3", "L":"4", "MN":"5", "R":"6", "AEIOUHWY":"."}
        for i in fin:
            ichi=i[0]
            ichi2=i[1]
            ni2=w[1]
            ni=w[0]
            for j in dictionary.keys():
                if ichi in j and ni in j and i not in fintemp:
                    for k in dictionary.keys():
                        if ichi2 in k and ni2 in k and i not in fintemp:
                            fintemp.append(i)
        fin=fintemp
    elif len(fin)>=1 and fin!=lst_dl and sflag==1:
        fintemp=[]
        dictionary = {"BFPV": "1", "CGJKQSXZ":"2", "DT":"3", "L":"4", "MN":"5", "R":"6", "AEIOUHWY":"."}
        for i in fin:
            ichi=i[0]
            ichi2=i[1]
            ni2=w[1]
            ni=w[0]
            for j in dictionary.keys():
                if ichi in j and ni in j and i not in fintemp:
                    fintemp.append(i)
        for i in lst_dl:
            ichi=i[0]
            ichi2=i[1]
            ni2=w[1]
            ni=w[0]
            for j in dictionary.keys():
                if ichi in j and ni in j and i not in fintemp:
                    fintemp.append(i)
        fin=fintemp
        if len(fin)>0:
            d2={a:ratio(a,w) for a in fin}
            two=max(d2.values())
            fin=[j for j in d2.keys() if d2[j]==two]
    if len(fin)==1 and sflag==1:
        if distance(fin[0],w)> len(min(fin[0],w))/2:
            for i in range(len(l)):
                if sd.encode(l["name"][i])==sd.encode(w):
                    fin.append(check_encoding(w,l["name"][i]))
            d2={a:jaro_winkler(a,w) for a in fin}
            two=max(d2.values())
            fin=[j for j in d2.keys() if d2[j]==two]
    if len(fin)==0 and sflag==1:
        fintemp=[]
        dictionary = {"BFPV": "1", "CGJKQSXZ":"2", "DT":"3", "L":"4", "MN":"5", "R":"6", "AEIOUHWY":"."}
        for i in fin:
            ichi=i[0]
            ni=w[0]
            for j in dictionary.keys():
                if ichi in j and ni in j and i not in fintemp:
                    fintemp.append(i)
        fin=fintemp
    if len(fin)>1:
        return fin[0]
    else:
        return fin


# In[14]:


df1=pd.read_csv("final_cat.csv")
df2=pd.read_csv("catalogue_new.csv")
for i in range(len(df1)):
    df1["name"][i]=df1["name"][i].replace(" ","")


# In[20]:


def driver_code(ap):
    pred=transcribe_audio_file(ap)
    word=pre_proc(pred).replace(".","")
    word=word.replace("!","")
    lst=[]
    for i in df1["name"]:
        if check_encoding(word,i):
            lst.append(check_encoding(word,i))
    return [lst,word]


# In[21]:
def fin(path):
    i=path
    initial_word=driver_code(i)
    res=list(set(initial_word[0]))
    word=initial_word[1].upper()
    result=get_matches(df1,word)
    if len(result)==1:
        try:
            print(df2["name"][df1[df1.name==result[0]].index.values])
            return (df2["name"][df1[df1.name==result[0]].index.values].to_list()[0])
        except:
            return (result[0])
    else:
        try:
            print(df2["name"][df1[df1.name==result].index.values][0])
            return (df2["name"][df1[df1.name==result[0]].index.values].to_list()[0])
        except:
            return (result)
























