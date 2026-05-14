import asyncio
import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


async def generate_mock_forecast() -> list[dict]:
    predictions = []
    now = datetime.utcnow()
    for i in range(1, 31):
        date = now.replace(day=min(now.day + i, 28))
        predictions.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "predicted_amount": round(5000 + i * 150, 2),
            }
        )
    return predictions


@router.websocket("/ws/predictions")
async def predictions_stream(websocket: WebSocket) -> None:
    await websocket.accept()

    try:
        forecast = await generate_mock_forecast()
        await websocket.send_json({"type": "forecast", "data": forecast})

        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30)
                msg = json.loads(data)

                if msg.get("action") == "refresh":
                    forecast = await generate_mock_forecast()
                    await websocket.send_json({"type": "forecast", "data": forecast})

                elif msg.get("action") == "ping":
                    await websocket.send_json(
                        {"type": "pong", "timestamp": datetime.utcnow().isoformat()}
                    )

            except asyncio.TimeoutError:
                await websocket.send_json(
                    {"type": "ping", "timestamp": datetime.utcnow().isoformat()}
                )

    except WebSocketDisconnect:
        pass
    except Exception:
        await websocket.close(code=1011)
