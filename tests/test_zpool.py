import typing as t
import pathlib

import yaml
from ward import test, raises

from cazier.zfs.plugins.modules._utils import Zpool

data: dict[str, t.Any] = yaml.safe_load(
    pathlib.Path(__file__).parent.joinpath("test_data.yaml").read_text(encoding="utf8")
)

for item in data[__name__]:

    # pylint: disable-next=cell-var-from-loop
    @test(f"parsing zpool list: {item['name']}")  # type: ignore[misc]
    def _(console: str = item["console"], _list: dict[str, t.Any] = item["list"]) -> None:
        assert Zpool.parse_console(console).dump() == _list


@test("parsing failures")  # type: ignore[misc]
def _() -> None:
    with raises(TypeError) as exception:
        Zpool.parse_console(
            """
test	27.2T	420K	27.2T	-	-	0%	0%	1.00x	ONLINE	-
	/tmp/01.raw	9.08T	141K	9.08T	-	-	0%	0.00%	-	ONLINE
	/dev/disk/by-id/scsi-SATA_SN9300G_SERIAL-part1	9.08T	142K	9.08T	-	-	0%	0.00%	-	ONLINE
	/dev/disk/by-id/scsi-SATA_SN9300G_SERIAL-part2	9.08T	142K	9.08T	-	-	0%	0.00%	-	ONLINE
"""
        )
    assert "Only using whole disk (or sparse images) is supported" in str(exception.raised)


for item in data[__name__]:

    # pylint: disable-next=cell-var-from-loop
    @test(f"zpool create command: {item['name']}")  # type: ignore[misc]
    def _(console: str = item["console"], create: str = item["create"]) -> None:
        assert " ".join(Zpool.parse_console(console).create_command()) == create
