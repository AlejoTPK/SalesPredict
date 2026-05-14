"""AI Insights service — Groq-powered natural language analysis."""


from groq import Groq

from app.core.config import settings


def _get_client() -> Groq | None:
    if not settings.groq_api_key:
        return None
    return Groq(api_key=settings.groq_api_key)


def _build_inventory_context(recommendations: list[dict]) -> str:
    top = recommendations[:4]
    lines = []
    for r in top:
        trend_word = "crecimiento" if r["trend_pct"] >= 0 else "decrecimiento"
        lines.append(
            f"- {r['product_name']}: {r['avg_monthly_sales']:.0f}u/mes (promedio), "
            f"tendencia {trend_word} {abs(r['trend_pct'])}%, "
            f"demanda esperada {r['forecasted_demand']:.0f}u, "
            f"recomendación compra {r['recommended_reorder']}u"
        )
    return "\n".join(lines)


def _build_forecast_context(forecast: list[dict]) -> str:
    if not forecast:
        return "No hay datos de forecast disponibles."
    total = sum(f["predicted"] for f in forecast)
    first = forecast[0]
    last = forecast[-1]
    growth = (last["predicted"] - first["predicted"]) / max(1, first["predicted"]) * 100
    return (
        f"Forecast a {len(forecast)} días: total esperado ${total:,.0f}, "
        f"inicio ${first['predicted']:,.0f}, fin ${last['predicted']:,.0f}, "
        f"trayectoria {'creciente' if growth >= 0 else 'decreciente'} ({growth:+.1f}%)"
    )


async def generate_inventory_insight(recommendations: list[dict]) -> str:
    client = _get_client()
    if not client:
        return _fallback_inventory(recommendations)

    ctx = _build_inventory_context(recommendations)
    prompt = (
        "Eres un analista de inventario experto para un CRM de ventas B2B llamado SalesPredict.\n"
        "Analiza estos datos de productos y da 2-3 recomendaciones accionables en español, "
        "estilo ejecutivo, directo, usando viñetas con •. Máximo 150 palabras.\n\n"
        f"Productos:\n{ctx}\n\n"
        "Responde solo con las recomendaciones, sin saludo ni despedida."
    )

    try:
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_completion_tokens=250,
        )
        return response.choices[0].message.content or ""
    except Exception:
        return _fallback_inventory(recommendations)


async def generate_forecast_insight(forecast: list[dict], historical: list[dict]) -> str:
    client = _get_client()
    if not client:
        return _fallback_forecast(forecast)

    fctx = _build_forecast_context(forecast)
    hctx = f"Histórico: {len(historical)} días de datos reales."
    prompt = (
        "Eres un analista financiero para un CRM B2B. Interpreta este forecast de ventas "
        "en 2-3 frases ejecutivas en español. Incluye: tendencia, mejor/peor día, "
        "y un dato curioso sobre el patrón detectado. Máximo 120 palabras.\n\n"
        f"{hctx}\n{fctx}\n\n"
        "Responde solo con el análisis, sin saludo ni despedida."
    )

    try:
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_completion_tokens=250,
        )
        return response.choices[0].message.content or ""
    except Exception:
        return _fallback_forecast(forecast)


def _fallback_inventory(recommendations: list[dict]) -> str:
    if not recommendations:
        return "No hay suficientes datos de productos para generar recomendaciones."
    top = recommendations[0]
    lines = [
        f"• **{top['product_name']}** es tu producto estrella — prioriza su reorden con {top['recommended_reorder']}u.",
    ]
    if len(recommendations) > 1:
        down = [r for r in recommendations if r["trend_pct"] < 0]
        if down:
            lines.append(
                f"• **{down[0]['product_name']}** muestra tendencia negativa ({down[0]['trend_pct']}%) — evalúa reducir stock."
            )
        up = [r for r in recommendations if r["trend_pct"] > 5]
        if len(up) > 1:
            lines.append(
                f"• {len(up)} productos con tendencia positiva — asegura inventario para cubrir la demanda creciente."
            )
    return "\n".join(lines)


def _fallback_forecast(forecast: list[dict]) -> str:
    if not forecast:
        return "Datos insuficientes para generar un análisis de forecast."
    total = sum(f["predicted"] for f in forecast)
    avg = total / len(forecast)
    first = forecast[0]["predicted"]
    last = forecast[-1]["predicted"]
    growth = ((last - first) / max(1, first) * 100) if first > 0 else 0
    trend = "alcista" if growth > 3 else "bajista" if growth < -3 else "estable"
    direction = "subiendo" if growth > 0 else "bajando" if growth < 0 else "estable"
    return (
        f"El pronóstico a {len(forecast)} días muestra una tendencia {trend} "
        f"({growth:+.1f}%). La media diaria es de ${avg:,.0f}. "
        f"El modelo detecta un patrón {direction} — "
        f"{'aprovecha para planificar compras anticipadas.' if growth > 0 else 'ajusta expectativas y revisa costos.' if growth < 0 else 'mantén el plan actual.'}"
    )
