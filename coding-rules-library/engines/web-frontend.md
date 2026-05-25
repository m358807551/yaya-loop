# Web 前端最佳实践（React / Vue / Svelte 共用）

> Stub 版本：未填充。请按 stub 章节逐项与 AI 协作补全。
> 适用：React 18+ / Vue 3 / Svelte 4+。具体框架特性单独追加章节。

## 1. 核心理念 / 项目结构

TODO：组件按功能分目录（feature-first）vs 按类型分（type-first）的选择；page / component / hook / store 的划分。

## 2. 渲染生命周期

TODO：组件挂载/更新/卸载钩子（useEffect / onMounted / onMount）；副作用的清理；何时该 memoize。

## 3. 状态管理

TODO：local state vs context vs global store（Zustand / Pinia / Svelte stores）的选择标准；服务端状态用 TanStack Query / SWR 隔离。

## 4. 事件与跨组件通信

TODO：props down / events up；何时该上 event bus 或 pub-sub；避免 `forwardRef` + `useImperativeHandle` 滥用。

## 5. 样式约定

TODO：CSS modules / Tailwind / styled-components / vanilla-extract 的选择；设计 token 的位置。

## 6. 性能陷阱

TODO：不必要的 re-render；useEffect 依赖错误；列表 key 错误；图片懒加载与字体加载策略。

## 7. 可访问性与 SEO

TODO：语义化标签；ARIA 何时该写；SSR / SSG / ISR 的选择对 SEO 的影响。

## 8. 测试

TODO：单元（Vitest / Jest）+ 组件（Testing Library）+ E2E（Playwright / Cypress）的分层；测试覆盖哪些边界。

## 9. 反模式速查

TODO：`any` 满天飞、`useEffect` 内做 fetch 不取消、props drilling 三层以上、CSS 全局污染。

## 10. 社区参考

- React 官方文档：https://react.dev
- Vue 官方风格指南：https://vuejs.org/style-guide/
- Svelte 官方教程：https://svelte.dev/tutorial
