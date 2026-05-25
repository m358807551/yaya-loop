# Python 编程最佳实践

> Stub 版本：未填充。请按 stub 章节逐项与 AI 协作补全。
> 适用版本：Python 3.11+

## 1. 静态类型（type hints）

TODO：所有公开 API 必标 type hints；`from __future__ import annotations`；何时该用 `TypeVar` / `ParamSpec` / `Self`。

## 2. 命名约定

TODO：snake_case 函数与变量 / PascalCase 类 / CONSTANT_CASE 常量；模块名小写；`_` 前缀私有；`__` 前缀 name mangling 的边界。

## 3. 模块组织

TODO：`__init__.py` 的作用与 re-export；相对 import vs 绝对 import；package 与 namespace package。

## 4. 控制流与异常

TODO：早返回偏好；EAFP vs LBYL；自定义异常层级；finally vs context manager（with）；try/except/else 的 else 用法。

## 5. 集合与迭代

TODO：list / tuple / set / dict 选型；comprehension 何时该写、何时该拆成 for 循环；generator 的内存优势；遍历时修改容器的陷阱。

## 6. 异步与并发

TODO：asyncio / threading / multiprocessing 的边界；async with / async for；任务取消（`CancelledError`）；GIL 对并发的影响。

## 7. 数据类与不可变

TODO：`dataclass` / `pydantic.BaseModel` / `attrs` 的选择；`frozen=True` 的使用场景；`__slots__` 何时该写。

## 8. 文档字符串与类型

TODO：docstring 风格（Google / NumPy / reST）选一种；mypy / pyright / ruff 配置基线。

## 9. lint / format

TODO：ruff（推荐）/ flake8 + isort + black；启用规则集；CI 集成。

## 10. 反模式速查

TODO：可变默认参数（`def f(x=[])`）、from module import *、`except:` 裸捕获、循环里改 list、用 dict 模拟 enum、`__init__.py` 写业务逻辑。

## 11. 社区参考

- PEP 8：https://peps.python.org/pep-0008/
- PEP 484（类型提示）：https://peps.python.org/pep-0484/
- ruff 文档：https://docs.astral.sh/ruff/
