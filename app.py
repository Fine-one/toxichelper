"""毒舌学习搭子 —— Streamlit 主程序

运行方式（在项目目录下）：
    uv run streamlit run app.py
"""
import os
from datetime import date

import streamlit as st

from pet import Pet

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

STAGE_PERSONA = {
    "蛋蛋": "你现在是刚孵化的「蛋蛋」，嘴最毒、最不耐烦，但每条吐槽必须夹一条具体可执行的学习建议。",
    "幼年体": "你现在是「幼年体」，刚破壳，嘴还是欠，但会先怼后哄，偶尔给点糖。",
    "成长期": "你现在是「成长期」，半夸半怼，像并肩作战的毒舌同桌。",
    "大佬搭子": "你现在是「大佬搭子」，傲娇式夸夸，表面嫌弃，其实很为主人骄傲。",
}

st.set_page_config(page_title="毒舌学习搭子", page_icon="🥚", layout="centered")


def get_api_key() -> str:
    """Key 读取优先级：页面填写 > Streamlit Secrets > 环境变量。"""
    key = st.session_state.get("user_api_key", "")
    if not key:
        try:
            key = st.secrets.get("DEEPSEEK_API_KEY", "")
        except Exception:
            key = ""
    if not key:
        key = os.environ.get("DEEPSEEK_API_KEY", "")
    return (key or "").strip()


def build_system(pet: Pet) -> str:
    persona = STAGE_PERSONA.get(pet.stage_name(), STAGE_PERSONA["蛋蛋"])
    return (
        "你是「毒舌学习搭子」，一只傲娇的 AI 学习宠物。\n"
        f"{persona}\n"
        "人设规则：\n"
        "1. 毒舌但傲娇，句句戳中要害，但立场永远是帮主人学习。\n"
        "2. 每次回复 2-3 句话，必须有 emoji，最好有梗，不要长篇大论。\n"
        f"3. 当前状态：阶段={pet.stage_name()}，好感={pet.hearts}/100，"
        f"连续打卡={pet.streak}天，被鸽={pet.skipped}次，累计打卡={pet.total_checkins}天。\n"
        "4. 好感越高、阶段越靠后，你和主人越亲近、越爱夸；被鸽时先骂醒，再给一条具体建议。\n"
        "5. 不要输出标题、列表或代码块，就像发微信一样说话。"
    )


def get_pet() -> Pet:
    if "pet" not in st.session_state:
        st.session_state.pet = Pet()
    return st.session_state.pet


def ensure_history() -> None:
    if "messages" not in st.session_state:
        pet = get_pet()
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    f"我是你的{pet.stage_name()}学习搭子，滚过来报到。"
                    "今天学了吗？没学别跟我说话 🥚"
                ),
            }
        ]


def call_deepseek(pet: Pet):
    """调用 DeepSeek（OpenAI 兼容接口）。没配 Key 或出错时降级。"""
    key = get_api_key()
    if not key:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=key, base_url=DEEPSEEK_BASE_URL)
        messages = [{"role": "system", "content": build_system(pet)}]
        messages += st.session_state.messages[-12:]
        resp = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
            temperature=0.9,
            max_tokens=200,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:  # 演示项目：统一降级为友好提示
        return f"🤖 DeepSeek 没接上：{exc}"


def pet_reply(pet: Pet, user_text: str, fallback: str) -> None:
    st.session_state.messages.append({"role": "user", "content": user_text})
    pet.remember("user", user_text)
    reply = call_deepseek(pet) or fallback
    st.session_state.messages.append({"role": "assistant", "content": reply})
    pet.remember("assistant", reply)


def handle_action(pet: Pet, action: str) -> None:
    today = date.today().isoformat()
    if action == "checkin":
        result = pet.checkin(today)
        if result["status"] == "already":
            st.session_state.messages.append(
                {"role": "assistant", "content": "今天已经打过卡了，重复打卡无效，滚去学习 📚"}
            )
            return
        pet_reply(pet, "我刚刚点了「今日打卡」✅", result["message"])
    elif action == "skip":
        result = pet.skip(today)
        if result["status"] == "conflict":
            st.session_state.messages.append(
                {"role": "assistant", "content": "今天都打卡了还点「我鸽了」？手滑是不是 😤"}
            )
            return
        pet_reply(pet, "我刚刚点了「我鸽了」🕊️", result["message"])


def render_sidebar(pet: Pet) -> None:
    st.sidebar.title("🥚 毒舌学习搭子")
    st.sidebar.caption(f"当前阶段：{pet.stage_name()}")
    st.sidebar.progress(pet.stage_progress())
    nxt = pet.next_stage()
    if nxt:
        st.sidebar.caption(f"距离「{nxt['name']}」还差 {nxt['min_exp'] - pet.exp} 经验")
    else:
        st.sidebar.caption("已满级，大佬搭子本子 🎓")
    st.sidebar.metric("❤️ 好感", pet.hearts)
    st.sidebar.metric("🔥 连续打卡", f"{pet.streak} 天")
    st.sidebar.metric("🕊️ 被鸽", f"{pet.skipped} 次")
    st.sidebar.metric("📅 累计打卡", f"{pet.total_checkins} 天")
    if pet.last_checkin:
        st.sidebar.caption(f"最近打卡：{pet.last_checkin}")
    st.sidebar.divider()

    with st.sidebar.expander("🔑 填 API Key（可选）", expanded=not get_api_key()):
        st.caption(
            "不想配环境变量？把 DeepSeek 的 Key 粘进来即可。"
            "仅保存在当前浏览器会话，不写入文件，刷新后需重填。"
        )
        st.text_input(
            "DeepSeek API Key",
            type="password",
            key="user_api_key",
            placeholder="sk-...",
            help="要长期保存：请改用 .streamlit/secrets.toml 或环境变量 DEEPSEEK_API_KEY。",
        )
        if get_api_key() and st.button("清除已填 Key"):
            st.session_state.pop("user_api_key", None)
            st.rerun()

    if not get_api_key():
        st.sidebar.warning("还没填 API Key：点左侧「🔑 填 API Key」粘一个，聊天才能接上 DeepSeek。")


def main() -> None:
    ensure_history()
    pet = get_pet()
    render_sidebar(pet)

    col1, col2 = st.columns(2)
    action = None
    if col1.button("✅ 今日打卡"):
        action = "checkin"
    if col2.button("🕊️ 我鸽了"):
        action = "skip"
    if action:
        handle_action(pet, action)

    prompt = st.chat_input("对蛋蛋说句话，比如：今天不想学了…")
    if prompt:
        pet_reply(pet, prompt, "（还没接上 DeepSeek，先夸你一句：肯打字就是进步 🥚）")

    for msg in st.session_state.messages:
        avatar = "🥚" if msg["role"] == "assistant" else "🧑‍💻"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    with st.expander("🧾 宠物记忆说明"):
        st.markdown(
            "- 养成数据存在项目目录的 `pet_memory.json`（最近对话、连续打卡天数、被鸽次数）。\n"
            "- 想重新养一只：停掉程序，删除 `pet_memory.json` 再启动。"
        )


if __name__ == "__main__":
    main()
