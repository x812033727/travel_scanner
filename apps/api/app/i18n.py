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

OAUTH_ERROR_DETAILS: dict[Locale, dict[str, str]] = {
    "en": {
        "password_not_set": "This account does not have a password yet",
        "oauth_cancelled": "Sign-in was cancelled",
        "oauth_state_invalid": "This sign-in request expired. Please try again.",
        "oauth_state_unavailable": "Sign-in verification is temporarily unavailable",
        "oauth_nonce_invalid": "This sign-in request is no longer valid",
        "oauth_token_invalid": "The provider could not verify this account",
        "oauth_secret_unreadable": "The provider credential could not be read",
        "oauth_email_required": "A verified email is required to create an account",
        "oauth_account_exists": (
            "An account already uses this email. Sign in and link it from Account."
        ),
        "oauth_identity_conflict": "This provider account is linked to another member",
        "oauth_identity_revoked": "Sign in and link this provider account again",
        "oauth_provider_unavailable": "This sign-in provider is not configured",
        "oauth_link_session_invalid": "The account-linking session expired",
        "oauth_identity_not_found": "This sign-in method could not be found",
        "oauth_last_method": "Keep at least one working sign-in method",
    },
    "ja": {
        "password_not_set": "このアカウントにはまだパスワードがありません",
        "oauth_cancelled": "ログインをキャンセルしました",
        "oauth_state_invalid": "ログイン操作の有効期限が切れました。もう一度お試しください",
        "oauth_state_unavailable": "ログイン確認を一時的に利用できません",
        "oauth_nonce_invalid": "このログイン操作は無効です",
        "oauth_token_invalid": "プロバイダーでアカウントを確認できませんでした",
        "oauth_secret_unreadable": "ログイン資格情報を読み取れませんでした",
        "oauth_email_required": "アカウント作成には確認済みメールアドレスが必要です",
        "oauth_account_exists": (
            "このメールのアカウントは既にあります。ログイン後、アカウント画面で連携してください"
        ),
        "oauth_identity_conflict": "このプロバイダーアカウントは別の会員に連携されています",
        "oauth_identity_revoked": "ログイン後、このプロバイダーを再連携してください",
        "oauth_provider_unavailable": "このログイン方法は未設定です",
        "oauth_link_session_invalid": "アカウント連携の有効期限が切れました",
        "oauth_identity_not_found": "このログイン方法が見つかりません",
        "oauth_last_method": "利用可能なログイン方法を1つ以上残してください",
    },
    "ko": {
        "password_not_set": "이 계정에는 아직 비밀번호가 없습니다",
        "oauth_cancelled": "로그인을 취소했습니다",
        "oauth_state_invalid": "로그인 요청이 만료되었습니다. 다시 시도하세요",
        "oauth_state_unavailable": "로그인 확인을 일시적으로 사용할 수 없습니다",
        "oauth_nonce_invalid": "이 로그인 요청은 더 이상 유효하지 않습니다",
        "oauth_token_invalid": "제공자가 이 계정을 확인하지 못했습니다",
        "oauth_secret_unreadable": "로그인 자격 증명을 읽을 수 없습니다",
        "oauth_email_required": "계정을 만들려면 확인된 이메일이 필요합니다",
        "oauth_account_exists": (
            "이 이메일을 사용하는 계정이 있습니다. 로그인 후 계정 화면에서 연결하세요"
        ),
        "oauth_identity_conflict": "이 제공자 계정은 다른 회원에게 연결되어 있습니다",
        "oauth_identity_revoked": "로그인 후 이 제공자 계정을 다시 연결하세요",
        "oauth_provider_unavailable": "이 로그인 방법이 설정되지 않았습니다",
        "oauth_link_session_invalid": "계정 연결 세션이 만료되었습니다",
        "oauth_identity_not_found": "이 로그인 방법을 찾을 수 없습니다",
        "oauth_last_method": "사용 가능한 로그인 방법을 하나 이상 유지하세요",
    },
    "zh-TW": {
        "password_not_set": "這個帳號尚未設定密碼",
        "oauth_cancelled": "已取消登入",
        "oauth_state_invalid": "登入驗證已失效，請重新操作",
        "oauth_state_unavailable": "登入驗證服務暫時無法使用",
        "oauth_nonce_invalid": "登入驗證已失效，請重新操作",
        "oauth_token_invalid": "登入身份驗證失敗",
        "oauth_secret_unreadable": "登入憑證無法解密",
        "oauth_email_required": "首次建立帳號需要已驗證的 Email",
        "oauth_account_exists": "此 Email 已有帳號，請先登入再到帳號頁連結",
        "oauth_identity_conflict": "這個登入帳號已連結其他會員",
        "oauth_identity_revoked": "請登入後重新連結此登入方式",
        "oauth_provider_unavailable": "這個登入方式尚未設定",
        "oauth_link_session_invalid": "帳號連結工作階段已失效",
        "oauth_identity_not_found": "找不到這個登入方式",
        "oauth_last_method": "至少需要保留一種可用的登入方式",
    },
    "zh-CN": {
        "password_not_set": "这个账号尚未设置密码",
        "oauth_cancelled": "已取消登录",
        "oauth_state_invalid": "登录验证已失效，请重新操作",
        "oauth_state_unavailable": "登录验证服务暂时无法使用",
        "oauth_nonce_invalid": "登录验证已失效，请重新操作",
        "oauth_token_invalid": "登录身份验证失败",
        "oauth_secret_unreadable": "无法读取登录凭证",
        "oauth_email_required": "首次创建账号需要已验证的邮箱",
        "oauth_account_exists": "此邮箱已有账号，请先登录再到账户页关联",
        "oauth_identity_conflict": "这个登录账号已关联其他会员",
        "oauth_identity_revoked": "请登录后重新关联此登录方式",
        "oauth_provider_unavailable": "这个登录方式尚未设置",
        "oauth_link_session_invalid": "账号关联会话已失效",
        "oauth_identity_not_found": "找不到这个登录方式",
        "oauth_last_method": "至少需要保留一种可用的登录方式",
    },
}

ERROR_DETAILS: dict[Locale, dict[str, str]] = {
    "en": {
        **OAUTH_ERROR_DETAILS["en"],
        "authentication_required": "Sign in to continue",
        "invalid_credentials": "Incorrect email or password",
        "email_exists": "This email is already registered",
        "admin_email_reserved": (
            "This email is reserved for an administrator. "
            "Ask the host administrator to create the account."
        ),
        "request_too_large": "The request is too large",
        "session_check_unavailable": (
            "The sign-in service is temporarily unavailable. Try again later."
        ),
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
        "hotspot_guide_ai_search_disabled": "AI attraction research is disabled",
        "hotspot_guide_ai_provider_not_configured": "The selected AI provider is not configured",
        "hotspot_guide_brave_not_configured": "Article research requires Brave Search",
        "hotspot_guide_ai_quota_exhausted": "Today's AI research quota is exhausted",
        "hotspot_guide_ai_search_not_found": "This AI research run could not be found",
        "hotspot_coordinates_missing": "This attraction does not have coordinates yet",
        "restaurant_google_not_configured": "Google restaurant search is not configured",
        "restaurant_google_budget_exhausted": (
            "This month's restaurant search safety budget is exhausted"
        ),
        "restaurant_provider_unavailable": "Google restaurant data is temporarily unavailable",
        "restaurant_hotspot_required": "Choose at least one attraction to scan",
        "restaurant_scan_not_found": "This restaurant scan could not be found",
        "restaurant_place_not_found": "This dining place could not be found",
        "restaurant_place_id_or_maps_url_required": "Enter a Google Place ID or Google Maps URL",
        "restaurant_maps_url_invalid": "Use a valid Google Maps HTTPS URL",
        "restaurant_maps_url_host_invalid": "Only official Google Maps URLs are accepted",
        "restaurant_maps_url_unavailable": "The Google Maps short URL could not be expanded",
        "restaurant_maps_redirect_limit": "The Google Maps URL redirected too many times",
        "restaurant_import_query_required": "Add a restaurant name or address for IDs Only search",
        "restaurant_import_in_progress": "The same import is already in progress",
        "restaurant_import_idempotency_unavailable": (
            "Safe duplicate prevention is temporarily unavailable"
        ),
        "restaurant_threshold_not_met": "The place needs at least 3.8 stars and 1,000 reviews",
        "restaurant_location_unavailable": (
            "The restaurant or attraction has no comparable location"
        ),
        "restaurant_outside_hotspot_radius": (
            "The restaurant is more than 10 km from the attraction"
        ),
        "restaurant_source_url_invalid": "Use a public HTTPS source URL",
        "restaurant_source_provider_owned": "A map page cannot support owned editorial data",
        "restaurant_source_url_private": "The source URL cannot point to a private network",
        "restaurant_source_claims_invalid": "Choose the fields supported by this source",
        "restaurant_coordinate_pair_required": "Ride latitude and longitude are both required",
        "restaurant_source_evidence_missing": "Some fields do not have official source evidence",
        "restaurant_editorial_name_required": "Enter a source-backed restaurant name",
        "trip_meal_slot_unavailable": "This day does not have an available meal slot",
        "trip_version_conflict": "This trip was updated elsewhere. Reload it and try again.",
        "trip_date_change_ambiguous": (
            "Choose either shifting the whole trip or setting explicit dates, not both"
        ),
        "trip_dates_unset": "This trip has no dates yet. Set a start and end date first.",
        "trip_dates_required": "Provide both a start date and an end date",
        "trip_date_out_of_bounds": "These dates are outside the supported range",
        "trip_date_range_invalid": "The end date cannot be before the start date",
        "trip_date_range_too_long": "A trip can be at most 61 days long",
        "trip_item_day_missing": (
            "Some items have no assigned day yet. Schedule them before changing the trip dates."
        ),
        "trip_shrink_confirmation_required": (
            "Shortening the trip deletes the plans on the removed days. Confirm to continue."
        ),
        "trip_search_dates_diverged": (
            "The trip dates no longer match the original search, so it cannot be repriced. "
            "Run a new search and save it as a trip."
        ),
    },
    "ja": {
        **OAUTH_ERROR_DETAILS["ja"],
        "authentication_required": "続行するにはログインしてください",
        "invalid_credentials": "メールアドレスまたはパスワードが正しくありません",
        "email_exists": "このメールアドレスは登録済みです",
        "admin_email_reserved": (
            "このメールアドレスは管理者用に予約されています。"
            "ホスト管理者にアカウント作成を依頼してください"
        ),
        "request_too_large": "リクエストが大きすぎます",
        "session_check_unavailable": (
            "ログインサービスが一時的に利用できません。しばらくしてからお試しください"
        ),
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
        "hotspot_guide_ai_search_disabled": "AIスポット検索は停止中です",
        "hotspot_guide_ai_provider_not_configured": "選択したAIプロバイダーは未設定です",
        "hotspot_guide_brave_not_configured": "記事検索にはBrave Searchが必要です",
        "hotspot_guide_ai_quota_exhausted": "本日のAI検索上限に達しました",
        "hotspot_guide_ai_search_not_found": "AI検索が見つかりません",
        "hotspot_coordinates_missing": "このスポットには座標がありません",
        "restaurant_google_not_configured": "Google レストラン検索は未設定です",
        "restaurant_google_budget_exhausted": "今月のレストラン検索安全上限に達しました",
        "restaurant_provider_unavailable": "Google レストラン情報を取得できません",
        "restaurant_hotspot_required": "スキャンするスポットを選択してください",
        "restaurant_scan_not_found": "レストランスキャンが見つかりません",
        "restaurant_place_not_found": "この飲食店が見つかりません",
        "restaurant_place_id_or_maps_url_required": (
            "Google Place IDまたはMaps URLを入力してください"
        ),
        "restaurant_maps_url_invalid": "有効なGoogle Maps HTTPS URLを使用してください",
        "restaurant_maps_url_host_invalid": "Google公式の地図URLのみ利用できます",
        "restaurant_maps_url_unavailable": "短縮URLを展開できませんでした",
        "restaurant_maps_redirect_limit": "地図URLの転送回数が多すぎます",
        "restaurant_import_query_required": "IDs Only検索用の店名または住所を入力してください",
        "restaurant_import_in_progress": "同じインポートを処理中です",
        "restaurant_import_idempotency_unavailable": "重複防止を一時的に利用できません",
        "restaurant_threshold_not_met": "評価3.8以上、口コミ1,000件以上が必要です",
        "restaurant_location_unavailable": "店舗またはスポットの比較用座標がありません",
        "restaurant_outside_hotspot_radius": "店舗はスポットから10 km以上離れています",
        "restaurant_source_url_invalid": "公開HTTPS情報源を使用してください",
        "restaurant_source_provider_owned": "地図ページは編集情報の根拠にできません",
        "restaurant_source_url_private": "内部ネットワークURLは利用できません",
        "restaurant_source_claims_invalid": "情報源が裏付ける項目を選択してください",
        "restaurant_coordinate_pair_required": "配車用の緯度と経度を両方入力してください",
        "restaurant_source_evidence_missing": "一部項目に公式情報源の根拠がありません",
        "restaurant_editorial_name_required": "情報源で確認できる店名を入力してください",
        "trip_meal_slot_unavailable": "この日には利用可能な食事枠がありません",
        "trip_version_conflict": (
            "旅行が別の場所で更新されました。再読み込みしてやり直してください。"
        ),
        "trip_date_change_ambiguous": (
            "全体の平行移動か日付の直接指定か、どちらか一方を選んでください"
        ),
        "trip_dates_unset": (
            "この旅行にはまだ日付がありません。開始日と終了日を先に設定してください。"
        ),
        "trip_dates_required": "開始日と終了日の両方を指定してください",
        "trip_date_out_of_bounds": "対応できる範囲外の日付です",
        "trip_date_range_invalid": "終了日は開始日より前にできません",
        "trip_date_range_too_long": "旅行は最長 61 日までです",
        "trip_item_day_missing": (
            "日付未設定の項目があります。先に予定へ組み込んでから日程を変更してください。"
        ),
        "trip_shrink_confirmation_required": (
            "旅行を短縮すると削除される日の予定が消えます。確認のうえ実行してください。"
        ),
        "trip_search_dates_diverged": (
            "旅行の日程が元の検索と一致しないため、再見積もりできません。新しく検索して保存してください。"
        ),
    },
    "ko": {
        **OAUTH_ERROR_DETAILS["ko"],
        "authentication_required": "계속하려면 로그인하세요",
        "invalid_credentials": "이메일 또는 비밀번호가 올바르지 않습니다",
        "email_exists": "이미 등록된 이메일입니다",
        "admin_email_reserved": (
            "이 이메일은 관리자용으로 예약되어 있습니다. "
            "호스트 관리자에게 계정 생성을 요청하세요"
        ),
        "request_too_large": "요청 내용이 너무 큽니다",
        "session_check_unavailable": (
            "로그인 서비스를 일시적으로 사용할 수 없습니다. 잠시 후 다시 시도해 주세요"
        ),
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
        "hotspot_guide_ai_search_disabled": "AI 명소 검색이 중지되었습니다",
        "hotspot_guide_ai_provider_not_configured": "선택한 AI 제공자가 설정되지 않았습니다",
        "hotspot_guide_brave_not_configured": "글 검색에는 Brave Search가 필요합니다",
        "hotspot_guide_ai_quota_exhausted": "오늘의 AI 검색 한도를 모두 사용했습니다",
        "hotspot_guide_ai_search_not_found": "AI 검색 실행을 찾을 수 없습니다",
        "hotspot_coordinates_missing": "이 명소에는 좌표가 없습니다",
        "restaurant_google_not_configured": "Google 음식점 검색이 설정되지 않았습니다",
        "restaurant_google_budget_exhausted": "이번 달 음식점 검색 안전 한도를 모두 사용했습니다",
        "restaurant_provider_unavailable": "Google 음식점 정보를 일시적으로 가져올 수 없습니다",
        "restaurant_hotspot_required": "스캔할 명소를 선택하세요",
        "restaurant_scan_not_found": "음식점 스캔을 찾을 수 없습니다",
        "restaurant_place_not_found": "이 음식점을 찾을 수 없습니다",
        "restaurant_place_id_or_maps_url_required": "Google Place ID 또는 Maps URL을 입력하세요",
        "restaurant_maps_url_invalid": "올바른 Google Maps HTTPS URL을 사용하세요",
        "restaurant_maps_url_host_invalid": "Google 공식 지도 URL만 사용할 수 있습니다",
        "restaurant_maps_url_unavailable": "단축 URL을 확장할 수 없습니다",
        "restaurant_maps_redirect_limit": "지도 URL 리디렉션이 너무 많습니다",
        "restaurant_import_query_required": "IDs Only 검색용 상호명 또는 주소를 입력하세요",
        "restaurant_import_in_progress": "동일한 가져오기를 처리 중입니다",
        "restaurant_import_idempotency_unavailable": "중복 방지를 일시적으로 사용할 수 없습니다",
        "restaurant_threshold_not_met": "평점 3.8 이상, 리뷰 1,000개 이상이어야 합니다",
        "restaurant_location_unavailable": "음식점 또는 명소의 비교 좌표가 없습니다",
        "restaurant_outside_hotspot_radius": "음식점이 명소에서 10 km 이상 떨어져 있습니다",
        "restaurant_source_url_invalid": "공개 HTTPS 출처 URL을 사용하세요",
        "restaurant_source_provider_owned": "지도 페이지는 편집 자료의 근거가 될 수 없습니다",
        "restaurant_source_url_private": "내부 네트워크 URL은 사용할 수 없습니다",
        "restaurant_source_claims_invalid": "출처가 뒷받침하는 항목을 선택하세요",
        "restaurant_coordinate_pair_required": "호출용 위도와 경도를 모두 입력하세요",
        "restaurant_source_evidence_missing": "일부 항목에 공식 출처 근거가 없습니다",
        "restaurant_editorial_name_required": "출처로 확인된 상호명을 입력하세요",
        "trip_meal_slot_unavailable": "이 날짜에는 사용할 수 있는 식사 슬롯이 없습니다",
        "trip_version_conflict": (
            "여행이 다른 곳에서 업데이트되었습니다. 다시 불러온 뒤 시도하세요."
        ),
        "trip_date_change_ambiguous": "전체 이동과 날짜 직접 지정 중 하나만 선택하세요",
        "trip_dates_unset": "이 여행에는 아직 날짜가 없습니다. 시작일과 종료일을 먼저 설정하세요.",
        "trip_dates_required": "시작일과 종료일을 모두 입력하세요",
        "trip_date_out_of_bounds": "지원 범위를 벗어난 날짜입니다",
        "trip_date_range_invalid": "종료일은 시작일보다 빠를 수 없습니다",
        "trip_date_range_too_long": "여행은 최대 61일까지 가능합니다",
        "trip_item_day_missing": (
            "날짜가 지정되지 않은 항목이 있습니다. 먼저 일정에 배치한 뒤 날짜를 변경하세요."
        ),
        "trip_shrink_confirmation_required": (
            "여행을 줄이면 제외되는 날의 일정이 삭제됩니다. 확인 후 진행하세요."
        ),
        "trip_search_dates_diverged": (
            "여행 날짜가 원래 검색과 달라 다시 견적을 낼 수 없습니다. 새로 검색한 뒤 저장하세요."
        ),
    },
    "zh-TW": {
        **OAUTH_ERROR_DETAILS["zh-TW"],
        "hotspot_not_found": "找不到這個景點",
        "hotspot_guide_not_found": "這筆景點介紹已無法使用",
        "hotspot_guide_url_invalid": "請使用公開 HTTPS 介紹連結",
        "hotspot_guide_youtube_url_invalid": "無法辨識這個 YouTube 連結",
        "hotspot_guide_youtube_not_configured": "尚未設定 YouTube 內容探索",
        "hotspot_guide_metadata_required": "手動文章需要標題與網站名稱",
        "hotspot_guide_ai_search_disabled": "AI 景點搜尋目前未啟用",
        "hotspot_guide_ai_provider_not_configured": "所選 AI 供應商尚未設定",
        "hotspot_guide_brave_not_configured": "文章搜尋需要 Brave Search 設定",
        "hotspot_guide_ai_quota_exhausted": "今日 AI 搜尋執行額度已用完",
        "hotspot_guide_ai_search_not_found": "找不到這次 AI 搜尋",
        "hotspot_coordinates_missing": "這個景點尚未設定座標",
        "restaurant_google_not_configured": "Google 餐廳搜尋尚未啟用",
        "restaurant_google_budget_exhausted": "本月餐廳搜尋安全額度已用完",
        "restaurant_provider_unavailable": "Google 餐廳資料目前無法取得",
        "restaurant_hotspot_required": "請選擇要掃描的景點",
        "restaurant_scan_not_found": "找不到這次餐廳掃描",
        "restaurant_place_not_found": "找不到這個餐飲地點",
        "restaurant_place_id_or_maps_url_required": "請輸入 Google Place ID 或 Maps 網址",
        "restaurant_maps_url_invalid": "請使用有效的 Google Maps HTTPS 網址",
        "restaurant_maps_url_host_invalid": "只接受 Google 官方地圖網址",
        "restaurant_maps_url_unavailable": "目前無法展開 Google Maps 短網址",
        "restaurant_maps_redirect_limit": "Google Maps 網址重新導向過多",
        "restaurant_import_query_required": "請補上店名或地址以執行 IDs Only 搜尋",
        "restaurant_import_in_progress": "相同匯入正在處理中",
        "restaurant_import_idempotency_unavailable": "目前無法安全保證匯入不重複",
        "restaurant_threshold_not_met": "店家必須至少 3.8 顆星且有 1,000 則評論",
        "restaurant_location_unavailable": "店家或景點缺少可比對座標",
        "restaurant_outside_hotspot_radius": "店家距離景點超過 10 公里",
        "restaurant_source_url_invalid": "請使用公開 HTTPS 來源網址",
        "restaurant_source_provider_owned": "地圖頁不可當成自有編輯資料來源",
        "restaurant_source_url_private": "來源網址不可指向內部網路",
        "restaurant_source_claims_invalid": "請選擇這筆來源實際佐證的欄位",
        "restaurant_coordinate_pair_required": "叫車座標必須同時提供經緯度",
        "restaurant_source_evidence_missing": "部分欄位缺少官方來源佐證",
        "restaurant_editorial_name_required": "請輸入可由來源佐證的店名",
        "trip_meal_slot_unavailable": "這一天沒有可設定的餐食卡",
    },
    "zh-CN": {
        **OAUTH_ERROR_DETAILS["zh-CN"],
        "authentication_required": "请先登录后再继续",
        "invalid_credentials": "Email 或密码不正确",
        "email_exists": "这个 Email 已经注册",
        "admin_email_reserved": "这个 Email 已保留给系统管理员，请由主机管理员建立账号",
        "request_too_large": "请求内容超过允许大小",
        "session_check_unavailable": "登录状态服务暂时无法使用，请稍后再试",
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
        "hotspot_guide_ai_search_disabled": "AI 景点搜索目前未启用",
        "hotspot_guide_ai_provider_not_configured": "所选 AI 供应商尚未设置",
        "hotspot_guide_brave_not_configured": "文章搜索需要 Brave Search 设置",
        "hotspot_guide_ai_quota_exhausted": "今日 AI 搜索执行额度已用完",
        "hotspot_guide_ai_search_not_found": "找不到这次 AI 搜索",
        "hotspot_coordinates_missing": "这个景点尚未设置坐标",
        "restaurant_google_not_configured": "Google 餐厅搜索尚未启用",
        "restaurant_google_budget_exhausted": "本月餐厅搜索安全额度已用完",
        "restaurant_provider_unavailable": "Google 餐厅数据目前无法获取",
        "restaurant_hotspot_required": "请选择要扫描的景点",
        "restaurant_scan_not_found": "找不到这次餐厅扫描",
        "restaurant_place_not_found": "找不到这个餐饮地点",
        "restaurant_place_id_or_maps_url_required": "请输入 Google Place ID 或 Maps 链接",
        "restaurant_maps_url_invalid": "请使用有效的 Google Maps HTTPS 链接",
        "restaurant_maps_url_host_invalid": "仅接受 Google 官方地图链接",
        "restaurant_maps_url_unavailable": "目前无法展开 Google Maps 短链接",
        "restaurant_maps_redirect_limit": "Google Maps 链接重定向过多",
        "restaurant_import_query_required": "请补充店名或地址以执行 IDs Only 搜索",
        "restaurant_import_in_progress": "相同导入正在处理中",
        "restaurant_import_idempotency_unavailable": "目前无法安全保证导入不重复",
        "restaurant_threshold_not_met": "商家必须至少 3.8 星且有 1,000 条评论",
        "restaurant_location_unavailable": "商家或景点缺少可比对坐标",
        "restaurant_outside_hotspot_radius": "商家距离景点超过 10 公里",
        "restaurant_source_url_invalid": "请使用公开 HTTPS 来源链接",
        "restaurant_source_provider_owned": "地图页不可作为自有编辑资料来源",
        "restaurant_source_url_private": "来源链接不可指向内部网络",
        "restaurant_source_claims_invalid": "请选择该来源实际佐证的字段",
        "restaurant_coordinate_pair_required": "叫车坐标必须同时提供经纬度",
        "restaurant_source_evidence_missing": "部分字段缺少官方来源佐证",
        "restaurant_editorial_name_required": "请输入可由来源佐证的店名",
        "trip_meal_slot_unavailable": "这一天没有可设置的餐食卡",
        "trip_version_conflict": "旅程已在其他地方更新，请重新载入后再操作",
        "trip_date_change_ambiguous": "请选择整趟平移，或直接指定开始与结束日期，不能同时使用",
        "trip_dates_unset": "这趟旅程还没有日期，请先指定开始与结束日期",
        "trip_dates_required": "请同时提供开始日期与结束日期",
        "trip_date_out_of_bounds": "旅程日期超出可支持的范围",
        "trip_date_range_invalid": "结束日期不可早于开始日期",
        "trip_date_range_too_long": "旅程最长 61 天",
        "trip_item_day_missing": "旅程中有尚未指定日期的项目，请先安排它们再调整旅程日期",
        "trip_shrink_confirmation_required": "缩短旅程会删除被移除日期上的安排，请确认后再执行",
        "trip_search_dates_diverged": (
            "旅程日期已与原始搜索不同，无法用旧搜索重新询价；请重新搜索后另存旅程"
        ),
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
