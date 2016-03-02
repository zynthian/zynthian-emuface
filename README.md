# Zynthian Emuface

This repository contains a Zynthian Box Emulator that eases development and testing. 
It allows to run the Zynthian User Interface and Synth Engines in a Desktop or Laptop Computer.

![Image of Zynthian Box Emulator](https://raw.githubusercontent.com/zynthian/zynthian-emuface/master/img/zynthian_emuface_control_screenshot.png)

### Requirements:

 * ZynAddSubFX (last version: 5.3)
 * FluidSynth
 * LinuxSampler (1.0)
 * setBfree
 * Carla
 
Perhaps you have to adjust the binary paths in the engine classes (zynthian-ui/zyngine/...)

### Install procedure:

```
mkdir zynthian
cd zynthian
git clone https://github.com/zynthian/zyncoder.git
git clone https://github.com/zynthian/zynthian-ui.git
git clone https://github.com/zynthian/zynthian-data.git
git clone https://github.com/zynthian/zynthian-emuface.git
echo 'PROTOTYPE-EMU' > zynthian_hw_version.txt
```
You have to put your samples in "zynthian-data/soundfonts", organized by type, in three subdirectories:

```
cd zynthian-data/soundfonts
mkdir gig
mkdir sfz
mkdir sf2
```
 
Also, you have to create a symlink to your ZynAddSubFX bank directory:

```
cd zynthian-data
ln -s your/zasfx/bankdir/path zynbanks
```

### Execution:
```
cd zynthian-emuface
./zynthian_emuface.py
```

You can set the environment variable "ZYNTHIANX":

```
export ZYNTHIANX=$DISPLAY
```

And zynthian UI will open the native GUI for every engine.


Read [this blog entry] (http://blog.zynthian.org/index.php/2016/02/27/zynthian-emulator) about the Zynthian Emulator.

You can learn more about the Zynthian Project reading [the blog] (http://blog.zynthian.org) or visiting [the website] (http://zynthian.org).
