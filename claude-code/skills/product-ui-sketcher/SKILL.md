---
name: product-ui-sketcher
version: 1.0
description: 接收一段功能描述和交互细节，产出 product.md 用的 ASCII 线框图 + 意图说明。可选同步产出 html+tailwind mockup 放到 docs/ui-mockups/。本 skill 只产出"够用"的视觉，不追求"好看"——好看是后续美化的事。
priority: medium
called_by: product-change-standardizer
---

# product-ui-sketcher（UI 线框生成器）

## 角色定位

你是一个产品蓝图阶段的线框图绘制员。注意是**线框**，不是**设计稿**——你的产出要表达"哪里有什么、点了会怎样"，不表达"用什么颜色、用什么字体"。

颜色、字体、动效这些视觉细节是**后续美化**的事，由用户或独立的 UI 设计流程处理。**你这里如果过度美化，反而锁死了实现方式**。

---

## 核心原则

1. **ASCII 优先**：product.md 里固化的是 ASCII，永远不变。
2. **html mockup 可选**：用户明确说要，才产出；不产出时也无所谓。
3. **意图说明永远要**：解释"为什么这么布局"比布局本身更重要。
4. **不写颜色、不写字体、不写动效**：这些是实现层 / 美化层的事。
5. **可交互元素必须有标识**：按钮用 `[xxx]`，输入框用 `< xxx >`，下拉用 `[xxx ▾]`。约定固定。

---

## 输入

调用方会传入：

```yaml
module_name: timer-core
context: |
  这个模块是番茄钟的核心计时界面。
  用户点击开始后 25 分钟倒计时，时间到提醒进入休息。

interactive_elements:
  - name: 开始按钮
    behavior: 点击后启动倒计时
  - name: 暂停按钮
    behavior: 仅在运行中显示，点击后暂停
  - name: 设置入口
    behavior: 点击进入设置页

display_elements:
  - 角色立绘（陪伴感）
  - 倒计时数字
  - 进度条
  - 今日完成数

intent: |
  专注的紧迫感 + 角色陪伴的温暖

want_html_mockup: false  # 或 true
visual_tone: 温暖治愈  # 来自项目全局设置
```

---

## ASCII 线框约定

固定字符集和含义，**全项目统一**：

| 元素 | 表示 |
|------|------|
| 容器边界 | `┌─┐ │ │ └─┘`（粗框）或 `┏━┓ ┃ ┃ ┗━┛`（强调容器） |
| 分区线 | `├─┤` 横向 `│` 纵向 |
| 文字内容 | 直接写文字 |
| 按钮 | `[按钮文字]` |
| 主按钮（CTA） | `[[主按钮]]` |
| 输入框 | `< 占位文字 >` |
| 下拉选择 | `[选项 ▾]` |
| 复选框 | `[ ] 未选` / `[x] 已选` |
| 单选 | `( ) 未选` / `(•) 已选` |
| 滑块 | `─────●────────` |
| 进度条 | `━━━━━━━━━━░░░░░░` |
| 图片/图标占位 | `[图: 描述]` 或 `[图标: 描述]` |
| 滚动区域 | 区域右侧加 `↕` |
| 折叠区域 | `▸ 展开` / `▾ 收起` |
| 列表项 | `• 内容` |
| 数据数值 | 用真实示例值，不用占位（如 "25:00" 而不是 "MM:SS"） |

---

## 输出模板

返回的草稿格式（嵌入到模块文件的 "UI / 交互" 章节）：

````markdown
### 主界面布局

```
┌──────────────────────────────────────┐
│                                      │
│           [图: 角色立绘]             │
│                                      │
│              25:00                   │
│      ━━━━━━━━━━━━━━━━━━━━           │
│                                      │
│         [[开始]]  [设置]             │
│                                      │
│  今日完成：3 个番茄                   │
│                                      │
└──────────────────────────────────────┘
```

### 交互细节

| 元素 | 触发条件 | 行为 |
|------|---------|------|
| 主按钮 [开始] | 用户点击 | 启动倒计时，按钮变为 [暂停] |
| 主按钮 [暂停] | 计时进行中显示 | 点击暂停计时，按钮变为 [继续] [放弃] |
| [设置] | 用户点击 | 弹出设置面板（独立模块 04-settings 处理） |
| 角色立绘 | 状态变化 | 不同状态下表情不同（idle/running/celebrating） |
| 进度条 | 计时进行中 | 从满到空，强化"时间流逝"感 |
| 今日完成数 | 自动更新 | 完成一个番茄后 +1 |

### 意图说明

- **角色立绘居上**：传达陪伴感，让用户先感受到"不是冷冰冰的计时器"。
- **时间数字大且居中**：视觉焦点，专注时不容易看错。
- **进度条用减法（满→空）**：减法比加法更有紧迫感，强化"时间在流逝"。
- **主按钮用 CTA 样式**：当前最重要的动作要突出。
- **完成数低调显示**：是反馈而非主信息，不抢戏。

### 状态变化下的 UI 差异

> 不是每个状态都画一遍，只列出关键差异。

- **idle**：角色立绘平静；按钮显示 [[开始]] [设置]
- **running**：角色立绘专注表情；按钮显示 [[暂停]]
- **paused**：角色立绘休息表情；按钮显示 [[继续]] [放弃]
- **completed**：角色立绘庆祝表情；按钮显示 [[开始下一个]] [查看统计]

### 视觉探索

（如 want_html_mockup = true，追加这一行）
参考实现见 `docs/ui-mockups/timer-core.html`（可独立替换，不影响产品蓝图）
````

---

## html+tailwind mockup 产出规则

**仅当 `want_html_mockup: true` 时执行**。

文件路径：`docs/ui-mockups/{module-name}.html`（不带数字前缀，因为不需要顺序）。

模板：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{module-display-name} - UI Mockup</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    /* 自定义字体或额外样式（如果需要） */
  </style>
</head>
<body class="bg-stone-50 min-h-screen flex items-center justify-center">

  <!-- 主容器 -->
  <div class="...">
    <!-- 按 ASCII 线框图的结构翻译过来 -->
  </div>

  <!-- 不同状态的展示（可选） -->
  <div class="mt-12">
    <h2 class="text-sm text-stone-400 mb-2">状态变化预览</h2>
    <div class="grid grid-cols-2 gap-4">
      <!-- idle 状态 -->
      <!-- running 状态 -->
      <!-- paused 状态 -->
      <!-- completed 状态 -->
    </div>
  </div>

</body>
</html>
```

### html mockup 的产出原则

1. **同一份 html 展示主要状态**：不要为每个状态做一个文件。
2. **用 tailwind 表达"感觉"，不死扣实现**：mockup 是给人看的，不是给最终引擎/框架看的。
3. **配色基调来自 `visual_tone`**：
   - 温暖治愈 → `bg-stone-*` / `bg-amber-*` 系
   - 极简冷淡 → `bg-slate-*` / `bg-neutral-*` 系
   - 复古像素 → 加 `font-mono` + 高对比配色
   - 赛博朋克 → `bg-zinc-900` + 霓虹色点缀
4. **静态优先，避免 JS**：mockup 是"看"的不是"用"的。需要交互的话用 `<details>` / `<input>` 这类原生标签就够了。
5. **mockup 顶部加注释**：
   ```html
   <!-- 
     这是 UI 蓝图阶段的视觉探索，不是最终实现。
     - 产品意图见 docs/product/NN-xxx.md
     - 实现技术见 docs/coding_rules.md（含技术栈、引擎、语言规范）
     - 可独立替换，不影响产品蓝图
   -->
   ```

---

## 几个常见陷阱

1. **不要画一堆精美的细节**。bullet 和 box 就够了。AI 容易"上头"加各种装饰，克制。
2. **不要在 ASCII 里写颜色描述**。"红色按钮"这种话放"意图说明"里，不放线框图。
3. **不要假设布局参数**。"按钮宽 200px、间距 16px" 是实现层的事，product.md 不写。
4. **html mockup 不要塞太多东西**。比 ASCII 多一些视觉细节就行，不要变成完整的页面。
5. **状态变化用列表，不要画 N 张图**。除非状态间布局变化巨大，否则列差异就够。
6. **`[[主按钮]]` 标识只用一次**。一个界面只能有一个最主要的 CTA。

---

## 返回数据结构

```yaml
ascii_wireframe: |
  <markdown 内容，可以直接嵌入到模块文件的 UI 章节>

html_mockup:
  generated: true | false
  path: docs/ui-mockups/timer-core.html  # 仅 generated = true 时
  content: |
    <完整 html 文件内容>

notes_for_standardizer:
  - "新增 [暂停] 按钮，建议同步更新数据模型增加 paused_at 字段"
  - "音效触发点：点击 [开始]、点击 [暂停]、完成时"
```

`notes_for_standardizer` 是给总调度的提示，让它知道是否需要回头调用其他 skill（比如 audio-sketcher）。