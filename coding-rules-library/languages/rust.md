# Rust 编程最佳实践

> Stub 版本：未填充。请按 stub 章节逐项与 AI 协作补全。
> 适用版本：Rust 1.75+（Edition 2021）

## 1. 类型系统与所有权

TODO：所有权 / 借用 / 生命周期心智模型；`Clone` 何时是设计气味；`Copy` 适用边界；类型转换（`as` / `From` / `TryFrom`）的优先级。

## 2. 命名约定

TODO：snake_case 函数与变量 / PascalCase 类型与 trait / SCREAMING_SNAKE_CASE 常量；getter 不带 `get_` 前缀；构造方法 `new` / `with_xxx` / `try_new`。

## 3. 项目组织

TODO：crate / module / file 的对应关系；`mod.rs` vs 同名文件；workspace 适用场景；feature flags 的最低门槛。

## 4. 错误处理

TODO：`Result<T, E>` 全链路；`?` 操作符；错误类型设计（thiserror / anyhow 的选择）；panic 的合法边界。

## 5. 集合与迭代

TODO：Vec / VecDeque / HashMap / BTreeMap 选型；Iterator trait 的链式调用；`collect::<Result<_, _>>()` 模式。

## 6. 异步与并发

TODO：tokio vs async-std vs smol；`Send + Sync` 约束；channel 选型（mpsc / oneshot / broadcast）；`spawn` 与任务生命周期。

## 7. 性能与内存

TODO：Box / Rc / Arc 的选择；Cow<'_, T> 的使用场景；零拷贝 (`&str` / `&[u8]`)；何时该 `#[inline]`。

## 8. unsafe 边界

TODO：使用 unsafe 的合法理由；如何最小化 unsafe 块；常见 UB 模式（aliasing / lifetime extension / uninit memory）。

## 9. 文档与测试

TODO：`///` 文档注释 + doctest；`#[cfg(test)]` 模块；integration test 目录约定；cargo doc 风格。

## 10. lint / format

TODO：rustfmt 配置；clippy 默认 + 推荐 lint 集；CI 必跑 `cargo fmt --check && cargo clippy -- -D warnings`。

## 11. 反模式速查

TODO：unwrap 满天飞、Clone 滥用、`mut` 滥用、过度泛型 / where 子句、`Arc<Mutex<_>>` 替代借用、忽视 lifetime warnings。

## 12. 社区参考

- Rust API Guidelines：https://rust-lang.github.io/api-guidelines/
- Rust by Example：https://doc.rust-lang.org/rust-by-example/
- The Rustonomicon（unsafe 必读）：https://doc.rust-lang.org/nomicon/
