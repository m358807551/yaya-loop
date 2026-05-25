# Godot 编程最佳实践

> 本文件作为 `coding_rules.md` 第三部分（引擎最佳实践）的外部引入。
> 适用版本：**Godot 4.3+**（多数实践对 4.x 通用）。
> 本文件只覆盖 Godot 引擎特有的最佳实践，不重复主文件已经写过的通用原则。

---

## 一、核心理念：场景即可复用对象

在 Godot 里，**场景（Scene）不是"关卡"，而是"可复用的节点组合"**。一个按钮、一个敌人、一个 HUD、一个关卡都是场景。理解这一点之前的所有"组织方式"都会走偏。

- **任何足够独立的功能单元都应该成为一个独立场景**：角色、敌人、子弹、UI 面板、可拾取物。
- **场景应该能在编辑器里"单独运行"**（点 Play Scene 按钮）。如果一个场景脱离上下文就崩，说明它对外部依赖太重。
- **场景树按"逻辑关系"组织，而不是按"空间关系"**。比如玩家不一定要放在 `Room` 节点下，即使他在房间里——除非空间从属关系真的有意义。

---

## 二、节点通信的铁律

> 这是 Godot 项目最容易腐烂的地方，规则一旦立住，整个项目结构会清爽很多。

### 2.1 黄金法则："Call down, signal up"

- **向下调用**：父节点调用子节点用 `get_node()` 或 `$NodePath` 是 OK 的。
- **向上通信**：子节点要让父节点或同级节点知道事情发生，**一律用信号**，不要用 `get_parent()`。
- **同级通信**：通过共同的父节点中转——信号发到父亲，父亲调用兄弟。

### 2.2 禁止的反模式

绝对不要写这样的代码：

```gdscript
# 全部是反模式
get_node("../../SomeNode/SomeOtherNode")
get_parent().get_parent().get_node("SomeNode")
get_tree().get_root().get_node("SomeNode/SomeOtherNode")
```

原因：场景树一变，这些路径全废。一个能 `get_parent()` 的节点，就没法单独运行测试，也没法在别的场景里复用。

### 2.3 信号的正确用法

- **自定义信号用 `signal` 关键字声明**，用 `signal_name.emit(args)` 触发（Godot 4 语法）。
- **优先在编辑器面板里连接信号**，对预先存在的节点；运行时实例化的节点在代码里 `connect`。
- **连接信号用 `Callable`**：`button.pressed.connect(_on_pressed)` 而不是字符串方法名，能让编辑器静态检查方法存在性。
- **信号名用过去式或事件名**：`health_changed`、`died`、`item_collected`，不是 `change_health` 这种命令式。
- **emit 后立即返回，不要假设接收方做了什么**——发送方不应该关心有没有人在听。

### 2.4 跨场景/远距离通信：事件总线

当两个节点距离太远，逐级转发信号变成"信号迷宫"时，引入一个 **autoload 事件总线**：

```gdscript
# Events.gd（注册为 autoload）
extends Node

signal player_died
signal score_changed(new_score: int)
signal level_completed(level_id: String)
```

任意节点都可以 `Events.player_died.emit()` 或 `Events.score_changed.connect(_on_score_changed)`。

**克制使用**：事件总线滥用会让数据流变得不可追踪。原则是——
- **同一场景内、近距离的通信，不要走总线**，直接信号连接。
- 只有**跨场景、跨模块、链路过长**时才用总线。
- 总线信号要分类清楚（玩家事件、UI 事件、关卡事件等），不要堆成一个 God Object。

---

## 三、Autoload（单例）使用规范

### 3.1 什么时候用 Autoload

合适的场景：

- **跨场景持久数据**：玩家存档、设置、当前进度（`change_scene_to_file()` 会销毁旧场景，autoload 不会）。
- **全局服务**：音频管理器、场景切换器、本地化、输入映射。
- **事件总线**（见 2.4）。
- **只读全局配置**：游戏常量、难度参数。

### 3.2 什么时候不要用 Autoload

- 只在一个场景里用的状态——直接放节点里。
- 仅仅是"想全局访问方便"——优先考虑通过 `@export` 传引用、或者用 Resource 共享数据。
- 业务逻辑不要塞进 autoload，autoload 越长越大就是 God Object 的预兆。

### 3.3 Autoload 编码规范

- **命名用 PascalCase**：`PlayerData`、`AudioManager`、`Events`。从代码里直接当作全局名访问。
- **Autoload 节点应该是无表现层的**，纯数据 + 信号 + 公开方法，不要挂渲染节点。
- **读多写少**：autoload 写操作越多，耦合越严重。优先暴露查询方法和信号，让外部"通知"它，而不是外部直接改它的字段。

---

## 四、Resource：数据驱动的核心工具

> Godot 的 `Resource` 类系统是它最强大、也最被新手忽略的特性，类似 Unity 的 ScriptableObject。

### 4.1 何时用 Resource

- **静态数据**：物品定义、技能数值、敌人参数、关卡配置、对话脚本。
- **配置文件**：相比 JSON，Resource 在 Inspector 里可视化编辑、类型安全、能引用其他 Resource 和 Texture。
- **跨节点共享状态**：把数据装进 Resource，多个节点 `@export var data: PlayerStats` 引用同一份。

### 4.2 自定义 Resource 标准写法

```gdscript
# res://resources/enemy_stats.gd
class_name EnemyStats
extends Resource

@export var enemy_name: String = ""
@export var max_health: int = 100
@export var attack: int = 10
@export var icon: Texture2D
@export var loot_table: Array[ItemData] = []
```

然后在 FileSystem 右键 → New → Resource → `EnemyStats`，创建 `.tres` 文件，在 Inspector 里填数值。

### 4.3 Resource 的几个关键陷阱

1. **同一 `.tres` 文件在内存中只有一份**：多个节点 `@export` 引用同一个 `.tres`，**修改其中一个会影响全部**。这是优点也是陷阱。
   - 如果需要每个节点独立的副本：在 Resource Inspector 里勾选 `Local to Scene`，或者在代码里 `stats = stats.duplicate()`。
2. **`.tres` vs `.res`**：文本格式 vs 二进制。开发期一律用 `.tres`，对 git 友好、可读、能手动 diff。`.res` 只在最终发布或大体积资源（如关卡数据）才考虑。
3. **运行时只能写入 `user://`，不能写入 `res://`**。存档之类用 `ResourceSaver.save(res, "user://save.tres")`。
4. **Resource 没有 `_process`**，它不是节点，不参与场景树。它就是数据。
5. **自定义 Resource 不会自动触发 `changed` 信号**——需要在 setter 里 `emit_changed()`：
   ```gdscript
   @export var hp: int:
       set(value):
           if hp != value:
               hp = value
               emit_changed()
   ```

### 4.4 数据驱动的典型流程

1. 设计期：用 Resource 定义数据结构（`ItemData`、`SkillData`）。
2. 配置期：在 FileSystem 里批量创建 `.tres` 文件（每件物品一个）。
3. 运行期：用 `load("res://items/sword.tres")` 或 `@export` 引用。
4. 改数值：直接在 Inspector 改 `.tres`，**不需要碰代码**。

---

## 五、`@export` 和 `@onready` 的正确使用

### 5.1 `@export`：暴露给设计者

- **凡是"非程序员也应该能调"的参数**，都用 `@export` 暴露：速度、血量、冷却时间、关卡时长。
- **类型必须显式标注**：`@export var speed: float = 100.0`，不要让类型推断。
- **节点引用也用 `@export`**：`@export var target: Node2D`。比 `get_node("../../Target")` 灵活得多——在 Inspector 里拖拽连接，场景树结构变化不影响。
- 复杂导出修饰符在编辑器有专门支持：`@export_range(0, 100)`、`@export_file("*.json")`、`@export_color_no_alpha`、`@export_enum("Easy", "Normal", "Hard")`。

### 5.2 `@onready`：场景树准备好后再求值

- **专用于获取子节点引用**：`@onready var sprite: Sprite2D = $Sprite2D`。
- **绝对不要把 `@export` 和 `@onready` 标在同一个变量上**——`@onready` 会在 `_ready()` 阶段覆盖 `@export` 从场景文件加载的值，Godot 4 已经把这个组合标记为 warning。
- **`@onready` 也要写类型**，让编辑器自动补全。

### 5.3 GDScript 文件成员顺序（官方推荐）

按这个顺序写，新加成员时不要乱插：

```
1. @tool
2. class_name
3. extends
4. # 文档字符串（可选）
5. signals
6. enums
7. constants
8. @export 变量
9. 普通公开变量
10. 私有变量（_ 开头）
11. @onready 变量
12. _init / _ready / _process / _physics_process
13. 其他公开方法
14. 私有方法
```

---

## 六、生命周期与帧

### 6.1 几个回调的区别

| 回调 | 何时调用 | 用途 |
|------|---------|------|
| `_init()` | 对象创建时（场景树还没构建） | 初始化与场景无关的内部状态 |
| `_enter_tree()` | 节点加入场景树时 | 注册到外部系统 |
| `_ready()` | 节点及其所有子节点都已进入场景树 | **获取子节点引用、连接信号** |
| `_process(delta)` | 每帧（渲染帧） | 动画、UI 更新 |
| `_physics_process(delta)` | 每物理帧（固定步长，默认 60Hz） | 移动、碰撞、AI |
| `_exit_tree()` | 节点离开场景树 | 反注册、释放资源 |

### 6.2 规则

- **物理、移动、碰撞放 `_physics_process`**：固定步长，可重现，跨帧率一致。
- **纯视觉、UI 放 `_process`**：变化时间步，配合 `delta` 插值就好。
- **没有更新需求的节点不要保留空的 `_process`**：哪怕是空函数也会被引擎每帧调用。如果不需要，直接删掉，或者用 `set_process(false)` / `set_physics_process(false)` 关掉。
- **`_ready()` 只在节点初次进入场景树时调用一次**——`add_child()` 会触发，`reparent` 不会再触发。
- **不要在 `_init` 里访问 `$Child`**：那时候子节点还没建好，会拿到 null。

### 6.3 `await` 和协程

- `await signal_name` / `await get_tree().create_timer(1.0).timeout`：暂停当前函数，等信号或计时器。
- **协程中的节点可能在 `await` 期间被销毁**，恢复后要检查 `is_instance_valid(self)` 或 `is_queued_for_deletion()`，否则操作已释放节点会崩。
- 这是 Godot 4 一个已知坑：`queue_free()` 后协程仍可能再跑一帧。

---

## 七、场景切换与节点生命周期

### 7.1 场景切换

- **`get_tree().change_scene_to_file("res://levels/level2.tscn")`**：切换主场景，**销毁旧场景下所有节点**（autoload 除外）。
- **`change_scene_to_packed(packed_scene)`**：用预加载好的 PackedScene 切换，避免运行时 IO 卡顿。
- **大场景预加载**：`var next_scene = preload("res://levels/big_level.tscn")` 或 `ResourceLoader.load_threaded_request()`。

### 7.2 创建和销毁节点

- **实例化**：`var enemy = enemy_scene.instantiate(); add_child(enemy)`。注意是 `instantiate()`，不是 Godot 3 的 `instance()`。
- **销毁**：用 `queue_free()`，**不要用 `free()`**——`queue_free` 在帧末统一销毁，避免遍历过程中删除导致的崩溃。
- **检查节点有效性**：用 `is_instance_valid(node)`，特别是异步代码恢复后。

---

## 八、性能注意事项（Godot 特有）

> 通用原则参考主文件 2.7。这里只列 Godot 特有的。

- **节点实例化是有成本的**。Godot 4 比 3 快很多，但每秒上百次的 `instantiate()` 仍然会卡顿。子弹、粒子、伤害数字这类高频对象用对象池。
- **对象池实现：**
  - 池里的对象用 `hide()` + `set_process(false)` + `set_physics_process(false)` + 从场景树 `remove_child()`，或者只是设置 `visible = false`。
  - **不要用 `set_deferred("process_mode", ...)`** 来停用池化对象——这是已知性能陷阱。
  - 池中对象不要放在 `process` 模式 `INHERIT` 下还指望省 CPU。
- **海量同质对象用 `MultiMeshInstance2D` / `MultiMeshInstance3D`** 或直接 `RenderingServer` API，绕过场景树开销。粒子、子弹幕、tile 装饰物的常见做法。
- **避免每帧字符串拼接**：`print("hp: " + str(hp))` 这种放热路径会有 GC 压力。
- **`get_node()` 有路径查找成本**：在 `_process` 里反复调用同一个 `get_node` 是反模式，缓存到 `@onready` 变量里。
- **`Orphan Nodes` 是泄漏信号**：在 Debugger → Monitors 里看，数字一直涨说明有节点 `remove_child` 后没 `queue_free`。

---

## 九、编辑器使用约定

### 9.1 文件系统

- **按功能（场景）分目录**：`scenes/player/` 下放 `player.tscn`、`player.gd`、`player.png`、`player_walk.tres`。同一个功能的所有相关资源在一起，不要 `scenes/`、`scripts/`、`textures/` 这种按类型分。
- **第三方资产统一放 `addons/`**，包含 LICENSE。
- **不希望显示的目录放空的 `.gdignore` 文件**（如脚本模板目录、临时工作目录）。
- **文件夹颜色**：右键 → Set Folder Color，用颜色区分核心模块、addon、临时目录。

### 9.2 命名约定（Godot 特有部分）

- **场景文件、脚本文件、目录用 `snake_case`**：`player_controller.gd`、`enemy_data.tres`。
- **C# 脚本文件用 `PascalCase`**（C# 文件名要和类名一致）。
- **场景内节点名用 `PascalCase`**：`PlayerSprite`、`HealthBar`，方便 `$PlayerSprite` 这种引用。
- **GDScript 的 `class_name` 用 `PascalCase`**：`class_name PlayerStats`。
- **某场景专属的子资源加前缀**：`player_idle.tres`、`player_run.tres`，方便搜索定位。

### 9.3 静态类型与警告

- **Godot 4.2+ 启用 Untyped Declarations 警告**（Project Settings → Debug → GDScript）：强制所有变量、函数返回值标类型。带来更好的自动补全和编译期错误。
- **简写类型推断用 `:=`**：`var enemies := []`、`var speed := 100.0`。
- **删除前用 "View Owners"**：FileSystem 里右键资源 → View Owners，检查谁在用，避免误删导致引用断裂。

---

## 十、信号连接的两种方式：编辑器 vs 代码

| 方式 | 何时用 |
|------|--------|
| 编辑器面板连接 | 场景里**预先存在的节点**之间的连接（如按钮 → 主控脚本） |
| 代码 `connect()` | 运行时**实例化**的节点（如子弹生成后连接 `body_entered`） |

- **编辑器连接的好处**：连接关系在 `.tscn` 文件里可见，git diff 能看到。
- **编辑器连接的坏处**：跨文件追踪困难，重构方法名容易漏掉。
- **代码连接的好处**：所有依赖关系集中在 `_ready()` 里，一眼看完。
- **代码连接的坏处**：阅读场景文件时看不到连接关系。

**项目内统一一种风格**，不要混用。本项目（在 `game_coding_rules.md` 1.1 第 4 条之下）默认：**编辑器内的同场景静态连接走面板，跨场景或动态实例化走代码**。

---

## 十一、Godot 特有的反模式速查

- **`get_parent()` / `get_node("../X")`**：见 2.2。
- **`$Child` 在 `_init()` 里访问**：节点还没建好。
- **@export + @onready 标在同一变量**：见 5.2。
- **空的 `_process` / `_physics_process`**：白白消耗每帧调用。
- **每帧 `get_node()`**：缓存到 `@onready` 变量。
- **`free()` 替代 `queue_free()`**：遍历删除会崩。
- **Resource 共享被忽视**：以为每个节点持有独立副本，结果改一个影响一片。
- **autoload 越长越大**：变成 God Object，所有跨模块依赖都塞进去。
- **场景树里搜索节点用 `find_child` / `get_tree().get_nodes_in_group()` 在热路径**：开销不低，缓存结果。
- **信号名用命令式**（`set_health` 而不是 `health_changed`）：搞混了"我让你做什么"和"我发生了什么"。

---

## 十二、调试与验证工具

- **Debugger → Profiler**：在你怀疑性能问题时开，先测后改。
- **Debugger → Monitors**：实时看 FPS、Process Time、Draw Calls、Node Count、Orphan Nodes。Node Count 持续上涨 = 泄漏。
- **Remote 场景树**：游戏运行时切到 Remote 标签，看实际的场景树结构。新手常被"场景里看到的"和"运行时实际的"差异坑到。
- **Play Scene（F6）**：单独运行当前场景，验证场景的独立性（参考第一节）。如果场景跑不起来，说明对外部依赖太重。