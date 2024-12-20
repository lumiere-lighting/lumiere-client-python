# Lumiere Client (Python)

## Install

- [Install `uv`](https://docs.astral.sh/uv/getting-started/installation/)
  - To install for all users on Raspberry Pi, a way to do it is: `curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sudo sh`
- Need Python dev,
  - `sudo apt-get install python3-dev`
- (optional) Install Python dependencies: `uv pip install -r pyproject.toml`
  - Note that `sudo` is used since the script will need to run as root. ??

## Configure

Configuration is managed through environment variables. These can be managed in a `.env` file if desired.

- `API_DOMAIN`: The location of the Lumiere API, should be something like this (no trailing slash): `https://api.lumiere.lighting`
- `PIXEL_LENGTH`: Number of LEDs that the client is connected to.
- `DMA_CHANNEL`: Defaults to `10`
- `GPIO_CHANNEL`: Defaults to `18`
- `BRIGHTNESS`: Brightness of LEDs (`0`-`255`); defaults to `255`.
- `STRIP_TYPE`: LED light configuration. Can be `rgb`, `grb`, etc; defaults to `rgb`.
- `MAX_SPREAD`: When displaying pixels, the spread is the amount of repeating of a color. Should be 1 or great; defaults to `5`.
- `LOG_LEVEL`: Sets the [minimum log level](https://docs.python.org/3/library/logging.html#levels); defaults to warning.
- `FRAME_RATE`: The frame rate for animations, might help with light rendering issues; defaults to 30.
- `GAMMA_CORRECTION`: [Gamma correction](https://learn.adafruit.com/led-tricks-gamma-correction) constant; set to 0 to turn off; defaults to 2.3.

## Usage

Run with `uv run lumiere-client/client.py`

Note that `sudo` is necessary to be able to access the GPIO pins. ??

## Deplopyment

### Raspberry Pi

Initial configuartion of the Raspberry Pi.

- `raspi-config`
  - Enable SSH
  - Unsure how to exactly make sure that the PWM pins are actually accessible? Enable SPI? Enable I2C?
  - Configure timezone
  - Make sure network is available on boot
  - Make sure it can connect to the internet.

Install the startup/service script.

- Copy the `init.d` script with something like:
  - `sudo cp ./deploy/lumiere-client.init.d /etc/init.d/lumiere-client && sudo chmod +x /etc/init.d/lumiere-client`
- Update the script as needed. Mostly this will just be updating the `dir` variable.
- Install to be able to be run on startup.
  - `sudo update-rc.d lumiere-client defaults`
