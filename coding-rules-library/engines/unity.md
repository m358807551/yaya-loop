# Unity 编程最佳实践

> Stub 版本：未填充。请按 stub 章节逐项与 AI 协作补全。
> 适用版本：Unity 2022.3 LTS+（多数实践对 6000.x 通用）

## 1. 核心理念 / 项目结构

TODO：MonoBehaviour 与 ScriptableObject 的边界；按功能分目录的 Assemblies Definition 实践。

## 2. 生命周期与帧

TODO：Awake / OnEnable / Start / Update / FixedUpdate / LateUpdate 的差异与选择；Coroutine 与 UniTask / Task 的取舍。

## 3. 资源管理

TODO：Resources / Addressables / AssetBundle 三选一的判断；ScriptableObject 作为配置/事件总线。

## 4. 事件 / 消息机制

TODO：UnityEvent vs C# event vs ScriptableObject Event 的取舍；Send/Broadcast Message 为何应避免。

## 5. 编辑器集成

TODO：`[SerializeField]` 私有字段惯例；Inspector 自定义；OdinInspector 介入点。

## 6. 性能陷阱

TODO：每帧 GetComponent / Find 的开销；GC.Alloc 来源；Object Pool 选型（自己写 vs UnityEngine.Pool）。

## 7. 调试工具

TODO：Profiler / Memory Profiler / Frame Debugger / Recorder 用法。

## 8. 反模式速查

TODO：单例 MonoBehaviour 满天飞、`Find` 在 Update 里、Coroutine 嵌套地狱、Inspector 拖拽过深。

## 9. 社区参考

- Unity 官方手册：https://docs.unity3d.com/Manual/index.html
- Microsoft Unity C# Style Guide：https://unity.com/resources/c-sharp-style-guide-e-book
- Unity Pure ECS 文档（DOTS）：https://docs.unity3d.com/Packages/com.unity.entities@latest
