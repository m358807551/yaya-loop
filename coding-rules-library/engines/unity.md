# Unity best practices

> **Incomplete stub:** Complete each TODO section with the AI before treating this as project-tested guidance.
> **Supported version:** Unity 2022.3 LTS and later; most guidance should also apply to Unity 6 releases.

## 1. Core model and project structure

TODO: Define the boundary between MonoBehaviour and ScriptableObject and establish feature-first organization with Assembly Definitions.

## 2. Lifecycle and frames

TODO: Define when to use Awake, OnEnable, Start, Update, FixedUpdate, and LateUpdate, and how to choose among Coroutine, UniTask, and Task.

## 3. Resource management

TODO: Define when to use Resources, Addressables, or AssetBundles, and how ScriptableObject is used for configuration or event channels.

## 4. Events and messaging

TODO: Choose among UnityEvent, C# events, and ScriptableObject event channels. Explain why SendMessage and BroadcastMessage should be avoided.

## 5. Editor integration

TODO: Define the `[SerializeField]` private-field convention, custom Inspector boundaries, and when Odin Inspector is justified.

## 6. Performance traps

TODO: Cover per-frame `GetComponent` and `Find`, common GC.Alloc sources, and when to use a custom pool or `UnityEngine.Pool`.

## 7. Debugging tools

TODO: Document Profiler, Memory Profiler, Frame Debugger, and Recorder workflows.

## 8. Anti-pattern checklist

TODO: Pervasive MonoBehaviour singletons, `Find` inside Update, deeply nested Coroutines, and excessive Inspector wiring.

## 9. References

- [Unity Manual](https://docs.unity3d.com/Manual/index.html)
- [Unity C# Style Guide](https://unity.com/resources/c-sharp-style-guide-e-book)
- [Unity Entities documentation](https://docs.unity3d.com/Packages/com.unity.entities@latest)
