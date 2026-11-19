"""第 60 批：播放器拖动进度条，音乐从头爆一声，视频切下一段又对不上口型：音频..."""

def seek_position(target, keyframe):
    """seek 到关键帧。"""
    raise NotImplementedError("TODO: seek_position")

def timestamp_reset(base, seek_pos):
    """时间戳重置。"""
    raise NotImplementedError("TODO: timestamp_reset")

def fade_curve(t, duration):
    """seek 淡入淡出。"""
    raise NotImplementedError("TODO: fade_curve")

def buffer_clear(buffer):
    """清空环形缓冲。"""
    raise NotImplementedError("TODO: buffer_clear")

def timebase_convert(ts, num, den):
    """时间基换算。"""
    raise NotImplementedError("TODO: timebase_convert")

def preroll_drop(samples, preroll):
    """丢弃前置样本。"""
    raise NotImplementedError("TODO: preroll_drop")

def multitrack_seek(tracks, target):
    """多轨 seek。"""
    raise NotImplementedError("TODO: multitrack_seek")

def async_confirm(state, ui_pos):
    """异步确认。"""
    raise NotImplementedError("TODO: async_confirm")

def merge_requests(requests):
    """合并 seek 请求。"""
    raise NotImplementedError("TODO: merge_requests")

def av_clock(audio, video):
    """音视频时钟差。"""
    raise NotImplementedError("TODO: av_clock")

def cache_isolation(path, track):
    """PCM 缓存隔离键。"""
    raise NotImplementedError("TODO: cache_isolation")

def subtitle_sync(subtitle_t, seek_t):
    """字幕同步。"""
    raise NotImplementedError("TODO: subtitle_sync")

def buffer_clock(clock, buffering):
    """缓冲期时钟。"""
    raise NotImplementedError("TODO: buffer_clock")
