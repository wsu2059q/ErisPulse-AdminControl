# ErisPulse AdminControl

ErisPulse 管理控制模块 - 提供框架管理和命令执行功能

## 功能特性

AdminControl 模块为 ErisPulse 框架提供了完整的管理控制功能

## 命令列表

### 列表命令（无需权限）

| 命令 | 简写 | 描述 |
|------|------|------|
| `/list-modules` | `/lm` | 列出所有已注册的模块 |
| `/list-adapters` | `/la` | 列出所有已注册的适配器 |
| `/list-all` | `/ls` | 列出所有组件（模块和适配器） |

### 框架管理（需要管理员权限）

| 命令 | 简写 | 描述 |
|------|------|------|
| `/restart-framework` | `/restart` | 重启 ErisPulse 框架 |
| `/reload-module <模块名>` | `/rm <模块名>` | 重新加载指定模块 |
| `/load-module <模块名>` | - | 加载指定模块 |
| `/unload-module <模块名>` | `/um <模块名>` | 卸载指定模块 |

### 适配器管理（需要管理员权限）

| 命令 | 简写 | 描述 |
|------|------|------|
| `/start-adapter <适配器名>` | - | 启动指定适配器 |
| `/stop-adapter <适配器名>` | - | 停止指定适配器 |
| `/enable-adapter <适配器名>` | - | 启用指定适配器 |
| `/disable-adapter <适配器名>` | - | 禁用指定适配器 |
| `/restart-adapter <适配器名>` | - | 重启指定适配器 |
| `/adapter-status [适配器名]` | - | 查看适配器运行状态 |

### 模块管理（需要管理员权限）

| 命令 | 简写 | 描述 |
|------|------|------|
| `/enable-module <模块名>` | - | 启用指定模块 |
| `/disable-module <模块名>` | - | 禁用指定模块 |

### 配置管理（需要管理员权限）

| 命令 | 简写 | 描述 |
|------|------|------|
| `/get-config <配置键>` | - | 获取模块/适配器配置 |
| `/set-config <配置键> <值>` | - | 设置模块/适配器配置 |

支持 JSON 格式的配置值：
```
/set-config MyModule {"key1": "value1", "key2": 123}
```

### 存储管理

| 命令 | 简写 | 描述 | 权限 |
|------|------|------|------|
| `/get-storage <键名>` | - | 获取存储值 | 需要管理员 |
| `/set-storage <键名> <值>` | - | 设置存储值 | 需要管理员 |
| `/delete-storage <键名>` | - | 删除存储值 | 需要管理员 |
| `/list-storage` | - | 列出所有存储键名 | 无需权限 |

支持 JSON 格式的存储值：
```
/set-storage user:123 {"name": "张三", "age": 25}
```

### 权限管理

| 命令 | 简写 | 描述 | 权限 |
|------|------|------|------|
| `/add-admin <用户ID/群组ID>` | - | 添加管理员 | 需要管理员 |
| `/remove-admin <用户ID/群组ID>` | - | 移除管理员 | 需要管理员 |
| `/list-admins` | - | 列出所有管理员 | 无需权限 |

## 安装

### 使用 epsdk 安装

```bash
epsdk install AdminControl
epsdk install HelpModule  # 可选，但推荐安装 使用`/help`即可查看全部已经注册的命令
```

### 首次配置

安装后，需要在 `config.toml` 中添加第一个管理员：

```toml
[AdminControl]
admins = ["你的用户ID"]
```

## 链接

- [ErisPulse](https://github.com/ErisPulse/ErisPulse)
- [项目主页](https://github.com/wsu2059q/ErisPulse-AdminControl)
