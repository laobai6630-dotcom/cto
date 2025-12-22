✅ 好的，给你一个只检查 projects/山脚下 的脚本：

把这个脚本保存为 D:\cto\check_project_sync.py：

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
只检查 projects/山脚下 目录与 GitHub 是否同步
"""

import os
import hashlib
from pathlib import Path
from datetime import datetime
import subprocess
import sys

class ProjectSyncChecker:
    """只检查项目目录的同步检查器"""
    
    def __init__(self):
        self.local_root = Path("D:/cto").resolve()
        self.project_dir = self.local_root / "projects" / "山脚下"
        self.report = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "project_path": str(self.project_dir),
            "total_files": 0,
            "synced_files": 0,
            "missing_github": [],
            "content_diff": [],
            "ignored_patterns": [".git", ".gitkeep", "__pycache__", ".pyc", ".log", "sync_report"],
        }
        self.local_files = {}
        self.github_files = {}
    
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
        """扫描本地项目目录的文件"""
        print(f"📂 扫描本地文件: {self.project_dir}")
        
        for root, dirs, files in os.walk(self.project_dir):
            dirs[:] = [d for d in dirs if not self.should_ignore(d)]
            
            for file in files:
                if self.should_ignore(file):
                    continue
                
                file_path = Path(root) / file
                # 相对于项目目录的路径
                rel_path = str(file_path.relative_to(self.project_dir)).replace("\\", "/")
                file_hash = self.get_file_hash(file_path)
                
                self.local_files[rel_path] = {
                    "path": str(file_path),
                    "hash": file_hash,
                    "size": file_path.stat().st_size if file_path.exists() else 0,
                }
                self.report["total_files"] += 1
        
        print(f"✅ 本地文件扫描完成：{self.report['total_files']} 个文件\n")
    
    def get_github_files(self):
        """从 git 获取 GitHub 上项目目录的文件"""
        print("🔗 获取 GitHub 文件列表...")
        
        try:
            # 获取 projects/山脚下 目录下的所有文件
            result = subprocess.run(
                ["git", "ls-files", "projects/山脚下"],
                cwd=str(self.local_root),
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                check=True
            )
            
            for file_path in result.stdout.strip().split('\n'):
                if file_path and not self.should_ignore(file_path):
                    # 只取 projects/山脚下 之后的相对路径
                    if file_path.startswith("projects/"):
                        rel_path = file_path.replace("projects/山脚下/", "")
                        if rel_path:  # 确保不是空字符串
                            self.github_files[rel_path] = {
                                "path": file_path,
                                "in_repo": True,
                            }
            
            print(f"✅ GitHub 文件列表获取完成：{len(self.github_files)} 个文件\n")
            
        except Exception as e:
            print(f"❌ 获取 GitHub 文件列表失败: {e}")
            return False
        
        return True
    
    def compare_files(self):
        """比对本地和 GitHub 的文件"""
        print("🔍 比对文件...\n")
        
        # 检查本地有但 GitHub 没有的文件
        for local_path in self.local_files:
            if local_path not in self.github_files:
                self.report["missing_github"].append(local_path)
        
        # 检查内容是否相同
        for github_path in self.github_files:
            if github_path in self.local_files:
                local_file = self.project_dir / github_path
                local_hash = self.get_file_hash(local_file)
                
                # 获取 GitHub 版本的哈希
                try:
                    full_github_path = f"projects/山脚下/{github_path}"
                    result = subprocess.run(
                        ["git", "hash-object", full_github_path],
                        cwd=str(self.local_root),
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='ignore',
                        check=True
                    )
                    github_hash = result.stdout.strip()
                    
                    if local_hash != github_hash:
                        self.report["content_diff"].append({
                            "file": github_path,
                            "local_hash": local_hash,
                            "github_hash": github_hash,
                        })
                    else:
                        self.report["synced_files"] += 1
                        
                except Exception as e:
                    print(f"⚠️  无法比对 {github_path}")
        
        print(f"✅ 文件比对完成\n")
    
    def generate_report(self):
        """生成报告"""
        report_file = self.project_dir / "project_sync_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# projects/山脚下 目录同步检查报告\n\n")
            f.write(f"**检查时间**: {self.report['time']}\n\n")
            f.write(f"**项目路径**: {self.report['project_path']}\n\n")
            f.write(f"**GitHub路径**: https://github.com/laobai6630-dotcom/cto/tree/main/projects/山脚下\n\n")
            
            # 总体状态
            f.write("## 📊 总体状态\n\n")
            f.write(f"| 指标 | 数值 |\n")
            f.write(f"|------|------|\n")
            f.write(f"| 总文件数 | {self.report['total_files']} |\n")
            f.write(f"| 已同步 | {self.report['synced_files']} |\n")
            f.write(f"| 本地独有 | {len(self.report['missing_github'])} |\n")
            f.write(f"| 内容不同 | {len(self.report['content_diff'])} |\n\n")
            
            # 同步率
            if self.report['total_files'] > 0:
                sync_rate = (self.report['synced_files'] / self.report['total_files']) * 100
                status = "✅" if sync_rate == 100 else "⚠️" if sync_rate >= 90 else "❌"
                f.write(f"**同步率**: {status} {sync_rate:.1f}%\n\n")
            
            # 本地独有文件
            if self.report['missing_github']:
                f.write("## ⚠️ 本地独有文件（未上传 GitHub）\n\n")
                for file_path in sorted(self.report['missing_github']):
                    f.write(f"- `{file_path}`\n")
                f.write("\n")
            
            # 内容不同的文件
            if self.report['content_diff']:
                f.write("## 🔄 内容不同的文件\n\n")
                f.write("**可能原因**：行尾符差异（CRLF vs LF）\n\n")
                for diff in self.report['content_diff']:
                    f.write(f"- `{diff['file']}`\n")
                f.write("\n")
                f.write("**解决方案**：\n")
                f.write("```bash\n")
                f.write("cd D:\\cto\n")
                f.write("git config core.autocrlf true\n")
                f.write("git add --renormalize .\n")
                f.write("git commit -m 'chore: normalize line endings'\n")
                f.write("git push origin main\n")
                f.write("```\n\n")
            
            # 总体结论
            f.write("## 💡 总体结论\n\n")
            if (not self.report['missing_github'] and 
                not self.report['content_diff']):
                f.write("✅ **项目目录已完全同步！无需操作。**\n\n")
            else:
                f.write("⚠️ **发现同步问题，请参考上方的解决方案。**\n\n")
        
        # 打印报告
        with open(report_file, 'r', encoding='utf-8') as f:
            report_content = f.read()
            print("="*70)
            print(report_content)
            print("="*70)
            print(f"\n📄 完整报告已保存到: {report_file}\n")
    
    def run(self):
        """运行检查"""
        print("\n" + "="*70)
        print("🚀 开始检查 projects/山脚下 与 GitHub 的同步状态...")
        print("="*70 + "\n")
        
        # 检查路径
        if not self.project_dir.exists():
            print(f"❌ 错误：项目目录不存在: {self.project_dir}")
            sys.exit(1)
        
        if not (self.local_root / ".git").exists():
            print(f"❌ 错误：{self.local_root} 不是 Git 仓库")
            sys.exit(1)
        
        self.scan_local_files()
        if not self.get_github_files():
            sys.exit(1)
        self.compare_files()
        self.generate_report()
        
        print("✅ 检查完成！\n")


if __name__ == "__main__":
    checker = ProjectSyncChecker()
    checker.run()