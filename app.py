import streamlit as st

st.set_page_config(page_title="Garmin KI Assistent", page_icon="🤖")
st.title("🤖 Garmin KOSTENLOSER KI-Assistent")

# HINWEIS: Erstelle einen kostenlosen Account auf huggingface.co
# Gehe in deine Einstellungen -> Access Tokens -> New Token (auf "Read" stellen)
# Kopiere den Schlüssel und füge ihn genau hier ein:
HF_TOKEN = "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"

html_echte_gratis_ki = f"""
<div style="text-align: center; margin-bottom: 20px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 14px 28px; font-size: 18px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 260px; transition: 0.3s; font-family: sans-serif;">
        🎙️ Mit Echter Gratis-KI sprechen
    </button>
    <p id="status" style="color: #555; font-family: sans-serif; margin-top: 15px; font-weight: bold; font-size: 15px;">Bereit. Klicke zum Sprechen.</p>
    <div id="antwort-box" style="margin-top: 20px; padding: 15px; border-radius: 8px; font-family: sans-serif; font-weight: bold; display: none; font-size: 16px;"></div>
</div>

<script>
const btn = document.getElementById('mic-btn');
const status = document.getElementById('status');
const antwortBox = document.getElementById('antwort-box');
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {{
    status.innerText = "Sprachsteuerung blockiert.";
}} else {{
    const rec = new Recognition();
    rec.lang = 'de-DE';

    function machPiep() {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => osc.stop(), 200);
    }}

    function sprich(text) {{
        window.speechSynthesis.cancel(); 
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
    }}

    btn.addEventListener('click', () => {{
        window.speechSynthesis.speak(new SpeechSynthesisUtterance("")); // iPad Audio aktivieren
        try {{ rec.start(); }} catch(e) {{}}
        status.innerText = "🔊 Ich höre zu... Sprich jetzt!";
        btn.style.backgroundColor = "#2baf2b"; 
        antwortBox.style.display = "none";
    }});
    
    rec.onresult = async (e) => {{
        const gehoert = e.results[0][0].transcript;
        const gehoertLower = gehoert.toLowerCase();
        
        if (gehoertLower.includes("okay garmin") || gehoertLower.includes("ok garmin") || gehoertLower.includes("okay gar")) {{
            machPiep();
            status.innerText = "🤖 KI überlegt sich eine Antwort...";
            
            const befehl = gehoertLower.replace(/okay garmin|ok garmin|okay gar/g, "").trim();
            
            // Deine alten, festen Befehle prüfen (behalten wir als Abkürzung!)
            let antwortText = "";
            if (befehl.includes("hallo")) antwortText = "Hallo Lukas! Wie kann ich dir heute helfen?";
            else if (befehl.includes("schule")) antwortText = "Die Hölle wurde erfolgreich lokalisiert.";
            else if (befehl.includes("fick dich")) antwortText = "Dich auch, mein Freund.";
            else if (befehl.includes("lukas")) antwortText = "Nein, nicht Lukas!";
            else if (befehl.includes("beenden")) antwortText = "Programm wird beendet.";

            // Wenn es kein fester Befehl ist, funken wir die echte, freie KI an!
            if (!antwortText && befehl) {{
                try {{
                    // Nutzt das extrem starke "Llama-3" Modell komplett kostenlos über Hugging Face
                    const response = await fetch("https://huggingface.co", {{
                        method: "POST",
                        headers: {{
                            "Authorization": "Bearer {HF_TOKEN}",
                            "Content-Type": "application/json"
                        }},
                        body: JSON.stringify({{
                            inputs: "<|begin_of_text|><|start_header_id|>system<|end_header_id|>Du bist Garmin, ein cooler Assistent. Antworte auf Deutsch und fasse dich extrem kurz in genau 1 Satz!<|eot_id|><|start_header_id|>user<|end_header_id|>" + befehl + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
                            parameters: {{ max_new_tokens: 60, stop: ["<|eot_id|>"] }}
                        }})
                    }});
                    
                    const data = await response.json();
                    let rawText = data[0].generated_text;
                    // Filtert das System-Prompt heraus, sodass nur die echte Antwort übrig bleibt
                    antwortText = rawText.split("<|start_header_id|>assistant<|end_header_id|>")[1].trim();
                }} catch (error) {{
                    antwortText = "Ich konnte die kostenlose KI-Schnittstelle gerade nicht erreichen.";
                }}
            }}

            // Antwort anzeigen und laut sprechen
            antwortBox.innerText = antwortText;
            antwortBox.style.backgroundColor = "#d1ecf1";
            antwortBox.style.color = "#0c5460";
            antwortBox.style.display = "block";
            status.innerText = "Gehört: '" + gehoert + "'";
            sprich(antwortText);

        } else {{
            status.innerText = "Ignoriert (Kein 'Okay Garmin'): '" + gehoert + "'";
        }}
        btn.style.backgroundColor = "#ff4b4b";
    }};
}}
</script>
"""

st.components.v1.html(html_echte_gratis_ki, height=260)
