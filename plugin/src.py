import vim

SEND_KEY_CMD = '''system('tmux send-keys -t {target} "{key}"')'''

LIST_PANES_CMD = '''system('tmux list-panes -F "#{pane_index}:#{pane_active}"')'''

SEARCH_LAST_CMD = "search('{substr}', 'bcn')"

GET_LINE_CMD = "getline({line_num})"

GET_FILE_PATH_CMD = "expand('%s')"

RUN_TEST_CMD = "{test_runner}  {test_runner_options} {path}"

TEST_RUNNER = vim.eval('g:test_runner')

if int(vim.eval("exists('g:setup_cmd')")):
    SETUP_CMD = vim.eval('g:setup_cmd')
else:
    SETUP_CMD = None

if int(vim.eval("exists('g:setup_test_runner_cmd')")):
    SETUP_TEST_RUNNER_CMD = vim.eval('g:setup_test_runner_cmd')
else:
    SETUP_TEST_RUNNER_CMD = None


if int(vim.eval("exists('g:test_runner_options')")):
    TEST_RUNNER_OPTIONS = vim.eval('g:test_runner_options')
else:
    TEST_RUNNER_OPTIONS = None


def split_pane():
    _split_pane()


def run_focused_test():

    runner_pane_idx = _get_idx_of_runner_pane()

    if runner_pane_idx == -1:
        print("Create another pane first.")
        return

    f_name = _get_function_name()
    c_name = _get_class_name()

    if not f_name:
        print("Didn't find an enclosing test method")
        return

    if not c_name:
        print("Didn't find an enclosing class")
        return

    path_to_file = vim.eval(GET_FILE_PATH_CMD)

    if TEST_RUNNER == 'nosetests':
        test_to_run = '{file_name}:{class_name}.{test}'.format(
            file_name=path_to_file,
            class_name=c_name,
            test=f_name
        )

    elif TEST_RUNNER == 'py.test':
        test_to_run = '{file_name}::{class_name}::{test}'.format(
            file_name=path_to_file,
            class_name=c_name,
            test=f_name
        )

    else:
        print("Invalid test runner. Must be one of [nosetests, py.test]")
        return

    cmd = RUN_TEST_CMD.format(
        test_runner=TEST_RUNNER,
        test_runner_options=TEST_RUNNER_OPTIONS if TEST_RUNNER_OPTIONS else '',
        path=test_to_run
    )

    _execute_cmd_in_pane(
        cmd,
        runner_pane_idx,
        SETUP_TEST_RUNNER_CMD
    )


def run_focused_class():

    runner_pane_idx = _get_idx_of_runner_pane()

    if runner_pane_idx == -1:
        print("Create another pane first.")
        return

    c_name = _get_class_name()

    if not c_name:
        print("Didn't find an enclosing class")
        return

    path_to_file = vim.eval(GET_FILE_PATH_CMD)

    test_to_run = '{file_name}:{class_name}'.format(
        file_name=path_to_file,
        class_name=c_name,
    )

    cmd = RUN_TEST_CMD.format(
        test_runner=TEST_RUNNER,
        test_runner_options=TEST_RUNNER_OPTIONS if TEST_RUNNER_OPTIONS else '',
        path=test_to_run
    )

    _execute_cmd_in_pane(
        cmd,
        runner_pane_idx,
        SETUP_TEST_RUNNER_CMD
    )


def run_all_tests_in_file():
    runner_pane_idx = _get_idx_of_runner_pane()

    if runner_pane_idx == -1:
        print("Create another pane first.")
        return

    path_to_file = vim.eval(GET_FILE_PATH_CMD)

    cmd = RUN_TEST_CMD.format(
        test_runner=TEST_RUNNER,
        test_runner_options=TEST_RUNNER_OPTIONS if TEST_RUNNER_OPTIONS else '',
        path=path_to_file
    )

    _execute_cmd_in_pane(
        cmd,
        runner_pane_idx,
        SETUP_TEST_RUNNER_CMD
    )


def _split_pane():
    runner_pane_idx = _get_idx_of_runner_pane()
    if runner_pane_idx != -1:
        print("Secondary Pane exists. Not creating a new one.")
        return
    vim.eval("system('tmux split-window -p 20')")

    # Get back into original window's context
    vim.eval("system('tmux last-pane')")

    runner_pane_idx = _get_idx_of_runner_pane()
    
    if SETUP_CMD:
        _execute_cmd_in_pane(
            SETUP_CMD,
            runner_pane_idx
        )


def _get_idx_of_runner_pane():
    panes = vim.eval(LIST_PANES_CMD).strip()
    panes = panes.split("\n")
    if len(panes) == 1:
        return -1
    for pane in panes:
        pane_id, pane_active = pane.split(':')
        if int(pane_active) == 0:
            return int(pane_id)


def _get_function_name():
    return _get_prev_line_having_substr("def test_")


def _get_class_name():
    return _get_prev_line_having_substr("class")


def _get_prev_line_having_substr(substr):
    """ hacky attempt to return ClassName or method_name
    from preceding lines that look like -
    class ClassName(a, b):
    def method_name(a, b, *args)
    """
    last_occ_idx = vim.eval(SEARCH_LAST_CMD.format(
        substr=substr
    ))
    if last_occ_idx == 0:
        return
    line_content = vim.eval(GET_LINE_CMD.format(
        line_num=last_occ_idx
    ))
    line_content = line_content.strip().split()
    substr_container = line_content[1]
    substr_name, _ = substr_container.split("(")
    return substr_name


def _execute_cmd_in_pane(
        command,
        runner_pane_idx,
        initializing_cmd=None
    ):

    if initializing_cmd:
        vim.eval(SEND_KEY_CMD.format(
            target=runner_pane_idx,
            key=initializing_cmd))

        vim.eval(SEND_KEY_CMD.format(
            target=runner_pane_idx,
            key='Enter'))

    vim.eval(SEND_KEY_CMD.format(
        target=runner_pane_idx,
        key=command))

    vim.eval(SEND_KEY_CMD.format(
        target=runner_pane_idx,
        key='Enter'))
