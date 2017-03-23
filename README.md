# whatsappSelenium

This is a very much WIP whatsapp-bot using selenium to control whatsapp-web.

---
## Setup

Use [this](https://github.com/Mawalu/whatsapp-phishing) to get your whatsapp-web _secrets_ file.


Then run

    git clone https://github.com/jakibaki/whatsappSelenium

to clone this repository.

Put your _secrets_-file in the whatsappSelenium folder and run

    python3 whatsApp.py

to start the bot. (you need chromedriver in your PATH)

You can edit the messageHandler method to do whatever you want.

This was tested on Debian sid and macOS 10.12.4 but there is nothing preventing it from running on Windows with a few changes

## Debian

    sudo apt install git python3-pip python3-selenium xvfb chromium
    sudo pip3 install pyvirtualdisplay 
    