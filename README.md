@Author:MeJustMeLOL
# GCC-ARM-Linker_Python-
This is just an idea when the IDE asks me for $99 to compile code bigger than 120k lines. 

Warnning 1 : the module dont have  Debug itself  ,so use it caution .

Warning 2 : i just test on code base created by Stm32Mx , and Keli package . in  Others case is beyone my expectation .
about the project  it base on  2  observable  from  CMD sytax and Linker , here is description  :

The module design following the work flow  : 
1. extract the  file extension from "Main Directory" reference as "project_dir" in code base
  
        source_files = find_files(project_dir, ".c", exclude_dirs=EXCLUDE_DIRS, exclude_files=EXCLUDE_FILES)
        header_files = find_files(project_dir, ".h", exclude_dirs=EXCLUDE_DIRS, exclude_files=EXCLUDE_FILES)

2. callback the  Folder Path 

        project_include_dirs = find_include_dirs(header_files)

3. User OutPut path  
    
        output_dir = r"....\dum_folder" # your path as output
        os.makedirs(output_dir, exist_ok=True)

4. it  will delivery all information above   as struct {GCC_systax}{opts} {FLAG}{I} {GCC_output FIle type}, then using Os libs as Cmd  prompt  . The FLAG is defined "CPU_FLAGS = ["-mcpu=cortex-m3", "-mthumb","-Os"]" .

        object_files = compile_source_files(source_files, project_include_dirs, output_dir)

5. Link it ,  just simply as steps 4 using join string and cmd  .
    
        output_elf = os.path.join(output_dir, "main.elf")
        link_object_files(object_files, output_elf)

6. creating hex file following the same Patter as step 5

       output_hex = os.path.join(output_dir, "main.hex")
    c  onvert_elf_to_hex(output_elf, output_hex)

        print(f"Compilation and linking complete. HEX file generated: {output_hex}")



1. failed result
      
      ![image](https://github.com/user-attachments/assets/12711e79-7145-4821-9f11-8098835b5b3d)
      
     Reason : linker scripts  is missing it leading to stm32link cant boot the code

2. try again

   ![image](https://github.com/user-attachments/assets/4493e4f6-c398-4a6e-8514-91a837b49217)

Okie let boot the code 

![image](https://github.com/user-attachments/assets/aed94631-ec40-4b87-a40e-0d7d7cdf85b6)


3. size comparation 

  Mine : 69kb     ||||||||||||    Keil : 50kb 
  
  it s a huge gape i will optimize  it latter , but i dont know how KKKKKKKKKKKKKKK. thanks for reading 
@cheer ! 
