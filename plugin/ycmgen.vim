let s:config_gen = expand("<sfile>:p:h:h") . "/config_gen.py"

command! -nargs=0 -complete=file_in_path -bang YcmGen call s:GenerateConfig(<bang>0)

function! s:GenerateConfig(overwrite)
    let l:cmd = "! " . s:config_gen
    if a:overwrite
        let l:cmd = l:cmd . " -f"
	endif

    execute l:cmd . " </dev/null"
endfunction()
