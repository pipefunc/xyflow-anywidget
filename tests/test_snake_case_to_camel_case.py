"""Test for the _snake_case_to_camel_case function."""

from xyflow.data_types import _snake_case_to_camel_case


def test_snake_case_to_camel_case():
    assert _snake_case_to_camel_case("snake_case") == "snakeCase"
    assert _snake_case_to_camel_case("snake_case_with_underscores") == "snakeCaseWithUnderscores"
    assert _snake_case_to_camel_case("SNAKE_CASE") == "SNAKECASE"
    assert _snake_case_to_camel_case("snake_case_with_numbers_123") == "snakeCaseWithNumbers123"
    assert _snake_case_to_camel_case("snake_case_with_numbers_123") == "snakeCaseWithNumbers123"
    assert _snake_case_to_camel_case("single") == "single"
