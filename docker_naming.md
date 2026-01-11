# Docker image and container naming

Image name: py-telegram-service-telegram-api

Format: <directory-name>-<service-name>

py-telegram-service = your project directory name
telegram-api = service name from compose file


Container name: telegram-service

You explicitly set this with container_name

If you want to control the image name as well:

```yaml
services:
  telegram-api:
    build:
      context: .
    image: telegram-notifier:1.0.0  # ← Control image name
    container_name: telegram-service
    # ...
```