# ErisPulse AdminControl

ErisPulse 管理控制模块 - 提供框架管理和命令执行功能

## 功能特性

AdminControl 模块为 ErisPulse 框架提供了完整的管理控制功能，包括：

- [组件列表查询] - 查看已注册的模块和适配器
- [状态监控] - 查看模块和适配器的详细状态
- [框架管理] - 重启框架、加载/卸载模块、启动/停止适配器
- [适配器控制] - 启用/禁用适配器

## 命令列表

### 列表命令

| 命令 | 简写 | 描述 |
|------|------|------|
| `/list-modules` | `/lm` | 列出所有已注册的模块 |
| `/list-adapters` | `/la` | 列出所有已注册的适配器 |
| `/list-all` | `/ls` | 列出所有组件（模块和适配器） |

### 框架管理

| 命令 | 简写 | 描述 |
|------|------|------|
| `/restart-framework` | `/restart` | 重启 ErisPulse 框架 |
| `/reload-module <模块名>` | `/rm <模块名>` | 重新加载指定模块 |
| `/load-module <模块名>` | - | 加载指定模块 |
| `/unload-module <模块名>` | `/um <模块名>` | 卸载指定模块 |
| `/start-adapter <适配器名>` | - | 启动指定适配器 |
| `/stop-adapter <适配器名>` | - | 停止指定适配器 |
| `/enable-adapter <适配器名>` | - | 启用指定适配器 |
| `/disable-adapter <适配器名>` | - | 禁用指定适配器 |

## 安装

### 使用 epsdk 安装

```bash
epsdk install AdminControl
epsdk install HelpModule  # 可选，但推荐安装 使用`/help`即可查看全部已经注册的命令
```

## 配置

AdminControl 模块不需要额外的配置，安装后会自动加载。

## 链接

- [ErisPulse](https://github.com/ErisPulse/ErisPulse)
- [项目主页](https://github.com/wsu2059q/ErisPulse-AdminControl)
