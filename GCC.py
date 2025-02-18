import os
import subprocess

# -------------------------------
# Configuration Variables
# -------------------------------

# Root directory of your project source files.
project_dir = r"D:\stm32\myproject\Gyro_read"

# Directories to exclude from scanning.
EXCLUDE_DIRS = [
    r"D:\stm32\myproject\Gyro_read\Drivers\CMSIS\Core\Template",
    r"D:\stm32\myproject\Gyro_read\Drivers\CMSIS\DSP\DSP_Lib_TestSuite\Common\platform",
    r"D:\stm32\myproject\Gyro_read\Drivers\CMSIS\NN",
    r"D:\stm32\myproject\Gyro_read\Drivers\CMSIS\Core_A",
    r"D:\stm32\myproject\Gyro_read\Drivers\CMSIS\DSP",
    r"D:\stm32\myproject\Gyro_read\Drivers\CMSIS\RTOS2",
    r"D:\stm32\myproject\Gyro_read\Drivers\mpu_driver",
    r"D:\stm32\myproject\Gyro_read\Drivers\storage",
    r"D:\stm32\myproject\Gyro_read\EWARM",
    r"D:\stm32\myproject\Gyro_read\Drivers\CMSIS\Device\ST\STM32F1xx\Source\Templates\arm",
    r"D:\stm32\myproject\Gyro_read\Drivers\CMSIS\Device\ST\STM32F1xx\Source\Templates\iar",
    r"D:\stm32\myproject\Gyro_read\MDK-ARM",
]

# Files to exclude from scanning (by filename substring).
EXCLUDE_FILES = [
    "_template.c",      # Skip any file containing _template.c
    "armlib_lock_glue.c",
    "cc932.c",
    "cc936.c",
    "cc949.c",
    "cc950.c",
    "ccsbcs.c",         # Exclude this to avoid duplicate definitions with unicode.c
    "startup_stm32f100xe.s",
    "startup_stm32f107xc.s",
    "startup_stm32f100xb.s",
    "startup_stm32f101x6.s",
    "startup_stm32f103xg.s",
    #"startup_stm32f103xb.s", # redundant, but doesn't hurt
    "startup_stm32f103x6.s", # redundant, but doesn't hurt
    "startup_stm32f101xg.s",
    "startup_stm32f102x6.s",
    "startup_stm32f101xb.s",
    "startup_stm32f101x6.s", # redundant, but doesn't hurt
    "startup_stm32f103xg.s", # redundant, but doesn't hurt
    "startup_stm32f103xe.s",
    "startup_stm32f102xb.s",
    "startup_stm32f107xc.s", # redundant, but doesn't hurt
    "startup_stm32f105xc.s",
    "startup_stm32f101xg.s", # redundant, but doesn't hurt
    "startup_stm32f101xe.s",
    #"startup_stm32f103xb.s", # redundant, but doesn't hurt
    "startup_stm32f103x6.s", # redundant, but doesn't hurt
]

# Base directories for external/system headers.
SYSTEM_DIRS = [
    r"C:/Users/tranj/AppData/Local/Arm/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include",
    r"C:/Users/tranj/AppData/Local/Arm/Packs/Keil/STM32F1xx_DFP/2.4.1/Device/Include",
    r"C:/Users/tranj/AppData/Local/Arm/Packs/ARM",
]

# User include directories (if needed).
USER_DIRS = [
    # e.g., r"C:/path/to/your/include",
]

# Target device macro.
TARGET_DEVICE = "STM32F103xB"

# CPU flags for Cortex-M3 devices (with size optimization).
CPU_FLAGS = ["-mcpu=cortex-m3", "-mthumb", "-Os"]

# Linker script path (adjust if needed).
LINKER_SCRIPT = r"D:\stm32\myproject\Gyro_read\linker scripts\stm32f103c8tx_flash.ld"

# -------------------------------
# Utility Functions
# -------------------------------

def find_files(directory, extension, exclude_dirs=None, exclude_files=None):
    """
    Recursively find files with the given extension in the specified directory,
    skipping directories and files that are in the exclusion lists.
    Returns a list of unique file paths.
    """
    matches = set()
    for root, _, files in os.walk(directory):
        if exclude_dirs and any(ex_dir in root for ex_dir in exclude_dirs):
            continue
        for file in files:
            if not file.endswith(extension):
                continue
            if exclude_files and any(ex in file for ex in exclude_files):
                continue
            matches.add(os.path.join(root, file))
    return list(matches)

def find_include_dirs(file_list):
    """Return a unique list of directories extracted from a list of files."""
    return list({os.path.dirname(file) for file in file_list})

def get_system_include_dirs(base_dirs):
    """
    Recursively search each base directory for header files (.h) and return
    a unique list of directories that contain them.
    """
    all_headers = []
    for base in base_dirs:
        if os.path.isdir(base):
            all_headers.extend(find_files(base, ".h"))
    return find_include_dirs(all_headers)

# -------------------------------
# Build Functions
# -------------------------------

def compile_source_files(source_files, project_include_dirs, output_dir, asm_files):
    """
    Compile each C and assembly source file into an object file.
    Returns a list of object file paths.
    """
    object_files = []

    # Gather include directories.
    system_includes = get_system_include_dirs(SYSTEM_DIRS)
    user_includes = get_system_include_dirs(USER_DIRS)

    # Compile C files.
    for source_file in source_files:
        base_name = os.path.basename(source_file)
        object_file = os.path.join(output_dir, base_name.replace('.c', '.o'))
        cmd = [
            "arm-none-eabi-gcc",
            *CPU_FLAGS,
            "-c",
            source_file,
            "-o",
            object_file,
            f"-D{TARGET_DEVICE}"
        ]
        for inc in project_include_dirs:
            cmd.append("-I" + inc)
        for inc in system_includes:
            if inc.strip():
                cmd.append("-I" + inc)
        for inc in user_includes:
            if inc.strip():
                cmd.append("-I" + inc)
        print(f"Compiling C: {source_file}")
        subprocess.run(cmd, check=True)
        object_files.append(object_file)

    # Compile assembly files.
    for asm_file in asm_files:
        base_name = os.path.basename(asm_file)
        object_file = os.path.join(output_dir, base_name.replace('.s', '.o'))
        asm_cmd = [
            "arm-none-eabi-as",
            asm_file,
            "-o", object_file
        ]
        for inc in project_include_dirs:
            asm_cmd.append("-I" + inc)
        print(f"Compiling ASM: {asm_file}")
        subprocess.run(asm_cmd, check=True)
        object_files.append(object_file)

    return object_files

def link_object_files(object_files, output_elf):
    """
    Link object files into an ELF executable using nosys specs and garbage collection.
    Deduplicates object files before linking.
    """
    unique_objects = list(dict.fromkeys(object_files))
    cmd = [
        "arm-none-eabi-gcc",
        *CPU_FLAGS,
        "-T", LINKER_SCRIPT,
        "-specs=nosys.specs",    # Provide stub syscall implementations.
        "-Wl,--gc-sections",
        "-o", output_elf
    ] + unique_objects
    print(f"Linking to create: {output_elf}")
    subprocess.run(cmd, check=True)

def convert_elf_to_hex(output_elf, output_hex):
    """
    Convert the ELF file to a HEX file.
    """
    cmd = ["arm-none-eabi-objcopy", "-O", "ihex", output_elf, output_hex]
    print(f"Converting ELF to HEX: {output_hex}")
    subprocess.run(cmd, check=True)

# -------------------------------
# Main Build Flow
# -------------------------------

def main():
    # Find all C and assembly source files in the project directory,
    # while skipping excluded directories and files.
    source_files = find_files(project_dir, ".c", exclude_dirs=EXCLUDE_DIRS, exclude_files=EXCLUDE_FILES)
    header_files = find_files(project_dir, ".h", exclude_dirs=EXCLUDE_DIRS, exclude_files=EXCLUDE_FILES)
    asm_files = find_files(project_dir, ".s", exclude_dirs=EXCLUDE_DIRS, exclude_files=EXCLUDE_FILES)

    # Determine project-specific include directories from header files.
    project_include_dirs = find_include_dirs(header_files)

    # Specify the output directory for compiled object files.
    output_dir = r"D:\stm32\myproject\Gyro_read\Core\Src\dum_folder"
    os.makedirs(output_dir, exist_ok=True)

    # Compile source files.
    object_files = compile_source_files(source_files, project_include_dirs, output_dir, asm_files)

    # Link object files into an ELF executable.
    output_elf = os.path.join(output_dir, "main.elf")
    link_object_files(object_files, output_elf)

    # Convert the ELF file to a HEX file.
    output_hex = os.path.join(output_dir, "main.hex")
    convert_elf_to_hex(output_elf, output_hex)

    print(f"Compilation and linking complete. HEX file generated: {output_hex}")

if __name__ == "__main__":
    main()
