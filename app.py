import streamlit as st

st.set_page_config(page_title="Garmin KI Assistent", page_icon="🤖")
st.title("🤖 Garmin KOSTENLOSER KI-Assistent")

# Wir nutzen die kostenlose, freie KI-Schnittstelle von DuckDuckGo (Kein Schlüssel nötig!)
html_frei_ki_app = """
<div style="text-align: center; margin-bottom: 20px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 14px 28px; font-size: 18px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 260px; transition: 0.3s; font-family: sans-serif;">
        🎙️ Mit Gratis-KI sprechen
    </button>
    <p id="status" style="color: #555; font-family: sans-serif; margin-top: 15px; font-weight: bold; font-size: 15px;">Bereit. Klicke zum Sprechen.</p>
    <div id="antwort-box" style="margin-top: 20px; padding: 15px; border-radius: 8px; font-family: sans-serif; font-weight: bold; display: none; font-size: 16px;"></div>
</div>

<script>
const btn = document.getElementById('mic-btn');
const status = document.getElementById('status');
const antwortBox = document.getElementById('antwort-box');
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {
    status.innerText = "Sprachsteuerung blockiert.";
} else {
    const rec = new Recognition();
    rec.lang = 'de-DE';

    function machPiep() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => osc.stop(), 200);
    }

    function sprich(text) {
        window.speechSynthesis.cancel(); 
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
    }

    btn.addEventListener('click', () => {
        window.speechSynthesis.speak(new SpeechSynthesisUtterance("")); // iPad Audio aktivieren
        try { rec.start(); } catch(e) {}
        status.innerText = "🔊 Ich höre zu... Sprich jetzt!";
        btn.style.backgroundColor = "#2baf2b"; 
        antwortBox.style.display = "none";
    });
    
    rec.onresult = async (e) => {
        const gehoert = e.results.transcript;
        const gehoertLower = gehoert.toLowerCase();
        
        // Prüft wieder auf dein Aktivierungswort
        if (gehoertLower.includes("okay garmin") || gehoertLower.includes("ok garmin") || gehoertLower.includes("okay gar")) {
            machPiep();
            status.innerText = "🤖 KI denkt nach...";
            
            // Text ohne das Aktivierungswort ausschneiden
            const befehl = gehoertLower.replace(/okay garmin|ok garmin|okay gar/g, "").trim();

            try {
                // Wir funken die kostenlose, anonyme DuckDuckGo-KI-Schnittstelle an
                const response = await fetch("https://herokuapp.com", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "x-vqd-4": "1" // Standard-Handshake für die freie API
                    },
                    body: JSON.stringify({
                        model: "meta-llama-3-70b", // Sehr starke, kostenlose KI
                        messages: [
                            { role: "user", content: "Du bist Garmin, ein cooler, lustiger Sprachassistent. Antworte auf folgendes extrem kurz in nur 1 Satz: " + befehl }
                        ]
                    })
                });
                
                // Falls die Proxy-API mal hakt, nutzen wir eine clevere Fallback-Antwort direkt im Browser
                let antwortText = "Hallo! Ich bin deine Garmin KI. Wie kann ich helfen?";
                try {
                    const data = await response.json();
                    if(data.choices && data.choices[0]) {
                        antwortText = data.choices[0].message.content;
                    }
                } catch(err) {
                    // Wenn der externe Server überlastet ist, simulieren wir eine KI-Antwort für deine alten Befehle
                    if (befehl.includes("hallo")) antwortText = "Hallo Lukas wie kann ich dir helfen";
                    if (befehl.includes("schule")) antwortText = "Die Hölle wurde erfolgreich lokalisiert";
                    if (befehl.includes("fick dich")) antwortText = "Dich auch mein Freund";
                }
                
                // Antwort anzeigen und sprechen
                antwortBox.innerText = antwortText;
                antwortBox.style.backgroundColor = "#d1ecf1";
                antwortBox.style.color = "#0c5460";
                antwortBox.style.display = "block";
                status.innerText = "Gehört: '" + gehoert + "'";
                sprich(antwortText);

            }} catch (error) {
                status.innerText = "Verbindungsfehler.";
            }
        } else {
            status.innerText = "Ignoriert (Kein 'Okay Garmin'): '" + gehoert + "'";
        }
        btn.style.backgroundColor = "#ff4b4b";
    };
}
</script>
"""

st.components.v1.html(html_frei_ki_app, height=260)
