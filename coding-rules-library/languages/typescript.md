# TypeScript 编程最佳实践

> Stub 版本：未填充。请按 stub 章节逐项与 AI 协作补全。
> 适用版本：TypeScript 5.4+

## 1. 静态类型与 strict 模式

TODO：tsconfig 必启 strict 全套；`any` / `unknown` / `never` 的边界；`as` 类型断言的滥用警惕。

## 2. 命名约定

TODO：PascalCase 类型 / camelCase 变量与函数 / CONSTANT_CASE 常量；接口前缀 `I` 之争（本项目选哪边）；type vs interface 的选择标准。

## 3. 模块组织

TODO：barrel files (`index.ts`) 利弊；named export vs default export；circular import 检测。

## 4. 控制流与错误处理

TODO：异常 vs Result 模式（neverthrow / fp-ts）；early return；Discriminated Union 表达可能失败的返回。

## 5. 集合与函数式 API

TODO：数组 `map` / `filter` / `reduce` 的可读性边界；`for...of` 与 `forEach` 的选择；不可变数据结构（Immer / structuredClone）。

## 6. 异步与并发

TODO：async/await 全链路；AbortController 取消；Promise.all / Promise.allSettled / Promise.race 的边界。

## 7. 类型工具与高级类型

TODO：常用工具类型（`Pick` / `Omit` / `Partial` / `Required` / `Record`）；条件类型与映射类型的可读性边界；`satisfies` 何时用。

## 8. lint / format

TODO：ESLint + Prettier 配置基线；typescript-eslint 严格规则集；import 排序规则。

## 9. 反模式速查

TODO：`any` 满天飞、`as` 强转绕过类型、空 catch、Promise 未 await、`Object.assign` 替代 spread。

## 10. 社区参考

- TypeScript 官方手册：https://www.typescriptlang.org/docs/handbook/intro.html
- typescript-eslint 推荐规则：https://typescript-eslint.io/rules/
- Type Challenges（提升类型功力）：https://github.com/type-challenges/type-challenges
