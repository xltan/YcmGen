# YcmGen
YouCompleteMe config generator that Works On My Machine™  

Liberally inspired by https://github.com/rdnetto/YCM-Generator  
Works with CMake projects only.  
No merchantability expressed or implied. May destroy your everything.  

## Installation
First install Python3 and CMake on your system.  
Then pass `tux3/YcmGen` to your favorite plugin manager.  
For example with Vundle you would write `Plugin 'tux3/YcmGen'` in your .vimrc and run `:PluginInstall`.  

## Usage
Go in a directory (or subdirectory) of a CMake project and run `:YcmGen` from within Vim.  
If a YouCompleteMe config file already exists, use `:YcmGen!` to overwrite it.  
The plugin will run CMake on your project and inspect the generated files for configuration flags and include directories, 
this may take a little while depending on your CMake project.
