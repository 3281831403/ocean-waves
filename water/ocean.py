"""海面波浪：谱能量、色散与 LOD 接缝：待实现的核心模块。"""


def normalize_spectrum(amplitudes):
    """归一化波浪谱振幅，总和为 1。"""
    raise NotImplementedError

def dispersion_wavelength(period):
    """深水波波长由周期按色散关系换算。"""
    raise NotImplementedError

def align_lod_seam(left, right):
    """相邻 LOD 接缝高度取平均。"""
    raise NotImplementedError

def foam_amount(slope, speed, threshold):
    """泡沫量由坡度、速度与阈值共同决定。"""
    raise NotImplementedError

def wave_normal(heights, spacing):
    """按波高重算海面法线斜率。"""
    raise NotImplementedError

def reflect_direction(incident, normal):
    """入射方向按法线反射。"""
    raise NotImplementedError

def depth_fog(depth, density):
    """深度雾按指数衰减。"""
    raise NotImplementedError

def caustic_falloff(depth, scale):
    """焦散强度随深度衰减。"""
    raise NotImplementedError

def buoyancy_samples(hull_length, spacing):
    """浮力采样点数量按船体长度与间距计算。"""
    raise NotImplementedError

def commit_chunks(statuses):
    """批量海面区块全部成功才提交。"""
    raise NotImplementedError
