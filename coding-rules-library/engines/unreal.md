# Unreal Engine best practices

> **Incomplete stub:** Complete each TODO section with the AI before treating this as project-tested guidance.
> **Supported version:** Unreal Engine 5.3 and later.

## 1. Core model and project structure

TODO: Define the Actor, Component, and Subsystem model; module boundaries; and the responsibility split between C++ and Blueprint.

## 2. Lifecycle and frames

TODO: Cover BeginPlay, Tick, and EndPlay; the lifetimes of GameInstance, World, Level, and Actor; and when to use FTickFunction or Tickable interfaces.

## 3. Resource management

TODO: Define UAsset, soft references, asynchronous loading, and the role of Asset Manager.

## 4. Events and messaging

TODO: Choose among Multicast Delegates, Event Dispatchers, and Subsystem broadcasts, and define when the Game Events Plugin is appropriate.

## 5. Editor integration

TODO: Document common UPROPERTY and UFUNCTION specifiers, Details Panel customization, and Editor Module boundaries.

## 6. Performance traps

TODO: Cover excessive Tick usage, Blueprint-to-C++ calls across Tick, Blueprint compilation time, and Static Mesh batching.

## 7. Debugging tools

TODO: Document Stat commands, Unreal Insights, Memory Profiler, and Blueprint Debugger.

## 8. Anti-pattern checklist

TODO: Excessive Cast usage, God Actors, an ever-growing singleton GameInstance, and Blueprint circular dependencies.

## 9. References

- [Epic C++ coding standard](https://docs.unrealengine.com/5.0/en-US/epic-cplusplus-coding-standard-for-unreal-engine/)
- [Tom Looman's Unreal Engine C++ guide](https://www.tomlooman.com/unreal-engine-cpp-guide/)
- Unreal Engine source code
