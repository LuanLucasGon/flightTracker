import pytest
from app.users.user_service import UserService
from app.shared.exceptions.domain_exceptions import ConflictException, InvalidDataException


class TestUserRegistrationStep1:

    def test_registration_with_valid_data_sends_confirmation_email(self, db, mocker):
        mock_publish = mocker.patch(
            "app.users.user_service.RabbitMQClient.publish"
        )
        service = UserService()

        service.register_step1(
            email="lucas@example.com",
            cpf="529.982.247-25",
            password="senha1234",
        )

        mock_publish.assert_called_once()
        call_args = mock_publish.call_args
        assert call_args[1]["queue"] == "email.confirmation"
        assert call_args[1]["message"]["to"] == "lucas@example.com"

    def test_registration_with_duplicatee_email_raises_conflitct(self, db, mocker):
        mocker.patch("app.users.user_service.RabbitMQClient.publish")
        mocker.patch(
            "app.users.user_repository.UserRepository.email_exists",
            return_value=True,
        )
        service = UserService()

        with pytest.raises(ConflictException) as exc_info:
            service.register_step1(
                email="lucas@example.com",
                cpf="529.982.247-25",
                password="senha1234",
            )

        assert "email" in exc_info.value.message.lower()

    def test_rewgistration_with_duplicated_cpf_raises_conflict(self, db, mocker):
        mocker.patch("app.users.user_service.RabbitMQClient.publish")
        mocker.patch(
            "app.users.user_repository.UserRepository.email_exists",
            return_value=False,
        )
        mocker.patch(
            "app.users.user_repository.UserRepository.cpf_exists",
            return_value=True,
        )
        service = UserService()

        with pytest.raises(ConflictException) as exc_info:
            service.register_step1(
                email="lucas@example.com",
                cpf="529.982.247-25",
                password="senha1234",
            )

        assert "cpf" in exc_info.value.message.lower()

    def test_registration_with_password_shorter_than_8_characters_raises_invalid_data(self, db, mocker):
        mocker.patch("app.users.user_service.RabbitMQClient.publish")
        mocker.patch(
            "app.users.user_repository.UserRepository.email_exists",
            return_value=False,
        )
        mocker.patch(
            "app.users.user_repository.UserRepository.cpf_exists",
            return_value=False,
        )
        service = UserService()

        with pytest.raises(InvalidDataException) as exc_info:
            service.register_step1(
                email="lucas@example.com",
                cpf="529.982.247-25",
                password="abc",
            )

        assert "password" in exc_info.value.message.lower()

    def test_registration_with_invalid_cpf_raises_invalid_data(self, db, mocker):
        mocker.patch("app.users.user_service.RabbitMQClient.publish")
        mocker.patch(
            "app.users.user_repository.UserRepository.email_exists",
            return_value=False,
        )
        mocker.patch(
            "app.users.user_repository.UserRepository.cpf_exists",
            return_value=False,
        )
        service = UserService()

        with pytest.raises(InvalidDataException) as exc_info:
            service.register_step1(
                email="lucas@example.com",
                cpf="111.111.111-11",
                password="senha1234",
            )

        assert "cpf" in exc_info.value.message.lower()