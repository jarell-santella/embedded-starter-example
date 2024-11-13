# k3-am67a-beaglemod-audio.dts

## Usage

Preprocess:
```bash
cpp -nostdinc -I ~/Development/audio-devicetree -undef -x assembler-with-cpp k3-am67a-beaglemod-audio.dts -o k3-am67a-beaglemod-audio.pp.dts
```

Compile:
```bash
dtc -@ -I dts -O dtb -o k3-am67a-beaglemod-audio.dtbo k3-am67a-beaglemod-audio.pp.dts
```

Copy:
```bash
cp k3-am67a-beaglemod-audio.dtbo /boot/firmware/overlays/k3-am67a-beaglemod-audio.dtbo
```
