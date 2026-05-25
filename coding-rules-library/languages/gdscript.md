# GDScript 编程最佳实践

> 本文件作为 `coding_rules.md` 第四部分（编程语言最佳实践）的外部引入。
> 适用版本：**GDScript 2.0**（Godot 4.x，4.3+ 默认）。
> 本文件只覆盖 GDScript 语言层面的实践，引擎层面（节点、信号、Resource、autoload）见 `engine-rules.md`（Godot），通用原则（设计模式、命名思想）见主文件 `coding_rules.md`。

---

## 一、静态类型：默认开启，不要省

> 这是 GDScript 最重要的一条实践，违反它项目腐烂速度会快一个数量级。

GDScript 是**渐进类型**的——可以全部不写类型也能跑。但**不写类型就不要用 GDScript**：你失去了自动补全、编译期错误检查，还有 28%-59% 的性能损失（基于 Godot 官方基准）。

### 1.1 强制规则

- **所有变量、参数、返回值都标类型**。Project Settings → Debug → GDScript → Untyped Declarations 设为 Warning 或 Error。
- **类型推断用 `:=`**（编译器能从右值推出来时）；**显式标注用 `:`**（编译器推不出，或想让代码更清晰时）。

```gdscript
# 推荐：右值类型明显，用推断
var speed := 100.0                    # float
var enemies := []                     # Array（但元素类型未知）
var position := Vector2(10, 20)       # Vector2

# 推荐：右值类型不明显或需要约束，显式标注
var enemies: Array[Enemy] = []        # 显式 typed array
@onready var sprite: Sprite2D = $Sprite2D
var damage: int = stats.attack        # 不写就推断成 Variant

# 函数签名一律标完整
func apply_damage(target: Node, amount: int) -> void:
    target.health -= amount

func find_nearest_enemy(from: Vector2) -> Enemy:
    # ...
    return null  # 返回类型显式，调用方知道可能拿到 null
```

### 1.2 Typed Array / Typed Dictionary

- **集合一律带元素类型**：`Array[Enemy]`、`Array[int]`、`Dictionary[String, ItemData]`（Dictionary 类型需要 Godot 4.4+）。
- **嵌套泛型只能一层**：`Array[Array]` 可以，`Array[Array[int]]` 不行（内层只能 untyped）。
- **typed array 在写入时做运行时检查**，类型不对会报错——这是优点，能在 bug 现场抓到，而不是后面 100 行才发现。

### 1.3 类型不是教条

- **闭包/小工具临时变量**用 `var x = foo()` 也无所谓——能读懂就好。
- **`Variant` 是合法工具**，不是耻辱：`Dictionary.get()`、`Array.pop_back()` 这类返回 Variant，接住就行。
- **`as` 类型转换的两种行为要记住**：
  - 转 Object 类型失败返回 `null`（安全）：`var p := body as Player` 然后 `if not p: return`
  - 转内置类型失败**直接崩**：`value as int` 如果 value 是 String 会崩。

---

## 二、命名约定

> 这一部分覆盖 GDScript 语言层面的命名。文件名、节点名、场景名等引擎层面的约定在 `godot最佳实践.md` 9.2。

### 2.1 标识符大小写

| 对象 | 风格 | 示例 |
|------|------|------|
| 变量、函数 | `snake_case` | `player_health`、`apply_damage()` |
| 私有变量、私有函数、虚函数 | `_snake_case`（下划线前缀） | `_internal_state`、`_ready()` |
| 常量 | `CONSTANT_CASE` | `MAX_HEALTH`、`DEFAULT_SPEED` |
| 枚举类型名 | `PascalCase` | `enum Direction` |
| 枚举成员 | `CONSTANT_CASE` | `Direction.NORTH` |
| `class_name` | `PascalCase` | `class_name PlayerStats` |
| 信号名 | `snake_case`，过去式或事件式 | `health_changed`、`died`、`item_collected` |
| 信号回调方法 | `_on_<signal_name>` 或 `_on_<source>_<signal_name>` | `_on_pressed`、`_on_player_died` |

### 2.2 文件名与 class_name 的关系

- **`.gd` 文件名 = `class_name` 转 `snake_case`**：`class_name PlayerStats` → `player_stats.gd`。
- 这避免跨平台大小写敏感问题（Windows 不分大小写，Linux 分）。

### 2.3 数字字面量约定

- **浮点数必带前导和后导零**：`0.5` 而不是 `.5`；`2.0` 而不是 `2.`。
- **大数用下划线分隔**：`1_000_000` 而不是 `1000000`。

### 2.4 命名表达意图

继承主文件 4.2 的通用原则，这里只补充 GDScript 相关的：

- **不要把类型嵌在名字里**：写 `health: int = 100` 而不是 `int_health = 100`。静态类型本身已经说明类型。
- **布尔用 `is_` / `has_` / `can_` / `should_` 开头**：`is_alive`、`has_key`、`can_jump`。
- **函数名是动词短语**：`spawn_enemy`、`apply_damage`，不是 `enemy_spawn`、`damage_handle`。
- **避免缩写**，行业通名除外（`pos`、`vel`、`hp`、`dt`、`fps`、`xy`）。

---

## 三、文件成员顺序（GDScript 官方推荐）

新加内容要按这个顺序插入，**不要往末尾乱堆**。

```gdscript
@tool                                          # 1. 编辑器工具脚本标注
class_name PlayerController                    # 2. 类名
extends CharacterBody2D                        # 3. 继承

## 玩家角色控制器                              # 4. 文档字符串（双 ##）
## 处理移动、跳跃、攻击等核心行为

signal health_changed(new_health: int)         # 5. 信号
signal died

enum State {                                   # 6. 枚举
    IDLE,
    RUNNING,
    JUMPING,
}

const MAX_HEALTH := 100                        # 7. 常量
const JUMP_VELOCITY := -400.0

static var instance_count: int = 0             # 8. 静态变量

@export var speed: float = 200.0               # 9. 导出变量
@export var max_jumps: int = 2

var current_health: int = MAX_HEALTH           # 10. 普通公开变量
var current_state: State = State.IDLE

var _jumps_remaining: int = 0                  # 11. 私有变量（_ 前缀）
var _last_damage_source: Node = null

@onready var sprite: Sprite2D = $Sprite2D      # 12. @onready 变量
@onready var hitbox: Area2D = $Hitbox

func _init() -> void:                          # 13. _init
    instance_count += 1

func _ready() -> void:                         # 14. _ready
    health_changed.connect(_on_health_changed)

func _process(delta: float) -> void: pass      # 15. _process / _physics_process
func _physics_process(delta: float) -> void: pass

func take_damage(amount: int) -> void:         # 16. 公开方法
    current_health -= amount
    health_changed.emit(current_health)

func _on_health_changed(new_value: int) -> void:  # 17. 私有方法（信号回调等）
    pass
```

注意 `@export` 要在普通变量之前，`@onready` 在普通变量之后——这是官方推荐顺序，**编辑器创建脚本的模板就是这个顺序**。

---

## 四、缩进与格式

- **用 Tab 缩进**，不用空格（Godot 编辑器默认）。
- **LF 行尾**，不是 CRLF。
- **UTF-8 编码，无 BOM**。
- **文件末尾保留一个换行符**。
- **延续行用 2 级缩进**，与正常代码块区分：

```gdscript
# 推荐
var result := some_long_function(
        first_argument,
        second_argument,
        third_argument,
)

# 长条件用括号包起来，逻辑运算符放行首
if (some_condition_that_is_long
        and another_condition
        and yet_another_one):
    do_something()
```

---

## 五、`@export` 与 `@onready` 实战

> 注：基本规则在 `godot最佳实践.md` 第五节已经覆盖；这里补充 GDScript 语言细节。

### 5.1 `@export` 的常用变体

```gdscript
@export var speed: float = 100.0                  # 基础
@export_range(0, 100, 1) var health: int = 100    # 范围 + 步长
@export_range(0.0, 1.0, 0.01) var volume: float   # 浮点滑块
@export_enum("Easy", "Normal", "Hard") var difficulty: int  # 下拉选项
@export_file("*.json") var config_path: String    # 文件选择器
@export_dir var save_dir: String                  # 目录选择器
@export_color_no_alpha var tint: Color            # 颜色（无 alpha）
@export_multiline var description: String         # 多行文本
@export_node_path("Sprite2D") var sprite_path: NodePath  # 限定节点类型
@export_group("Movement")                         # 分组（之后的导出归入该组）
@export var speed: float
@export var jump_height: float
@export_group("")                                 # 结束分组
```

### 5.2 setter / getter 语法

Godot 4 的 setter/getter 写法和 Godot 3 不同：

```gdscript
var hp: int = 100:
    set(value):
        if hp != value:
            hp = value
            health_changed.emit(hp)
    get:
        return hp

# 简写：只有 setter
var name: String = "":
    set(value):
        name = value
        _update_label()

# 用独立函数：
var hp: int = 100:
    set = _set_hp,
    get = _get_hp

func _set_hp(value: int) -> void:
    hp = value
    health_changed.emit(hp)

func _get_hp() -> int:
    return hp
```

**陷阱**：setter 里直接 `self.x = value` 会**无限递归**。要么写 `hp = value`（直接赋后端字段），要么用 backing field（`_hp`）。

---

## 六、信号语法（Godot 4 风格）

> 注：信号的架构使用见 `godot最佳实践.md` 第二节；这里只讲 GDScript 语法。

### 6.1 声明与触发

```gdscript
# 声明带类型的信号参数（强烈推荐）
signal health_changed(new_health: int, max_health: int)
signal died

# 触发（Godot 4 用 .emit，不是 emit_signal()）
health_changed.emit(current_hp, MAX_HEALTH)
died.emit()
```

### 6.2 连接

```gdscript
# 推荐：Callable 风格，编辑器能静态检查方法存在
button.pressed.connect(_on_button_pressed)

# 带绑定参数
button.pressed.connect(_on_button_pressed.bind("attack"))

# 一次性连接（触发一次后自动断开）
timer.timeout.connect(_on_timeout, CONNECT_ONE_SHOT)

# 延迟到 idle 帧再调用
some_signal.connect(_on_some_signal, CONNECT_DEFERRED)

# 用 lambda 做临时回调
button.pressed.connect(func(): print("clicked"))

# 不推荐：字符串方法名（Godot 3 风格，没有静态检查）
button.connect("pressed", self, "_on_button_pressed")  # ✗
```

### 6.3 信号回调命名

- 自己监听自己的信号：`_on_<signal_name>`，如 `_on_pressed`、`_on_health_changed`。
- 监听别人的信号：`_on_<source>_<signal_name>`，如 `_on_player_died`、`_on_enemy_hit`。

---

## 七、Lambda 与 Callable

GDScript 2.0 支持 lambda（函数字面量）。**临时小函数用 lambda，复用的用普通函数**。

```gdscript
# 用于排序、过滤、map
var sorted := enemies.duplicate()
sorted.sort_custom(func(a, b): return a.threat > b.threat)

var visible_enemies := enemies.filter(func(e): return e.is_visible())
var damages := enemies.map(func(e): return e.attack)
var total := enemies.reduce(func(acc, e): return acc + e.attack, 0)

# 用于信号回调
button.pressed.connect(func(): score += 10)

# 命名 lambda（在栈追踪中显示名字，调试更友好）
var compute_damage := func compute(base: int, multi: float) -> int:
    return int(base * multi)
print(compute_damage.call(10, 1.5))

# 闭包：捕获外部变量
func _ready():
    var threshold := 50
    var high_hp := enemies.filter(func(e): return e.hp > threshold)
```

### 7.1 Lambda 的注意点

- **调用 lambda 用 `.call()`**：`my_lambda.call(arg1, arg2)`，不能直接 `my_lambda(...)`。这是 Callable 的统一约定。
- **闭包按值捕获**：lambda 创建时捕获变量的快照。但**引用类型（Array、Dictionary、Object）的内容修改是共享的**：

```gdscript
var counter := 0
var inc := func(): counter += 1  # 修改的是 lambda 内的副本
inc.call()
print(counter)  # 仍然是 0

var items := []
var add_item := func(): items.append(1)  # Array 是引用，修改的是同一个
add_item.call()
print(items)  # [1]
```

- **lambda 不能是 static**。复用的工具函数用普通 static 函数。

### 7.2 性能提示

热路径里用 lambda 做 `filter/map` 有调用开销，比直接写 for 循环慢。**冷路径用 lambda 求可读性，热路径（每帧调用、大数组迭代）用 for 循环**。

---

## 八、错误处理

> GDScript **没有 try-catch**。不要被网上某些过时教程误导。

### 8.1 三种错误信号

```gdscript
# 1. assert：开发期断言，发布版可关闭（默认关闭）
# 用于"绝不应该发生"的不变式
func take_damage(amount: int) -> void:
    assert(amount >= 0, "damage amount must be non-negative")
    health -= amount

# 2. push_error：报错并记录，但程序继续运行
# 用于"出错了但能容忍"的情况
func load_config(path: String) -> Dictionary:
    if not FileAccess.file_exists(path):
        push_error("config file not found: %s" % path)
        return {}
    # ...

# 3. push_warning：警告，不影响运行
func deprecated_function() -> void:
    push_warning("deprecated_function is deprecated, use new_function instead")
```

### 8.2 不存在的关键字

- **没有 `throw`**：GDScript 不能抛出异常。
- **没有 `try` / `except`**：不能捕获异常。
- **没有 `finally`**：用 `_exit_tree()` 或 `func _notification(what)` 处理清理。

### 8.3 错误处理模式

由于没有异常，约定俗成的做法：

**模式一：返回错误码 + 输出参数（Godot API 风格）**

```gdscript
var file := FileAccess.open("res://data.json", FileAccess.READ)
if not file:
    var err := FileAccess.get_open_error()
    push_error("failed to open: %s" % err)
    return
```

**模式二：返回 null + 调用方检查**

```gdscript
func find_enemy_by_id(id: int) -> Enemy:
    for e in enemies:
        if e.id == id:
            return e
    return null

var e := find_enemy_by_id(42)
if not e:
    return
```

**模式三：返回结构体（包含 success + 数据 + 错误信息）**

```gdscript
class Result:
    var success: bool
    var data: Variant
    var error: String

func load_data() -> Result:
    var r := Result.new()
    # ...
    return r
```

### 8.4 关于 null

GDScript 的 null 是个常见 bug 源：

- **函数返回可能为 null**：明确写在返回类型上（`-> Enemy`）并标注在文档里。调用方必须检查。
- **`is_instance_valid(node)`**：检查 Object 是否还活着（没被 free）。访问已释放对象会**直接崩**，所以 await 之后、协程中要先检查。
- **`node.is_queued_for_deletion()`**：检查节点是否已经 `queue_free()` 过但还没真正释放。
- **数组/字典默认值用空容器，不用 null**：`var items: Array[Item] = []` 而不是 `var items: Array[Item] = null`。少一道判断。

---

## 九、文档字符串

GDScript 4 用 `##` 双井号写文档字符串，编辑器和文档生成器能识别。

```gdscript
## 玩家角色控制器。
##
## 处理移动、跳跃、攻击等核心行为。
## 不负责输入采集——输入由 [InputHandler] 单独处理。
class_name PlayerController
extends CharacterBody2D

## 玩家当前血量。降至 0 时触发 [signal died]。
var current_health: int = 100

## 对玩家造成伤害。
## [param amount] 伤害值，必须 >= 0。
## [param source] 伤害来源节点，用于伤害日志。
## 返回剩余血量。
func take_damage(amount: int, source: Node) -> int:
    # ...
    return current_health
```

要点：

- **`##` 是文档注释**，`#` 是普通注释。两者作用不同。
- **支持 BBCode**：`[b]粗体[/b]`、`[code]代码[/code]`、`[param x]`、`[signal foo]`、`[method bar]`、`[member baz]`。
- **类的文档字符串写在 `class_name` 行之后、`extends` 行之后**（成员顺序见第三节）。
- **重要的公开 API 都要写**；私有方法（`_` 前缀）可以不写。

---

## 十、控制流惯例

### 10.1 函数 return 的位置

- **`return` 用在函数的开头（守卫语句）或结尾**。
- **避免在函数中间 return**，让数据流容易追踪。

```gdscript
# 推荐：开头守卫 + 结尾返回
func apply_damage(target: Node, amount: int) -> int:
    if not is_instance_valid(target):
        return 0
    if amount <= 0:
        return 0

    var actual_damage := _calculate_damage(target, amount)
    target.health -= actual_damage
    return actual_damage

# 不推荐：中间 return 多个分支
func apply_damage(target: Node, amount: int) -> int:
    if is_instance_valid(target):
        if amount > 0:
            var d := _calc(target, amount)
            target.health -= d
            return d
        else:
            return 0
    return 0
```

### 10.2 迭代修改容器

**遍历时不要修改容器**——会跳元素或越界。

```gdscript
# 反模式
for e in enemies:
    if e.is_dead:
        enemies.erase(e)  # ✗ 跳元素

# 推荐：filter 反向构造
enemies = enemies.filter(func(e): return not e.is_dead)

# 推荐：倒序遍历删除
for i in range(enemies.size() - 1, -1, -1):
    if enemies[i].is_dead:
        enemies.remove_at(i)

# 推荐：先收集要删的，再统一删
var to_remove: Array[Enemy] = []
for e in enemies:
    if e.is_dead:
        to_remove.append(e)
for e in to_remove:
    enemies.erase(e)
```

### 10.3 三元运算符

GDScript 用 Python 风格（`a if cond else b`），**不是 `cond ? a : b`**：

```gdscript
var status := "alive" if hp > 0 else "dead"
var first := items[0] if not items.is_empty() else null
```

---

## 十一、Packed Arrays（性能场景）

GDScript 有专门的紧凑数组类型，存大量同质数据时性能更好：

| 类型 | 用途 |
|------|------|
| `PackedByteArray` | 字节流（文件、网络） |
| `PackedInt32Array` / `PackedInt64Array` | 整数数组 |
| `PackedFloat32Array` / `PackedFloat64Array` | 浮点数组 |
| `PackedStringArray` | 字符串数组 |
| `PackedVector2Array` / `PackedVector3Array` | 向量数组（粒子位置、路径点） |
| `PackedColorArray` | 颜色数组 |

**何时用**：
- 元素量上万、且类型同质。
- 性能敏感的迭代或修改。
- 网络传输或文件序列化（直接转 PackedByteArray）。

**何时不用**（用普通 `Array[T]`）：
- 元素量在几百以内——便利性更重要。
- 类型混合或需要存对象。
- 频繁 insert/erase（Packed 数组的修改开销更高）。

---

## 十二、static 关键字（Godot 4）

GDScript 4 支持静态变量、静态函数、静态构造器：

```gdscript
class_name MathUtils
extends Object

# 静态变量：全类共享
static var instance_count: int = 0

# 静态函数：不依赖实例
static func clamp_angle(angle: float) -> float:
    return fposmod(angle + PI, TAU) - PI

# 静态构造器：脚本加载时执行一次
static func _static_init() -> void:
    print("MathUtils loaded")
```

**用途**：
- **工具函数库**：纯函数式的辅助方法（`MathUtils.clamp_angle(x)`）。
- **类级别计数器**：全类共享的统计。

**注意**：
- 静态函数**无法访问 `self` 和实例成员**。
- **Lambda 不能是 static**。
- 静态变量在脚本卸载时清空，**不是真正的全局**——跨场景持久数据还是用 autoload + Resource。

---

## 十三、GDScript 反模式速查

- **不写类型**：见第一节。
- **`@onready` 和 `@export` 标在同一变量**：`@onready` 在 `_ready()` 阶段覆盖 `@export` 的值，Godot 4 会发出 `ONREADY_WITH_EXPORT` 警告。
- **setter 里 `self.x = value`**：无限递归。
- **遍历容器时修改容器**：跳元素或越界。见 10.2。
- **`free()` 替代 `queue_free()`**：见 `godot最佳实践.md`。
- **`emit_signal("name", args)` 字符串风格**：Godot 4 用 `signal_name.emit(args)`，Godot 3 风格已经过时。
- **`connect("signal", self, "method")` 字符串风格**：Godot 4 用 `signal.connect(callable)`，参考 6.2。
- **return 在函数中间多处**：见 10.1。
- **过度使用 `Variant`**：所有 untyped 变量都是 Variant，性能损失 + 失去静态检查。
- **lambda 滥用在热路径**：见 7.2。
- **`==` 比较节点用引用相等**：节点比较用 `==`（Godot 内部就是引用比较），但**不要比较已释放的节点**，先 `is_instance_valid`。
- **数组用 `null` 作默认值**：用 `[]`，少一道判断。
- **每帧 `print`**：日志会被刷爆，肉眼看不过来；用 `print` + 计数器，或者直接断点。

---

## 十四、调试小工具

- **`print()`**：基础输出。
- **`prints("hp:", hp, "pos:", position)`**：自动加空格分隔，多值调试方便。
- **`printt(...)`**：用 Tab 分隔，列对齐。
- **`print_debug()`**：附带文件名和行号。
- **`breakpoint`**：代码里写这一行，运行时触发断点（编辑器内运行）。
- **`OS.alert("message")`**：弹窗（调试时用，发布版不要留）。
- **`@warning_ignore("unused_variable")`**：临时压制某条警告。滥用是反模式——警告通常是对的。