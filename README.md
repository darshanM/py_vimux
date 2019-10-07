# Vim + Tmux + py.test

Python port of [vimux](https://github.com/benmills/vimux) with built-in `py.test` and `nosetests` support (inspired from [vimux-nose-test](https://github.com/pitluga/vimux-nose-test)).


## Requirements
* Vim with Python 3 support. You can check if you have by running `:echo has("python3")`. If this returns `1`, you are good to go.

## Installation

Using Vundle - `Plugin 'darshanM/py_vimux'`


## Base Use Case

* Call `:CreateTmuxPane` from within Vim in a Tmux window to open a horizontal 20% split.
* Call `:RunTest` to run a test file underneath the cursor (or `:RunClass` to run all tests in the class or `:RunFile` to run all tests in a file)


## Usage

Sample `.vimrc`.

```
" Vim Key Bindings
map <Leader>rs :CreateTmuxPane<CR>
autocmd FileType python map <Leader>rf :RunTest<CR>
autocmd FileType python map <Leader>rF :RunClass<CR>
autocmd FileType python map <Leader>ra :RunFile<CR>


" Required
let g:test_runner = 'py.test'
" Optional
let g:setup_cmd='make connect;'
" Optional
let g:test_runner_options = '-s'

```

## Documentation

|Function|Description|
|---|---|
|`:CreateTmuxPane`| Creates a 20% horizontal Tmux Split.|
|`:RunTest`|Runs the test under the cursor.|
|`:RunClass`|Runs all the tests in the class nearest to the cursor|
|`:RunFile`|Runs all the tests in the file|



## Options

Things to add to your `.vimrc`

|Option|Description|Required|
|---|---|---|
|`test_runner`| either `py.test` or `nosetests`|Yes|
|`test_runner_options`| Optional params to be passed into `test_runner`|No|
|`setup_cmd`| Optional command that runs after creating the tmux split (i.e - after `:CreateTmuxPane` gets called.) |No|
