# 部署到 Streamlit Community Cloud（免费在线 Demo）

> 为什么不用 Hugging Face Spaces：目前 HF 免费账号创建 Gradio/Docker 型 Space（Streamlit 现在归 Docker 型）需要 PRO 订阅，Static Space 又跑不了 Python，所以改用 Streamlit 官方免费托管。

## 一键部署

点击 README 里的 Deploy to Streamlit 按钮，或在浏览器打开：

```text
https://share.streamlit.io/deploy?repository=Fine-one%2Ftoxichelper&branch=main&mainModule=app.py
```

用 GitHub 登录 → 确认仓库 / 分支 / 入口文件 → 点 Deploy。

## 手动部署

1. 打开 https://share.streamlit.io ，用 GitHub 登录。
2. 点 **Create app**（或 New app）。
3. 选仓库 `Fine-one/toxichelper`、分支 `main`、入口文件 `app.py`。
4. 点 **Deploy**，等 1-3 分钟构建完成。
5. 得到链接：`https://<应用名>.streamlit.app`。

## Key 怎么给（两种，二选一）

- **访客自己填**：什么都不用配，打开链接后在左侧「🔑 填 API Key」粘 Key 就能玩（适合交 Demo）。
- **免填**：App 的 Settings → Secrets 里加 `DEEPSEEK_API_KEY = "sk-..."`。

## 常见问题

- 部署后点不开：确认入口文件是 `app.py`。
- 页面提示没 Key：在左侧窗口填一个即可，刷新后需重填。
- 想更新：往 GitHub 推新代码，Streamlit Cloud 会自动重新部署（或手动 Reboot app）。
