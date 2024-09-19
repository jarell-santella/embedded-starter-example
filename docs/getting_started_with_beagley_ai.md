# Getting started with Beagley-AI

## Prerequisites

1. 15 W (5 V @ 3 A) power supply capable of supplying power via USB-C.
2. 32 GB (minimum) microSD card.
3. Visual Studio Code (VS Code) is installed on the host computer.

## Flashing the Beagley-AI

1. Install the BeagleBoard Imager (bb-imager) for your respective operating system [here](https://beagley-ai.beagleboard.io/bb-imager/).
2. Ensure that your microSD card can be written to.
3. Click "CHOOSE DEVICE".
4. Select the "Beagley-AI" option.
5. Click "CHOOSE OS".
6. Select the "BeagleY-AI Debian v6.1.x XFCE (Recommended)" option.
7. Click "CHOOSE STORAGE".
8. Select your microSD card.
9. Click "NEXT".
10. Click "EDIT SETTINGS".
11. Set all of the settings in the "General" tab appropriately.
12. Click "SERVICES".
13. Click "Enable SSH".
14. Click "Allow public-key authentication only".
15. Click "RUN SSH-KEYGEN".
16. Click "SAVE".
17. Click "YES".
18. Flash the microSD card!
19. Insert the microSD card into the BeagleY-AI.

> [!NOTE]
> When configuring my wireless LAN, I selected "Hidden SSID" even though my SSID is not hidden.

## Connecting to the BeagleY-AI

1. Connect the BeagleY-AI to power via its USB-C port.
2. Wait for the red light to go away. Once the light is flashing green in a heartbeat pattern, proceed.
3. Open a new Terminal.
4. Run `ssh username@hostname` where `username` and `hostname` are the values set for the BeagleY-AI.
5. Type in "yes" and hit enter/return if prompted with "Are you sure you want to continue connecing (yes/no/[fingerprint])?".
6. You are now connected! You can type `echo "Hello world!"` and this will execute on your BeagleY-AI.

## Setting up the development environment

1. Open VS Code.
2. Install the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) VS Code extension by Microsoft.
3. Open the Command Palette (Command + Shift + P) and type in `Remote-SSH: Add New SSH Host...`.
4. Select `Remote-SSH: Add New SSH Host...` and type in `ssh username@hostname` where `username` and `hostname` are the values set for the BeagleY-AI.
5. Open the Command Palette and type in `Remote-SSH: Connect to Host...`.
6. Select the hostname of your BeagleY-AI.
7. You are now connected to your BeagleY-AI via SSH from VS Code on your host computer. You can now create, read, update, and delete any file on the BeagleY-AI from your host computer, and more importantly, transfer files.

# Resources

- https://docs.beagle.cc/latest/boards/beagley/ai/02-quick-start.html
