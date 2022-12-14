# HTTP Status

HTTP Status checks the HTTP Codes of registered sites and also checks when the site's SSL will expire.

## Instalation

To run the project use `Docker`

```bash
  docker compose build
  docker compose up
```

## Build your own keys and move to directory keys

- When running talisman, it forces everything to HTTPS except when it's in debug mode, so it needs some keys to use HTTPS.

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

## Autor

- [@jonfarias](https://www.github.com/jonfarias)

## License

[MIT](https://choosealicense.com/licenses/mit/)
