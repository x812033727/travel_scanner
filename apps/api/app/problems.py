from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, status: int, code: str, detail: str) -> None:
        self.status = status
        self.code = code
        self.detail = detail


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    titles = {
        400: "請求內容不正確",
        401: "需要登入",
        402: "可用次數不足",
        403: "沒有操作權限",
        404: "找不到資料",
        409: "資料狀態衝突",
        422: "輸入內容不正確",
        429: "操作太頻繁",
        500: "伺服器發生錯誤",
        503: "服務暫時無法使用",
    }
    payload: dict[str, Any] = {
        "type": f"https://travel-scanner.local/problems/{exc.code}",
        "title": titles.get(exc.status, "請求未完成"),
        "status": exc.status,
        "code": exc.code,
        "detail": exc.detail,
        "request_id": getattr(request.state, "request_id", None),
    }
    return JSONResponse(payload, status_code=exc.status, media_type="application/problem+json")


FIELD_LABELS = {
    "email": "Email",
    "password": "密碼",
    "origin": "出發地",
    "destination": "目的地",
    "departure_date": "出發日期",
    "return_date": "回程日期",
    "travel_window": "旅行日期範圍",
    "trip_length_range": "旅行天數",
    "target_price": "目標價格",
    "resource_id": "追蹤項目",
    "resource_type": "追蹤類型",
}


def _localized_issue(error: dict[str, Any]) -> str:
    raw_location = error.get("loc")
    location: list[Any] = list(raw_location) if isinstance(raw_location, (list, tuple)) else []
    field = next(
        (part for part in reversed(location) if isinstance(part, str) and part != "body"),
        None,
    )
    label = FIELD_LABELS.get(field or "", str(field).replace("_", " ") if field else "輸入內容")
    raw = str(error.get("msg") or "輸入內容格式不正確").removeprefix("Value error, ")
    replacements = {
        "Field required": "必填",
        "value is not a valid email address": "Email 格式不正確",
        "String should have at least 10 characters": "至少需要 10 個字元",
        "Input should be greater than 0": "必須大於零",
        "travel window end must be after start": "結束日期必須晚於開始日期",
        "travel window cannot exceed 180 days": "日期範圍不可超過 180 天",
        "maximum trip length cannot be shorter than minimum": "最長天數不可少於最短天數",
        "minimum nightly price cannot exceed maximum": "每晚最低價格不可高於最高價格",
        "return_date must be after departure_date": "回程日期必須晚於出發日期",
        "round_trip requires return_date": "來回行程必須填寫回程日期",
        "origin, destination and departure_date are required": "出發地、目的地與出發日期皆為必填",
        "children must match children_ages": "兒童人數必須與年齡數量相同",
        "children ages must be between 0 and 17": "兒童年齡必須介於 0 至 17 歲",
    }
    message = next(
        (value for key, value in replacements.items() if key.casefold() in raw.casefold()),
        None,
    )
    if message is None:
        issue_type = str(error.get("type") or "")
        if issue_type == "missing":
            message = "必填"
        elif "date" in issue_type:
            message = "請填寫有效日期"
        elif issue_type == "string_too_short":
            message = "內容太短"
        elif issue_type == "string_too_long":
            message = "內容太長"
        else:
            message = "格式或內容不正確"
    return f"{label}：{message}"


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    details = list(dict.fromkeys(_localized_issue(error) for error in exc.errors()))
    payload: dict[str, Any] = {
        "type": "https://travel-scanner.local/problems/validation_error",
        "title": "輸入內容不正確",
        "status": 422,
        "code": "validation_error",
        "detail": "；".join(details),
        "request_id": getattr(request.state, "request_id", None),
    }
    return JSONResponse(payload, status_code=422, media_type="application/problem+json")
