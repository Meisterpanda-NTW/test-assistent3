import streamlit as st
import ollama

st.set_page_config(page_title="Garmin KI", page_icon="🎙️")
st.title("🎙️ Garmin KI Assistent")

html_code = """
<div style="text-align:center; margin-bottom:20px;">

<button id="mic-btn" style="background:#ff4b4b;color:white;border:none;padding:12px 24px;border-radius:8px;font-size:16px;font-weight:bold;cursor:pointer;width:250px;">
🎙️ Assistent starten
</button>

<p id="status" style="font-family:sans-serif;font-weight:bold;margin-top:15px;">
Bereit.
</p>

<div id="antwort-box" style="display:none;margin-top:20px;padding:15px;border-radius:8px;background:#e2e2e2;font-family:sans-serif;font-weight:bold;"></div>

</div>

<script>
const btn = document.getElementById("mic-btn");
const status = document.getElementById("status");
const antwortBox = document.getElementById("antwort-box");

const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {
    status.innerText = "Browser unterstützt SpeechRecognition nicht";
}
else {

    const rec = new Recognition();

    rec.lang = 'de-DE';
    rec.interimResults = false;

    let warteAufBefehl = false;
    let aktiv = false;

    function piep() {
        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => osc.stop(), 250);
    }

    function sprich(text) {
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
    }

    btn.addEventListener("click", () => {
        aktiv = true;
        rec.start();

        status.innerText = "💤 Warte auf Okay Garmin";
        btn.style.background = "orange";
    });

    rec.onresult = async (e) => {

        const gehoert = e.results[0][0].transcript.toLowerCase();

st.components.v1.html(html_code, height=350)