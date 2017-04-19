import pytest

from idsfree.actions.default.api import run_default_idsfree


def test_run_default_idsfree_runs_ok():

    #
    # FILL THIS WITH A TEST
    #
    # assert run_prepare_idsfree() is None
    pass


def test_run_default_idsfree_empty_input():

    with pytest.raises(AssertionError):
        run_default_idsfree(None)
