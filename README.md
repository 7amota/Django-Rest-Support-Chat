# Django Rest Support Chat

Django Rest Support Chat is a real-time support chat application built using Django and Django Rest Framework. This application allows users to communicate in real-time through a chat interface, making it ideal for providing customer support or facilitating communication within a team.

## Features

- **Real-time Communication**: Utilizes WebSocket technology for real-time messaging, enabling instant communication between users.
- **User Authentication**: Secure user authentication system ensures that only authorized users can access the chat application.
- **RESTful API**: Built with Django Rest Framework, providing a powerful and flexible API for integrating the chat functionality into other applications or services.
- **Customizable**: Easily customizable to fit the specific needs of your project or organization.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/7amota/Django-Rest-Support-Chat.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. Access the chat application at `http://localhost:8000/`.

## Usage

1. Register as a new user or log in with existing credentials.
2. Start chatting with other users in real-time.

## Contributing

Contributions are welcome! If you encounter any bugs or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
