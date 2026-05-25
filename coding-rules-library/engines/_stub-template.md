# {{ENGINE_NAME}} 编程最佳实践

> Stub 版本：未填充。建议在前 3 个 feature 实现过程中由 AI + 用户协作补全。
> 安装方式：BOOTSTRAP STEP 3 由 AI 复制本文件为 `docs/coding-rules/engine-rules.md`，引导用户填关键章节。
> 适用版本：{{ENGINE_VERSION}}

## 必填章节（按 stub 顺序逐一填充）

凡新填一节，删除该节顶部的 `TODO` 标记。所有 TODO 都消失时，本文件升级为「实战版」（去掉首行的 stub 警告）。

---

## 1. 核心理念 / 项目结构

TODO：本引擎或平台的核心组织模型是什么（场景树 / 组件 ECS / Actor / 路由层级）？项目目录约定（按功能分还是按文件类型分）？

## 2. 生命周期与帧

TODO：哪些回调按帧调用？固定步长 vs 变化步长的边界在哪？协程 / await / async 行为？暂停语义？

## 3. 资源管理

TODO：如何加载 / 实例化 / 引用？资源是否可热重载？引擎自带的资源系统（如 Unity 的 ScriptableObject / Godot 的 Resource）应优先使用什么场景？

## 4. 事件 / 消息机制

TODO：本引擎首选的事件机制是什么（信号 / event / observable / pub-sub）？跨场景通信用什么（事件总线 / 服务定位器）？

## 5. 编辑器集成

TODO：编辑器面板暴露字段的写法（如 `@export` / `[SerializeField]`）？预制体 / 蓝图工作流？编辑器辅助工具（gizmo / inspector 自定义）何时该写？

## 6. 性能陷阱

TODO：本引擎特有的热点（如每帧字符串分配 / GetComponent / 节点查找）？对象池适用场景？

## 7. 调试工具

TODO：内置 profiler / monitor 怎么用？常见泄漏信号（如 Orphan Nodes 增长）？热重载支持程度？

## 8. 反模式速查

TODO：本引擎社区共识的"千万别这么写"清单。

## 9. 社区参考

- [TODO 官方文档链接]
- [TODO 社区最佳实践链接]
- [TODO 著名样板项目链接]
