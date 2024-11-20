# k3-am67a-beaglemod-audio.dts

## Context

I have a BeagleY-AI board and I am attempting to interface an audio device using the TLV320AIC3104 codec over I2C. Because the BeagleY-AI does not have a master clock, I am using a [12 MHz crystal oscillator from Abracon](https://abracon.com/Oscillators/ACHL.pdf).

## Issue

The audio device is being connected to the BeagleY-AI via I2C (on address 18):
```bash
beagle@beagleyai:~$ i2cdetect -y -r 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- 18 -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- 54 -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --
```

But the audio device itself does not show up (this is when the overlay is loaded):
```bash
beagle@beagleyai:~$ aplay -l
aplay: device_list:274: no soundcards found...
```

This is the output of the same command, without loading the overlay:
```bash
beagle@beagleyai:~$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: HDMI [it66122 HDMI], device 0: davinci-mcasp.0-i2s-hifi i2s-hifi-0 [davinci-mcasp.0-i2s-hifi i2s-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

## Things already tried

### Compiling with invalid nodes or syntax

The compilation just failed.

### Using the [this overlay for AM625](https://openbeagle.org/beagleboard/BeagleBoard-DeviceTrees/-/blob/ad0bebd8aa292200189974677a227bf306c8b61a/src/arm64/overlays/k3-am625-beaglemod-audio.dts)

This did not work as the chip on the BeagleY-AI is the AM-67A.

### Including all header files mentioned [here](https://github.com/torvalds/linux/blob/master/arch/arm64/boot/dts/ti/k3-am67a-beagley-ai.dts) for the AM67A

This largely did not work and only caused more problems with compilation steps. It was quite troublesome and slow and I did not finish resolving all of the problems going down this route such as compilation failures due to a header file not being available, syntax not being correct out of the box, and other errors.

### Wire the hardware incorrectly

This only affects the output of `i2cdetect -y -r 1` where the I2C device on address 18 is no longer in the output.

### Some outputs

Loaded overlays:
```bash
beagle@beagleyai:~$ cat /boot/firmware/extlinux/extlinux.conf
menu title BeagleY-AI microSD (extlinux.conf) (swap enabled)

timeout 50

default microSD (default)

label microSD (production test)
    kernel /Image
    append console=ttyS2,115200n8 root=/dev/mmcblk1p3 ro rootfstype=ext4 rootwait net.ifnames=0 quiet
    fdtdir /
    fdt /ti/k3-am67a-beagley-ai.dtb
    fdtoverlays /overlays/k3-am67a-beagley-ai-hdmi-dss0-dpi1.dtbo /overlays/k3-am67a-beagley-ai-lincolntech-185lcd-panel.dtbo /overlays/k3-am67a-beagley-ai-csi0-imx219.dtbo /overlays/k3-am67a-beagley-ai-csi1-imx219.dtbo
    #initrd /initrd.img

label transfer microSD rootfs to NVMe (advanced)
    kernel /Image
    append console=ttyS2,115200n8 root=/dev/mmcblk1p3 ro rootfstype=ext4 rootwait net.ifnames=0 init=/usr/sbin/init-beagle-flasher-mv-rootfs-to-nvme
    fdtdir /
    fdt /ti/k3-am67a-beagley-ai.dtb
    initrd /initrd.img

label microSD (debug)
    kernel /Image
    append console=ttyS2,115200n8 earlycon=ns16550a,mmio32,0x02800000 root=/dev/mmcblk1p3 ro rootfstype=ext4 rootwait net.ifnames=0
    fdtdir /
    fdt /ti/k3-am67a-beagley-ai.dtb
    #initrd /initrd.img

label microSD (default)
    kernel /Image
    append console=ttyS2,115200n8 root=/dev/mmcblk1p3 ro rootfstype=ext4 resume=/dev/mmcblk1p2 rootwait net.ifnames=0 quiet
    fdtdir /
    fdt /ti/k3-am67a-beagley-ai.dtb
    #fdtoverlays /overlays/<file>.dtbo
    #fdtoverlays /overlays/k3-am67a-beagley-ai-i2c-arm.dtbo
    #fdtoverlays /overlays/k3-am67a-beagley-ai-spidev0.dtbo
    #fdtoverlays /overlays/k3-am67a-beagley-ai-spi0-1cs.dtbo
    #fdtoverlays /overlays/k3-am67a-beagley-ai-spi0-2cs.dtbo
    #fdtoverlays /overlays/BB-BONE-AUDI-02-00A0.dtbo
    fdtoverlays /overlays/k3-am67a-beaglemod-audio.dtbo
    #initrd /initrd.img
```

Kernel logs during boot:
```bash
beagle@beagleyai:~$ dmesg | grep -i 'tlv320aic3104\|mcasp\|sound'
[   17.599452] Modules linked in: algif_aead cc33xx mac80211 libarc4 cfg80211 cc33xx_sdio rpmsg_ctrl rpmsg_char wave5 virtio_rpmsg_bus rpmsg_ns e5010_jpeg_enc pvrsrvkm(O) crct10dif_ce snd_soc_davinci_mcasp videobuf2_dma_contig snd_soc_ti_udma snd_soc_simple_card at24 cpufreq_dt v4l2_mem2mem snd_soc_simple_card_utils snd_soc_ti_edma snd_soc_hdmi_codec videobuf2_memops pwm_fan snd_soc_ti_sdma rti_wdt videobuf2_v4l2 videobuf2_common snd_soc_core videodev btti_uart snd_pcm_dmaengine mc snd_pcm bluetooth ti_k3_r5_remoteproc ti_k3_dsp_remoteproc snd_timer ti_k3_common snd uio_pdrv_genirq uio dm_mod loop efi_pstore
[   17.600739] Modules linked in: algif_aead cc33xx mac80211 libarc4 cfg80211 cc33xx_sdio rpmsg_ctrl rpmsg_char wave5 virtio_rpmsg_bus rpmsg_ns e5010_jpeg_enc pvrsrvkm(O) crct10dif_ce snd_soc_davinci_mcasp videobuf2_dma_contig snd_soc_ti_udma snd_soc_simple_card at24 cpufreq_dt v4l2_mem2mem snd_soc_simple_card_utils snd_soc_ti_edma snd_soc_hdmi_codec videobuf2_memops pwm_fan snd_soc_ti_sdma rti_wdt videobuf2_v4l2 videobuf2_common snd_soc_core videodev btti_uart snd_pcm_dmaengine mc snd_pcm bluetooth ti_k3_r5_remoteproc ti_k3_dsp_remoteproc snd_timer ti_k3_common snd uio_pdrv_genirq uio dm_mod loop efi_pstore
[   22.495234] platform sound: deferred probe pending
```

Kernel modules loaded:
```bash
beagle@beagleyai:~$ lsmod
Module                  Size  Used by
xt_conntrack           16384  1
nft_chain_nat          16384  3
xt_MASQUERADE          20480  1
nf_nat                 40960  2 nft_chain_nat,xt_MASQUERADE
nf_conntrack_netlink    49152  0
nf_conntrack          139264  4 xt_conntrack,nf_nat,nf_conntrack_netlink,xt_MASQUERADE
nf_defrag_ipv6         24576  1 nf_conntrack
nf_defrag_ipv4         16384  1 nf_conntrack
xfrm_user              45056  1
xfrm_algo              16384  1 xfrm_user
xt_addrtype            16384  2
nft_compat             20480  4
nf_tables             221184  57 nft_compat,nft_chain_nat
nfnetlink              20480  4 nft_compat,nf_conntrack_netlink,nf_tables
br_netfilter           32768  0
bridge                249856  1 br_netfilter
stp                    16384  1 bridge
llc                    16384  2 bridge,stp
snd_seq_dummy          16384  0
snd_hrtimer            16384  1
snd_seq                77824  7 snd_seq_dummy
snd_seq_device         16384  1 snd_seq
algif_aead             16384  0
cc33xx                307200  0
mac80211              851968  1 cc33xx
libarc4                16384  1 mac80211
cfg80211              794624  2 mac80211,cc33xx
cc33xx_sdio            20480  0
rpmsg_ctrl             16384  0
rpmsg_char             16384  1 rpmsg_ctrl
wave5                 114688  0
virtio_rpmsg_bus       24576  0
rpmsg_ns               20480  1 virtio_rpmsg_bus
e5010_jpeg_enc         36864  0
pvrsrvkm             1310720  0
crct10dif_ce           16384  1
snd_soc_davinci_mcasp    40960  0
videobuf2_dma_contig    24576  2 e5010_jpeg_enc,wave5
snd_soc_ti_udma        16384  1 snd_soc_davinci_mcasp
snd_soc_simple_card    24576  0
at24                   24576  0
cpufreq_dt             20480  0
v4l2_mem2mem           28672  2 e5010_jpeg_enc,wave5
snd_soc_simple_card_utils    28672  1 snd_soc_simple_card
snd_soc_ti_edma        16384  1 snd_soc_davinci_mcasp
snd_soc_hdmi_codec     24576  0
videobuf2_memops       20480  1 videobuf2_dma_contig
pwm_fan                24576  0
snd_soc_ti_sdma        16384  1 snd_soc_davinci_mcasp
rti_wdt                16384  0
videobuf2_v4l2         24576  3 v4l2_mem2mem,e5010_jpeg_enc,wave5
videobuf2_common       53248  6 videobuf2_dma_contig,videobuf2_v4l2,v4l2_mem2mem,e5010_jpeg_enc,wave5,videobuf2_memops
snd_soc_core          217088  7 snd_soc_davinci_mcasp,snd_soc_ti_sdma,snd_soc_ti_edma,snd_soc_hdmi_codec,snd_soc_ti_udma,snd_soc_simple_card_utils,snd_soc_simple_card
videodev              237568  5 videobuf2_v4l2,videobuf2_common,v4l2_mem2mem,e5010_jpeg_enc,wave5
btti_uart              24576  0
snd_pcm_dmaengine      16384  1 snd_soc_core
mc                     57344  4 videodev,videobuf2_v4l2,videobuf2_common,v4l2_mem2mem
snd_pcm               114688  5 snd_soc_davinci_mcasp,snd_soc_hdmi_codec,snd_soc_simple_card_utils,snd_soc_core,snd_pcm_dmaengine
bluetooth             749568  1 btti_uart
ti_k3_r5_remoteproc    36864  0
ti_k3_dsp_remoteproc    20480  0
snd_timer              36864  3 snd_seq,snd_hrtimer,snd_pcm
ti_k3_common           20480  1 ti_k3_dsp_remoteproc
snd                    94208  8 snd_seq,snd_seq_device,snd_soc_hdmi_codec,snd_timer,snd_soc_core,snd_pcm
uio_pdrv_genirq        20480  0
uio                    20480  1 uio_pdrv_genirq
dm_mod                139264  0
loop                   32768  0
efi_pstore             16384  0
```

## Useful links

- https://github.com/torvalds/linux/blob/master/arch/arm64/boot/dts/ti/k3-am67a-beagley-ai.dts
- https://www.kernel.org/doc/Documentation/devicetree/bindings/sound/tlv320aic3x.txt
- https://github.com/beagleboard/bb.org-overlays/blob/master/src/arm/PB-I2C1-TLV320AIC3104.dts
- https://openbeagle.org/beagleboard/BeagleBoard-DeviceTrees/-/blob/ad0bebd8aa292200189974677a227bf306c8b61a/src/arm64/overlays/k3-am625-beaglemod-audio.dts

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
