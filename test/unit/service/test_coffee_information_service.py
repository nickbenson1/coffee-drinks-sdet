# pylint: disable=redefined-outer-name,missing-module-docstring,missing-function-docstring,unused-variable,implicit-str-concat

import uuid
import pytest
from expects import expect, equal, be_a, raise_error
from domain.model.coffee_drink import CoffeeDrink
from domain.model.coffee_information import CoffeeInformation
from service.coffee_information_service import CoffeeInformationService
from exception.invalid_uuid_exception import InvalidUUIDException
from exception.not_found_exception import NotFoundException


def describe_get_all_information():
    def test_should_return_coffee_information(
        coffee_information_repository_mock, coffee_information
    ):
        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )
        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        result = coffee_information_service.get_all_information()

        expect(result).to(be_a(type(coffee_information)))
        expect(result).to(equal(coffee_information))


def describe_get_drink_by_id():
    def test_should_return_coffee_drink(
        coffee_information_repository_mock, coffee_information, valid_coffee_drink_id
    ):
        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )
        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        result = coffee_information_service.get_drink_by_id(valid_coffee_drink_id)

        coffee_drink = __get_drink_by_value(
            coffee_information, str(valid_coffee_drink_id)
        )
        expect(result).to(be_a(type(coffee_drink)))
        expect(result).to(equal(coffee_drink))

    @pytest.mark.parametrize(
        "invalid_coffee_drink_id",
        [
            uuid.uuid1(),
            uuid.uuid3(uuid.NAMESPACE_X500, "name"),
            uuid.uuid5(uuid.NAMESPACE_X500, "another name"),
            "",
            " ",
            123,
            "@*(#$%!",
            "1234",
            "asdf",
            "ASDF",
        ],
    )
    def test_should_raise_invalid_uuid_exception_when_uuid_not_version_4(
        coffee_information_repository_mock, coffee_information, invalid_coffee_drink_id
    ):
        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )
        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        expect(
            lambda: coffee_information_service.get_drink_by_id(invalid_coffee_drink_id)
        ).to(raise_error(InvalidUUIDException))

    def test_should_raise_not_found_exception_when_uuid_not_found(
        coffee_information_repository_mock, coffee_information
    ):
        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )
        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        non_existent_coffee_drink_id = uuid.uuid4()
        expect(
            lambda: coffee_information_service.get_drink_by_id(
                non_existent_coffee_drink_id
            )
        ).to(raise_error(NotFoundException))


def describe_get_drink_by_title():
    def test_should_return_coffee_drink(
        coffee_information_repository_mock, coffee_information, valid_coffee_drink_title
    ):
        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )
        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        result = coffee_information_service.get_drink_by_title(valid_coffee_drink_title)

        coffee_drink = __get_drink_by_value(
            coffee_information, valid_coffee_drink_title
        )
        expect(result).to(be_a(type(coffee_drink)))
        expect(result).to(equal(coffee_drink))

    def test_should_raise_not_found_exception_when_title_not_found(
        coffee_information_repository_mock, coffee_information
    ):
        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )
        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        non_existent_coffee_drink_title = "a vague name"
        expect(
            lambda: coffee_information_service.get_drink_by_title(
                non_existent_coffee_drink_title
            )
        ).to(raise_error(NotFoundException))


@pytest.fixture
def coffee_information_repository_mock(mocker):
    return mocker.Mock()


@pytest.fixture
def coffee_information(valid_coffee_drink_id, valid_coffee_drink_title):
    return CoffeeInformation(
        coffee_drinks=[
            CoffeeDrink(
                id=str(valid_coffee_drink_id),
                title=valid_coffee_drink_title,
                description="this is a test",
                ingredients=["ingredient 1", "ingredient 2"],
            )
        ]
    )


@pytest.fixture
def valid_coffee_drink_id():
    return uuid.uuid4()


@pytest.fixture
def valid_coffee_drink_title():
    return "stub coffee"


def __get_drink_by_value(coffee_information, value: str):
    normalized_value = value.casefold()
    for coffee_drink in coffee_information.coffee_drinks:
        if coffee_drink.id.casefold() == normalized_value:
            return coffee_drink

        if coffee_drink.title.casefold() == normalized_value:
            return coffee_drink

    return None  # pragma: no cover
