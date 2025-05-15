import numpy as np
import base64
from typing import List

def split_audio(audio: np.ndarray, chunk_size: int) -> List[np.ndarray]:
    """
    将音频数据按 chunk_size 分片。
    :param audio: 输入音频的 numpy 数组
    :param chunk_size: 每片帧数
    :return: 分片后的 numpy 数组列表
    """
    return [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]


def audio_to_base64(audio: np.ndarray) -> str:
    """
    将 numpy 数组音频片段转为 base64 编码字符串。
    :param audio: 单个音频片段的 numpy 数组
    :return: base64 编码字符串
    """
    return base64.b64encode(audio.astype(np.float32).tobytes()).decode('utf-8') 