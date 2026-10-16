{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # description: \
from earsketch import *\
\
setTempo(122)\
# Jazz House (Extended) with Legato Sax - EarSketch (Python)\
from earsketch import *\
\
init()\
setTempo(122)\
\
# ---------- SOUNDS (swap from the Sound Browser if needed) ----------\
KICK   = OS_KICK01\
CLAP   = OS_CLAP01\
HAT    = OS_OPENHAT01\
SNARE  = OS_SNARE01\
\
CHORDS = HIPHOP_DUSTYGROOVE_001   # replace with a jazz piano/keys loop\
BASS   = Y11_BASS_2       # replace with a warm bass loop\
SAX    = HIPHOP_DUSTYGROOVE_007   # REPLACE with a sustained sax note\
\
# ---------- TRACKS ----------\
T_KICK, T_CLAP, T_HAT, T_SNARE = 1, 2, 3, 4\
T_CHORDS, T_BASS, T_SAX = 5, 6, 7\
\
# ---------- SECTION MAP (measures) ----------\
# Intro     1-9\
# Groove    9-17\
# Verse    17-33   (sax enters)\
# Breakdown 33-41  (no drums or bass)\
# Drop     41-65   (full band + sax)\
# Outro    65-73\
\
# ---------- CHORDS: whole song ----------\
fitMedia(CHORDS, T_CHORDS, 1, 73)\
setEffect(T_CHORDS, FILTER, FILTER_FREQ, 300, 1, 8000, 9)   # intro filter sweep\
setEffect(T_CHORDS, FILTER, FILTER_FREQ, 8000, 33, 1200, 37) # breakdown muffle\
setEffect(T_CHORDS, FILTER, FILTER_FREQ, 1200, 37, 8000, 41) # reopen into drop\
\
# ---------- BASS ----------\
fitMedia(BASS, T_BASS, 9, 33)\
fitMedia(BASS, T_BASS, 41, 69)\
\
# ---------- DRUM HELPER ----------\
def drums(start, end, kick=True, clap=True, hat=True, ghost=False):\
    for m in range(start, end):\
        if kick:\
            makeBeat(KICK, T_KICK, m, "0+++0+++0+++0+++")\
        if clap:\
            makeBeat(CLAP, T_CLAP, m, "----0-------0---")\
        if hat:\
            makeBeat(HAT, T_HAT, m, "--0---0---0---0-")\
        if ghost:\
            makeBeat(SNARE, T_SNARE, m, "------0-----0-0-")\
\
drums(9, 17, clap=False, ghost=False)       # groove: kick + hats only\
drums(17, 33, ghost=False)                  # verse: add claps\
drums(41, 65, ghost=True)                   # drop: everything + ghost snares\
drums(65, 69, clap=False, hat=False)        # outro: just kick\
\
# Build-up fill before the drop: snare rolls in the last 2 measures of the breakdown\
for m in range(39, 41):\
    makeBeat(SNARE, T_SNARE, m, "0-0-0-0-0-0-0000")\
\
# ---------- LEGATO SAX ----------\
# Trick: one sustained sax sample per phrase, then automate PITCHSHIFT.\
# Notes hold their pitch, then glide into the next with no gap = legato.\
# Values are semitones above the sample's original pitch.\
GLIDE = 0.12   # glide length in measures (shorter = tighter, longer = silkier)\
\
def sax_phrase(start, notes):\
    total = 0\
    for n in notes:\
        total += n[1]\
    fitMedia(SAX, T_SAX, start, start + total)\
    t = start\
    for i in range(len(notes)):\
        shift = notes[i][0]\
        length = notes[i][1]\
        end = t + length\
        if i < len(notes) - 1:\
            nxt = notes[i + 1][0]\
            setEffect(T_SAX, PITCHSHIFT, PITCHSHIFT_SHIFT, shift, t, shift, end - GLIDE)\
            setEffect(T_SAX, PITCHSHIFT, PITCHSHIFT_SHIFT, shift, end - GLIDE, nxt, end)\
        else:\
            setEffect(T_SAX, PITCHSHIFT, PITCHSHIFT_SHIFT, shift, t, shift, end)\
        t = end\
\
# Each phrase is 8 measures: (semitone shift, length in measures)\
PHRASE_A = [(0, 1), (3, 0.5), (5, 0.5), (7, 1.5), (5, 0.5), (3, 1), (2, 1), (0, 2)]\
PHRASE_B = [(7, 1), (10, 0.5), (12, 0.5), (10, 1), (7, 1), (5, 1.5), (3, 0.5), (0, 2)]\
\
sax_phrase(17, PHRASE_A)    # verse\
sax_phrase(25, PHRASE_B)\
sax_phrase(41, PHRASE_A)    # drop\
sax_phrase(49, PHRASE_B)\
sax_phrase(57, PHRASE_A)\
\
setEffect(T_SAX, REVERB, REVERB_TIME, 2500)\
setEffect(T_SAX, DELAY, DELAY_TIME, 375)\
setEffect(T_SAX, DELAY, DELAY_FEEDBACK, -20)\
\
# ---------- MIX ----------\
setEffect(T_KICK,   VOLUME, GAIN, -4)\
setEffect(T_CLAP,   VOLUME, GAIN, -8)\
setEffect(T_HAT,    VOLUME, GAIN, -12)\
setEffect(T_SNARE,  VOLUME, GAIN, -14)\
setEffect(T_BASS,   VOLUME, GAIN, -6)\
setEffect(T_SAX,    VOLUME, GAIN, -7)\
\
# ---------- OUTRO FADE ----------\
setEffect(T_CHORDS, VOLUME, GAIN, -8, 1, -8, 65)\
setEffect(T_CHORDS, VOLUME, GAIN, -8, 65, -60, 73)\
\
finish()}