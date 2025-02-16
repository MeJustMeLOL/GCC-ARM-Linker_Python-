@Author:MeJustMeLOL
# GCC-ARM-Linker_Python-
This is just an idea when the IDE asks me for $99 to compile code bigger than 120k lines.
Warnning 1 : the module dont have  Debug itself  ,so use it caution .
Warning 2 : i just test on code base created by Stm32Mx , and Keli package . in  Others case is beyone my expectation .
about the project  it base on  2  observable  from  CMD sytax and Linker , here is description  :

The module design following the work flow  : 
1. extract the  file extension from "Main Directory" reference as project_dir in code base 
    source_files = find_files(project_dir, ".c", exclude_dirs=EXCLUDE_DIRS, exclude_files=EXCLUDE_FILES)
    header_files = find_files(project_dir, ".h", exclude_dirs=EXCLUDE_DIRS, exclude_files=EXCLUDE_FILES)
2. callback the  Folder Path 
    # Determine project-specific include directories (from your header files).
    project_include_dirs = find_include_dirs(header_files)
3. User OutPut path  
    # Specify the output directory for compiled object files.
    output_dir = r"....\dum_folder" # your path as output
    os.makedirs(output_dir, exist_ok=True)
4. it  will delivery all information above   as struct {GCC_systax}{opts} {FLAG}{I} {GCC_output FIle type}, then using Os libs as Cmd  prompt  . The FLAG is defined "CPU_FLAGS = ["-mcpu=cortex-m3", "-mthumb","-Os"]" 
    # Compile the source files.
    object_files = compile_source_files(source_files, project_include_dirs, output_dir)
5. Link it ,  just simply as steps 4 using join string and cmd  .
    # Link object files into an ELF executable.
    output_elf = os.path.join(output_dir, "main.elf")
    link_object_files(object_files, output_elf)
6. creating hex file following the same Patter as step 5
    # Convert the ELF file to a HEX file.
    output_hex = os.path.join(output_dir, "main.hex")
    convert_elf_to_hex(output_elf, output_hex)

    print(f"Compilation and linking complete. HEX file generated: {output_hex}")


@cheer ! 
