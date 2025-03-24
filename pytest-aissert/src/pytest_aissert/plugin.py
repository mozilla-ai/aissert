import pytest
import yaml
import pytest_aissert.decorators as decorators


def pytest_addoption(parser):
    group = parser.getgroup('aissert-pytest')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2025',
        help='Set the value for the fixture "bar".'
    )
    print("<<called addoption>>")
    parser.addini('HELLO', 'Dummy pytest.ini setting')



def pytest_generate_tests(metafunc):
    """ This allows us to load tests from external files by
    parametrizing tests with each test case found in a data_X
    file """
    # TODO externalize
    if all(x in metafunc.fixturenames for x in ['question_yaml', 'answer_yaml']):
        with open("tests/questions/example_001.yaml") as q_yaml_file:
            q_yaml = yaml.safe_load(q_yaml_file)
        with open("tests/answers/example_001.yaml") as a_yaml_file:
            a_yaml = yaml.safe_load(a_yaml_file)
        metafunc.parametrize(
            ('question_yaml', 'answer_yaml'),
            [
                (q_yaml, a_yaml),
                (q_yaml, a_yaml),
            ],
            scope="session"
        )

def pytest_sessionfinish(session, exitstatus):
    print(f'<<< {decorators.current_report} >>>')



"""
@pytest.hookimpl(wrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    do_something_before_next_hook_executes()

    # If the outcome is an exception, will raise the exception.
    res = yield

    new_res = post_process_result(res)

    # Override the return value to the plugin system.
    return new_res"
"""