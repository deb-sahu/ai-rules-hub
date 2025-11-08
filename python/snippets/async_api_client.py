import asyncio
import aiohttp
from typing import Dict, Any, Optional


class AsyncApiClient:
    """Asynchronous API client using aiohttp."""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def get(self, endpoint: str) -> Dict[str, Any]:
        """Make GET request."""
        if not self._session:
            raise RuntimeError("Session not initialized. Use context manager.")

        url = f"{self.base_url}{endpoint}"
        async with self._session.get(url) as response:
            response.raise_for_status()
            return await response.json()

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request."""
        if not self._session:
            raise RuntimeError("Session not initialized. Use context manager.")

        url = f"{self.base_url}{endpoint}"
        async with self._session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()


# Usage example
async def main():
    async with AsyncApiClient("https://api.example.com") as client:
        users = await client.get("/users")
        print(f"Fetched {len(users)} users")


if __name__ == "__main__":
    asyncio.run(main())
