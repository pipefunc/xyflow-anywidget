"""Tests for the example functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from .examples.basic_examples import examples as basic_examples
from .examples.data_science_examples import examples as data_science_examples
from .examples.interactive_demos import examples as interactive_demos

if TYPE_CHECKING:
    from collections.abc import Callable

    from xyflow import XYFlowWidget


@pytest.mark.parametrize("example", basic_examples)
def test_basic_examples(example: Callable[[], XYFlowWidget]) -> None:
    example()


@pytest.mark.parametrize("example", data_science_examples)
def test_data_science_examples(example: Callable[[], XYFlowWidget]) -> None:
    example()


@pytest.mark.parametrize("example", interactive_demos)
def test_interactive_demos(example: Callable[[], XYFlowWidget]) -> None:
    example()
