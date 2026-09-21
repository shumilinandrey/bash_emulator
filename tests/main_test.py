import pytest
from src.main import cd, ls, exit_app


@pytest.mark.parametrize(
    "args, expected",
    [
        ([""], "ls "),
        (["1"], "ls 1"),
        (["1", "2", "3"], "ls 1 2 3")
    ]
)
def test_ls(args: list[str], expected: str) -> None:
    """Тестирование команды ls"""
    assert ls(args) == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        ([""], "cd "),
        (["1"], "cd 1"),
        (["1", "2", "3"], "cd 1 2 3")
    ]
)
def test_cd(args: list[str], expected: str) -> None:
    """Тестирование команды cd"""
    assert cd(args) == expected


def test_exit() -> None:
    """Тестирование команды exit"""
    with pytest.raises(SystemExit) as exit_code:
        exit_app()
    assert exit_code.value.code == 0

