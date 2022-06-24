"""Stream type classes for tap-pokemon."""

from __future__ import annotations

from singer_sdk import typing as th

from tap_pokemon.client import PokemonStream


class _Endpoint(PokemonStream):
    """Base class for side endpoints."""

    name = "__dummy__"
    schema: dict = {"properties": {}}


class _PokemonSpeciesEndpoint(_Endpoint):
    """Dummy Pokémon species endpoint class."""

    path = "/api/v2/pokemon-species/{name}"
    records_jsonpath = "$"


class PokemonSpecies(PokemonStream):
    """Pokémon stream class."""

    name = "__pokemon_species"
    path = "/api/v2/pokemon-species"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.IntegerType,
            description="The Pokemon's Pokédex number.",
            required=True,
        ),
        th.Property(
            "name",
            th.StringType,
            description="The Pokemon's name.",
            required=True,
        ),
        th.Property(
            "is_legendary",
            th.BooleanType,
            description="Whether the Pokemon is legendary.",
            required=True,
        ),
    ).to_dict()

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """Post-process a row.

        Args:
            row: A row of data.
            context: Stream sync context.

        Returns:
            A row of data.
        """
        dummy_stream = _PokemonSpeciesEndpoint(self._tap, schema={"properties": {}})

        records_iterator = iter(dummy_stream.request_records({"name": row["name"]}))
        return next(records_iterator, None)
