"""海面波浪：谱能量、色散与 LOD 接缝."""

import math

# 深水重力波色散关系使用的重力加速度。
GRAVITY = 9.81


def _flatten(values):
    """把任意嵌套的序列展开为一维列表。"""
    for value in values:
        if isinstance(value, (list, tuple)):
            yield from _flatten(value)
        else:
            yield value


def normalize_spectrum(amplitudes):
    """归一化波浪谱振幅，总和为 1。

    多方向波浪叠加时各分量振幅必须共享同一个总能量尺度，否则谱能量
    不守恒；总和为零（静水面）时退化为均匀分布。
    """
    values = [float(a) for a in amplitudes]
    total = sum(values)
    if total <= 0.0:
        n = len(values)
        if n == 0:
            return []
        return [1.0 / n] * n
    return [a / total for a in values]


def dispersion_wavelength(period):
    """深水波波长由周期按色散关系换算。

    深水重力波满足 ``L = g * T^2 / (2 * pi)``，不能用浅水或线性近似。
    """
    return GRAVITY * period * period / (2.0 * math.pi)


def align_lod_seam(left, right):
    """相邻 LOD 接缝高度取平均。

    左侧区块的末端和右侧区块的首端共用同一条接缝，取两侧高度的平均
    值写回两端，消除 LOD 切换时的高度跳变。
    """
    left = list(left)
    right = list(right)
    if not left or not right:
        return left, right
    seam = (left[-1] + right[0]) / 2.0
    left[-1] = seam
    right[0] = seam
    return left, right


def foam_amount(slope, speed, threshold):
    """泡沫量由坡度、速度与阈值共同决定。

    泡沫来自陡峭波面在风/流作用下的破碎，应按坡度而不是绝对高度判定；
    超过阈值的部分才产生泡沫，并限制在 [0, 1]。
    """
    amount = slope * speed - threshold
    if amount <= 0.0:
        return 0.0
    return min(amount, 1.0)


def wave_normal(heights, spacing):
    """按波高重算海面法线斜率。

    波高变化后必须重新计算表面斜率；用中心差分估计 x 方向斜率，返回
    未归一化的法线 ``[dh/dx, 1, dh/dz]``（一维波高时 z 方向斜率为 0）。
    """
    values = [float(h) for h in heights]
    if len(values) < 2 or spacing <= 0.0:
        return [0.0, 1.0, 0.0]
    slope_x = (values[-1] - values[0]) / ((len(values) - 1) * spacing)
    return [slope_x, 1.0, 0.0]


def reflect_direction(incident, normal):
    """入射方向按法线反射。

    反射探针的采样方向必须按法线重投影：``r = d - 2 * (d·n) * n``，
    其中 ``d`` 为入射方向，``n`` 为单位法线。
    """
    dot = sum(i * n for i, n in zip(incident, normal))
    return [i - 2.0 * dot * n for i, n in zip(incident, normal)]


def depth_fog(depth, density):
    """深度雾按指数衰减。

    深度与密度使用统一单位（米、每米），返回 ``1 - exp(-depth*density)``
    的雾浓度，0 表示无雾、1 表示完全遮蔽。
    """
    return 1.0 - math.exp(-depth * density)


def caustic_falloff(depth, scale):
    """焦散强度随深度衰减。

    焦散强度按 ``1 / (1 + depth * scale)`` 衰减，越深越弱。
    """
    return 1.0 / (1.0 + depth * scale)


def buoyancy_samples(hull_length, spacing):
    """浮力采样点数量按船体长度与间距计算。

    沿船体均匀布置采样点并包含首尾两端，数量为
    ``floor(hull_length / spacing) + 1``，避免采样间距与船体尺寸脱节。
    """
    if spacing <= 0.0:
        return 0
    return int(math.floor(hull_length / spacing)) + 1


def commit_chunks(statuses):
    """批量海面区块全部成功才提交。

    ``statuses`` 可包含嵌套区块状态；只有所有区块都成功时才返回 True，
    防止批量更新只应用一半。
    """
    return all(bool(status) for status in _flatten(statuses))
