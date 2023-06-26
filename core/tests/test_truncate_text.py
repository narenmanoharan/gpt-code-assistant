import pytest
from core.functions import truncate_text_to_token_limit, count_tokens


@pytest.fixture(scope="module")
def max_tokens():
    return 5


@pytest.mark.parametrize(
    "data, expected",
    [
        ("", True),
        ("This is a long string with many tokens", True),
        (["This", "is", "a", "sample", "sentence", "and", "this", "is", "another"], True),
        ([("This", 1), ("is", 2), ("a", 3), ("sample", 4), ("sentence", 5), ("and", 6), ("this", 7), ("is", 8)], True),
        ("This", True),
        (["T", "h", "i", "s"], True),
        ([("T", 1), ("h", 2), ("i", 3), ("s", 4)], True),
        ("This is a string with special chars!@#", True),
    ],
)
def test_truncate_text_to_token_limit(data, expected, max_tokens):
    result = truncate_text_to_token_limit(data, max_tokens)
    assert (count_tokens(result) <= max_tokens) == expected


def test_truncate_text_invalid_data_type_in_list(max_tokens):
    data = ["This", 1, ("is", 2)]
    with pytest.raises(ValueError):
        truncate_text_to_token_limit(data, max_tokens)
