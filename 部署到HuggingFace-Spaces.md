# 部署到 Hugging Face Spaces（拿到在线 Demo 链接）

目标：把 4 个文件传上去，配好 Key，得到 `https://huggingface.co/spaces/<你的用户名>/<空间名>` 的在线链接。

## 第 1 步：注册 / 登录

打开 https://huggingface.co ，用邮箱或 GitHub 注册登录。

## 第 2 步：创建 Space

右上角头像 → **New Space**：

- Space name：`dushe-study-buddy`（或拼音，如 `dushe-xuexi-dazi`）
- License：选 MIT 即可
- Select the Space SDK：选 **Streamlit**
- Space hardware：选免费的 **CPU basic**
- 可见性：Public（笔试要交链接）或 Private 都可以

点 **Create Space**。

## 第 3 步：上传 4 个文件

进入 Space 页面 → **Files** 标签 → **Add file** → **Upload files**，上传：

- `app.py`
- `pet.py`
- `requirements.txt`
- `README.md`

上传完点下方 **Commit changes**。

> 想用 git 也行：
>
> ```bash
> git clone https://huggingface.co/spaces/<你的用户名>/<空间名>
> # 把 4 个文件复制进去
> git add . && git commit -m "init" && git push
> ```

## 第 4 步：给 Key（两种方式，二选一）

### 方式 A：让访客自己填（交 Demo 最简单，什么都不用配）

上传完 4 个文件后直接打开 Space。访客在页面左侧「🔑 填 API Key」里粘贴自己的 DeepSeek Key 就能玩。
Key 只存在访客自己的浏览器会话里，不写入仓库、不写入 Space。

### 方式 B：你帮访客配好，打开就能聊（可选）

1. 进入 Space 页面 → **Settings** → **Variables and secrets**。
2. 在 **Secrets** 区点 **New secret**：
   - Name：`DEEPSEEK_API_KEY`
   - Value：`sk-你的DeepSeek密钥`
3. 保存。Space 会自动重启。

> 名字必须一字不差是 `DEEPSEEK_API_KEY`，代码按这个名字读取。
> 如果两边都有 Key，访客在页面填的 Key 优先。

## 第 5 步：打开链接

重启完成后，回到 Space 的 **App** 标签，就能看到聊天界面。

在线链接格式：

```text
https://huggingface.co/spaces/<你的用户名>/<空间名>
```

## 验证清单

- 左侧有「🔑 填 API Key」窗口；没配 Secret 时它默认展开
- 聊天框能收到毒舌回复
- 点「✅ 今日打卡」后，左侧好感 / 连续打卡变化
- 点「🕊️ 我鸽了」后，被骂且给出建议
- 刷新页面后状态还在（同一容器内）

## 常见问题

- 页面提示「还没填 API Key」：在左侧「🔑 填 API Key」里粘一个即可；或检查 Secret 名是否写对。
- 构建失败：看 Settings → **Factory rebuild** 的日志，通常是 `requirements.txt` 没传或文件名不对。
- 记忆重置：免费 Space 重启/重建会重置 `pet_memory.json`，这是预期行为；长期养建议本地跑。
- 想更新代码：直接在 Files 里覆盖上传再 Commit，或 git push，Space 会自动 rebuild。
