# C# 编程最佳实践

> Stub 版本：未填充。请按 stub 章节逐项与 AI 协作补全。
> 适用版本：C# 12 / .NET 8+

## 1. 静态类型与 nullable

TODO：启用 nullable reference types；`?` 与 `!` 的边界；何时该 `required`。

## 2. 命名约定

TODO：PascalCase 与 camelCase 的边界；接口前缀 `I`；async 方法后缀 `Async`；私有字段 `_camelCase`。

## 3. 文件成员顺序

TODO：using / namespace / class / 字段 / 构造 / 属性 / 方法的顺序；Microsoft 官方推荐。

## 4. 控制流与异常

TODO：异常 vs Result<T, E> 模式；early return vs single exit；using / using-declaration / IAsyncDisposable。

## 5. 集合与 LINQ

TODO：IEnumerable / IReadOnlyList / IList / List 的选择；LINQ 的性能边界（避免热路径 lazy 链）；ToList vs ToArray。

## 6. 异步与并发

TODO：async/await 全链路；ConfigureAwait(false) 的位置；CancellationToken 全链路透传；ValueTask 适用场景。

## 7. 内存与性能

TODO：struct vs class；Span<T> / Memory<T> 适用；ArrayPool；string 拼接（StringBuilder / string interpolation）。

## 8. 文档与 XML 注释

TODO：`///` 写公共 API；`<summary>` / `<param>` / `<returns>` 的最低门槛。

## 9. lint / format

TODO：dotnet format / EditorConfig / Roslyn analyzers；StyleCop / SonarLint 的取舍。

## 10. 反模式速查

TODO：async void、catch (Exception)、struct 大于 16 字节、可变 struct、Dispose 模式忘写。

## 11. 社区参考

- Microsoft C# 编码约定：https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions
- C# Language Design：https://github.com/dotnet/csharplang
- .NET API Guidelines：https://learn.microsoft.com/dotnet/standard/design-guidelines/
