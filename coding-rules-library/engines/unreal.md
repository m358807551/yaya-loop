# Unreal Engine 编程最佳实践

> Stub 版本：未填充。请按 stub 章节逐项与 AI 协作补全。
> 适用版本：UE 5.3+

## 1. 核心理念 / 项目结构

TODO：Actor / Component / Subsystem 三层心智模型；Modules 划分；C++ + Blueprint 双层职责边界。

## 2. 生命周期与帧

TODO：BeginPlay / Tick / EndPlay；GameInstance / World / Level / Actor 各自的生命周期；FTickFunction 与 Tickable 接口。

## 3. 资源管理

TODO：UAsset / Soft Reference / Async Load；Asset Manager 的角色。

## 4. 事件 / 消息机制

TODO：Multicast Delegate vs Event Dispatcher vs Subsystem broadcast；何时该走 Game Events Plugin。

## 5. 编辑器集成

TODO：UPROPERTY / UFUNCTION 标记常用项；Details Panel 自定义；Editor Module 划分。

## 6. 性能陷阱

TODO：Tick 滥用；BP 跨 Tick 调用 C++ 的开销；蓝图编译时间；Static Mesh 合批。

## 7. 调试工具

TODO：Stat 命令家族；Unreal Insights；Memory Profiler；Blueprint Debugger。

## 8. 反模式速查

TODO：Cast 滥用、God Actor、Singleton GameInstance 越长越大、BP 中循环依赖。

## 9. 社区参考

- Epic 官方编码规范：https://docs.unrealengine.com/5.0/en-US/epic-cplusplus-coding-standard-for-unreal-engine/
- Tom Looman 的 Unreal C++ 入门：https://www.tomlooman.com/unreal-engine-cpp-guide/
- Unreal Source Code（最佳学习材料）
