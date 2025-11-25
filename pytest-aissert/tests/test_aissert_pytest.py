"""Tests for pytest-aissert plugin."""


def test_hello_ini_setting(pytester):
    """Test that HELLO ini setting can be configured and accessed."""
    pytester.makeini("""
        [pytest]
        HELLO = world
    """)

    pytester.makepyfile("""
        import pytest

        @pytest.fixture
        def hello(request):
            return request.config.getini('HELLO')

        def test_hello_world(hello):
            assert hello == 'world'
    """)

    result = pytester.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_hello_world PASSED*",
        ]
    )

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0
