"""Test for the _snake_case_to_camel_case function."""

from xyflow.data_types import _camel_case_to_snake_case, _snake_case_to_camel_case


def test_snake_case_to_camel_case():
    assert _snake_case_to_camel_case("snake_case") == "snakeCase"
    assert _snake_case_to_camel_case("snake_case_with_underscores") == "snakeCaseWithUnderscores"
    assert _snake_case_to_camel_case("SNAKE_CASE") == "SNAKECASE"
    assert _snake_case_to_camel_case("snake_case_with_numbers_123") == "snakeCaseWithNumbers123"
    assert _snake_case_to_camel_case("snake_case_with_numbers_123") == "snakeCaseWithNumbers123"
    assert _snake_case_to_camel_case("single") == "single"


def test_camel_case_to_snake_case():
    assert _camel_case_to_snake_case("camelCase") == "camel_case"
    assert _camel_case_to_snake_case("camelCaseWithUnderscores") == "camel_case_with_underscores"
    assert _camel_case_to_snake_case("camelCase") == "camel_case"
    assert _camel_case_to_snake_case("camelCaseWithNumbers123") == "camel_case_with_numbers123"
    assert _camel_case_to_snake_case("single") == "single"


def test_roundtrip():
    assert _snake_case_to_camel_case(_camel_case_to_snake_case("camelCase")) == "camelCase"
    assert _camel_case_to_snake_case(_snake_case_to_camel_case("snake_case")) == "snake_case"
    assert _camel_case_to_snake_case(_snake_case_to_camel_case("simple")) == "simple"
    assert _snake_case_to_camel_case(_camel_case_to_snake_case("simple")) == "simple"


def test_roundtrip_with_numbers():
    assert _snake_case_to_camel_case(_camel_case_to_snake_case("camelCase123")) == "camelCase123"
    assert _camel_case_to_snake_case(_snake_case_to_camel_case("snake_case123")) == "snake_case123"
    assert _camel_case_to_snake_case(_snake_case_to_camel_case("simple123")) == "simple123"
