#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查本地cto文件夹与GitHub仓库是否同步的工具

使用方式：
    python check_sync.py

输出：
    生成 sync_report.md 报告文件
"""

import os
import hashlib
import json
from pathlib import Path
from datetime import datetime
import subprocess
import sys

class SyncChecker:
    """本地和GitHub文件同步检查器"""
    
    def __init__(self):
        self.local_root = Path("D:/cto").resolve()
        self.project_root = self.local_root / "projects" / "山脚下"
        self.report = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "local_root": str(self.local_root),
            "total_files": 0,
            "synced_files": 0,
            "missing_local": [],
            "missing_github": [],
            "content_diff": [],
            "ignored_patterns": [".git", ".gitkeep", "__pycache__", ".pyc", ".log"],
        }
        self.github_files = {}
        self.local_files = {}
        
    def should_ignore(self, path):
        """判断是否应该忽略该文件"""
        path_str = str(path).lower()
        for pattern in self.report["ignored_patterns"]:
            if pattern in path_str:
                return True
        return False
    
    def get_file_hash(self, file_path):
        """计算文件的MD5哈希"""
        if not file_path.exists():
            return None
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def scan_local_files(self):
        """扫描本地文件"""
        print("📂 扫描本地文件...")
        
        for root, dirs, files in os.walk(self.local_root):
            # 移除要忽略的目录
            dirs[:] = [d for d in dirs if not self.should_ignore(d)]
            
            for file in files:
                if self.should_ignore(file):
                    continue
                    
                file_path = Path(root) / file
                # 相对于 cto 的路径
                rel_path = file_path.relative_to(self.local_root)
                file_hash = self.get_file_hash(file_path)
                
                self.local_files[str(rel_path)] = {
                    "path": str(file_path),
                    "hash": file_hash,
                    "size": file_path.stat().st_size if file_path.exists() else 0,
                }
                self.report["total_files"] += 1
        
        print(f"✅ 本地文件扫描完成：{self.report['total_files']} 个文件")
    
    def get_github_files(self):
        """从 git 获取 GitHub 上的文件列表"""
        print("🔗 获取 GitHub 文件列表...")
        
        try:
            # 使用 git ls-files 获取仓库中的所有文件
            result = subprocess.run(
                ["git", "ls-files"],
                cwd=str(self.local_root),
                capture_output=True,
                text=True,
                check=True
            )
            
            for file_path in result.stdout.strip().split('\n'):
                if file_path and not self.should_ignore(file_path):
                    self.github_files[file_path] = {
                        "path": file_path,
                        "in_repo": True,
                    }
            
            print(f"✅ GitHub 文件列表获取完成：{len(self.github_files)} 个文件")
            
        except Exception as e:
            print(f"❌ 获取 GitHub 文件列表失败: {e}")
            print("   请确保安装了 Git 并且 D:\\cto 是 Git 仓库")
            return False
        
        return True
    
    def compare_files(self):
        """比对本地和 GitHub 的文件"""
        print("🔍 比对文件...")
        
        # 转换 Windows 路径为 Unix 路径以便比对
        local_files_normalized = {
            k.replace("\\", "/"): v 
            for k, v in self.local_files.items()
        }
        
        # 检查本地有但 GitHub 没有的文件
        for local_path in local_files_normalized:
            if local_path not in self.github_files:
                self.report["missing_github"].append(local_path)
        
        # 检查 GitHub 有但本地没有的文件
        for github_path in self.github_files:
            if github_path not in local_files_normalized:
                self.report["missing_local"].append(github_path)
        
        # 检查内容是否相同
        for github_path in self.github_files:
            if github_path in local_files_normalized:
                local_file = Path(self.local_root) / github_path
                local_hash = self.get_file_hash(local_file)
                
                # 获取 GitHub 版本的哈希
                try:
                    result = subprocess.run(
                        ["git", "hash-object", github_path],
                        cwd=str(self.local_root),
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    github_hash = result.stdout.strip()
                    
                    if local_hash != github_hash:
                        self.report["content_diff"].append({
                            "file": github_path,
                            "local_hash": local_hash,
                            "github_hash": github_hash,
                            "status": "内容不同"
                        })
                    else:
                        self.report["synced_files"] += 1
                        
                except Exception as e:
                    print(f"⚠️  无法比对 {github_path}: {e}")
        
        print(f"✅ 文件比对完成")
    
    def generate_report(self):
        """生成报告文件"""
        print("📝 生成报告...")
        
        report_file = self.project_root / "sync_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 本地 ↔ GitHub 文件同步检查报告\n\n")
            f.write(f"**检查时间**: {self.report['time']}\n\n")
            f.write(f"**本地路径**: {self.report['local_root']}\n\n")
            
            # 总体状态
            f.write("## 📊 总体状态\n\n")
            f.write(f"| 指标 | 数值 |\n")
            f.write(f"|------|------|\n")
            f.write(f"| 总文件数 | {self.report['total_files']} |\n")
            f.write(f"| 已同步 | {self.report['synced_files']} |\n")
            f.write(f"| 本地独有 | {len(self.report['missing_github'])} |\n")
            f.write(f"| GitHub独有 | {len(self.report['missing_local'])} |\n")
            f.write(f"| 内容不同 | {len(self.report['content_diff'])} |\n\n")
            
            # 同步率
            if self.report['total_files'] > 0:
                sync_rate = (self.report['synced_files'] / self.report['total_files']) * 100
                f.write(f"**同步率**: {sync_rate:.2f}%\n\n")
            
            # 本地独有文件（未上传到 GitHub）
            if self.report['missing_github']:
                f.write("## ⚠️ 本地独有文件（未上传 GitHub）\n\n")
                for file_path in sorted(self.report['missing_github']):
                    f.write(f"- {file_path}\n")
                f.write("\n")
            
            # GitHub独有文件（本地未同步）
            if self.report['missing_local']:
                f.write("## ⚠️ GitHub独有文件（本地未同步）\n\n")
                for file_path in sorted(self.report['missing_local']):
                    f.write(f"- {file_path}\n")
                f.write("\n")
            
            # 内容不同的文件
            if self.report['content_diff']:
                f.write("## 🔄 内容不同的文件\n\n")
                for diff in self.report['content_diff']:
                    f.write(f"### {diff['file']}\n\n")
                    f.write(f"- **本地哈希**: {diff['local_hash']}\n")
                    f.write(f"- **GitHub哈希**: {diff['github_hash']}\n")
                    f.write(f"- **状态**: {diff['status']}\n\n")
            
            # 忽略的文件模式
            f.write("## 🚫 忽略的文件模式\n\n")
            for pattern in self.report['ignored_patterns']:
                f.write(f"- {pattern}\n")
            f.write("\n")
            
            # 建议
            f.write("## 💡 建议\n\n")
            if self.report['missing_github']:
                f.write("1. **本地独有文件**: 决定是否需要上传到 GitHub\n")
                f.write("   ```bash\n")
                f.write("   git add .\n")
                f.write("   git commit -m 'sync: add missing files'\n")
                f.write("   git push origin main\n")
                f.write("   ```\n\n")
            
            if self.report['missing_local']:
                f.write("2. **GitHub独有文件**: 需要从 GitHub 同步到本地\n")
                f.write("   ```bash\n")
                f.write("   git pull origin main\n")
                f.write("   ```\n\n")
            
            if self.report['content_diff']:
                f.write("3. **内容不同的文件**: 需要手动合并或覆盖\n")
                f.write("   ```bash\n")
                f.write("   git status\n")
                f.write("   git diff [filename]  # 查看具体差异\n")
                f.write("   git checkout HEAD -- [filename]  # 使用 GitHub 版本覆盖\n")
                f.write("   ```\n\n")
            
            if (not self.report['missing_github'] and 
                not self.report['missing_local'] and 
                not self.report['content_diff']):
                f.write("✅ **所有文件已同步！无需操作。**\n\n")
        
        print(f"✅ 报告已生成: {report_file}")
        print(f"\n📄 报告文件: {report_file}")
        
        # 同时输出到控制台
        with open(report_file, 'r', encoding='utf-8') as f:
            print("\n" + "="*60)
            print(f.read())
            print("="*60)
    
    def run(self):
        """运行检查"""
        print("\n🚀 开始检查本地 ↔ GitHub 文件同步...\n")
        
        # 检查本地路径是否存在
        if not self.local_root.exists():
            print(f"❌ 错误：本地路径不存在: {self.local_root}")
            sys.exit(1)
        
        # 检查是否是 git 仓库
        if not (self.local_root / ".git").exists():
            print(f"❌ 错误：{self.local_root} 不是 Git 仓库")
            sys.exit(1)
        
        self.scan_local_files()
        
        if not self.get_github_files():
            sys.exit(1)
        
        self.compare_files()
        self.generate_report()
        
        print("\n✅ 检查完成！\n")


if __name__ == "__main__":
    checker = SyncChecker()
    checker.run()