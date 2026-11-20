"""第 60 批：播放器拖动进度条，音乐从头爆一声，视频切下一段又对不上口型：音频...

音频 seek 管线的最小实现：解码位置、时间戳、淡入淡出、缓冲、
时间基、前置样本、多轨、异步确认、请求合并、音视频时钟、
PCM 缓存隔离、字幕同步与缓冲期时钟。
"""


def seek_position(target, keyframe):
    """seek 到关键帧。

    解码器只能从关键帧开始解码；目标位置早于关键帧时从关键帧起播，
    否则直接跳到目标位置。
    """
    return max(target, keyframe)


def timestamp_reset(base, seek_pos):
    """时间戳重置。

    seek 后输出时间戳以 ``base`` 为原点重新计算，而不是从 0 开始，
    避免与视频 PTS 错位。
    """
    return base + seek_pos


def fade_curve(t, duration):
    """seek 淡入淡出。

    返回 ``t`` 时刻的淡入增益，范围 ``[0, 1]``；``duration`` 为 0 时立即满音量。
    """
    if duration <= 0:
        return 1.0
    return max(0.0, min(1.0, t / duration))


def buffer_clear(buffer):
    """清空环形缓冲。

    原地清空，确保旧样本不会混入 seek 后的新位置。
    """
    buffer.clear()
    return buffer


def timebase_convert(ts, num, den):
    """时间基换算。

    把以 ``num/den`` 为时间基的时间戳换算为秒。
    """
    if den == 0:
        raise ZeroDivisionError("timebase denominator must be non-zero")
    return ts * num / den


def preroll_drop(samples, preroll):
    """丢弃前置样本。

    从关键帧解码时，前面 ``preroll`` 个样本早于 seek 目标，需要丢弃。
    """
    if preroll <= 0:
        return list(samples)
    return list(samples[preroll:])


def multitrack_seek(tracks, target):
    """多轨 seek。

    所有轨道同步 seek 到同一目标位置，避免评论轨停留在旧位置。
    """
    return [target for _ in tracks]


def async_confirm(state, ui_pos):
    """异步确认。

    硬件解码器 seek 异步完成：只有已就绪时才把新位置交给界面，
    否则返回 -1 表示界面继续显示旧时间。
    """
    return ui_pos if state == "ready" else -1


def merge_requests(requests):
    """合并 seek 请求。

    seek 过程中产生的多个请求只保留最终目标位置（取最大值），
    防止重复请求打乱顺序。
    """
    requests = list(requests)
    if not requests:
        return None
    return max(requests)


def av_clock(audio, video):
    """音视频时钟差。

    返回音频时钟与视频时钟之差，用于恢复播放后的同步校正。
    """
    return audio - video


def cache_isolation(path, track):
    """PCM 缓存隔离键。

    缓存键同时包含文件路径和音轨标识，切换音轨后不会复用旧 PCM。
    """
    return f"{path}:{track}"


def subtitle_sync(subtitle_t, seek_t):
    """字幕同步。

    seek 后字幕/章节时间整体平移到新的播放位置。
    """
    return subtitle_t + seek_t


def buffer_clock(clock, buffering):
    """缓冲期时钟。

    网络流触发重新缓冲时时钟暂停，避免缓冲期间时钟继续走。
    """
    return 0 if buffering else clock
