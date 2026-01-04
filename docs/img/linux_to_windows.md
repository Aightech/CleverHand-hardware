# hc32l110 template from Linux to Windows
## Prerequistes 
* DAPLink
* Communication module with hc332l110 microcontroller
* Makefile and rules.mk from [hc32l110 template](https://github.com/IOsetting/hc32l110-template)


### 1. Install GNU Arm Embedded Toolchain
First, download the toolchain from Arm GNU Toolchain Downloads. Select the suitable Arm GNU Toolchain for your host (mingw-w64-i686 for Windows 10 or later) and toolchain target. For windows users and bare-metal targets, download *arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi.zip*. Zip file was selected based on personal preference as the path to the file is easier to locate. Use a third-party software to extract the files in the zip file. This is because extracting with the in-built windows “extract all” function returned error 0x80010135, which mainly happens due to exceeding Windows' 260-character limit. [7-zip](https://www.7-zip.org/) for windows x64 was downloaded and used. The path to the extracted file is then input into the makefile.

### 2. Install PyOCD
To install PyOCD, one must make sure that the latest version of pip is installed in the computer. Also, make sure that pip is added to the PATH system variable. This can be done by editing the environmental variable in the control panel. Use pip to install PyOCD by running:

`py -m pip install pyocd`

and verify the installation by running:

`pyocd --version`

in the command prompt.

### 3. Install MAKE
Download the latest version of Make for Windows on [GNUWin 32](https://gnuwin32.sourceforge.net/packages/make.htm). It includes a complete package, except sources. Add the bin directory of the downloaded file to the PATH system variable and verify installation by running:

`Make --version`


### 4. Clone the repository  
The repository from [hc32l110 template](https://github.com/IOsetting/hc32l110-template) was cloned to a local workspace on VSCode. 


## Amendments to the makefile
### 1. ARM_TOOLCHAIN
Changed the path to ARM_TOOLCHAIN. Note that for windows, backslash \ is used instead of slash /. For example, the path to ARM_TOOLCHAIN would look something like:

`C:\\Users\\<name_of_user>\\<location_of_file>\\arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi\\arm-gnu-toolchain-13.2.Rel1-mingw-w64-i686-arm-none-eabi\\bin`

It should be pointed to the bin directory of the file. 

### 2. FLASH_PROGRM
PyOCD was selected as DAPLink was used. Therefore:

`FLASH_PROGRM    ?= pyocd`

### 3. /
All the slashes / are changed to backslashes \ so that it is compatible with Windows syntax.

## Amendments to rules.mk
### 1. CSOURCE and CFILES
The original rules.mk from the repository uses the Linux FIND command to locate the c sources files in the library and to add them to CSOURCES. However, the FIND command does not exist for Windows. CFILES were therefore added manually as follows:

```
CFILES := Libraries\\CMSIS\\HC32L110\\source\\system_hc32l110.c
CFILES += User\\main.c # Adding individual c source files
```
All subfiles in the *HC32L110_Driver* in the *Libraries* file were added manually. Besides, a CSOURCES variable was defined using the ‘wildcard’ function for windows to locate the c source files. However, this did not workout perfectly well. Therefore, one extra line of code was written for the definition of CSOURCES:
```
CSOURCES := $(foreach dir, $(CDIRS), $(wildcard $(TOP)\\$(dir)\\*.c))
CSOURCES += $(addprefix $(TOP)\\, $(CFILES))
```
Overall, a list of c source files is compiled.

### 2.	Compiling 
This is the original code:
```make
# Compile c to obj -- should be `$(BDIR)/%.o: $(TOP)/%.c`, but since $(TOP) is base folder so non-path also works
$(BDIR)/%.o: $(TOP)/%.c
    @printf "  CC\t$<\n"
    @mkdir -p $(dir $@)
    $(Q)$(CC) $(TGT_CFLAGS) $(TGT_INCFLAGS) -MT $@ -o $@ -c $< -MD -MF $(BDIR)/$*.d -MP

# Compile asm to obj
$(BDIR)/%.o: $(TOP)/%.s
    @printf "  AS\t$<\n"
    @mkdir -p $(dir $@)
    $(Q)$(CC) $(TGT_ASFLAGS) -o $@ -c $<

# Link object files to elf
$(BDIR)/$(PROJECT).elf: $(OBJS) $(TOP)/$(LDSCRIPT)
    @printf "  LD\t$(LDSCRIPT) -> $@\n"
    $(Q)$(CC) $(TGT_LDFLAGS) -T$(TOP)/$(LDSCRIPT) $(OBJS) -o $@

# Convert elf to bin
%.bin: %.elf
    @printf "  OBJCP BIN\t$@\n"
    $(Q)$(OBJCOPY) -I elf32-littlearm -O binary  $< $@

# Convert elf to hex
%.hex: %.elf
    @printf "  OBJCP HEX\t$@\n"
    $(Q)$(OBJCOPY) -I elf32-littlearm -O ihex  $< $@
```

The ‘printf’ command is not readily available on Windows. Similarly, the ‘mkdir -p’ command that exists for Linux but not Windows. This section of the code set the rules for compiling the c source files and assembly files into object files, links the object files into an ELF executable, and to binary and hex formats. For example, the first 5 lines compiles c source files to object files, and creates a new directory using ‘mkdir -p’ if the directory does not initially exists. To do this in Windows, ‘printf’ commands were replaced with ‘echo’, and ‘mkdir -p’ were replaced with ‘if not exist’. Here is the amended version:
```make
# Compile C to obj
$(BDIR)\\%.o: $(TOP)\\%.c
    @echo "  CC  $<"
    @if not exist $(dir $@) mkdir $(dir $@)
    $(Q)$(CC) $(TGT_CFLAGS) $(TGT_INCFLAGS) -MT $@ -o $@ -c $< -MD -MF $(BDIR)\\$*.d -MP

# Compile ASM to obj
$(BDIR)\\%.o: $(TOP)\\%.s
    @echo "  AS  $<"
    @if not exist $(dir $@) mkdir $(dir $@)
    $(Q)$(CC) $(TGT_ASFLAGS) -o $@ -c $<

# Link object files to ELF
$(BDIR)\\$(PROJECT).elf: $(OBJS) $(TOP)\\$(LDSCRIPT)
    @echo "  LD  $(LDSCRIPT) -> $@"
    $(Q)$(CC) $(TGT_LDFLAGS) -T$(TOP)\\$(LDSCRIPT) $(OBJS) -o $@

# Convert ELF to BIN
%.bin: %.elf
    @echo "  OBJCP BIN $@"
    $(Q)$(OBJCOPY) -I elf32-littlearm -O binary $< $@

# Convert ELF to HEX
%.hex: %.elf
    @echo "  OBJCP HEX $@"
    $(Q)$(OBJCOPY) -I elf32-littlearm -O ihex $< $@
```

### 3. /
All the slashes / are changed to backslashes \ so that it is compatible with Windows syntax.

## Compiling and uploading the code
When make clean and make are run in the terminal, the following output was given:
```
C:\Users\<name_of_user>\<location_of_file>\hc32l110_clvhd(2)\hc32l110_clvhd(2)>make clean

if exist .\\Build rd /s /q .\\Build

C:\Users\<name_of_user>\<location_of_file>\hc32l110_clvhd(2)\hc32l110_clvhd(2)>make

"  CC  .\\\Libraries\\CMSIS\\HC32L110\\source\\system_hc32l110.c"
"  CC  .\\\User\\main.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\adc.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\adt.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\base_timer.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\clk.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\crc.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\ddl.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\flash.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\gpio.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\i2c.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\interrupts_hc32l110.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\lpm.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\lpt.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\lpuart.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\lvd.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\pca.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\reset.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\rgb.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\rtc.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\spi.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\trim.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\uart.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\vc.c"
"  CC  .\\\Libraries\\HC32L110_Driver\\src\\wdt.c"
"  AS  .\\\Libraries\\CMSIS\\HC32L110\\source\\startup_hc32l110.s"
"  LD  Libraries\\LDScripts\\hc32l110x4.ld -> .\\Build\\app.elf"
C:/Users/Byron Chan/Documents/trial/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi/arm-gnu-toolchain-13.2.Rel1-mingw-w64-i686-arm-none-eabi/bin/../lib/gcc/arm-none-eabi/13.2.1/../../../../arm-none-eabi/bin/ld.exe: C:/Users/Byron Chan/Documents/trial/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi/arm-gnu-toolchain-13.2.Rel1-mingw-w64-i686-arm-none-eabi/bin/../lib/gcc/arm-none-eabi/13.2.1/thumb/v6-m/nofp\libc_nano.a(libc_a-closer.o): in function `_close_r':
closer.c:(.text._close_r+0xc): warning: _close is not implemented and will always fail
C:/Users/Byron Chan/Documents/trial/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi/arm-gnu-toolchain-13.2.Rel1-mingw-w64-i686-arm-none-eabi/bin/../lib/gcc/arm-none-eabi/13.2.1/../../../../arm-none-eabi/bin/ld.exe: C:/Users/Byron Chan/Documents/trial/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi/arm-gnu-toolchain-13.2.Rel1-mingw-w64-i686-arm-none-eabi/bin/../lib/gcc/arm-none-eabi/13.2.1/thumb/v6-m/nofp\libc_nano.a(libc_a-lseekr.o): in function `_lseek_r':
lseekr.c:(.text._lseek_r+0x10): warning: _lseek is not implemented and will always fail
C:/Users/Byron Chan/Documents/trial/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi/arm-gnu-toolchain-13.2.Rel1-mingw-w64-i686-arm-none-eabi/bin/../lib/gcc/arm-none-eabi/13.2.1/../../../../arm-none-eabi/bin/ld.exe: C:/Users/Byron Chan/Documents/trial/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi/arm-gnu-toolchain-13.2.Rel1-mingw-w64-i686-arm-none-eabi/bin/../lib/gcc/arm-none-eabi/13.2.1/thumb/v6-m/nofp\libc_nano.a(libc_a-readr.o): in function `_read_r':
readr.c:(.text._read_r+0x10): warning: _read is not implemented and will always fail
C:/Users/Byron Chan/Documents/trial/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi/arm-gnu-toolchain-13.2.Rel1-mingw-w64-i686-arm-none-eabi/bin/../lib/gcc/arm-none-eabi/13.2.1/../../../../arm-none-eabi/bin/ld.exe: C:/Users/Byron Chan/Documents/trial/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi/arm-gnu-toolchain-13.2.Rel1-mingw-w64-i686-arm-none-eabi/bin/../lib/gcc/arm-none-eabi/13.2.1/thumb/v6-m/nofp\libc_nano.a(libc_a-writer.o): in function `_write_r':
writer.c:(.text._write_r+0x10): warning: _write is not implemented and will always fail
C:/Users/Byron Chan/Documents/trial/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi/arm-gnu-toolchain-13.2.Rel1-mingw-w64-i686-arm-none-eabi/bin/../lib/gcc/arm-none-eabi/13.2.1/../../../../arm-none-eabi/bin/ld.exe: warning: .\\Build\\app.elf has a LOAD segment with RWX permissions
Memory region         Used Size  Region Size  %age Used
             RAM:        1112 B         2 KB     54.30%
           FLASH:        8576 B        16 KB     52.34%
"  OBJCP BIN .\\Build\\app.bin"
"  OBJCP HEX .\\Build\\app.hex"
"Build successful! Output files are in .\\Build"
```
When make flash is run, the following output was given:
```
C:\Users\<name_of_user>\<location_of_file>\hc32l110_clvhd(2)\hc32l110_clvhd(2)>make flash
"Flashing with pyocd"
"Else if is else if-ing"
pyocd erase -c -t hc32l110c4ua --config ".\\Misc\\pyocd.yaml"
0000921 W STLink, CMSIS-DAPv2 and PicoProbe probes are not supported because no libusb library was found. [common]
0001087 I Erasing chip...[eraser]
0001400 I Chip erase complete [eraser]
pyocd load. \\Build\\app.hex -t hc32l110 --config ".\\Misc\\pyocd.yaml"
0000882 W STLink, CMSIS-DAPv2 and PicoProbe probbes are not supported because no libusb library was found. [common]
0001052 I Loading C:\Users\<name_of_user>\<location_of_file>\hc32l110_clvhd\Build\app.hex [load_cmd]
[==================================================] 100%
0003217 I Erased 3584 bytes (7 sectors), programmed 3584 bytes (7 pages), skipped 0 bytes (0 pages) at 1.62 kB/s [loader]
```