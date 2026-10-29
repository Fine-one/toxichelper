# 🥚 毒舌学习搭子

一个会骂你拖延、也会傲娇夸你的 AI 学习宠物（养成 + 提效结合）。

技术栈：Python + Streamlit + DeepSeek API（OpenAI 兼容接口）+ JSON 文件记忆。

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=Fine-one%2Ftoxichelper&branch=main&mainModule=app.py)

## 功能

- **聊天**：毒舌人设，句句戳中要害但有用；每次 2-3 句，有 emoji、有梗
- **今日打卡**：经验 +15、好感 +5，连续打卡会累积
- **我鸽了**：好感 -10、连续打卡清零，毒舌骂醒 + 给一条具体建议
- **等级成长**：蛋蛋 → 幼年体 → 成长期 → 大佬搭子（越养越亲近）
- **记忆**：`pet_memory.json` 存最近对话、连续打卡天数、被鸽次数

## 在线 Demo 怎么玩（评审人看这里，零部署）

**在线 Demo：https://fine-one-toxichelper-app-efajuh.streamlit.app/**

1. 打开上面的在线 Demo 链接。
2. 在页面左侧「🔑 填 API Key」窗口里，粘贴一个 DeepSeek API Key（`sk-...`）。
3. 直接聊天、点「✅ 今日打卡」、点「🕊️ 我鸽了」。

> Key 只在当前浏览器会话里使用，**不写入文件、不提交 git、不保存**，刷新页面后重填一次即可。
> 没有 Key？去 https://platform.deepseek.com 注册 → API Keys → 创建，充值 10 元能玩很久。

## 自己部署

### 方式 A：本地运行

WSL / macOS / Linux：

```bash
git clone <你的仓库地址>
cd <仓库目录>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows：双击 `启动-Windows.bat`，或：

```bat
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\streamlit run app.py
```

本地想长期记住 Key：新建 `.streamlit/secrets.toml`，写入：

```toml
DEEPSEEK_API_KEY = "sk-你的key"
```

### 方式 B：Streamlit Community Cloud（推荐在线部署，免费）

点下面的按钮，用 GitHub 登录后按提示确认即可（仓库、分支、入口文件已自动填好）：

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=Fine-one%2Ftoxichelper&branch=main&mainModule=app.py)

或手动：打开 https://share.streamlit.io → **New app** → 选本仓库、分支 `main`、入口文件 `app.py` → Deploy。

> 备注：Hugging Face Spaces 免费版现在不能托管 Streamlit（Docker 型 Space 需 PRO），所以在线 Demo 用 Streamlit Cloud。
> Key 不用配 Secret，访客在左侧窗口自己填；想免填，可在 Advanced settings 加 Secret `DEEPSEEK_API_KEY`。

## 文件结构

| 文件 | 作用 |
| --- | --- |
| `app.py` | Streamlit 界面 + DeepSeek 对话 + 页面内填 Key 窗口 |
| `pet.py` | 养成逻辑 + JSON 记忆 |
| `requirements.txt` | 依赖 |
| `README.md` | 说明（本文件） |
| `.gitignore` | 排除 `.venv/`、`.streamlit/secrets.toml`、`pet_memory.json` |
| `启动-Windows.bat` | Windows 一键启动（可选） |

## 养成数值

| 操作 | 经验 | 好感 | 连续打卡 |
| --- | --- | --- | --- |
| 今日打卡 | +15 | +5（上限 100） | +1（隔天断则重来） |
| 我鸽了 | 不变 | -10（下限 0） | 清零 |

等级：蛋蛋(0) → 幼年体(20) → 成长期(60) → 大佬搭子(120)。

## 安全说明

- **API Key 不进 git**：`.gitignore` 已排除 `.streamlit/secrets.toml`、`.venv/`、`pet_memory.json`。
- 页面里填的 Key 只存在浏览器会话，刷新即失效，不落盘。
- 代码和教程里不出现任何真实 Key。

## 交付内容

- 图文教程（小红书风格）：`小红书图文教程.md`
- 创作说明：`创作说明.md`
- 部署步骤：`部署到Streamlit-Cloud.md`
