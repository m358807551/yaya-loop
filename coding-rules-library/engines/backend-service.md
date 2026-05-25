# 后端服务最佳实践（无引擎，纯服务）

> Stub 版本：未填充。请按 stub 章节逐项与 AI 协作补全。
> 适用：REST / GraphQL / RPC 服务，任何语言实现。

## 1. 核心理念 / 项目结构

TODO：按业务领域分目录（DDD-style）vs 按技术层分（controller / service / repository）的选择；路由文件的边界。

## 2. 请求生命周期

TODO：middleware 顺序；请求级 context（trace id / user id）的传递；超时与取消的层层透传。

## 3. 数据持久化

TODO：ORM vs 原生 SQL；事务边界；连接池配置；migration 工具与历史。

## 4. 错误处理与日志

TODO：错误分类（client error vs server error）；HTTP 状态码语义；结构化日志（JSON）；trace / metric / log 三件套的接入。

## 5. 鉴权与权限

TODO：session / JWT / OAuth 的选择；权限粒度（路由级 / 资源级 / 字段级）；CSRF / XSS 防御。

## 6. 性能与可观测性

TODO：N+1 查询识别；缓存层级（本地 / Redis / CDN）；APM 工具；慢查询日志。

## 7. 并发与限流

TODO：限流算法（令牌桶 / 漏桶 / 滑动窗口）；幂等性设计；分布式锁的使用边界。

## 8. 测试

TODO：单元测试与集成测试的边界；contract test；测试数据的隔离（per-test schema / transaction rollback）。

## 9. 反模式速查

TODO：业务逻辑写进 controller、ORM 关系级联误删、N+1 查询、错误消息泄漏内部细节。

## 10. 社区参考

- 12-Factor App：https://12factor.net/
- Microsoft REST API Guidelines：https://github.com/microsoft/api-guidelines
- Google API Design Guide：https://cloud.google.com/apis/design
