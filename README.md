# Delab Chatbot

## Vorbereitungen
In delab_chatbot/download/utils.py wird das Package delab-socialmedia importiert.
Dieses lässt sich nicht regulär importieren, daher muss das github repository (https://github.com/juliandehne/delab-socialmedia) gecloned werden
und ein sys Pfad zum directory erstellt werden (nach dem Vorbil in Zeile 8).

Zum Ordner secret/ müssen die Dateien mostodon_secret.yaml und reddit_secret.yaml
hinzugefügt werden, die die Zugangsdaten zu den jeweiligen Bot-Applications enthalten. 
Alternativ könne die Zugangsdataen auch in das Skript download/utils an den 
entsprechenden Stellen eingefügt werden.

## Webseite starten
Um die Webseite zu starten, muss in den Ordner djange_chatbot gewechselt werden und 
der "python3 manage.py runserver" aufgerufen werden.

