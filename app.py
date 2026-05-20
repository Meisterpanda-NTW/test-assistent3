import streamlit as st
        s.lang = "de-DE";
        window.speechSynthesis.speak(s);
    }

    btn.onclick = () => {
        active = true;
        rec.start();
        status.innerText = "Sage: OK Garmin";
    }

    rec.onresult = (e) => {
        const text = e.results[0][0].transcript.toLowerCase();

        if (!wait) {
            if (text.includes("okay garmin")) {
                wait = true;
                status.innerText = "Ich höre...";
                rec.stop();
            }
        } else {
            wait = false;

            status.innerText = "Frage wird gesendet...";

            // 👉 Streamlit Übergabe via URL
            const url = new URL(window.location);
            url.searchParams.set("text", text);
            window.location = url;
        }
    }

    rec.onend = () => {
        if (active) setTimeout(() => rec.start(), 300);
    }
}
</script>
"""

st.components.v1.html(html, height=300)

# --- Streamlit Query Input ---
query = st.query_params.get("text")

if query:
    st.info(f"Du: {query}")

    st.session_state.chat.append({"role": "user", "content": query})

    response = ollama.chat(
        model="llama3",
        messages=st.session_state.chat
    )

    answer = response["message"]["content"]

    st.session_state.chat.append({"role": "assistant", "content": answer})

    st.success(answer)

    st.markdown("### 💬 Chat Verlauf")
    for m in st.session_state.chat[1:]:
        if m["role"] == "user":
            st.write("🧑 Du:", m["content"])
        else:
            st.write("🤖 KI:", m["content"])
