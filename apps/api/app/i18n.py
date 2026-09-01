from typing import Annotated, Literal, cast

from fastapi import Header

Locale = Literal["en", "ja", "ko", "zh-TW", "zh-CN"]
LOCALES: tuple[Locale, ...] = ("en", "ja", "ko", "zh-TW", "zh-CN")
DEFAULT_LOCALE: Locale = "zh-TW"

PROVIDER_LOCALES: dict[str, dict[Locale, str]] = {
    "google": {locale: locale for locale in LOCALES},
    "booking": {
        "en": "en-gb",
        "ja": "ja",
        "ko": "ko",
        "zh-TW": "zh-tw",
        "zh-CN": "zh-cn",
    },
    "skyscanner": {locale: locale for locale in LOCALES},
}

PROBLEM_TITLES: dict[Locale, dict[int | str, str]] = {
    "en": {
        400: "Invalid request",
        401: "Sign-in required",
        402: "Not enough uses",
        403: "Permission denied",
        404: "Not found",
        409: "Data conflict",
        422: "Invalid input",
        429: "Too many requests",
        500: "Server error",
        503: "Service unavailable",
        "default": "Request not completed",
    },
    "ja": {
        400: "リクエストが正しくありません",
        401: "ログインが必要です",
        402: "利用回数が不足しています",
        403: "権限がありません",
        404: "データが見つかりません",
        409: "データが競合しています",
        422: "入力内容が正しくありません",
        429: "操作が多すぎます",
        500: "サーバーエラー",
        503: "サービスを利用できません",
        "default": "リクエストを完了できませんでした",
    },
    "ko": {
        400: "잘못된 요청",
        401: "로그인이 필요합니다",
        402: "사용 횟수가 부족합니다",
        403: "권한이 없습니다",
        404: "데이터를 찾을 수 없습니다",
        409: "데이터 충돌",
        422: "잘못된 입력",
        429: "요청이 너무 많습니다",
        500: "서버 오류",
        503: "서비스를 사용할 수 없습니다",
        "default": "요청을 완료하지 못했습니다",
    },
    "zh-TW": {
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
        "default": "請求未完成",
    },
    "zh-CN": {
        400: "请求内容不正确",
        401: "需要登录",
        402: "可用次数不足",
        403: "没有操作权限",
        404: "找不到数据",
        409: "数据状态冲突",
        422: "输入内容不正确",
        429: "操作太频繁",
        500: "服务器发生错误",
        503: "服务暂时无法使用",
        "default": "请求未完成",
    },
}

GENERIC_DETAILS: dict[Locale, str] = {
    "en": "The request could not be completed. Please try again.",
    "ja": "リクエストを完了できませんでした。もう一度お試しください。",
    "ko": "요청을 완료하지 못했습니다. 다시 시도해 주세요.",
    "zh-TW": "請求未完成，請稍後再試。",
    "zh-CN": "请求未完成，请稍后再试。",
}

ERROR_DETAILS: dict[Locale, dict[str, str]] = {
    "en": {
        "authentication_required": "Sign in to continue",
        "invalid_credentials": "Incorrect email or password",
        "email_exists": "This email is already registered",
        "invalid_token": "Your session expired. Sign in again.",
        "inactive_user": "This account is currently unavailable",
        "rate_limited": "Too many attempts. Try again later.",
        "rate_limit_exceeded": "Too many attempts. Try again later.",
        "insufficient_uses": "You need more uses to continue",
        "trip_not_found": "This trip could not be found",
        "search_not_found": "This search could not be found",
        "hotspot_not_found": "This attraction could not be found",
        "hotspot_guide_not_found": "This introduction is no longer available",
        "hotspot_guide_url_invalid": "Use a public HTTPS introduction link",
        "hotspot_guide_youtube_url_invalid": "This YouTube URL is not supported",
        "hotspot_guide_youtube_not_configured": "YouTube discovery is not configured",
        "hotspot_guide_metadata_required": "Article title and website are required",
    },
    "ja": {
        "authentication_required": "続行するにはログインしてください",
        "invalid_credentials": "メールアドレスまたはパスワードが正しくありません",
        "email_exists": "このメールアドレスは登録済みです",
        "invalid_token": "ログインの有効期限が切れました。再度ログインしてください",
        "inactive_user": "このアカウントは現在利用できません",
        "rate_limited": "操作が多すぎます。しばらくしてからお試しください",
        "rate_limit_exceeded": "操作が多すぎます。しばらくしてからお試しください",
        "insufficient_uses": "続行するには利用回数を追加してください",
        "trip_not_found": "旅行が見つかりません",
        "search_not_found": "検索が見つかりません",
        "hotspot_not_found": "観光スポットが見つかりません",
        "hotspot_guide_not_found": "この紹介は利用できません",
        "hotspot_guide_url_invalid": "公開HTTPSリンクを入力してください",
        "hotspot_guide_youtube_url_invalid": "対応していないYouTube URLです",
        "hotspot_guide_youtube_not_configured": "YouTube検索が設定されていません",
        "hotspot_guide_metadata_required": "記事タイトルとサイト名を入力してください",
    },
    "ko": {
        "authentication_required": "계속하려면 로그인하세요",
        "invalid_credentials": "이메일 또는 비밀번호가 올바르지 않습니다",
        "email_exists": "이미 등록된 이메일입니다",
        "invalid_token": "로그인이 만료되었습니다. 다시 로그인하세요",
        "inactive_user": "현재 사용할 수 없는 계정입니다",
        "rate_limited": "요청이 너무 많습니다. 잠시 후 다시 시도하세요",
        "rate_limit_exceeded": "요청이 너무 많습니다. 잠시 후 다시 시도하세요",
        "insufficient_uses": "계속하려면 사용 횟수를 추가하세요",
        "trip_not_found": "여행을 찾을 수 없습니다",
        "search_not_found": "검색을 찾을 수 없습니다",
        "hotspot_not_found": "명소를 찾을 수 없습니다",
        "hotspot_guide_not_found": "이 소개는 더 이상 사용할 수 없습니다",
        "hotspot_guide_url_invalid": "공개 HTTPS 소개 링크를 입력하세요",
        "hotspot_guide_youtube_url_invalid": "지원하지 않는 YouTube URL입니다",
        "hotspot_guide_youtube_not_configured": "YouTube 탐색이 설정되지 않았습니다",
        "hotspot_guide_metadata_required": "글 제목과 사이트 이름이 필요합니다",
    },
    "zh-TW": {
        "hotspot_not_found": "找不到這個景點",
        "hotspot_guide_not_found": "這筆景點介紹已無法使用",
        "hotspot_guide_url_invalid": "請使用公開 HTTPS 介紹連結",
        "hotspot_guide_youtube_url_invalid": "無法辨識這個 YouTube 連結",
        "hotspot_guide_youtube_not_configured": "尚未設定 YouTube 內容探索",
        "hotspot_guide_metadata_required": "手動文章需要標題與網站名稱",
    },
    "zh-CN": {
        "authentication_required": "请先登录后再继续",
        "invalid_credentials": "Email 或密码不正确",
        "email_exists": "这个 Email 已经注册",
        "invalid_token": "登录状态已失效，请重新登录",
        "inactive_user": "这个账号目前无法使用",
        "rate_limited": "操作太频繁，请稍后再试",
        "rate_limit_exceeded": "操作太频繁，请稍后再试",
        "insufficient_uses": "可用次数不足，请先获取更多次数",
        "trip_not_found": "找不到这个旅程",
        "search_not_found": "找不到这次搜索",
        "hotspot_not_found": "找不到这个景点",
        "hotspot_guide_not_found": "这条景点介绍已不可用",
        "hotspot_guide_url_invalid": "请使用公开 HTTPS 介绍链接",
        "hotspot_guide_youtube_url_invalid": "无法识别这个 YouTube 链接",
        "hotspot_guide_youtube_not_configured": "尚未设置 YouTube 内容探索",
        "hotspot_guide_metadata_required": "手动文章需要标题和网站名称",
    },
}


def request_locale(headers: object) -> Locale:
    getter = getattr(headers, "get", None)
    return normalize_locale(getter("x-travel-locale") if callable(getter) else None)


def normalize_locale(value: str | None) -> Locale:
    if value in LOCALES:
        return cast(Locale, value)
    return DEFAULT_LOCALE


async def current_locale(
    x_travel_locale: Annotated[str | None, Header()] = None,
) -> Locale:
    return normalize_locale(x_travel_locale)


def provider_locale(provider: str, locale: Locale) -> str:
    return PROVIDER_LOCALES.get(provider, PROVIDER_LOCALES["google"])[locale]
