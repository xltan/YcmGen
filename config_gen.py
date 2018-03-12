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

    tmpdir = tempfile.mkdtemp()
    ret = genConf(tmpdir, cmake_path)
    dbpath = 'compile_commands.json'
    shutil.copyfile(os.path.join(tmpdir, dbpath), os.path.join(cmake_path, dbpath))
    confpath = os.path.join(os.path.dirname(__file__), CONFIG_FUNCTIONS_FILE)
    shutil.copyfile(confpath, os.path.join(cmake_path, CONFIG_FILE_NAME))
    shutil.rmtree(tmpdir, ignore_errors=True)
    return ret

def source_bat(bat_file):
    # interesting = {"INCLUDE", "LIB", "LIBPATH", "PATH"}
    result = {}

    process = subprocess.Popen('"%s"& set' % (bat_file),
                        stdout=subprocess.PIPE,
                        shell=True)
    (out, err) = process.communicate()

    for line in out.split("\n"):
        if '=' not in line:
            continue
        line = line.strip()
        key, value = line.split('=', 1)
        result[key] = value
    return result

def genConf(tmpdir, cmake_path): 
    os.chdir(tmpdir)
    print("Running cmake in \""+tmpdir+"\"...")
    res = source_bat('C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat')
    os.environ.update(res)
    return subprocess.call(["cmake", "-G", "NMake Makefiles", "-D", "CMAKE_EXPORT_COMPILE_COMMANDS=1", cmake_path], cwd=tmpdir, stdout=open(os.devnull, 'wb'), stderr=subprocess.STDOUT)

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
