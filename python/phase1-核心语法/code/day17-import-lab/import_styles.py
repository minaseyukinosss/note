"""实验：import x  vs  from x import y。"""

print("=== 1. import 整个模块 ===")
import math_utils

print("math_utils.add(2, 3) =", math_utils.add(2, 3))
print("模块对象:", math_utils)

print("\n=== 2. from ... import 单个名字 ===")
from math_utils import multiply

print("multiply(4, 5) =", multiply(4, 5))
# print(add(1, 2))  # NameError：没有 import add，只能用 multiply

print("\n=== 3. import 后再 from import（同一模块只加载一次）===")
from math_utils import add

print("add(10, 20) =", add(10, 20))
