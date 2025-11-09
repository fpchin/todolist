# 仓库重命名指南：todolist → GTMS

本指南帮助您将仓库从 `todolist` 重命名为 `gtms`。

## 一、在 GitHub 上重命名仓库

### 如果仓库已在 GitHub 上：

1. 登录 GitHub: https://github.com/fpchin/todolist
2. 点击仓库右上角的 **Settings** (设置)
3. 在顶部找到 **Repository name** 输入框
4. 将 `todolist` 改为 `gtms`
5. 点击 **Rename** 按钮

✅ GitHub 会自动创建重定向，旧 URL 仍可访问

### 如果仓库尚未创建：

1. 登录 GitHub: https://github.com
2. 点击右上角 "+" → "New repository"
3. 输入仓库名称：**`gtms`**
4. 描述：Golf Tournament Management System
5. 选择 Public 或 Private
6. **不要**勾选 "Initialize this repository"
7. 点击 "Create repository"

## 二、更新本地配置

### 1. 更新 Git Remote URL

在当前项目目录执行：

```bash
# 方法 A：如果在 GitHub 上重命名了仓库
# GitHub 会自动重定向，无需更改（推荐）

# 方法 B：显式更新 remote URL
git remote set-url origin https://github.com/fpchin/gtms.git

# 验证新 URL
git remote -v
```

### 2. 重命名本地目录（可选）

```bash
# 退出当前目录
cd ..

# 重命名目录
mv todolist gtms

# 进入新目录
cd gtms

# 验证 git 仓库仍然正常
git status
```

### 3. 推送到新仓库（如果是新建的）

```bash
# 添加新的 GitHub 远程仓库
git remote add github https://github.com/fpchin/gtms.git

# 推送所有代码
git push github claude/gtms-architecture-design-011CUvS889crYY2gMhw3YuYC:main

# 或推送当前分支
git push -u github claude/gtms-architecture-design-011CUvS889crYY2gMhw3YuYC
```

## 三、更新文档引用（已完成）

✅ 已更新 `docs/00_legacy_analysis_guide.md` 中的路径引用
- 旧路径：`/home/user/todolist/`
- 新路径：`/home/user/gtms/`

## 四、克隆新仓库

重命名后，其他人可以使用新 URL 克隆：

```bash
# 克隆仓库
git clone https://github.com/fpchin/gtms.git
cd gtms

# 启动服务
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## 五、验证清单

完成重命名后，请验证：

- [ ] GitHub 仓库名称已改为 `gtms`
- [ ] 本地可以正常 `git pull` 和 `git push`
- [ ] README.md 中的仓库链接正确
- [ ] Docker 服务正常启动
- [ ] 应用可以正常访问

## 六、如果遇到问题

### 问题 1：git push 失败
```bash
# 错误：remote: Repository not found
# 解决：更新 remote URL
git remote set-url origin https://github.com/fpchin/gtms.git
```

### 问题 2：本地目录名称不一致
```bash
# 可以保持目录名为 todolist，不影响 Git 操作
# 或者按照步骤二重命名目录
```

### 问题 3：需要更新团队成员的克隆
通知团队成员更新本地配置：
```bash
cd todolist  # 或原目录名
git remote set-url origin https://github.com/fpchin/gtms.git
git pull
```

## 完成！

重命名完成后，您的 GTMS 项目将使用更准确的仓库名称。

**新仓库地址**：https://github.com/fpchin/gtms
**克隆命令**：`git clone https://github.com/fpchin/gtms.git`
