#!/usr/bin/env python3

import sys
import os
import tempfile
import subprocess
import shutil

CONFIG_FILE_NAME = '.ycm_extra_conf.py'
CONFIG_FUNCTIONS_FILE = 'conf_functions.py'

def main():
    # Try to locate the parent CMake project
    cmake_path = findParentFile('CMakeLists.txt', os.getcwd())
    if cmake_path == None:
        print("Couldn't find a CMakeLists.txt!")
        return 1
    print('Found CMakeLists.txt in "'+cmake_path+'"')

    # Refuse to overwrite unless explicitely asked to
    if os.path.exists(os.path.join(cmake_path, CONFIG_FILE_NAME)) and not '-f' in sys.argv[1:]:
        print("A YouCompleteMe config file already exists in \""+cmake_path+"\", giving up.")
        return 1

    tmpdir = tempfile.mkdtemp()
    ret = genConf(tmpdir, cmake_path)
    shutil.rmtree(tmpdir, ignore_errors=True)
    return ret

def genConf(tmpdir, cmake_path): 
    with open(os.path.dirname(__file__)+'/'+CONFIG_FUNCTIONS_FILE, 'r') as file:
        config_functions = file.read()
    os.chdir(tmpdir)
    if runCMake(tmpdir, cmake_path) != 0:
        print("Failed to run CMake, couldn't generate YCM config");
        return 1

    # Find the project name from the cache
    with open('CMakeCache.txt', 'r') as file:
        cache_data = file.read()
    pos = cache_data.index('CMAKE_PROJECT_NAME:STATIC')
    if pos == -1:
        print("Failed to parse CMake cache")
        return -1
    project_name = cache_data[pos+len('CMAKE_PROJECT_NAME:STATIC')+1:]
    pos = project_name.find('\n')
    if pos != -1:
        project_name = project_name[:pos]

    # Find the flags from the project.dir
    flags = []
    includes = []
    with open('CMakeFiles/'+project_name+'.dir/flags.make', 'r') as file:
        flags_data = filter(None, file.read().split('\n'))
    for line in flags_data:
        if (line.startswith('C_FLAGS') or line.startswith('CXX_FLAGS')) and line.find('=') != -1:
            flags.extend(line[line.find('=')+1:].strip().split(' '))
        if (line.startswith('C_INCLUDES') or line.startswith('CXX_INCLUDES')) and line.find('=') != -1:
            includes.extend(line[line.find('=')+1:].strip().split(' '))

    # Write the config
    writeConf(cmake_path, flags, includes, config_functions)
    print("YouCompleteMe configuration generated successfully!")

# Writes the YCM config file
def writeConf(path, flags, includes, config_functions):
    with open(path+'/'+CONFIG_FILE_NAME, 'w') as conf_file:
        conf_file.write("import os,ycm_core\n")

        conf_file.write("flags = [\n")
        for flag in flags:
            conf_file.write("'"+flag+"',\n")
        for include in includes:
            conf_file.write("'"+include+"',\n")
        conf_file.write("]\n")

        conf_file.write(config_functions)

# Runs CMake for a project in the given temporary directory
def runCMake(tmpdir, project_dir):
    print("Running cmake in \""+tmpdir+"\"...")
    return subprocess.call(["cmake", project_dir], cwd=tmpdir, stdout=open(os.devnull, 'wb'), stderr=subprocess.STDOUT)

# Goes up as needed in the directory hierarchy until a given file is found, or the root is reached
def findParentFile(filename, base_path=None):
    if base_path==None:
        base_path = os.getcwd()
    if os.path.exists(os.path.join(base_path, filename)):
        return base_path
    if os.path.samefile(base_path, os.path.dirname(base_path)):
        return None
    else:
        return findParentFile(filename, os.path.dirname(base_path))


if(__name__ == "__main__"):
    sys.exit(main())
