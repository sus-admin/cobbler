"""
Test module to assert the performance of deserializing the object tree.
"""

from typing import Any, Callable, Dict, Tuple

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from cobbler.api import CobblerAPI
from cobbler.items.distro import Distro
from cobbler.items.image import Image
from cobbler.items.profile import Profile
from cobbler.items.system import System

from tests.performance import CobblerTree


@pytest.mark.parametrize(
    "cache_enabled,enable_menu",
    [
        (
            False,
            False,
        ),
        (
            True,
            False,
        ),
        (
            False,
            True,
        ),
        (
            True,
            True,
        ),
    ],
)
def test_deserialize(
    benchmark: BenchmarkFixture,
    cobbler_api: CobblerAPI,
    create_distro: Callable[[str], Distro],
    create_profile: Callable[[str, str, str], Profile],
    create_image: Callable[[str], Image],
    create_system: Callable[[str, str, str], System],
    cache_enabled: bool,
    enable_menu: bool,
):
    """
    Test that benchmarks the file based deserialization process of Cobbler.
    """

    def setup_func() -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
        api = cobbler_api
        CobblerTree.remove_all_objs(api)
        CobblerTree.create_all_objs(
            api, create_distro, create_profile, create_image, create_system
        )
        del api
        return (), {}

    def deserialize():
        # pylint: disable=protected-access
        CobblerAPI.__shared_state = {}  # pyright: ignore [reportPrivateUsage]
        CobblerAPI.__has_loaded = False  # pyright: ignore [reportPrivateUsage]
        api = CobblerAPI()
        api.deserialize()

    # Arrange
    cobbler_api.settings().cache_enabled = cache_enabled
    cobbler_api.settings().enable_menu = enable_menu

    # Act
    result = benchmark.pedantic(
        deserialize, setup=setup_func, rounds=CobblerTree.test_rounds
    )

    # Cleanup
    CobblerTree.remove_all_objs(cobbler_api)

    # Assert
