import asyncio
from typing import Any, List

import scooze.database.card as db
from bson import ObjectId
from scooze.card import CardT, FullCard
from scooze.models.card import CardModelIn, CardModelOut


async def get_card_by(property_name: str, value, card_class: CardT = FullCard) -> CardT:
    """
    Search the database for the first card that matches the given criteria.

    Args:
        property_name: The property to check.
        value: The value to match on.
        card_class: The type of card to return.

    Returns:
        The first matching card, or None if none were found.
    """

    card_model = await db.get_card_by_property(
        property_name=property_name,
        value=value,
    )
    if card_model is not None:
        return card_class.from_model(card_model)


async def get_cards_by(
    property_name: str,
    values: list[Any],
    card_class: CardT = FullCard,
    paginated: bool = False,
    page: int = 1,
    page_size: int = 10,
) -> List[CardT]:
    """
    Search the database for cards matching the given criteria, with options for
    pagination.

    Args:
        property_name: The property to check.
        values: A list of values to match on.
        paginated: Whether to paginate the results.
        page: The page to look at, if paginated.
        page_size: The size of each page, if paginated.

    Returns:
        A list of cards matching the search criteria, or empty list if none
        were found.
    """

    card_models = await db.get_cards_by_property(
        property_name=property_name,
        values=values,
        paginated=paginated,
        page=page,
        page_size=page_size,
    )
    return [card_class.from_model(m) for m in card_models]


async def get_cards_all(
    card_class: CardT = FullCard,
) -> List[CardT]:
    """
    Get all cards from the database. WARNING: may be extremely large.

    Returns:
        A list of all cards in the database.
    """

    card_models = await db.get_cards_all()
    return [card_class.from_model(m) for m in card_models]


async def add_card(card: CardT) -> ObjectId:
    """
    Add a card to the database.

    Args:
        card: The card to insert.

    Returns:
        The ID of the inserted card, or None if it was unable.
    """

    card_model = CardModelIn.model_validate(card.__dict__)
    model = await db.add_card(card=card_model)
    if model is not None:
        return model.id


async def add_cards(cards: List[CardT]) -> List[ObjectId]:
    """
    Add a list of cards to the database.

    Args:
        cards: The list of cards to insert.

    Returns:
        The IDs of the inserted cards, or empty list if unable.
    """

    card_models = [CardModelIn.model_validate(card.__dict__) for card in cards]
    return await db.add_cards(cards=card_models)


async def delete_card(id: str) -> bool:
    """
    Delete a card from the database.

    Args:
        id: The ID of the card to delete.

    Returns:
        True if the card is deleted, False otherwise.
    """

    return await db.delete_card(id=id) is not None


async def delete_cards_all() -> int:
    """
    Delete all cards in the database.

    Returns:
        The number of cards deleted, or None if none could be deleted.
    """

    return await db.delete_cards_all()
