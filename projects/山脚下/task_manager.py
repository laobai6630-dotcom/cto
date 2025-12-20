# -*- coding: utf-8 -*-
"""山脚下项目任务管理桌面程序（Windows 11）

说明：
- GUI: Tkinter（Windows常见Python发行版自带，无需额外安装依赖）
- 任务：57项，按阶段分类展示
- 每项任务：完成状态（☐/✅）+ 任务名 + 备注输入框 + 保存按钮 + 更新时间戳
- 数据持久化：task_manager_data.json（启动加载、变更自动保存、关闭自动保存）
- 配置持久化：task_manager_config.json（窗口大小/位置）

运行：
    python task_manager.py
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.simpledialog import askstring
except ModuleNotFoundError:  # pragma: no cover
    tk = None  # type: ignore[assignment]
    ttk = None  # type: ignore[assignment]
    askstring = None  # type: ignore[assignment]


@dataclass(frozen=True)
class TaskDefinition:
    stage: str
    task_id: str
    name: str


DEFAULT_TASKS: List[TaskDefinition] = [
    # 阶段1：基础框架搭建（第1-2周）
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 1.1", "审查并测试四个采集程序"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 1.2", "创建scheduler_main.py主调度程序"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 1.3", "数据清洗和预处理"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 1.4", "历史数据备份策略"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 2.1", "提取134个原始特征"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 2.2", "合成10个AI特征"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 2.3", "计算10个筹码特征"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 2.4", "特征标准化和处理"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 2.5", "计算特征重要性"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 3.1", "训练3个基础模型"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 3.2", "集成3个模型"),
    TaskDefinition("阶段1：基础框架搭建（第1-2周）", "Task 3.3", "模型评估"),
    # 阶段2：相似度筛选+对照组（第3周）
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.1.1", "识别对照组（跌幅前20名）"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.1.2", "提取对照组特征"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.1.3", "对比分析（分离度评分）"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.2.1", "相似度筛选主程序"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.2.2", "递进筛选逻辑（50%-40%-30%）"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.3.1", "30天跟踪"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.3.2", "效果评估"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.3.3", "生成日报"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.3.4", "生成周报"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.3.5", "生成月报"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.4.1", "Dashboard主页"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.4.2", "Dashboard逻辑"),
    TaskDefinition("阶段2：相似度筛选+对照组（第3周）", "Task 2.4.3", "Dashboard数据文件"),
    # 阶段3：高级功能+GitHub工作流（第4周）
    TaskDefinition("阶段3：高级功能+GitHub工作流（第4周）", "Task 3.1.1", "密码保护认证"),
    TaskDefinition("阶段3：高级功能+GitHub工作流（第4周）", "Task 3.2.1", "多语言支持（i18n）"),
    TaskDefinition("阶段3：高级功能+GitHub工作流（第4周）", "Task 3.2.2", "网页元素国际化"),
    TaskDefinition("阶段3：高级功能+GitHub工作流（第4周）", "Task 3.3.1", "daily.yml工作流"),
    TaskDefinition("阶段3：高级功能+GitHub工作流（第4周）", "Task 3.3.2", "weekly.yml工作流"),
    TaskDefinition("阶段3：高级功能+GitHub工作流（第4周）", "Task 3.3.3", "monthly.yml工作流"),
    TaskDefinition("阶段3：高级功能+GitHub工作流（第4周）", "Task 3.3.4", "trigger.yml工作流"),
    TaskDefinition("阶段3：高级功能+GitHub工作流（第4周）", "Task 3.3.5", "deploy.yml工作流"),
    TaskDefinition("阶段3：高级功能+GitHub工作流（第4周）", "Task 3.4.1", "监督报告生成"),
    TaskDefinition("阶段3：高级功能+GitHub工作流（第4周）", "Task 3.4.2", "Monitor监控页面"),
    # 阶段4：优化+文档+上线（第5周+）
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.1.1", "数据处理优化"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.1.2", "模型预测优化"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.1.3", "网页性能优化"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.1.4", "数据库优化"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.2.1", "单元测试"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.2.2", "集成测试"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.2.3", "回归测试"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.2.4", "压力测试"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.3.1", "README.md"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.3.2", "ARCHITECTURE.md"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.3.3", "API_REFERENCE.md"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.3.4", "DEPLOYMENT.md"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.3.5", "MAINTENANCE.md"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.3.6", "CHANGELOG.md"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.4.1", "生产环境配置"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.4.2", "GitHub Runner配置"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.4.3", "网页部署"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.4.4", "备份与恢复测试"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.5.1", "日志系统"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.5.2", "监控告警体系"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.5.3", "定期巡检计划"),
    TaskDefinition("阶段4：优化+文档+上线（第5周+）", "Task 4.5.4", "故障应急预案"),
]


@dataclass(frozen=True)
class StoragePaths:
    data_path: Path
    config_path: Path


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe_mkdir(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        return


def get_storage_paths() -> StoragePaths:
    """优先使用票据要求的Windows目录；不可用时回退到脚本所在目录。"""

    if os.name == "nt":
        preferred_base = Path(r"D:\cto\projects\山脚下")
    else:
        preferred_base = Path(__file__).resolve().parent

    _safe_mkdir(preferred_base)

    preferred_data = preferred_base / "task_manager_data.json"
    preferred_cfg = preferred_base / "task_manager_config.json"

    if preferred_data.parent.exists() and preferred_cfg.parent.exists():
        return StoragePaths(data_path=preferred_data, config_path=preferred_cfg)

    fallback = Path(__file__).resolve().parent
    return StoragePaths(
        data_path=fallback / "task_manager_data.json",
        config_path=fallback / "task_manager_config.json",
    )


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_json_atomic(path: Path, data: Dict[str, Any]) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    _safe_mkdir(path.parent)
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp_path.replace(path)


if tk is not None and ttk is not None:

    class ScrollableFrame(ttk.Frame):
        def __init__(self, master: "tk.Misc"):
            super().__init__(master)

            self._canvas = tk.Canvas(self, highlightthickness=0)
            self._scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
            self._canvas.configure(yscrollcommand=self._scrollbar.set)

            self.content = ttk.Frame(self._canvas)
            self._window_id = self._canvas.create_window((0, 0), window=self.content, anchor="nw")

            self._canvas.pack(side="left", fill="both", expand=True)
            self._scrollbar.pack(side="right", fill="y")

            self.content.bind("<Configure>", self._on_content_configure)
            self._canvas.bind("<Configure>", self._on_canvas_configure)

            self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)
            self._canvas.bind_all("<Button-4>", self._on_mousewheel)
            self._canvas.bind_all("<Button-5>", self._on_mousewheel)

        def _on_content_configure(self, _event: "tk.Event") -> None:
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))

        def _on_canvas_configure(self, event: "tk.Event") -> None:
            self._canvas.itemconfigure(self._window_id, width=event.width)

        def _on_mousewheel(self, event: "tk.Event") -> None:
            if getattr(event, "num", None) == 4:
                self._canvas.yview_scroll(-1, "units")
                return
            if getattr(event, "num", None) == 5:
                self._canvas.yview_scroll(1, "units")
                return

            delta = int(-1 * (event.delta / 120)) if getattr(event, "delta", 0) else 0
            if delta:
                self._canvas.yview_scroll(delta, "units")


    class TaskRow:
        def __init__(
            self,
            master: "tk.Misc",
            *,
            task_id: str,
            stage: str,
            task_name: str,
            initial_completed: bool,
            initial_note: str,
            initial_updated_at: str,
            on_change,
            on_delete,
            on_rename,
        ):
            self.task_id = task_id
            self.stage = stage
            self._on_change = on_change
            self._on_delete = on_delete
            self._on_rename = on_rename

            self.completed = initial_completed
            self.note_var = tk.StringVar(value=initial_note)
            self.updated_at_var = tk.StringVar(value=initial_updated_at)
            self._last_saved_note = initial_note

            self.frame = ttk.Frame(master)

            self.status_label = ttk.Label(self.frame, text="", width=3, anchor="center")
            self.status_label.grid(row=0, column=0, padx=(2, 6), pady=2, sticky="w")

            self.name_label = ttk.Label(self.frame, text="", anchor="w")
            self.name_label.grid(row=0, column=1, padx=(0, 10), pady=2, sticky="w")

            self.note_entry = ttk.Entry(self.frame, textvariable=self.note_var)
            self.note_entry.grid(row=0, column=2, padx=(0, 10), pady=2, sticky="ew")

            self.save_button = ttk.Button(self.frame, text="保存", width=6, command=self.save_note)
            self.save_button.grid(row=0, column=3, padx=(0, 10), pady=2)

            self.updated_label = ttk.Label(self.frame, textvariable=self.updated_at_var, width=19)
            self.updated_label.grid(row=0, column=4, padx=(0, 6), pady=2, sticky="e")

            self.frame.columnconfigure(2, weight=1)

            self._set_task_name(task_name)
            self._refresh_status_ui()

            self.status_label.bind("<Button-1>", lambda _e: self.toggle_completed())
            self.status_label.bind("<Button-3>", self._show_context_menu)
            self.name_label.bind("<Button-3>", self._show_context_menu)
            self.note_entry.bind("<Button-3>", self._show_context_menu)

            self.note_entry.bind("<FocusOut>", lambda _e: self.save_note(auto=True))
            self.note_entry.bind("<Return>", lambda _e: self.save_note())

        def _set_task_name(self, task_name: str) -> None:
            self.task_name = task_name
            self.name_label.configure(text="%s - %s" % (self.task_id, task_name))

        def _refresh_status_ui(self) -> None:
            if self.completed:
                self.status_label.configure(text="✅", foreground="#1a7f37")
            else:
                self.status_label.configure(text="☐", foreground="#666666")

        def toggle_completed(self) -> None:
            self.completed = not self.completed
            self.updated_at_var.set(_now_str())
            self._refresh_status_ui()
            self._on_change(self)

        def save_note(self, auto: bool = False) -> None:
            note = self.note_var.get().strip()
            self.note_var.set(note)

            if auto and note == self._last_saved_note:
                return

            self._last_saved_note = note
            self.updated_at_var.set(_now_str())
            self._on_change(self)

        def _show_context_menu(self, event: "tk.Event") -> None:
            menu = tk.Menu(self.frame, tearoff=0)
            menu.add_command(label="编辑任务名称", command=self._rename_task)
            menu.add_separator()
            menu.add_command(label="删除任务", command=self._delete_task)
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        def _delete_task(self) -> None:
            self._on_delete(self.task_id)

        def _rename_task(self) -> None:
            if askstring is None:
                return

            new_name = askstring("编辑任务名称", "请输入新的任务名称：", initialvalue=self.task_name)
            if not new_name:
                return

            new_name = new_name.strip()
            if not new_name:
                return

            self._set_task_name(new_name)
            self.updated_at_var.set(_now_str())
            self._on_rename(self)


    class TaskManagerApp:
        def __init__(self) -> None:
            self.paths = get_storage_paths()
            self._pending_save_after_id = None  # type: Optional[str]

            self.root = tk.Tk()
            self.root.title("山脚下项目任务管理（Shanjiaxia Project Task Manager）")
            self.root.minsize(800, 600)

            self._configure_styles()
            self._load_data()
            self._build_ui()
            self._load_config()

            self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        def _configure_styles(self) -> None:
            style = ttk.Style()
            try:
                style.theme_use("clam")
            except Exception:
                return

        def _load_data(self) -> None:
            raw = load_json(self.paths.data_path)

            self.data = {"version": 1, "tasks": {}}  # type: Dict[str, Any]

            tasks_any = raw.get("tasks")
            if isinstance(tasks_any, dict):
                self.data["tasks"] = tasks_any

            for task in DEFAULT_TASKS:
                self.data["tasks"].setdefault(
                    task.task_id,
                    {
                        "task_id": task.task_id,
                        "stage": task.stage,
                        "name": task.name,
                        "completed": False,
                        "note": "",
                        "updated_at": "",
                    },
                )

        def _build_ui(self) -> None:
            main = ttk.Frame(self.root, padding=10)
            main.pack(fill="both", expand=True)

            self.paned = ttk.PanedWindow(main, orient="horizontal")
            self.paned.pack(fill="both", expand=True)

            left = ttk.Frame(self.paned)
            self.paned.add(left, weight=3)

            self.scroll = ScrollableFrame(left)
            self.scroll.pack(fill="both", expand=True)

            right = ttk.Frame(self.paned, padding=(10, 0, 0, 0))
            self.paned.add(right, weight=1)

            stats = ttk.LabelFrame(right, text="统计信息", padding=10)
            stats.pack(fill="x")

            self.total_var = tk.StringVar(value="0")
            self.done_var = tk.StringVar(value="0")
            self.percent_var = tk.StringVar(value="0%")

            ttk.Label(stats, text="总任务数：").grid(row=0, column=0, sticky="w")
            ttk.Label(stats, textvariable=self.total_var).grid(row=0, column=1, sticky="e")

            ttk.Label(stats, text="已完成数：").grid(row=1, column=0, sticky="w", pady=(6, 0))
            ttk.Label(stats, textvariable=self.done_var).grid(row=1, column=1, sticky="e", pady=(6, 0))

            ttk.Label(stats, text="完成进度：").grid(row=2, column=0, sticky="w", pady=(6, 0))
            ttk.Label(stats, textvariable=self.percent_var).grid(row=2, column=1, sticky="e", pady=(6, 0))

            self.progress = ttk.Progressbar(stats, orient="horizontal", mode="determinate")
            self.progress.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))

            stats.columnconfigure(0, weight=1)

            self._build_task_rows()
            self._refresh_stats()

        def _build_task_rows(self) -> None:
            for child in self.scroll.content.winfo_children():
                child.destroy()

            self.rows = {}  # type: Dict[str, TaskRow]

            by_stage = {}  # type: Dict[str, List[TaskDefinition]]
            for task in DEFAULT_TASKS:
                by_stage.setdefault(task.stage, []).append(task)

            for stage, tasks in by_stage.items():
                stage_frame = ttk.LabelFrame(self.scroll.content, text=stage, padding=10)
                stage_frame.pack(fill="x", expand=True, pady=(0, 10))

                header = ttk.Frame(stage_frame)
                header.pack(fill="x", pady=(0, 6))
                ttk.Label(header, text="状态", width=4).grid(row=0, column=0, sticky="w")
                ttk.Label(header, text="任务", width=40).grid(row=0, column=1, sticky="w")
                ttk.Label(header, text="备注", width=30).grid(row=0, column=2, sticky="w")
                ttk.Label(header, text="", width=6).grid(row=0, column=3)
                ttk.Label(header, text="更新时间", width=19).grid(row=0, column=4, sticky="e")
                header.columnconfigure(2, weight=1)

                for task in tasks:
                    record_any = self.data["tasks"].get(task.task_id, {})
                    record = record_any if isinstance(record_any, dict) else {}

                    row = TaskRow(
                        stage_frame,
                        task_id=task.task_id,
                        stage=stage,
                        task_name=str(record.get("name") or task.name),
                        initial_completed=bool(record.get("completed")),
                        initial_note=str(record.get("note") or ""),
                        initial_updated_at=str(record.get("updated_at") or ""),
                        on_change=self._on_row_change,
                        on_delete=self._delete_task,
                        on_rename=self._rename_task,
                    )
                    row.frame.pack(fill="x", expand=True)
                    self.rows[task.task_id] = row

        def _on_row_change(self, row: TaskRow) -> None:
            self.data["tasks"][row.task_id] = {
                "task_id": row.task_id,
                "stage": row.stage,
                "name": row.task_name,
                "completed": row.completed,
                "note": row.note_var.get(),
                "updated_at": row.updated_at_var.get(),
            }

            self._refresh_stats()
            self.schedule_save()

        def _rename_task(self, row: TaskRow) -> None:
            self._on_row_change(row)

        def _delete_task(self, task_id: str) -> None:
            row = self.rows.pop(task_id, None)
            if row is not None:
                row.frame.destroy()

            if task_id in self.data.get("tasks", {}):
                del self.data["tasks"][task_id]

            self._refresh_stats()
            self.schedule_save()

        def _refresh_stats(self) -> None:
            total = len(self.rows)
            done = sum(1 for row in self.rows.values() if row.completed)
            percent = int(round((done / float(total)) * 100)) if total else 0

            self.total_var.set(str(total))
            self.done_var.set(str(done))
            self.percent_var.set("%d%%" % percent)
            self.progress.configure(maximum=100, value=percent)

        def schedule_save(self) -> None:
            if self._pending_save_after_id is not None:
                try:
                    self.root.after_cancel(self._pending_save_after_id)
                except Exception:
                    pass

            self._pending_save_after_id = self.root.after(500, self.save_all)

        def save_all(self) -> None:
            self._pending_save_after_id = None
            save_json_atomic(self.paths.data_path, self.data)

        def _load_config(self) -> None:
            cfg = load_json(self.paths.config_path)
            geometry = cfg.get("geometry")
            if isinstance(geometry, str) and geometry:
                try:
                    self.root.geometry(geometry)
                    return
                except Exception:
                    pass

            self.root.geometry("1000x700+100+100")

        def save_config(self) -> None:
            cfg = {
                "version": 1,
                "geometry": self.root.geometry(),
                "saved_at": _now_str(),
            }
            save_json_atomic(self.paths.config_path, cfg)

        def on_close(self) -> None:
            try:
                self.save_config()
            finally:
                try:
                    self.save_all()
                finally:
                    self.root.destroy()

        def run(self) -> None:
            self.root.mainloop()


def main() -> None:
    if tk is None or ttk is None:  # pragma: no cover
        raise RuntimeError(
            "当前Python环境缺少Tkinter（tkinter）模块。\n"
            "Windows 11 通常自带 Tkinter；若在精简Python环境中运行，请安装带 Tk 支持的 Python。"
        )

    app = TaskManagerApp()
    app.run()


if __name__ == "__main__":
    main()
