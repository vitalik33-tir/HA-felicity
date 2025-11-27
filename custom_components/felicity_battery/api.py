from __future__ import annotations

import asyncio
import json
import logging
import re

_LOGGER = logging.getLogger(__name__)


class FelicityApiError(Exception):
    """Error while communicating with Felicity battery."""


class FelicityClient:
    """TCP client for Felicity battery local API."""

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

    async def async_get_data(self) -> dict:
        """Send command and get JSON response."""
        try:
            reader, writer = await asyncio.open_connection(self._host, self._port)

            # Та же команда, что мы посылали через printf | nc
            writer.write(b"wifilocalMonitor:get dev real infor")
            await writer.drain()

            try:
                # 4 кБ за глаза, но можно и больше
                data = await asyncio.wait_for(reader.read(8192), timeout=3.0)
            finally:
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass

        except Exception as err:
            raise FelicityApiError(
                f"Error talking to {self._host}:{self._port}: {err}"
            ) from err

        if not data:
            raise FelicityApiError("No data received from battery")

        text = data.decode("ascii", errors="ignore").strip()
        _LOGGER.debug("Raw Felicity response: %r", text)

        # ---- ФИКС КРИВОГО JSON ----
        # Некоторые прошивки отдают что-то вроде:
        # ..."Estate":960,"Bfault":0[[140,130],[256,258]],...
        # т.е. массив температур без имени поля BTemp.
        # Попробуем аккуратно вставить "BTemp":
        if '"BTemp":' not in text and '"Bfault":' in text:
            fixed, n = re.subn(
                r'"Bfault":\s*([-0-9]+)\s*\[\[',
                r'"Bfault":\1,"BTemp":[[',
                text,
            )
            if n:
                _LOGGER.debug(
                    "Patched Felicity JSON: inserted BTemp key (%s replacement(s))", n
                )
                text = fixed
        # ---- КОНЕЦ ФИКСА ----

        try:
            parsed = json.loads(text)
        except Exception as err:
            # сюда попадём, если даже после фикса JSON всё ещё кривой
            raise FelicityApiError(f"Invalid JSON from battery: {text}") from err

        return parsed
