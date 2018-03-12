let s:config_gen = expand("<sfile>:p:h:h") . "/config_gen.py"

command! -nargs=0 -complete=file_in_path -bang YcmGen call s:GenerateConfig()

function! s:GenerateConfig()
    let l:cmd = "silent !python " . s:config_gen
    execute l:cmd . " -f"
endfunction()
