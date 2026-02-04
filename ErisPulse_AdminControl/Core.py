from ErisPulse.Core.Bases import BaseModule
from ErisPulse.Core.Event import command


class Main(BaseModule):

    def __init__(self, sdk):
        self.sdk = sdk

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
        
        self.logger.info("AdminControl 模块已卸载")
        return True

    def _register_commands(self):
        
        # ========== 列表命令 ==========
        
        @command(["list-modules", "lm"], help="列出所有已注册的模块")
        async def list_modules_handler(event):
            await self._list_modules(event)
        
        @command(["list-adapters", "la"], help="列出所有已注册的适配器")
        async def list_adapters_handler(event):
            await self._list_adapters(event)
        
        @command(["list-all", "ls"], help="列出所有组件（模块和适配器）")
        async def list_all_handler(event):
            await self._list_all(event)
        
        # ========== 框架管理命令 ==========
        
        @command(["restart-framework", "restart"], help="重启 ErisPulse 框架")
        async def restart_framework_handler(event):
            await self._restart_framework(event)
        
        @command(["reload-module", "rm"], help="重新加载指定模块", usage="reload-module <模块名>")
        async def reload_module_handler(event):
            await self._reload_module(event)
        
        @command(["load-module"], help="加载指定模块", usage="load-module <模块名>")
        async def load_module_handler(event):
            await self._load_module(event)
        
        @command(["unload-module", "um"], help="卸载指定模块", usage="unload-module <模块名>")
        async def unload_module_handler(event):
            await self._unload_module(event)
        
        @command(["start-adapter"], help="启动指定适配器", usage="start-adapter <适配器名>")
        async def start_adapter_handler(event):
            await self._start_adapter(event)
        
        @command(["stop-adapter"], help="停止指定适配器", usage="stop-adapter <适配器名>")
        async def stop_adapter_handler(event):
            await self._stop_adapter(event)
        
        @command(["enable-adapter"], help="启用指定适配器", usage="enable-adapter <适配器名>")
        async def enable_adapter_handler(event):
            await self._enable_adapter(event)
        
        @command(["disable-adapter"], help="禁用指定适配器", usage="disable-adapter <适配器名>")
        async def disable_adapter_handler(event):
            await self._disable_adapter(event)
        
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

    # ========== 列表命令实现 ==========

    async def _list_modules(self, event):
        from ErisPulse.finders import ModuleFinder
        
        finder = ModuleFinder()
        registered = finder.get_all_names()
        loaded = self.sdk.module.list_loaded()
        
        lines = []
        lines.append("┌" + "─" * 58 + "┐")
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + "  已注册模块列表".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("├" + "─" * 58 + "┤")
        
        for module_name in registered:
            module_info = finder.get_module_info(module_name)
            version = module_info.get("version", "未知") if module_info else "未知"
            package = module_info.get("package", "") if module_info else ""
            is_loaded = module_name in loaded
            status = "[运行中]" if is_loaded else "[未加载]"
            
            lines.append("│" + " " * 58 + "│")
            lines.append("│  模块: " + module_name.ljust(52) + "│")
            lines.append("│  版本: " + version.ljust(52) + "│")
            lines.append("│  包:   " + (package if package else "本地").ljust(52) + "│")
            lines.append("│  状态: " + status.ljust(52) + "│")
        
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + f"  总计: {len(registered)} 个已注册模块".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("└" + "─" * 58 + "┘")
        
        await event.reply("\n".join(lines))

    async def _list_adapters(self, event):
        from ErisPulse.finders import AdapterFinder
        
        finder = AdapterFinder()
        registered = finder.get_all_names()
        items = self.sdk.adapter.list_items()
        
        lines = []
        lines.append("┌" + "─" * 58 + "┐")
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + "  已注册适配器列表".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("├" + "─" * 58 + "┤")
        
        for adapter_name in registered:
            adapter_info = finder.get_adapter_info(adapter_name)
            version = adapter_info.get("version", "未知") if adapter_info else "未知"
            package = adapter_info.get("package", "") if adapter_info else ""
            is_enabled = items.get(adapter_name, False)
            status = "[已启用]" if is_enabled else "[已禁用]"
            
            lines.append("│" + " " * 58 + "│")
            lines.append("│  适配器: " + adapter_name.ljust(50) + "│")
            lines.append("│  版本:   " + version.ljust(50) + "│")
            lines.append("│  包:     " + (package if package else "本地").ljust(50) + "│")
            lines.append("│  状态:   " + status.ljust(50) + "│")
        
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + f"  总计: {len(registered)} 个已注册适配器".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("└" + "─" * 58 + "┘")
        
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
        lines.append("┌" + "─" * 58 + "┐")
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + "  ErisPulse 组件概览".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("├" + "─" * 58 + "┤")
        lines.append("│" + " " * 58 + "│")
        lines.append("│  模块".rjust(40) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("│    已注册: " + f"{len(modules)} 个".ljust(42) + "│")
        lines.append("│    已加载: " + f"{len(loaded_modules)} 个".ljust(42) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("│  适配器".rjust(40) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("│    已注册: " + f"{len(adapters)} 个".ljust(42) + "│")
        lines.append("│    已启用: " + f"{len(enabled_adapters)} 个".ljust(42) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("├" + "─" * 58 + "┤")
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + "  已加载模块".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        
        for module in loaded_modules:
            lines.append("│    [运行] " + module.ljust(48) + "│")
        
        if not loaded_modules:
            lines.append("│    (无)".center(58) + "│")
        
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + "  已启用适配器".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        
        for adapter_name in enabled_adapters:
            lines.append("│    [启用] " + adapter_name.ljust(48) + "│")
        
        if not enabled_adapters:
            lines.append("│    (无)".center(58) + "│")
        
        lines.append("│" + " " * 58 + "│")
        lines.append("└" + "─" * 58 + "┘")
        
        await event.reply("\n".join(lines))

    # ========== 框架管理命令实现 ==========

    async def _restart_framework(self, event):
        lines = []
        lines.append("┌" + "─" * 58 + "┐")
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + "  正在重启 ErisPulse 框架...".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("└" + "─" * 58 + "┘")
        await event.reply("\n".join(lines))
        
        from ErisPulse import restart
        try:
            await restart()
        except Exception as e:
            self.logger.error(f"重启框架时出错: {e}")
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  [错误] 重启失败".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  {str(e)}".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))

    async def _reload_module(self, event):
        """重新加载指定模块"""
        args = event.get_command_args()
        if not args:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  [错误] 请指定模块名称".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  用法: /reload-module <模块名>".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        module_name = args[0]
        
        if not self.sdk.module.is_loaded(module_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [未加载] 模块 '{module_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        lines = []
        lines.append("┌" + "─" * 58 + "┐")
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + f"  正在重新加载模块 '{module_name}'...".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("└" + "─" * 58 + "┘")
        await event.reply("\n".join(lines))
        
        try:
            # 先卸载
            success = await self.sdk.module.unload(module_name)
            if success:
                # 再加载
                success = await self.sdk.module.load(module_name)
                if success:
                    lines = []
                    lines.append("┌" + "─" * 58 + "┐")
                    lines.append("│" + " " * 58 + "│")
                    lines.append("│" + f"  [成功] 模块 '{module_name}' 已重新加载".center(58) + "│")
                    lines.append("│" + " " * 58 + "│")
                    lines.append("└" + "─" * 58 + "┘")
                    await event.reply("\n".join(lines))
                else:
                    lines = []
                    lines.append("┌" + "─" * 58 + "┐")
                    lines.append("│" + " " * 58 + "│")
                    lines.append("│" + f"  [失败] 模块 '{module_name}' 加载失败".center(58) + "│")
                    lines.append("│" + " " * 58 + "│")
                    lines.append("└" + "─" * 58 + "┘")
                    await event.reply("\n".join(lines))
            else:
                lines = []
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 58 + "│")
                lines.append("│" + f"  [失败] 模块 '{module_name}' 卸载失败".center(58) + "│")
                lines.append("│" + " " * 58 + "│")
                lines.append("└" + "─" * 58 + "┘")
                await event.reply("\n".join(lines))
        except Exception as e:
            self.logger.error(f"重新加载模块 {module_name} 时出错: {e}")
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [错误] {str(e)}".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))

    async def _load_module(self, event):
        args = event.get_command_args()
        if not args:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  [错误] 请指定模块名称".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  用法: /load-module <模块名>".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        module_name = args[0]
        
        if self.sdk.module.is_loaded(module_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [已加载] 模块 '{module_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        if not self.sdk.module.exists(module_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [未找到] 模块 '{module_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        lines = []
        lines.append("┌" + "─" * 58 + "┐")
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + f"  正在加载模块 '{module_name}'...".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("└" + "─" * 58 + "┘")
        await event.reply("\n".join(lines))
        
        try:
            success = await self.sdk.module.load(module_name)
            if success:
                lines = []
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 58 + "│")
                lines.append("│" + f"  [成功] 模块 '{module_name}' 已加载".center(58) + "│")
                lines.append("│" + " " * 58 + "│")
                lines.append("└" + "─" * 58 + "┘")
                await event.reply("\n".join(lines))
            else:
                lines = []
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 58 + "│")
                lines.append("│" + f"  [失败] 模块 '{module_name}' 加载失败".center(58) + "│")
                lines.append("│" + " " * 58 + "│")
                lines.append("└" + "─" * 58 + "┘")
                await event.reply("\n".join(lines))
        except Exception as e:
            self.logger.error(f"加载模块 {module_name} 时出错: {e}")
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [错误] {str(e)}".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))

    async def _unload_module(self, event):
        args = event.get_command_args()
        if not args:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  [错误] 请指定模块名称".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  用法: /unload-module <模块名>".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        module_name = args[0]
        
        if not self.sdk.module.is_loaded(module_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [未加载] 模块 '{module_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        lines = []
        lines.append("┌" + "─" * 58 + "┐")
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + f"  正在卸载模块 '{module_name}'...".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("└" + "─" * 58 + "┘")
        await event.reply("\n".join(lines))
        
        try:
            success = await self.sdk.module.unload(module_name)
            if success:
                lines = []
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 58 + "│")
                lines.append("│" + f"  [成功] 模块 '{module_name}' 已卸载".center(58) + "│")
                lines.append("│" + " " * 58 + "│")
                lines.append("└" + "─" * 58 + "┘")
                await event.reply("\n".join(lines))
            else:
                lines = []
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 58 + "│")
                lines.append("│" + f"  [失败] 模块 '{module_name}' 卸载失败".center(58) + "│")
                lines.append("│" + " " * 58 + "│")
                lines.append("└" + "─" * 58 + "┘")
                await event.reply("\n".join(lines))
        except Exception as e:
            self.logger.error(f"卸载模块 {module_name} 时出错: {e}")
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [错误] {str(e)}".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))

    async def _start_adapter(self, event):
        args = event.get_command_args()
        if not args:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  [错误] 请指定适配器名称".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  用法: /start-adapter <适配器名>".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        adapter_name = args[0]
        
        if not self.sdk.adapter.exists(adapter_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [未找到] 适配器 '{adapter_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        if not self.sdk.adapter.is_enabled(adapter_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [已禁用] 适配器 '{adapter_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  请先启用适配器".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        lines = []
        lines.append("┌" + "─" * 58 + "┐")
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + f"  正在启动适配器 '{adapter_name}'...".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("└" + "─" * 58 + "┘")
        await event.reply("\n".join(lines))
        
        try:
            await self.sdk.adapter.startup([adapter_name])
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [成功] 适配器 '{adapter_name}' 已启动".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
        except Exception as e:
            self.logger.error(f"启动适配器 {adapter_name} 时出错: {e}")
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [错误] {str(e)}".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))

    async def _stop_adapter(self, event):
        args = event.get_command_args()
        if not args:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  [错误] 请指定适配器名称".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  用法: /stop-adapter <适配器名>".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        adapter_name = args[0]
        
        if not self.sdk.adapter.exists(adapter_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [未找到] 适配器 '{adapter_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        lines = []
        lines.append("┌" + "─" * 58 + "┐")
        lines.append("│" + " " * 58 + "│")
        lines.append("│" + f"  正在停止适配器 '{adapter_name}'...".center(58) + "│")
        lines.append("│" + " " * 58 + "│")
        lines.append("└" + "─" * 58 + "┘")
        await event.reply("\n".join(lines))
        
        try:
            # 获取适配器实例并调用 shutdown
            adapter_instance = self.sdk.adapter.get(adapter_name)
            if adapter_instance:
                await adapter_instance.shutdown()
                lines = []
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 58 + "│")
                lines.append("│" + f"  [成功] 适配器 '{adapter_name}' 已停止".center(58) + "│")
                lines.append("│" + " " * 58 + "│")
                lines.append("└" + "─" * 58 + "┘")
                await event.reply("\n".join(lines))
            else:
                lines = []
                lines.append("┌" + "─" * 58 + "┐")
                lines.append("│" + " " * 58 + "│")
                lines.append("│" + f"  [未运行] 适配器 '{adapter_name}'".center(58) + "│")
                lines.append("│" + " " * 58 + "│")
                lines.append("└" + "─" * 58 + "┘")
                await event.reply("\n".join(lines))
        except Exception as e:
            self.logger.error(f"停止适配器 {adapter_name} 时出错: {e}")
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [错误] {str(e)}".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))

    async def _enable_adapter(self, event):
        args = event.get_command_args()
        if not args:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  [错误] 请指定适配器名称".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  用法: /enable-adapter <适配器名>".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        adapter_name = args[0]
        
        if not self.sdk.adapter.exists(adapter_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [未找到] 适配器 '{adapter_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        if self.sdk.adapter.is_enabled(adapter_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [已启用] 适配器 '{adapter_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        success = self.sdk.adapter.enable(adapter_name)
        if success:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [成功] 适配器 '{adapter_name}' 已启用".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  使用 /start-adapter 启动它".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
        else:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [失败] 启用适配器 '{adapter_name}' 失败".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))

    async def _disable_adapter(self, event):
        args = event.get_command_args()
        if not args:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  [错误] 请指定适配器名称".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + "  用法: /disable-adapter <适配器名>".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        adapter_name = args[0]
        
        if not self.sdk.adapter.exists(adapter_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [未找到] 适配器 '{adapter_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        if not self.sdk.adapter.is_enabled(adapter_name):
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [已禁用] 适配器 '{adapter_name}'".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
            return
        
        success = self.sdk.adapter.disable(adapter_name)
        if success:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [成功] 适配器 '{adapter_name}' 已禁用".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
        else:
            lines = []
            lines.append("┌" + "─" * 58 + "┐")
            lines.append("│" + " " * 58 + "│")
            lines.append("│" + f"  [失败] 禁用适配器 '{adapter_name}' 失败".center(58) + "│")
            lines.append("│" + " " * 58 + "│")
            lines.append("└" + "─" * 58 + "┘")
            await event.reply("\n".join(lines))
