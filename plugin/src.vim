if !has('python3')
    echo "Needs Python 3 Installed."
    finish
endif

command! -nargs=0 CallHN call Split_pane()

command! -nargs=0 RunTest call RunTestUnderCursor()

command! -nargs=0 RunClass call RunClassUnderCursor()

command! -nargs=0 RunFile call RunFile()

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')
let g:test_runner = 'py.test'

function! Split_pane()
exe 'py3file ' . escape(s:plugin_path, ' ') . '/src.py'
python3 split_pane()
endfunction


function! RunTestUnderCursor()
exe 'py3file ' . escape(s:plugin_path, ' ') . '/src.py'
python3 run_focused_test()
endfunction



function! RunClassUnderCursor()
exe 'py3file ' . escape(s:plugin_path, ' ') . '/src.py'
python3 run_focused_class()
endfunction


function! RunFile()
exe 'py3file ' . escape(s:plugin_path, ' ') . '/src.py'
python3 run_all_tests_in_file()
endfunction
