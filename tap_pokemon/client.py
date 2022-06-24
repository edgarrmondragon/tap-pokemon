"""REST client handling, including PokemonStream base class."""

from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlparse

from singer_sdk import RESTStream


class PokemonStream(RESTStream):
    """Pokemon stream class."""

    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.next"

    @property
    def url_base(self) -> str:
        """Base URL of the Pokémon API.

        Returns:
            Base URL of the Pokémon API.
        """
        return self.config["base_url"]

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        headers["User-Agent"] = f"{self.tap_name}/{self._tap.plugin_version}"
        return headers

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params: dict = {}
        next_url = urlparse(next_page_token) if next_page_token else None

        if next_url:
            query = parse_qs(next_url.query)
            params["offset"] = query.get("offset", [""])[0]
            params["limit"] = query.get("limit", [""])[0]
        else:
            params["limit"] = 100

        return params
