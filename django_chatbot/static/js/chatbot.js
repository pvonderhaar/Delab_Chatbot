document.getElementById('postButton').addEventListener('click', async function() {
            const userInput = document.getElementById('user_input').value;
            if (!userInput.trim()) return; // Verhindert leere Nachrichten

            const chatBox = document.getElementById('chatBox');
            const loadingDots = document.getElementById('loadingDots');

            // Nutzer-Nachricht erstellen
            const userMessage = document.createElement('div');
            userMessage.classList.add('chat-message');
            userMessage.innerHTML = `
                <img src="${STATIC_PATHS.profileYou}" alt="profile_user0.png">
                <div class="chat-text">
                    <strong>You</strong>${userInput}
                </div>
            `;
            chatBox.appendChild(userMessage);
            document.getElementById('user_input').value = ""; // Eingabe leeren

            // Ladeanimation aktivieren
            loadingDots.style.display = "block";

            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            const response = await fetch("/ask/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `user_input=${encodeURIComponent(userInput)}`
            });

            const data = await response.json();

            // Ladeanimation verstecken
            loadingDots.style.display = "none";
            let botText = "Oops! Something went wrong!";
            let showAnalytics = false;

            if (data.answer && data.answer.df && data.answer.df.length > 0) {
                botText = data.answer.df[0].out_llm;
                showAnalytics = true;
            }


            // Chatbot-Nachricht erstellen
            const botMessage = document.createElement('div');
            botMessage.classList.add('chat-message');
            botMessage.innerHTML = `
                <img src="${STATIC_PATHS.profileBot}" alt="profile_user0.png">
                <div class="chat-text">
                    <strong>Chatbot</strong>${botText}
                </div>
            `;
            chatBox.appendChild(botMessage);
            if (showAnalytics) {
                document.getElementById("chatExtras").style.display = "block";
                const analyticsList = document.getElementById("analyticsList");
                analyticsList.innerHTML = ""; // Clear vorherigen Inhalt

                data.answer.features.forEach((feature,index) => {
                    const item = document.createElement("li");
                    if (index === 0) {
                        item.innerHTML = `<strong>User Comment: </strong>  Sentiment: Neutral ${feature.sent_neutral}, Positive ${feature.sent_positive}, Negative ${feature.sent_negative}`;
                        analyticsList.appendChild(item);
                    } else if (index === 1) {
                        item.innerHTML = `<strong>Input Comment: </strong>  Sentiment: Neutral ${feature.sent_neutral}, Positive ${feature.sent_positive}, Negative ${feature.sent_negative}`;
                        analyticsList.appendChild(item);

                        const secondItem = document.createElement("li");
                        secondItem.innerHTML = `<strong> Between Comments </strong> Justification: ${feature.argpred_1_dev}`;
                        analyticsList.appendChild(secondItem);
                    }

                });
                const interventionProb = data.answer.intervention_prob[0];
                const trafficLightImg = document.getElementById("trafficLightImg");

                // Bildpfad festlegen je nach Wahrscheinlichkeit
                let imgFullPath = "";

                if (interventionProb > 0.6) {
                    imgFullPath = STATIC_PATHS.red;
                } else if (interventionProb > 0.4) {
                    imgFullPath = STATIC_PATHS.yellow;
                } else {
                    imgFullPath = STATIC_PATHS.green;
                }

                trafficLightImg.src = imgFullPath;
            }

            // Automatisches Scrollen zum neuesten Beitrag
            chatBox.scrollTop = chatBox.scrollHeight;
        });

        document.getElementById("jsonUploadForm").addEventListener("submit", async function(event) {
            event.preventDefault(); // Standardformularverhalten verhindern

            const formData = new FormData();
            const jsonFile = document.getElementById("jsonFile").files[0];

            if (!jsonFile) {
                alert("Bitte eine JSON-Datei auswählen.");
                return;
            }

            formData.append("jsonFile", jsonFile);

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch("/upload_json/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken // CSRF-Token für Sicherheit
                    },
                    body: formData
                });

                const result = await response.json();
                document.getElementById("uploadMessage").innerText = result.message;
            } catch (error) {
                console.error("Fehler beim Hochladen:", error);
                document.getElementById("uploadMessage").innerText = "Fehler beim Hochladen!";
            }
        });
        document.getElementById("reloadButton").addEventListener("click", () => {
            location.reload();
        });