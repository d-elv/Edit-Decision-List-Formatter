framerate = 25


def seconds(value):
    if isinstance(value, str):  # value seems to be a timestamp
        _zip_ft = zip((3600, 60, 1, 1/framerate), value.split(':'))
        return sum(f * float(t) for f,t in _zip_ft)
    elif isinstance(value, (int, float)):  # frames
        return value / framerate
    else:
        return 0

def timecodeParser(seconds):

    # Jank mode (more accurate than below. Still not correct)
    return '{h:02d}:{m:02d}:{s:02d}:{f:02d}' \
        .format(h=int(seconds/3600),
            m=int(seconds/60%60),
            s=int(seconds%60),
            f=int((seconds-int(seconds))*27.942))


    # Original code (Doesn't fully work)

    # return '{h:02d}:{m:02d}:{s:02d}:{f:02d}' \
    # .format(h=int(seconds/3600),
    #         m=int(seconds/60%60),
    #         s=int(seconds%60),
    #         f=int((seconds-int(seconds))*framerate))

    # hh = (seconds/3600)
    # mm = (seconds/60%60)
    # ss = (seconds%60)
    # ff =
    # return "{} : {} : {} : {}".format(hh, mm, ss, ff)






def _frames(seconds):
    return seconds * framerate

def tc_to_fr(timecode, start=None):
    return _frames(seconds(timecode))

def fr_to_tc(frames, start=None):
    return timecodeParser(seconds(frames))

# print(tc_to_fr('00:00:12:20')) # 320
# print(fr_to_tc(320))  # '00:00:12:20'
# testTC = 580
# fr_to_tc(testTC)
# tc_to_fr(testTC)
# testTC = testTC + 10005
# fr_to_tc(testTC)
# testTCinfr = fr_to_tc(testTC)
# print(testTCinfr)
#
# 10585 frames in 423.4 seconds.
# There is 2.5 frames to 0.1 second.