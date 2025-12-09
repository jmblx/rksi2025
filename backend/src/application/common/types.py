from typing import NamedTuple


class PaginationData(NamedTuple):
    per_page: int | None
    last_record_id: int | None
