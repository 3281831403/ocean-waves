# 海面波浪：谱能量、色散与 LOD 接缝

海面在远近距离同时出现平滩和锯齿：波浪谱多方向叠加后能量不守恒，深水波长用错色散关系，LOD 接缝高度跳变，泡沫按高度而不是坡度判定，法线不随波高重算，反射探针斜视角投影错，深度雾和透明度单位混用，焦散不随深度衰减，浮力采样点与船体尺寸不匹配，批量海面区块只更新一半。

## 目录结构

```
README.md
conftest.py
.gitignore
water/__init__.py
water/ocean.py
tests/test_ocean.py
```

## 当前状态

`water/ocean.py` 中所有函数只保留签名与文档字符串，函数体统一
`raise NotImplementedError`。`tests/test_ocean.py` 有 15 个参数化用例，
初始全部失败。

## 需要修复的 10 个问题

1. 波浪谱振幅归一化
2. 深水波长按色散关系换算
3. LOD 接缝高度对齐
4. 泡沫按坡度与速度判定
5. 波高变化后重算法线
6. 反射探针按法线重投影
7. 深度雾与透明度统一单位
8. 焦散强度随深度衰减
9. 浮力采样点按船体尺寸计算
10. 批量海面区块统一提交

## 验收

```bash
python -m pytest -q
```

初始应得到 `15 failed`，且没有 collection error。实现 `water/ocean.py`
后 15 条用例应全部通过。
