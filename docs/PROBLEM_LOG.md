# AxiomWeave 问题日志

记录开发过程中发生了什么、原因、解决方式和结果，避免相同问题再次出现。

## 001. Windows 路径大小写导致 Memory 项目目录分裂

### 发生了什么

同一个物理项目分别从 `D:\Code\AxiomWeave` 和 `D:\code\AxiomWeave` 启动后，AxiomWeave 生成了 `ed72c87b157c9f92` 与 `afed45de5f28812c` 两个项目目录。两个目录都没有 Memory 文件，但目录时间和 `/memory` 的空结果让 Session 恢复与长期记忆看起来不一致。诊断时调用 `get_memory_dir()` 也会通过 `mkdir` 创建空目录，因此该读取路径并非完全无副作用。

### 原因

旧实现直接对 `str(Path.cwd())` 执行 SHA-256。Windows 文件系统通常不区分路径大小写，但字符串哈希区分大小写，导致同一物理目录得到不同项目标识。同时，资源管理器的目录“修改日期”不会因为再次访问已有目录而更新，不能用它判断最近一次 REPL 启动时间。

### 解决方式

在 `agents/memory.py` 的 `_project_hash()` 中，先通过 `Path.cwd().resolve()` 解析路径，再使用 `os.path.normcase()` 按平台规范化，最后计算哈希。加入中文注释说明 Windows 大小写语义，并在 `tests/test_memory.py` 增加回归测试，验证两种路径写法生成相同哈希。旧目录迁移作为独立待解决事项保留。

### 结果

两种路径写法现在都会映射到 `dfc174bd87dff0ec`。旧目录不会自动迁移；当前 `ed72c87b157c9f92` 与 `afed45de5f28812c` 均为空，可在关闭 AxiomWeave 后手动删除。今后诊断 Memory 时需要注意 `get_memory_dir()` 的目录创建副作用。
