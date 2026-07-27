# Day 17：模块与 import 实验

在 `code/` 目录下运行（确保当前目录包含这些文件）：

```bash
cd python/phase1-核心语法/code/day17-import-lab
```

## 实验 1：`__name__ == "__main__"`

```bash
# 直接运行：会打印「作为脚本直接运行」
python greet.py

# 被 import：只打印「模块被加载」，不进 if 分支
python -c "import greet"
```

观察：同一个文件，**直接运行**时 `__name__` 是 `"__main__"`；**被 import** 时是模块名 `"greet"`。

## 实验 2：`import x` vs `from x import y`

```bash
python import_styles.py
```

观察：

- `import math_utils` → 通过 `math_utils.add` 访问，命名空间清晰。
- `from math_utils import multiply` → 当前文件可直接写 `multiply()`，但不知道来自哪个模块。
- 同一模块无论 import 几次，**顶层 print 只出现一次**（模块缓存）。

## 实验 3：循环导入（会炸）

```bash
python -c "import module_a"
```

预期：`ImportError` 或 `AttributeError`（部分初始化）。看 traceback 里 A、B 谁先谁后。

## 实验 4：延迟 import 缓解循环依赖

`module_b_lazy.py` 顶层不再 import A，只在 `func_b()` 被调用时才 import：

```bash
python -c "from module_b_lazy import func_b; print(func_b())"
```

对比实验 3：A、B 顶层互相 import 必炸；**拆掉一边的顶层 import**（或抽到第三个模块）才能打破环。

## 记录

做完后把结论写进 [`../../notes/01-学习手册.md`](../../notes/01-学习手册.md) Day 17 记录区。
