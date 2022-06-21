# Huizenzoeker / website change detector
Starts a python script four times that looks at housing websites in NL and sends a telegram notification if they change hash. False positives may happen.
Could be used for more than just the housing market.

## telegram_send
needs to be installed, and configured as root.
To configure as root, do sudo so and THEN telegram-send --configure.

## systemd
systemd service needs to be in /etc/systemd/system and needs to be 'installed' like normally like https://roboticsbackend.com/make-a-raspberry-pi-3-program-start-on-boot/