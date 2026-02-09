from ErisPulse.Core.Bases import BaseModule
from ErisPulse.Core.Event import command


class Main(BaseModule):

    def __init__(self, sdk):
        self.sdk = sdk

    def _get_admins(self):
        """获取管理员列表"""
        config = self.sdk.config.getConfig("AdminControl")
        if config:
            return config.get("admins", [])
        return []

    def is_admin(self, event):
        """检查用户是否是管理员"""
        admins = self._get_admins()
        if not admins:
            self.logger.warning("未配置管理员列表，所有用户都无法执行管理命令")
            return False
        
        user_id = event.get("user_id")
        group_id = event.get("group_id")
        
        # 检查用户ID
        if user_id and str(user_id) in admins:
            return True
        
        # 检查群组ID（允许群组管理）
        if group_id and str(group_id) in admins:
            return True
        
        return False

    @staticmethod
    def get_load_strategy():
        from ErisPulse.loaders import ModuleLoadStrategy
        return ModuleLoadStrategy(lazy_load=False, priority=100)

    async def on_load(self, event):
        # SDK 对象会在模块实例化时设置
        self.sdk = self.sdk
        self.logger = self.sdk.logger.get_child("AdminControl")
        self.logger.info("AdminControl 模块正在加载...")
        
        # 注册所有管理命令
        self._register_commands()
        
        self.logger.info("AdminControl 模块已加载")
        return True

    async def on_unload(self, event):
        # 注销所有命令
        command.unregister(self._list_modules_handler)
        command.unregister(self._list_adapters_handler)
        command.unregister(self._list_all_handler)
        command.unregister(self._restart_framework_handler)
        command.unregister(self._reload_module_handler)
        command.unregister(self._load_module_handler)
        command.unregister(self._unload_module_handler)
        command.unregister(self._start_adapter_handler)
        command.unregister(self._stop_adapter_handler)
        command.unregister(self._enable_adapter_handler)
        command.unregister(self._disable_adapter_handler)
        command.unregister(self._get_config_handler)
        command.unregister(self._set_config_handler)
        command.unregister(self._add_admin_handler)
        command.unregister(self._remove_admin_handler)
        command.unregister(self._list_admins_handler)
        command.unregister(self._get_storage_handler)
        command.unregister(self._set_storage_handler)
        command.unregister(self._delete_storage_handler)
        command.unregister(self._list_storage_handler)
        command.unregister(self._enable_module_handler)
        command.unregister(self._disable_module_handler)
        command.unregister(self._restart_adapter_handler)
        command.unregister(self._adapter_status_handler)
        
        self.logger.info("AdminControl 模块已卸载")
        return True

    def _register_commands(self):
        
        # ========== 列表命令 ==========
        
        @command(["list-modules", "lm"], group="list", help="列出所有已注册的模块")
        async def list_modules_handler(event):
            await self._list_modules(event)
        
        @command(["list-adapters", "la"], group="list", help="列出所有已注册的适配器")
        async def list_adapters_handler(event):
            await self._list_adapters(event)
        
        @command(["list-all", "ls"], group="list", help="列出所有组件（模块和适配器）")
        async def list_all_handler(event):
            await self._list_all(event)
        
        # ========== 框架管理命令（需要管理员权限）==========
        
        @command(["restart-framework", "restart"], group="framework", help="重启 ErisPulse 框架", permission=lambda e: self.is_admin(e))
        async def restart_framework_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._restart_framework(event)
        
        @command(["reload-module", "rm"], group="module", help="重新加载指定模块", usage="reload-module <模块名>", permission=lambda e: self.is_admin(e))
        async def reload_module_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._reload_module(event)
        
        @command(["load-module"], group="module", help="加载指定模块", usage="load-module <模块名>", permission=lambda e: self.is_admin(e))
        async def load_module_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._load_module(event)
        
        @command(["unload-module", "um"], group="module", help="卸载指定模块", usage="unload-module <模块名>", permission=lambda e: self.is_admin(e))
        async def unload_module_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._unload_module(event)
        
        @command(["start-adapter"], group="adapter", help="启动指定适配器", usage="start-adapter <适配器名>", permission=lambda e: self.is_admin(e))
        async def start_adapter_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._start_adapter(event)
        
        @command(["stop-adapter"], group="adapter", help="停止指定适配器", usage="stop-adapter <适配器名>", permission=lambda e: self.is_admin(e))
        async def stop_adapter_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._stop_adapter(event)
        
        @command(["enable-adapter"], group="adapter", help="启用指定适配器", usage="enable-adapter <适配器名>", permission=lambda e: self.is_admin(e))
        async def enable_adapter_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._enable_adapter(event)
        
        @command(["disable-adapter"], group="adapter", help="禁用指定适配器", usage="disable-adapter <适配器名>", permission=lambda e: self.is_admin(e))
        async def disable_adapter_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._disable_adapter(event)
        
        # ========== 配置管理命令（需要管理员权限）==========
        
        @command(["get-config"], group="config", help="获取模块/适配器配置", usage="get-config <配置键>", permission=lambda e: self.is_admin(e))
        async def get_config_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._get_config(event)
        
        @command(["set-config"], group="config", help="设置模块/适配器配置", usage="set-config <配置键> <值>", permission=lambda e: self.is_admin(e))
        async def set_config_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._set_config(event)
        
        @command(["add-admin"], group="admin", help="添加管理员", usage="add-admin <用户ID/群组ID>", permission=lambda e: self.is_admin(e))
        async def add_admin_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._add_admin(event)
        
        @command(["remove-admin"], group="admin", help="移除管理员", usage="remove-admin <用户ID/群组ID>", permission=lambda e: self.is_admin(e))
        async def remove_admin_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._remove_admin(event)
        
        @command(["list-admins"], group="admin", help="列出所有管理员")
        async def list_admins_handler(event):
            await self._list_admins(event)
        
        # ========== 存储管理命令（需要管理员权限）==========
        
        @command(["get-storage"], group="storage", help="获取存储值", usage="get-storage <键名>", permission=lambda e: self.is_admin(e))
        async def get_storage_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._get_storage(event)
        
        @command(["set-storage"], group="storage", help="设置存储值", usage="set-storage <键名> <值>", permission=lambda e: self.is_admin(e))
        async def set_storage_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._set_storage(event)
        
        @command(["delete-storage"], group="storage", help="删除存储值", usage="delete-storage <键名>", permission=lambda e: self.is_admin(e))
        async def delete_storage_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._delete_storage(event)
        
        @command(["list-storage"], group="storage", help="列出所有存储键名")
        async def list_storage_handler(event):
            await self._list_storage(event)
        
        # ========== 模块管理命令（需要管理员权限）==========
        
        @command(["enable-module"], group="module", help="启用指定模块", usage="enable-module <模块名>", permission=lambda e: self.is_admin(e))
        async def enable_module_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._enable_module(event)
        
        @command(["disable-module"], group="module", help="禁用指定模块", usage="disable-module <模块名>", permission=lambda e: self.is_admin(e))
        async def disable_module_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._disable_module(event)
        
        # ========== 适配器管理命令（需要管理员权限）==========
        
        @command(["restart-adapter"], group="adapter", help="重启指定适配器", usage="restart-adapter <适配器名>", permission=lambda e: self.is_admin(e))
        async def restart_adapter_handler(event):
            if not self.is_admin(event):
                await event.reply("权限不足：此命令需要管理员权限")
                return
            await self._restart_adapter(event)
        
        @command(["adapter-status"], group="adapter", help="查看适配器运行状态", usage="adapter-status [适配器名]")
        async def adapter_status_handler(event):
            await self._adapter_status(event)
        
        # 保存处理器引用以便后续注销
        self._list_modules_handler = list_modules_handler
        self._list_adapters_handler = list_adapters_handler
        self._list_all_handler = list_all_handler
        self._restart_framework_handler = restart_framework_handler
        self._reload_module_handler = reload_module_handler
        self._load_module_handler = load_module_handler
        self._unload_module_handler = unload_module_handler
        self._start_adapter_handler = start_adapter_handler
        self._stop_adapter_handler = stop_adapter_handler
        self._enable_adapter_handler = enable_adapter_handler
        self._disable_adapter_handler = disable_adapter_handler
        self._get_config_handler = get_config_handler
        self._set_config_handler = set_config_handler
        self._add_admin_handler = add_admin_handler
        self._remove_admin_handler = remove_admin_handler
        self._list_admins_handler = list_admins_handler
        self._get_storage_handler = get_storage_handler
        self._set_storage_handler = set_storage_handler
        self._delete_storage_handler = delete_storage_handler
        self._list_storage_handler = list_storage_handler
        self._enable_module_handler = enable_module_handler
        self._disable_module_handler = disable_module_handler
        self._restart_adapter_handler = restart_adapter_handler
        self._adapter_status_handler = adapter_status_handler

    # ========== 列表命令实现 ==========

    async def _list_modules(self, event):
        from ErisPulse.finders import ModuleFinder
        
        finder = ModuleFinder()
        registered = finder.get_all_names()
        loaded = self.sdk.module.list_loaded()
        
        lines = []
        lines.append("已注册模块列表")
        lines.append("━━━━━")
        lines.append("")
        
        for module_name in registered:
            module_info = finder.get_module_info(module_name)
            version = module_info.get("version", "未知") if module_info else "未知"
            package = module_info.get("package", "") if module_info else ""
            is_loaded = module_name in loaded
            status = "运行中" if is_loaded else "未加载"
            
            lines.append(f"{module_name}")
            lines.append(f"  版本: {version}")
            lines.append(f"  包:   {package if package else '本地'}")
            lines.append(f"  状态: {status}")
            lines.append("")
        
        lines.append("━━━━━")
        lines.append(f"总计: {len(registered)} 个已注册模块")
        
        await event.reply("\n".join(lines))

    async def _list_adapters(self, event):
        from ErisPulse.finders import AdapterFinder
        
        finder = AdapterFinder()
        registered = finder.get_all_names()
        items = self.sdk.adapter.list_items()
        
        lines = []
        lines.append("已注册适配器列表")
        lines.append("━━━━━")
        lines.append("")
        
        for adapter_name in registered:
            adapter_info = finder.get_adapter_info(adapter_name)
            version = adapter_info.get("version", "未知") if adapter_info else "未知"
            package = adapter_info.get("package", "") if adapter_info else ""
            is_enabled = items.get(adapter_name, False)
            status = "已启用" if is_enabled else "已禁用"
            
            lines.append(f"{adapter_name}")
            lines.append(f"  版本: {version}")
            lines.append(f"  包:   {package if package else '本地'}")
            lines.append(f"  状态: {status}")
            lines.append("")
        
        lines.append("━━━━━")
        lines.append(f"总计: {len(registered)} 个已注册适配器")
        
        await event.reply("\n".join(lines))

    async def _list_all(self, event):
        from ErisPulse.finders import ModuleFinder, AdapterFinder
        
        module_finder = ModuleFinder()
        adapter_finder = AdapterFinder()
        
        modules = module_finder.get_all_names()
        adapters = adapter_finder.get_all_names()
        loaded_modules = self.sdk.module.list_loaded()
        adapter_items = self.sdk.adapter.list_items()
        
        enabled_adapters = [k for k, v in adapter_items.items() if v]
        
        lines = []
        lines.append("ErisPulse 组件概览")
        lines.append("━━━━━")
        lines.append("")
        lines.append("模块")
        lines.append(f"  已注册: {len(modules)} 个")
        lines.append(f"  已加载: {len(loaded_modules)} 个")
        lines.append("")
        lines.append("适配器")
        lines.append(f"  已注册: {len(adapters)} 个")
        lines.append(f"  已启用: {len(enabled_adapters)} 个")
        lines.append("")
        lines.append("━━━━━")
        lines.append("")
        lines.append("已加载模块")
        
        for module in loaded_modules:
            lines.append(f"  运行: {module}")
        
        if not loaded_modules:
            lines.append("  (无)")
        
        lines.append("")
        lines.append("已启用适配器")
        
        for adapter_name in enabled_adapters:
            lines.append(f"  启用: {adapter_name}")
        
        if not enabled_adapters:
            lines.append("  (无)")
        
        await event.reply("\n".join(lines))

    # ========== 框架管理命令实现 ==========

    async def _restart_framework(self, event):
        await event.reply("正在重启 ErisPulse 框架...")
        
        from ErisPulse import restart
        try:
            await restart()
        except Exception as e:
            self.logger.error(f"重启框架时出错: {e}")
            await event.reply(f"错误: 重启失败\n{str(e)}")

    async def _reload_module(self, event):
        """重新加载指定模块"""
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定模块名称\n用法: /reload-module <模块名>")
            return
        
        module_name = args[0]
        
        if not self.sdk.module.is_loaded(module_name):
            await event.reply(f"未加载: 模块 '{module_name}'")
            return
        
        await event.reply(f"正在重新加载模块 '{module_name}'...")
        
        try:
            # 先卸载
            success = await self.sdk.module.unload(module_name)
            if success:
                # 再加载
                success = await self.sdk.module.load(module_name)
                if success:
                    await event.reply(f"成功: 模块 '{module_name}' 已重新加载")
                else:
                    await event.reply(f"失败: 模块 '{module_name}' 加载失败")
            else:
                await event.reply(f"失败: 模块 '{module_name}' 卸载失败")
        except Exception as e:
            self.logger.error(f"重新加载模块 {module_name} 时出错: {e}")
            await event.reply(f"错误: {str(e)}")

    async def _load_module(self, event):
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定模块名称\n用法: /load-module <模块名>")
            return
        
        module_name = args[0]
        
        if self.sdk.module.is_loaded(module_name):
            await event.reply(f"已加载: 模块 '{module_name}'")
            return
        
        if not self.sdk.module.exists(module_name):
            await event.reply(f"未找到: 模块 '{module_name}'")
            return
        
        await event.reply(f"正在加载模块 '{module_name}'...")
        
        try:
            success = await self.sdk.module.load(module_name)
            if success:
                await event.reply(f"成功: 模块 '{module_name}' 已加载")
            else:
                await event.reply(f"失败: 模块 '{module_name}' 加载失败")
        except Exception as e:
            self.logger.error(f"加载模块 {module_name} 时出错: {e}")
            await event.reply(f"错误: {str(e)}")

    async def _unload_module(self, event):
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定模块名称\n用法: /unload-module <模块名>")
            return
        
        module_name = args[0]
        
        if not self.sdk.module.is_loaded(module_name):
            await event.reply(f"未加载: 模块 '{module_name}'")
            return
        
        await event.reply(f"正在卸载模块 '{module_name}'...")
        
        try:
            success = await self.sdk.module.unload(module_name)
            if success:
                await event.reply(f"成功: 模块 '{module_name}' 已卸载")
            else:
                await event.reply(f"失败: 模块 '{module_name}' 卸载失败")
        except Exception as e:
            self.logger.error(f"卸载模块 {module_name} 时出错: {e}")
            await event.reply(f"错误: {str(e)}")

    async def _start_adapter(self, event):
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定适配器名称\n用法: /start-adapter <适配器名>")
            return
        
        adapter_name = args[0]
        
        if not self.sdk.adapter.exists(adapter_name):
            await event.reply(f"未找到: 适配器 '{adapter_name}'")
            return
        
        if not self.sdk.adapter.is_enabled(adapter_name):
            await event.reply(f"已禁用: 适配器 '{adapter_name}'\n请先启用适配器")
            return
        
        await event.reply(f"正在启动适配器 '{adapter_name}'...")
        
        try:
            await self.sdk.adapter.startup([adapter_name])
            await event.reply(f"成功: 适配器 '{adapter_name}' 已启动")
        except Exception as e:
            self.logger.error(f"启动适配器 {adapter_name} 时出错: {e}")
            await event.reply(f"错误: {str(e)}")

    async def _stop_adapter(self, event):
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定适配器名称\n用法: /stop-adapter <适配器名>")
            return
        
        adapter_name = args[0]
        
        if not self.sdk.adapter.exists(adapter_name):
            await event.reply(f"未找到: 适配器 '{adapter_name}'")
            return
        
        await event.reply(f"正在停止适配器 '{adapter_name}'...")
        
        try:
            # 获取适配器实例并调用 shutdown
            adapter_instance = self.sdk.adapter.get(adapter_name)
            if adapter_instance:
                await adapter_instance.shutdown()
                await event.reply(f"成功: 适配器 '{adapter_name}' 已停止")
            else:
                await event.reply(f"未运行: 适配器 '{adapter_name}'")
        except Exception as e:
            self.logger.error(f"停止适配器 {adapter_name} 时出错: {e}")
            await event.reply(f"错误: {str(e)}")

    async def _enable_adapter(self, event):
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定适配器名称\n用法: /enable-adapter <适配器名>")
            return
        
        adapter_name = args[0]
        
        if not self.sdk.adapter.exists(adapter_name):
            await event.reply(f"未找到: 适配器 '{adapter_name}'")
            return
        
        if self.sdk.adapter.is_enabled(adapter_name):
            await event.reply(f"已启用: 适配器 '{adapter_name}'")
            return
        
        success = self.sdk.adapter.enable(adapter_name)
        if success:
            await event.reply(f"成功: 适配器 '{adapter_name}' 已启用\n使用 /start-adapter 启动它")
        else:
            await event.reply(f"失败: 启用适配器 '{adapter_name}' 失败")

    async def _disable_adapter(self, event):
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定适配器名称\n用法: /disable-adapter <适配器名>")
            return
        
        adapter_name = args[0]
        
        if not self.sdk.adapter.exists(adapter_name):
            await event.reply(f"未找到: 适配器 '{adapter_name}'")
            return
        
        if not self.sdk.adapter.is_enabled(adapter_name):
            await event.reply(f"已禁用: 适配器 '{adapter_name}'")
            return
        
        success = self.sdk.adapter.disable(adapter_name)
        if success:
            await event.reply(f"成功: 适配器 '{adapter_name}' 已禁用")
        else:
            await event.reply(f"失败: 禁用适配器 '{adapter_name}' 失败")

    # ========== 配置管理命令实现 ==========

    async def _get_config(self, event):
        """获取模块/适配器配置"""
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定配置键\n用法: /get-config <配置键>")
            return
        
        config_key = args[0]
        value = self.sdk.config.getConfig(config_key)
        
        lines = []
        lines.append(f"配置项: {config_key}")
        lines.append("━━━━━")
        if value is None:
            lines.append("值: (未设置)")
        elif isinstance(value, (dict, list)):
            import json
            lines.append(f"值:\n{json.dumps(value, indent=2, ensure_ascii=False)}")
        else:
            lines.append(f"值: {value}")
        
        await event.reply("\n".join(lines))

    async def _set_config(self, event):
        """设置模块/适配器配置"""
        args = event.get_command_args()
        if len(args) < 2:
            await event.reply("错误: 请指定配置键和值\n用法: /set-config <配置键> <值>")
            return
        
        config_key = args[0]
        value_str = " ".join(args[1:])
        
        # 尝试解析值（支持 JSON）
        import json
        try:
            if value_str.startswith("{") or value_str.startswith("["):
                value = json.loads(value_str)
            else:
                value = value_str
        except json.JSONDecodeError:
            value = value_str
        
        success = self.sdk.config.setConfig(config_key, value)
        if success:
            await event.reply(f"成功: 配置 '{config_key}' 已设置")
        else:
            await event.reply(f"失败: 设置配置 '{config_key}' 失败")

    async def _add_admin(self, event):
        """添加管理员"""
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定用户ID或群组ID\n用法: /add-admin <用户ID/群组ID>")
            return
        
        admin_id = args[0]
        admins = self._get_admins()
        
        if admin_id in admins:
            await event.reply(f"已存在: '{admin_id}' 已是管理员")
            return
        
        admins.append(admin_id)
        
        config = self.sdk.config.getConfig("AdminControl", {})
        config["admins"] = admins
        self.sdk.config.setConfig("AdminControl", config)
        
        await event.reply(f"成功: '{admin_id}' 已添加为管理员")

    async def _remove_admin(self, event):
        """移除管理员"""
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定用户ID或群组ID\n用法: /remove-admin <用户ID/群组ID>")
            return
        
        admin_id = args[0]
        admins = self._get_admins()
        
        if admin_id not in admins:
            await event.reply(f"未找到: '{admin_id}' 不是管理员")
            return
        
        admins.remove(admin_id)
        
        config = self.sdk.config.getConfig("AdminControl", {})
        config["admins"] = admins
        self.sdk.config.setConfig("AdminControl", config)
        
        await event.reply(f"成功: '{admin_id}' 已从管理员列表中移除")

    async def _list_admins(self, event):
        """列出所有管理员"""
        admins = self._get_admins()
        
        lines = []
        lines.append("管理员列表")
        lines.append("━━━━━")
        if admins:
            for admin_id in admins:
                lines.append(f"  {admin_id}")
        else:
            lines.append("  (无)")
        lines.append("━━━━━")
        lines.append(f"总计: {len(admins)} 个管理员")
        
        await event.reply("\n".join(lines))

    # ========== 存储管理命令实现 ==========

    async def _get_storage(self, event):
        """获取存储值"""
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定键名\n用法: /get-storage <键名>")
            return
        
        key = args[0]
        value = self.sdk.storage.get(key)
        
        lines = []
        lines.append(f"存储键: {key}")
        lines.append("━━━━━")
        if value is None:
            lines.append("值: (未设置)")
        elif isinstance(value, (dict, list)):
            import json
            lines.append(f"值:\n{json.dumps(value, indent=2, ensure_ascii=False)}")
        else:
            lines.append(f"值: {value}")
        
        await event.reply("\n".join(lines))

    async def _set_storage(self, event):
        """设置存储值"""
        args = event.get_command_args()
        if len(args) < 2:
            await event.reply("错误: 请指定键名和值\n用法: /set-storage <键名> <值>")
            return
        
        key = args[0]
        value_str = " ".join(args[1:])
        
        # 尝试解析值（支持 JSON）
        import json
        try:
            if value_str.startswith("{") or value_str.startswith("["):
                value = json.loads(value_str)
            else:
                value = value_str
        except json.JSONDecodeError:
            value = value_str
        
        success = self.sdk.storage.set(key, value)
        if success:
            await event.reply(f"成功: 存储键 '{key}' 已设置")
        else:
            await event.reply(f"失败: 设置存储键 '{key}' 失败")

    async def _delete_storage(self, event):
        """删除存储值"""
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定键名\n用法: /delete-storage <键名>")
            return
        
        key = args[0]
        success = self.sdk.storage.delete(key)
        if success:
            await event.reply(f"成功: 存储键 '{key}' 已删除")
        else:
            await event.reply(f"失败: 删除存储键 '{key}' 失败")

    async def _list_storage(self, event):
        """列出所有存储键名"""
        keys = self.sdk.storage.get_all_keys()
        
        lines = []
        lines.append("存储键名列表")
        lines.append("━━━━━")
        if keys:
            for key in keys:
                value = self.sdk.storage.get(key)
                value_type = type(value).__name__
                lines.append(f"  {key} ({value_type})")
        else:
            lines.append("  (无)")
        lines.append("━━━━━")
        lines.append(f"总计: {len(keys)} 个存储项")
        
        await event.reply("\n".join(lines))

    # ========== 模块管理命令实现 ==========

    async def _enable_module(self, event):
        """启用指定模块"""
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定模块名称\n用法: /enable-module <模块名>")
            return
        
        module_name = args[0]
        
        if not self.sdk.module.exists(module_name):
            await event.reply(f"未找到: 模块 '{module_name}'")
            return
        
        if self.sdk.module.is_enabled(module_name):
            await event.reply(f"已启用: 模块 '{module_name}'")
            return
        
        success = self.sdk.module.enable(module_name)
        if success:
            await event.reply(f"成功: 模块 '{module_name}' 已启用")
        else:
            await event.reply(f"失败: 启用模块 '{module_name}' 失败")

    async def _disable_module(self, event):
        """禁用指定模块"""
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定模块名称\n用法: /disable-module <模块名>")
            return
        
        module_name = args[0]
        
        if not self.sdk.module.exists(module_name):
            await event.reply(f"未找到: 模块 '{module_name}'")
            return
        
        if not self.sdk.module.is_enabled(module_name):
            await event.reply(f"已禁用: 模块 '{module_name}'")
            return
        
        success = self.sdk.module.disable(module_name)
        if success:
            await event.reply(f"成功: 模块 '{module_name}' 已禁用")
        else:
            await event.reply(f"失败: 禁用模块 '{module_name}' 失败")

    # ========== 适配器管理命令实现 ==========

    async def _restart_adapter(self, event):
        """重启指定适配器"""
        args = event.get_command_args()
        if not args:
            await event.reply("错误: 请指定适配器名称\n用法: /restart-adapter <适配器名>")
            return
        
        adapter_name = args[0]
        
        if not self.sdk.adapter.exists(adapter_name):
            await event.reply(f"未找到: 适配器 '{adapter_name}'")
            return
        
        await event.reply(f"正在重启适配器 '{adapter_name}'...")
        
        try:
            # 先停止
            adapter_instance = self.sdk.adapter.get(adapter_name)
            if adapter_instance:
                await adapter_instance.shutdown()
            
            # 再启动
            await self.sdk.adapter.startup([adapter_name])
            await event.reply(f"成功: 适配器 '{adapter_name}' 已重启")
        except Exception as e:
            self.logger.error(f"重启适配器 {adapter_name} 时出错: {e}")
            await event.reply(f"错误: {str(e)}")

    async def _adapter_status(self, event):
        """查看适配器运行状态"""
        from ErisPulse.finders import AdapterFinder
        
        args = event.get_command_args()
        finder = AdapterFinder()
        
        if args:
            # 查看单个适配器状态
            adapter_name = args[0]
            
            if not self.sdk.adapter.exists(adapter_name):
                await event.reply(f"未找到: 适配器 '{adapter_name}'")
                return
            
            adapter_info = finder.get_adapter_info(adapter_name)
            version = adapter_info.get("version", "未知") if adapter_info else "未知"
            is_enabled = self.sdk.adapter.is_enabled(adapter_name)
            is_running = self.sdk.adapter.get(adapter_name) is not None
            
            lines = []
            lines.append(f"适配器: {adapter_name}")
            lines.append("━━━━━")
            lines.append(f"版本: {version}")
            lines.append(f"已启用: {'是' if is_enabled else '否'}")
            lines.append(f"运行中: {'是' if is_running else '否'}")
        else:
            # 查看所有适配器状态
            registered = finder.get_all_names()
            items = self.sdk.adapter.list_items()
            
            lines = []
            lines.append("适配器运行状态")
            lines.append("━━━━━")
            lines.append("")
            
            for adapter_name in registered:
                is_enabled = items.get(adapter_name, False)
                is_running = self.sdk.adapter.get(adapter_name) is not None
                
                status = "运行中" if is_running else "已停止"
                if not is_enabled:
                    status = "已禁用"
                
                lines.append(f"{adapter_name}: {status}")
        
        await event.reply("\n".join(lines))
