## Inheritance in httpx

```text
Exception (built-in)
└── httpx.HTTPError (base class for all httpx exceptions)
    ├── httpx.RequestError (network/connection errors)
    │   ├── httpx.ConnectError
    │   ├── httpx.TimeoutException
    │   └── ...
    ├── httpx.HTTPStatusError (4xx/5xx responses)
    └── ...
```