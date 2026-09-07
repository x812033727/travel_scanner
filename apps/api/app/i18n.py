from contextvars import ContextVar, Token
from typing import Annotated, Literal, cast

from fastapi import Header

Locale = Literal["en", "ja", "ko", "zh-TW", "zh-CN"]
LOCALES: tuple[Locale, ...] = ("en", "ja", "ko", "zh-TW", "zh-CN")
DEFAULT_LOCALE: Locale = "zh-TW"

# The locale of the request being served, bound by RequestContextMiddleware so
# deep serializers (trip items, for one) can localize without every caller
# threading the header through. Outside a request it is the site default.
_request_locale: ContextVar[Locale] = ContextVar("request_locale", default=DEFAULT_LOCALE)

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
            # Added 2026-09-07: every public error code the API raises now says what
        # went wrong. Before this a reader outside zh-TW got GENERIC_DETAILS —
        # one sentence for 124 different problems.
        "admin_required": "This is for system administrators only",
        "affiliate_link_expired": "This partner link has expired. Refresh the page and try again",
        "affiliate_link_invalid": "This partner link is not valid",
        "affiliate_link_not_found": "That partner link could not be found",
        "affiliate_partner_not_found": "That partner could not be found",
        "affiliate_source_invalid": "Choose a search or a saved trip first",
        "ai_planner_unavailable": (
            "The AI planner is temporarily unavailable and did not read your description. Try "
            "again shortly"
        ),
        "alert_exists": "This item already has a price alert",
        "alert_limit_reached": "You have reached the limit of 20 price alerts",
        "alert_not_found": "That price alert could not be found",
        "alert_resource_not_found": "There is nothing to track at that price",
        "alert_update_empty": "Change at least one field of the price alert",
        "area_requires_destination": "Filtering by area needs a destination as well",
        "clickout_unavailable": "No secure booking link is available right now",
        "day_outside_trip": "That day is outside the trip's dates",
        "dependencies_unavailable": "The database, its schema or Redis is unavailable",
        "deployment_admin_required": "This is for deployment administrators only",
        "destination_id_required": "Use destination_id for an extension city",
        "destination_mismatch": "city_code and destination_id do not agree",
        "destination_required": "Give either city_code or destination_id",
        "expense_not_found": "That expense could not be found",
        "flight_anchor_unavailable": "The trip's dates are incomplete, so a flight cannot be set",
        "flight_status_item_not_found": "That flight item could not be found",
        "flight_status_lookup_expired": "This flight status lookup has expired",
        "flight_status_lookup_not_found": "That flight status lookup could not be found",
        "flight_track_unavailable": "The schedule has no actual track for this flight yet",
        "flightaware_not_configured": "FlightAware flight status is not enabled",
        "flightaware_unavailable": (
            "FlightAware data is unavailable right now. Please try again later"
        ),
        "food_merchant_location_unverified": "This shop's location has not been verified yet",
        "fx_rate_unavailable": "That exchange rate is unavailable right now",
        "holiday_country_unknown": "There is no holiday data for that country",
        "holiday_range_invalid": "The end date is before the start date",
        "holiday_range_too_wide": "Holidays can be looked up three years at a time",
        "hotel_offer_expired": (
            "This offer has expired. Refresh the hotel comparison and choose again"
        ),
        "hotspot_official_website_invalid": "An official website must be a public HTTPS URL",
        "hotspot_official_website_not_official": (
            "This address is not an official website we can approve"
        ),
        "hotspot_source_not_found": "That source could not be found",
        "idempotency_key_required": "An Idempotency-Key header is required",
        "idempotency_key_reused": (
            "This Idempotency-Key has already been used for another operation"
        ),
        "idempotency_result_unavailable": (
            "This Idempotency-Key has no replayable result; use a new key"
        ),
        "invalid_external_reference": "An external reference must be 1 to 200 characters",
        "invalid_food_cursor": "That food page cursor is not valid",
        "invalid_line_link_token": "That LINE link token is not valid",
        "invalid_line_signature": "The LINE webhook signature is not valid",
        "invalid_line_webhook": "The LINE webhook payload is not valid",
        "invalid_place_bias": "A place search centre needs both a latitude and a longitude",
        "invalid_place_kinds": "Place kinds currently support cities only",
        "invalid_place_query": "A place keyword must be 2 to 120 characters",
        "invalid_place_regions": "Place search currently covers Japan, South Korea and Thailand",
        "invalid_session_token": "That place search session token is not valid",
        "invalid_usage_cursor": "That usage history cursor is not valid",
        "invalid_user": "This account cannot be used right now",
        "itinerary_candidate_invalid": (
            "The planner returned a place that does not exist in the catalog"
        ),
        "itinerary_candidates_changed": "Some places or shops have changed. Preview the plan again",
        "itinerary_date_out_of_range": "That meal date is outside the trip",
        "itinerary_exact_locations_required": (
            "There are not enough verified places or shops, so the plan is unchanged"
        ),
        "itinerary_optimization_limit": "Too many movable places in one day. Lock some items first",
        "itinerary_optimization_unavailable": "No comparable route result came back",
        "itinerary_optimization_unchanged": (
            "This is already the suggested order, so there is nothing to apply"
        ),
        "itinerary_preview_expired": "This plan preview has expired. Generate it again",
        "itinerary_preview_stale": "The plan's items have changed. Preview it again",
        "line_api_unavailable": "The LINE API is temporarily unavailable",
        "line_delivery_failed": "The LINE test message could not be sent right now",
        "line_friend_required": "Add the LINE official account as a friend again",
        "line_not_configured": "LINE price alerts are not enabled",
        "line_not_linked": "No LINE account is linked yet",
        "line_webhook_too_large": "The LINE webhook payload is too large",
        "location_resolve_in_progress": "The same place is already being matched. Please wait",
        "meal_skip_not_supported": "Only lunch and dinner can be skipped",
        "naver_maps_not_configured": "NAVER Maps place search is not enabled",
        "offer_expired": "This offer has expired. Check the price again before booking",
        "offer_not_found": "That offer could not be found",
        "offer_unreadable": "This offer can no longer be read",
        "photo_not_found": "No photo is available for this place",
        "photo_provider_unavailable": "The place photo service is temporarily unavailable",
        "place_not_found": "That place could not be found",
        "place_provider_not_configured": "Place search for South Korea is not enabled",
        "place_provider_not_found": "That place source is not supported",
        "plan_not_found": "That optimization result could not be found",
        "provider_not_configured": "No live pricing provider is available for this search",
        "provider_unavailable": "The original flight provider is unavailable right now",
        "rate_limit_unavailable": "The safety check service is temporarily unavailable",
        "registration_closed": "New accounts are paused right now",
        "route_apply_in_progress": "The same route is already being applied. Please wait",
        "route_compute_in_progress": "A route for the same day is already being calculated",
        "route_default_mode_mismatch": "Preview the day's default transport mode first",
        "route_items_insufficient": "At least two items with a location are needed",
        "route_items_invalid": "The start and the end must be items on the same day",
        "route_items_limit": "Too many places in one request. Pick a single day or a smaller range",
        "route_items_not_adjacent": (
            "Routes can only be calculated between adjacent items on the same day"
        ),
        "route_location_unavailable": "Confirm both of these places before looking up a route",
        "route_preview_expired": "This route preview has expired. Look it up again",
        "route_provider_not_configured": (
            "The routing service for this transport mode is not enabled yet"
        ),
        "route_queue_unavailable": "The background routing service is temporarily unavailable",
        "route_unavailable": "No usable route came back. Please try again later",
        "saved_item_not_found": "That saved item could not be found",
        "search_not_expandable": "This search is not the kind that can take more flight sources",
        "search_offers_unreadable": (
            "The flight offers saved with this search can no longer be read"
        ),
        "session_expired": "Your session has expired. Please sign in again",
        "shared_trip_not_found": "That shared trip could not be found",
        "system_itinerary_item_immutable": (
            "Fixed flight, hotel and meal cards can only be created by the system"
        ),
        "travel_provider_unavailable": "No live pricing provider is available for this trip",
        "trip_item_not_found": "That item could not be found",
        "trip_ledger_full": "This trip's expense list is full",
        "trip_ledger_not_empty": (
            "The currency cannot change while there are expenses. Clear them first"
        ),
        "trip_place_not_found": "That unscheduled place could not be found",
        "trip_places_empty": "Paste at least one place or Google Maps link",
        "trip_places_too_many_lines": "Too many places in one paste. Paste them in smaller batches",
        "trip_planning_fields_missing": (
            "The trip has no destination or dates, so it cannot be re-planned"
        ),
        "trip_reoptimization_unavailable": (
            "The providers returned no usable combination for this trip"
        ),
        "trip_search_missing": "The original search is no longer available",
        "unsupported_area": "This destination has no such area",
        "unsupported_city_code": "That city code is not supported",
        "unsupported_region": "Destination discovery covers Japan, South Korea and Thailand",
        "usage_balance_invalid": "The reserved-use balance is in an inconsistent state",
        "usage_operation_unknown": "That usage operation is not recognised",
        "usage_package_not_found": "That usage pack could not be found",
        "weather_api_not_enabled": (
            "The Google Weather API is not enabled, or the server key does not allow it"
        ),
        "weather_location_unavailable": (
            "The trip has no usable coordinates yet. Confirm at least one place first"
        ),
        "weather_not_configured": "The weather service is not set up",
        "weather_provider_rejected": (
            "MET Norway rejected the request; check the User-Agent setting"
        ),
        "weather_provider_unavailable": "Google Weather is temporarily not responding",
        "weather_rate_limited": "The Google Weather quota is temporarily exhausted",
        "weather_response_invalid": "The Google Weather response was incomplete",
        "food_area_not_found": "That area could not be found",
        "food_merchant_not_found": "That shop could not be found",
        "google_maps_not_configured": "Google Maps place data is not configured",
        "hotspot_intro_ai_quota_exhausted": "Today's introduction generation quota is used up",
        "queue_unavailable": "The background queue is temporarily unavailable",
        "unsupported_destination": "That destination link includes something we do not support",
        "usage_account_missing": "This account does not have a usage balance yet",
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
            # Added 2026-09-07: every public error code the API raises now says what
        # went wrong. Before this a reader outside zh-TW got GENERIC_DETAILS —
        # one sentence for 124 different problems.
        "admin_required": "この機能はシステム管理者専用です",
        "affiliate_link_expired": "提携リンクの有効期限が切れています。ページを更新してください",
        "affiliate_link_invalid": "この提携リンクは無効です",
        "affiliate_link_not_found": "提携リンクが見つかりません",
        "affiliate_partner_not_found": "提携先が見つかりません",
        "affiliate_source_invalid": "検索か保存済みの旅程を指定してください",
        "ai_planner_unavailable": (
            "AI プランナーが一時的に利用できず、入力内容は読み取られませんでした。"
            "しばらくしてからお試しください"
        ),
        "alert_exists": "この項目にはすでに価格通知があります",
        "alert_limit_reached": "価格通知は 20 件までです",
        "alert_not_found": "この価格通知が見つかりません",
        "alert_resource_not_found": "追跡できる価格の対象が見つかりません",
        "alert_update_empty": "価格通知の項目を少なくとも一つ変更してください",
        "area_requires_destination": "エリアで絞り込むには目的地の指定も必要です",
        "clickout_unavailable": "現在利用できる安全な予約リンクがありません",
        "day_outside_trip": "その日は旅程の期間外です",
        "dependencies_unavailable": "データベース、スキーマ、または Redis が利用できません",
        "deployment_admin_required": "この機能はデプロイ管理者専用です",
        "destination_id_required": "拡張都市には destination_id を使ってください",
        "destination_mismatch": "city_code と destination_id が一致しません",
        "destination_required": "city_code か destination_id のどちらかが必要です",
        "expense_not_found": "この明細が見つかりません",
        "flight_anchor_unavailable": "旅程の日付が揃っていないため、航空券を設定できません",
        "flight_status_item_not_found": "この航空券の項目が見つかりません",
        "flight_status_lookup_expired": "この運航状況の照会は期限切れです",
        "flight_status_lookup_not_found": "この運航状況の照会が見つかりません",
        "flight_track_unavailable": "この便の実際の航跡データはまだありません",
        "flightaware_not_configured": "FlightAware の運航状況は有効になっていません",
        "flightaware_unavailable": (
            "FlightAware の運航データを取得できません。"
            "しばらくしてからお試しください"
        ),
        "food_merchant_location_unverified": "この店舗の場所はまだ確認されていません",
        "fx_rate_unavailable": "この為替レートは現在取得できません",
        "holiday_country_unknown": "その国の祝日データはありません",
        "holiday_range_invalid": "終了日が開始日より前です",
        "holiday_range_too_wide": "祝日は一度に三年分まで照会できます",
        "hotel_offer_expired": "この料金は期限切れです。ホテル比較を更新してから選び直してください",
        "hotspot_official_website_invalid": (
            "公式サイトは公開された HTTPS の URL である必要があります"
        ),
        "hotspot_official_website_not_official": "この URL は承認できる公式サイトではありません",
        "hotspot_source_not_found": "このスポットの情報源が見つかりません",
        "idempotency_key_required": "Idempotency-Key ヘッダーが必要です",
        "idempotency_key_reused": "この Idempotency-Key は別の操作ですでに使われています",
        "idempotency_result_unavailable": (
            "この Idempotency-Key には再生できる結果がありません。"
            "新しいキーを使ってください"
        ),
        "invalid_external_reference": "外部参照は 1〜200 文字にしてください",
        "invalid_food_cursor": "グルメ一覧のページ位置が不正です",
        "invalid_line_link_token": "LINE の連携トークンの形式が正しくありません",
        "invalid_line_signature": "LINE Webhook の署名が無効です",
        "invalid_line_webhook": "LINE Webhook の形式が無効です",
        "invalid_place_bias": "地点検索の中心には緯度と経度の両方が必要です",
        "invalid_place_kinds": "地点の種類は現在 cities のみ対応しています",
        "invalid_place_query": "地点のキーワードは 2〜120 文字にしてください",
        "invalid_place_regions": "地点検索は現在、日本・韓国・タイに対応しています",
        "invalid_session_token": "地点検索のセッションコードの形式が正しくありません",
        "invalid_usage_cursor": "利用履歴のページ位置が不正です",
        "invalid_user": "このアカウントは現在利用できません",
        "itinerary_candidate_invalid": "AI が登録されていない場所を返しました",
        "itinerary_candidates_changed": (
            "一部のスポットや店舗が変更されました。もう一度プレビューしてください"
        ),
        "itinerary_date_out_of_range": "食事の日付が旅程の範囲外です",
        "itinerary_exact_locations_required": (
            "確認済みのスポットや店舗が足りないため、"
            "旅程は変更されません"
        ),
        "itinerary_optimization_limit": (
            "一日に最適化できる移動可能な場所が多すぎます。"
            "いくつか固定してください"
        ),
        "itinerary_optimization_unavailable": "比較できる動線の結果が得られませんでした",
        "itinerary_optimization_unchanged": (
            "すでに推奨どおりの並びなので、適用するものがありません"
        ),
        "itinerary_preview_expired": "旅程のプレビューが期限切れです。もう一度作成してください",
        "itinerary_preview_stale": "旅程の項目が変更されました。もう一度プレビューしてください",
        "line_api_unavailable": "LINE の API が一時的に利用できません",
        "line_delivery_failed": "LINE のテストメッセージを送信できませんでした",
        "line_friend_required": "LINE 公式アカウントを友だちに追加し直してください",
        "line_not_configured": "LINE の価格通知は有効になっていません",
        "line_not_linked": "LINE アカウントがまだ連携されていません",
        "line_webhook_too_large": "LINE Webhook の内容が大きすぎます",
        "location_resolve_in_progress": "同じ場所を照合中です。しばらくお待ちください",
        "meal_skip_not_supported": "スキップできるのは昼食と夕食だけです",
        "naver_maps_not_configured": "NAVER マップの地点検索は有効になっていません",
        "offer_expired": "この料金は期限切れです。予約前に再度確認してください",
        "offer_not_found": "この料金が見つかりません",
        "offer_unreadable": "この料金は読み取れなくなりました",
        "photo_not_found": "この場所の写真はありません",
        "photo_provider_unavailable": "地点写真のサービスが一時的に利用できません",
        "place_not_found": "この地点が見つかりません",
        "place_provider_not_configured": "韓国の地点検索は有効になっていません",
        "place_provider_not_found": "対応していない地点の提供元です",
        "plan_not_found": "最適化のプランが見つかりません",
        "provider_not_configured": "この検索に使えるリアルタイム価格の提供元がありません",
        "provider_unavailable": "元の航空券の提供元が現在利用できません",
        "rate_limit_unavailable": "安全確認のサービスが一時的に利用できません",
        "registration_closed": "現在、新規登録を停止しています",
        "route_apply_in_progress": "同じルートを適用中です。しばらくお待ちください",
        "route_compute_in_progress": "同じ日のルートを計算中です",
        "route_default_mode_mismatch": "その日の既定の交通手段を先にプレビューしてください",
        "route_items_insufficient": "場所のある項目が二つ以上必要です",
        "route_items_invalid": "出発と到着は同じ日の項目である必要があります",
        "route_items_limit": "一度に計算できる場所が多すぎます。単日か狭い範囲を指定してください",
        "route_items_not_adjacent": "ルートは同じ日の隣り合う項目の間だけ計算できます",
        "route_location_unavailable": "ルートを調べる前に、この二つの場所を確定してください",
        "route_preview_expired": "ルートのプレビューが期限切れです。もう一度検索してください",
        "route_provider_not_configured": "この交通手段のルート検索サービスはまだ有効ではありません",
        "route_queue_unavailable": "バックグラウンドのルート検索が一時的に利用できません",
        "route_unavailable": "利用できるルートが得られませんでした。しばらくしてからお試しください",
        "saved_item_not_found": "この保存済みの項目が見つかりません",
        "search_not_expandable": "この検索は航空券の情報源を追加できる種類ではありません",
        "search_offers_unreadable": "この検索で保存された航空券の料金は読み取れなくなりました",
        "session_expired": "ログインの有効期限が切れました。もう一度ログインしてください",
        "shared_trip_not_found": "この共有された旅程が見つかりません",
        "system_itinerary_item_immutable": (
            "固定の航空券・ホテル・食事のカードはシステムのみが作成できます"
        ),
        "travel_provider_unavailable": "この旅程に使えるリアルタイム価格の提供元がありません",
        "trip_item_not_found": "この項目が見つかりません",
        "trip_ledger_full": "この旅程の明細は上限に達しています",
        "trip_ledger_not_empty": "明細があるうちは通貨を変更できません。先に明細を空にしてください",
        "trip_place_not_found": "この未配置の場所が見つかりません",
        "trip_places_empty": "場所か Google マップのリンクを一つ以上貼り付けてください",
        "trip_places_too_many_lines": "一度に貼り付けた場所が多すぎます。分けて貼り付けてください",
        "trip_planning_fields_missing": "旅程に目的地か日付がないため、組み直せません",
        "trip_reoptimization_unavailable": "提供元から使える組み合わせが返ってきませんでした",
        "trip_search_missing": "元の検索は利用できなくなりました",
        "unsupported_area": "この目的地にそのエリアはありません",
        "unsupported_city_code": "この都市コードには対応していません",
        "unsupported_region": "目的地の探索は日本・韓国・タイに対応しています",
        "usage_balance_invalid": "保留分の回数の帳簿状態が正しくありません",
        "usage_operation_unknown": "不明な回数消費の操作です",
        "usage_package_not_found": "この回数パックが見つかりません",
        "weather_api_not_enabled": (
            "Google Weather API が無効か、サーバーの "
            "API キーで許可されていません"
        ),
        "weather_location_unavailable": (
            "旅程に使える座標がまだありません。まず一つ以上の場所を確定してください"
        ),
        "weather_not_configured": "天気のサービスが設定されていません",
        "weather_provider_rejected": (
            "MET Norway がリクエストを拒否しました。"
            "User-Agent の設定を確認してください"
        ),
        "weather_provider_unavailable": "Google Weather が一時的に応答していません",
        "weather_rate_limited": "Google Weather の照会枠が一時的に不足しています",
        "weather_response_invalid": "Google Weather の応答が不完全でした",
        "food_area_not_found": "このエリアが見つかりません",
        "food_merchant_not_found": "この店舗の情報が見つかりません",
        "google_maps_not_configured": "Google マップの地点データが設定されていません",
        "hotspot_intro_ai_quota_exhausted": "本日の紹介文の生成枠を使い切りました",
        "queue_unavailable": "バックグラウンドのキューが一時的に利用できません",
        "unsupported_destination": "目的地の指定に対応していない項目が含まれています",
        "usage_account_missing": "このアカウントには回数の残高がまだありません",
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
            # Added 2026-09-07: every public error code the API raises now says what
        # went wrong. Before this a reader outside zh-TW got GENERIC_DETAILS —
        # one sentence for 124 different problems.
        "admin_required": "이 기능은 시스템 관리자 전용입니다",
        "affiliate_link_expired": "제휴 링크가 만료되었습니다. 페이지를 새로고침해 주세요",
        "affiliate_link_invalid": "유효하지 않은 제휴 링크입니다",
        "affiliate_link_not_found": "제휴 링크를 찾을 수 없습니다",
        "affiliate_partner_not_found": "제휴 업체를 찾을 수 없습니다",
        "affiliate_source_invalid": "검색 또는 저장된 여행을 먼저 지정해 주세요",
        "ai_planner_unavailable": (
            "AI 플래너를 일시적으로 사용할 수 없어 입력한 "
            "설명을 읽지 못했습니다. 잠시 후 다시 시도해 "
            "주세요"
        ),
        "alert_exists": "이 항목에는 이미 가격 알림이 있습니다",
        "alert_limit_reached": "가격 알림은 20건까지 만들 수 있습니다",
        "alert_not_found": "해당 가격 알림을 찾을 수 없습니다",
        "alert_resource_not_found": "추적할 가격 항목을 찾을 수 없습니다",
        "alert_update_empty": "가격 알림 항목을 하나 이상 변경해 주세요",
        "area_requires_destination": "지역으로 거르려면 목적지도 함께 지정해야 합니다",
        "clickout_unavailable": "지금 사용할 수 있는 안전한 예약 링크가 없습니다",
        "day_outside_trip": "그 날짜는 여행 기간 밖입니다",
        "dependencies_unavailable": "데이터베이스, 스키마 또는 Redis를 사용할 수 없습니다",
        "deployment_admin_required": "이 기능은 배포 관리자 전용입니다",
        "destination_id_required": "확장 도시에는 destination_id를 사용해 주세요",
        "destination_mismatch": "city_code와 destination_id가 일치하지 않습니다",
        "destination_required": "city_code 또는 destination_id 중 하나가 필요합니다",
        "expense_not_found": "해당 지출 내역을 찾을 수 없습니다",
        "flight_anchor_unavailable": "여행 날짜가 완전하지 않아 항공편을 설정할 수 없습니다",
        "flight_status_item_not_found": "해당 항공편 항목을 찾을 수 없습니다",
        "flight_status_lookup_expired": "이 운항 정보 조회는 만료되었습니다",
        "flight_status_lookup_not_found": "해당 운항 정보 조회를 찾을 수 없습니다",
        "flight_track_unavailable": "이 항공편의 실제 항적 데이터가 아직 없습니다",
        "flightaware_not_configured": "FlightAware 운항 정보가 활성화되지 않았습니다",
        "flightaware_unavailable": (
            "FlightAware 항공 데이터를 가져올 수 없습니다. "
            "잠시 후 다시 시도해 주세요"
        ),
        "food_merchant_location_unverified": "이 가게의 위치가 아직 확인되지 않았습니다",
        "fx_rate_unavailable": "해당 환율을 지금 가져올 수 없습니다",
        "holiday_country_unknown": "해당 국가의 공휴일 데이터가 없습니다",
        "holiday_range_invalid": "종료일이 시작일보다 앞섭니다",
        "holiday_range_too_wide": "공휴일은 한 번에 3년치까지 조회할 수 있습니다",
        "hotel_offer_expired": (
            "이 요금은 만료되었습니다. 호텔 비교를 새로고침한 "
            "뒤 다시 선택해 주세요"
        ),
        "hotspot_official_website_invalid": "공식 웹사이트는 공개된 HTTPS 주소여야 합니다",
        "hotspot_official_website_not_official": "이 주소는 승인 가능한 공식 웹사이트가 아닙니다",
        "hotspot_source_not_found": "해당 명소 출처를 찾을 수 없습니다",
        "idempotency_key_required": "Idempotency-Key 헤더가 필요합니다",
        "idempotency_key_reused": "이 Idempotency-Key는 다른 작업에 이미 사용되었습니다",
        "idempotency_result_unavailable": (
            "이 Idempotency-Key에는 재생할 결과가 없습니다. "
            "새 키를 사용해 주세요"
        ),
        "invalid_external_reference": "외부 참조는 1~200자여야 합니다",
        "invalid_food_cursor": "맛집 목록의 페이지 커서 형식이 올바르지 않습니다",
        "invalid_line_link_token": "LINE 연결 토큰 형식이 올바르지 않습니다",
        "invalid_line_signature": "LINE 웹훅 서명이 유효하지 않습니다",
        "invalid_line_webhook": "LINE 웹훅 형식이 유효하지 않습니다",
        "invalid_place_bias": "장소 검색 중심에는 위도와 경도가 모두 필요합니다",
        "invalid_place_kinds": "장소 종류는 현재 cities만 지원합니다",
        "invalid_place_query": "장소 검색어는 2~120자여야 합니다",
        "invalid_place_regions": "장소 검색은 현재 일본, 한국, 태국을 지원합니다",
        "invalid_session_token": "장소 검색 세션 코드 형식이 올바르지 않습니다",
        "invalid_usage_cursor": "사용 내역의 페이지 커서 형식이 올바르지 않습니다",
        "invalid_user": "이 계정은 현재 사용할 수 없습니다",
        "itinerary_candidate_invalid": "AI가 등록되지 않은 장소를 반환했습니다",
        "itinerary_candidates_changed": (
            "일부 명소나 가게가 변경되었습니다. 다시 "
            "미리보기를 실행해 주세요"
        ),
        "itinerary_date_out_of_range": "식사 날짜가 여행 범위를 벗어납니다",
        "itinerary_exact_locations_required": "확인된 명소나 가게가 부족하여 일정은 그대로입니다",
        "itinerary_optimization_limit": (
            "하루에 최적화할 수 있는 이동 가능 장소가 "
            "너무 많습니다. 일부를 고정해 주세요"
        ),
        "itinerary_optimization_unavailable": "비교할 동선 결과를 얻지 못했습니다",
        "itinerary_optimization_unchanged": "이미 권장 순서이므로 적용할 변경이 없습니다",
        "itinerary_preview_expired": "일정 미리보기가 만료되었습니다. 다시 생성해 주세요",
        "itinerary_preview_stale": "일정 항목이 변경되었습니다. 다시 미리보기를 실행해 주세요",
        "line_api_unavailable": "LINE API를 일시적으로 사용할 수 없습니다",
        "line_delivery_failed": "LINE 테스트 메시지를 보내지 못했습니다",
        "line_friend_required": "LINE 공식 계정을 다시 친구로 추가해 주세요",
        "line_not_configured": "LINE 가격 알림이 활성화되지 않았습니다",
        "line_not_linked": "아직 LINE 계정이 연결되지 않았습니다",
        "line_webhook_too_large": "LINE 웹훅 내용이 너무 큽니다",
        "location_resolve_in_progress": "같은 장소를 매칭하는 중입니다. 잠시 기다려 주세요",
        "meal_skip_not_supported": "점심과 저녁만 건너뛸 수 있습니다",
        "naver_maps_not_configured": "NAVER 지도 장소 검색이 활성화되지 않았습니다",
        "offer_expired": "이 요금은 만료되었습니다. 예약 전에 다시 확인해 주세요",
        "offer_not_found": "해당 요금을 찾을 수 없습니다",
        "offer_unreadable": "이 요금은 더 이상 읽을 수 없습니다",
        "photo_not_found": "이 장소의 사진이 없습니다",
        "photo_provider_unavailable": "장소 사진 서비스를 일시적으로 사용할 수 없습니다",
        "place_not_found": "해당 장소를 찾을 수 없습니다",
        "place_provider_not_configured": "한국 장소 검색이 활성화되지 않았습니다",
        "place_provider_not_found": "지원하지 않는 장소 제공자입니다",
        "plan_not_found": "최적화 결과를 찾을 수 없습니다",
        "provider_not_configured": "이 검색에 사용할 실시간 가격 공급사가 없습니다",
        "provider_unavailable": "원래 항공권 공급사를 지금 사용할 수 없습니다",
        "rate_limit_unavailable": "보안 확인 서비스를 일시적으로 사용할 수 없습니다",
        "registration_closed": "현재 신규 가입을 중단하고 있습니다",
        "route_apply_in_progress": "같은 경로를 적용하는 중입니다. 잠시 기다려 주세요",
        "route_compute_in_progress": "같은 날짜의 경로를 계산하는 중입니다",
        "route_default_mode_mismatch": "해당 날짜의 기본 이동 수단을 먼저 미리보기 해 주세요",
        "route_items_insufficient": "위치가 있는 일정 항목이 두 개 이상 필요합니다",
        "route_items_invalid": "출발과 도착은 같은 날의 항목이어야 합니다",
        "route_items_limit": (
            "한 번에 계산할 장소가 너무 많습니다. 하루 "
            "또는 더 좁은 범위를 지정해 주세요"
        ),
        "route_items_not_adjacent": "경로는 같은 날 인접한 항목 사이에서만 계산할 수 있습니다",
        "route_location_unavailable": "경로를 찾기 전에 두 장소를 먼저 확정해 주세요",
        "route_preview_expired": "경로 미리보기가 만료되었습니다. 다시 조회해 주세요",
        "route_provider_not_configured": "이 이동 수단의 경로 서비스가 아직 활성화되지 않았습니다",
        "route_queue_unavailable": "백그라운드 경로 서비스를 일시적으로 사용할 수 없습니다",
        "route_unavailable": "사용할 수 있는 경로를 얻지 못했습니다. 잠시 후 다시 시도해 주세요",
        "saved_item_not_found": "저장한 항목을 찾을 수 없습니다",
        "search_not_expandable": "이 검색은 항공권 출처를 더 추가할 수 있는 유형이 아닙니다",
        "search_offers_unreadable": "이 검색에 저장된 항공권 요금은 더 이상 읽을 수 없습니다",
        "session_expired": "로그인이 만료되었습니다. 다시 로그인해 주세요",
        "shared_trip_not_found": "공유된 여행을 찾을 수 없습니다",
        "system_itinerary_item_immutable": "고정된 항공·숙소·식사 카드는 시스템만 만들 수 있습니다",
        "travel_provider_unavailable": "이 여행에 사용할 실시간 가격 공급사가 없습니다",
        "trip_item_not_found": "해당 항목을 찾을 수 없습니다",
        "trip_ledger_full": "이 여행의 지출 내역이 한도에 도달했습니다",
        "trip_ledger_not_empty": (
            "지출 내역이 있으면 통화를 바꿀 수 없습니다. "
            "먼저 내역을 비워 주세요"
        ),
        "trip_place_not_found": "배치되지 않은 해당 장소를 찾을 수 없습니다",
        "trip_places_empty": "장소 또는 Google 지도 링크를 하나 이상 붙여넣어 주세요",
        "trip_places_too_many_lines": (
            "한 번에 붙여넣은 장소가 너무 많습니다. "
            "나누어 붙여넣어 주세요"
        ),
        "trip_planning_fields_missing": "여행에 목적지나 날짜가 없어 다시 계획할 수 없습니다",
        "trip_reoptimization_unavailable": "공급사에서 사용할 수 있는 조합을 받지 못했습니다",
        "trip_search_missing": "원래 검색을 더 이상 사용할 수 없습니다",
        "unsupported_area": "이 목적지에는 해당 지역이 없습니다",
        "unsupported_city_code": "지원하지 않는 도시 코드입니다",
        "unsupported_region": "목적지 탐색은 일본, 한국, 태국을 지원합니다",
        "usage_balance_invalid": "예약된 사용 횟수의 정산 상태가 올바르지 않습니다",
        "usage_operation_unknown": "알 수 없는 횟수 차감 작업입니다",
        "usage_package_not_found": "해당 횟수 팩을 찾을 수 없습니다",
        "weather_api_not_enabled": (
            "Google Weather API가 비활성 상태이거나 "
            "서버 API 키가 이를 허용하지 않습니다"
        ),
        "weather_location_unavailable": (
            "여행에 사용할 수 있는 좌표가 아직 없습니다. "
            "장소를 하나 이상 확정해 주세요"
        ),
        "weather_not_configured": "날씨 서비스가 설정되지 않았습니다",
        "weather_provider_rejected": (
            "MET Norway가 요청을 거부했습니다. User-Agent "
            "설정을 확인해 주세요"
        ),
        "weather_provider_unavailable": "Google Weather가 일시적으로 응답하지 않습니다",
        "weather_rate_limited": "Google Weather 조회 한도가 일시적으로 부족합니다",
        "weather_response_invalid": "Google Weather 응답 형식이 불완전합니다",
        "food_area_not_found": "해당 지역을 찾을 수 없습니다",
        "food_merchant_not_found": "해당 가게 정보를 찾을 수 없습니다",
        "google_maps_not_configured": "Google 지도 장소 데이터가 설정되지 않았습니다",
        "hotspot_intro_ai_quota_exhausted": "오늘의 소개 생성 한도를 모두 사용했습니다",
        "queue_unavailable": "백그라운드 대기열을 일시적으로 사용할 수 없습니다",
        "unsupported_destination": "목적지 연결에 지원하지 않는 항목이 포함되어 있습니다",
        "usage_account_missing": "이 계정에는 아직 사용 횟수 잔액이 없습니다",
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
            # Added 2026-09-07: every public error code the API raises now says what
        # went wrong. Before this a reader outside zh-TW got GENERIC_DETAILS —
        # one sentence for 124 different problems.
        "admin_required": "此功能仅限系统管理员使用",
        "affiliate_link_expired": "合作链接已过期，请重新整理",
        "affiliate_link_invalid": "合作链接无效",
        "affiliate_link_not_found": "找不到合作链接",
        "affiliate_partner_not_found": "找不到合作平台",
        "affiliate_source_invalid": "请指定搜索或已保存旅程",
        "ai_planner_unavailable": "AI 规划暂时无法使用，这次没有读到你的描述，请稍后再试",
        "alert_exists": "这个项目已经建立价格通知",
        "alert_limit_reached": "已达 20 笔价格通知上限",
        "alert_not_found": "找不到这笔价格通知",
        "alert_resource_not_found": "找不到可追踪的价格项目",
        "alert_update_empty": "请至少修改一个价格通知栏位",
        "area_requires_destination": "筛选区域时必须同时指定目的地",
        "clickout_unavailable": "目前没有可用的安全订票链接",
        "day_outside_trip": "这一天不在旅程日期范围内",
        "dependencies_unavailable": "数据库、数据结构或 Redis 目前无法使用",
        "deployment_admin_required": "此功能仅限部署管理员使用",
        "destination_id_required": "延伸城市请使用 destination_id",
        "destination_mismatch": "city_code 与 destination_id 不一致",
        "destination_required": "必须提供 city_code 或 destination_id",
        "expense_not_found": "找不到这笔账目",
        "flight_anchor_unavailable": "旅程日期不完整，无法设定航班",
        "flight_status_item_not_found": "找不到这个航班项目",
        "flight_status_lookup_expired": "这笔航班动态查询已到期",
        "flight_status_lookup_not_found": "找不到这笔航班动态查询",
        "flight_track_unavailable": "班表数据尚无可用的实际航迹",
        "flightaware_not_configured": "FlightAware 航班动态尚未启用",
        "flightaware_unavailable": "FlightAware 航班数据目前无法取得，请稍后再试",
        "food_merchant_location_unverified": "店家地点尚未完成验证",
        "fx_rate_unavailable": "目前无法取得这个汇率",
        "holiday_country_unknown": "没有这个国家的假日数据",
        "holiday_range_invalid": "结束日期早于开始日期",
        "holiday_range_too_wide": "一次最多查询三年份的假日",
        "hotel_offer_expired": "这笔报价已过期，请重新整理饭店比价后再选择",
        "hotspot_official_website_invalid": "官方网站必须是公开 HTTPS URL",
        "hotspot_official_website_not_official": "这个网址不是可核准的官方网站",
        "hotspot_source_not_found": "找不到这个景点来源",
        "idempotency_key_required": "缺少 Idempotency-Key",
        "idempotency_key_reused": "这个 Idempotency-Key 已经用于另一个操作",
        "idempotency_result_unavailable": "这个 Idempotency-Key 没有可重播的结果，请改用新的键",
        "invalid_external_reference": "外部参照必须是 1 至 200 个字元",
        "invalid_food_cursor": "美食分页游标格式不正确",
        "invalid_line_link_token": "LINE 关联凭证格式不正确",
        "invalid_line_signature": "LINE webhook 签章无效",
        "invalid_line_webhook": "LINE webhook 格式无效",
        "invalid_place_bias": "地点搜索中心必须同时包含经纬度",
        "invalid_place_kinds": "地点类型目前只支持 cities",
        "invalid_place_query": "地点关键字须为 2 至 120 个字元",
        "invalid_place_regions": "地点搜索目前支持日本、韩国与泰国",
        "invalid_session_token": "地点搜索工作阶段代码格式错误",
        "invalid_usage_cursor": "使用记录游标格式不正确",
        "invalid_user": "这个账号目前无法使用",
        "itinerary_candidate_invalid": "AI 返回了不存在的正式地点",
        "itinerary_candidates_changed": "部分景点或店家已变更，请重新预览",
        "itinerary_date_out_of_range": "用餐日期超出旅程范围",
        "itinerary_exact_locations_required": "正式景点或店家不足，原行程保持不变",
        "itinerary_optimization_limit": "一天可最佳化的可移动地点太多，请先锁定部分项目",
        "itinerary_optimization_unavailable": "没有取得可比较的动线结果",
        "itinerary_optimization_unchanged": "目前已是建议安排，不需要套用",
        "itinerary_preview_expired": "行程预览已过期，请重新产生",
        "itinerary_preview_stale": "行程项目已变更，请重新预览",
        "line_api_unavailable": "LINE API 暂时无法使用",
        "line_delivery_failed": "LINE 测试讯息暂时无法送出",
        "line_friend_required": "请重新加入 LINE 官方账号好友",
        "line_not_configured": "LINE 价格通知尚未启用",
        "line_not_linked": "尚未关联 LINE 账号",
        "line_webhook_too_large": "LINE webhook 内容过大",
        "location_resolve_in_progress": "相同地点正在配对，请稍候",
        "meal_skip_not_supported": "只有午餐与晚餐可以跳过",
        "naver_maps_not_configured": "NAVER Maps 地点搜索尚未启用",
        "offer_expired": "报价已过期，前往订票前请先重新验价",
        "offer_not_found": "找不到这笔报价",
        "offer_unreadable": "这笔报价已无法读取",
        "photo_not_found": "目前没有可用的地点照片",
        "photo_provider_unavailable": "地点照片服务暂时无法使用",
        "place_not_found": "找不到这个地点",
        "place_provider_not_configured": "韩国地点搜索服务尚未启用",
        "place_provider_not_found": "不支持的地点来源",
        "plan_not_found": "找不到最佳化方案",
        "provider_not_configured": "目前没有可用于这次搜索的实时查价供应商",
        "provider_unavailable": "原始航班供应商目前无法使用",
        "rate_limit_unavailable": "安全验证服务暂时无法使用",
        "registration_closed": "目前暂停开放新账号注册",
        "route_apply_in_progress": "相同路线正在套用，请稍候",
        "route_compute_in_progress": "相同日期的路线正在计算",
        "route_default_mode_mismatch": "请先预览当日默认交通方式",
        "route_items_insufficient": "至少需要两个有位置的行程项目",
        "route_items_invalid": "起点与终点必须是同一天的行程项目",
        "route_items_limit": "一次可计算的行程地点太多，请指定单日或较小范围",
        "route_items_not_adjacent": "只能计算同一天相邻行程之间的路线",
        "route_location_unavailable": "请先确认这两个行程地点后再查路",
        "route_preview_expired": "路线预览已过期，请重新查询",
        "route_provider_not_configured": "此交通方式的路线服务尚未启用，请先设定对应 Provider",
        "route_queue_unavailable": "后台路线服务暂时无法使用",
        "route_unavailable": "目前无法取得可用路线，请稍后再试",
        "saved_item_not_found": "找不到这个收藏项目",
        "search_not_expandable": "这次搜索不是可以再扩充航班来源的类型",
        "search_offers_unreadable": "这次搜索存下来的航班报价已无法读取",
        "session_expired": "登录已逾期，请重新登录",
        "shared_trip_not_found": "找不到这个分享旅程",
        "system_itinerary_item_immutable": "固定航班、饭店与餐食卡只能由系统建立",
        "travel_provider_unavailable": "目前没有可用于这趟旅程的实时查价供应商",
        "trip_item_not_found": "找不到这个行程项目",
        "trip_ledger_full": "这趟旅程的账目已达上限",
        "trip_ledger_not_empty": "账目已有记录，无法更改币别。请先清空账目再切换。",
        "trip_place_not_found": "找不到这个待安排地点",
        "trip_places_empty": "请至少贴上一个地点或 Google Maps 链接",
        "trip_places_too_many_lines": "一次贴上的地点太多，请分批贴",
        "trip_planning_fields_missing": "旅程缺少目的地或日期，无法重新排行程",
        "trip_reoptimization_unavailable": "供应商目前没有可用组合",
        "trip_search_missing": "原始搜索已无法使用",
        "unsupported_area": "这个目的地没有这个区域",
        "unsupported_city_code": "目前不支持这个城市代码",
        "unsupported_region": "目前目的地探索支持日本、韩国与泰国",
        "usage_balance_invalid": "保留次数的账务状态不正确",
        "usage_operation_unknown": "未知的计次操作",
        "usage_package_not_found": "找不到这个次数包",
        "weather_api_not_enabled": "Google Weather API 尚未启用，或服务器 API 密钥限制不允许此服务",
        "weather_location_unavailable": "旅程尚无可用坐标，请先确认至少一个行程地点",
        "weather_not_configured": "天气服务尚未设定",
        "weather_provider_rejected": "MET Norway 拒绝了请求，请检查 User-Agent 设定",
        "weather_provider_unavailable": "Google Weather 暂时无法响应",
        "weather_rate_limited": "Google Weather 查询额度暂时不足",
        "weather_response_invalid": "Google Weather 响应格式不完整",
        "food_area_not_found": "找不到这个区域",
        "food_merchant_not_found": "找不到这笔店家数据",
        "google_maps_not_configured": "Google Maps 地点数据目前未设定",
        "hotspot_intro_ai_quota_exhausted": "今日介绍产生额度已用完",
        "queue_unavailable": "后台队列暂时无法使用",
        "unsupported_destination": "目的地关联包含不支持的项目",
        "usage_account_missing": "此会员尚未建立次数账户",
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
        "trip_limit_reached": "You have reached the shared limit of 20 saved trips",
        "search_not_found": "This search could not be found",
        "hotspot_not_found": "This attraction could not be found",
        "unsupported_theme": "This theme is not available",
        "hotspot_theme_not_found": "This theme could not be found",
        "hotspot_intro_not_found": "This introduction could not be found",
        "hotspot_intro_body_required": "The introduction text is empty or too long",
        "hotspot_theme_slug_exists": "A theme with this code already exists",
        "theme_months_not_applicable": "Months do not apply to this theme",
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
        "trip_origin_required": "This trip has no departure airport yet. Choose one first.",
        "trip_destination_unsupported": (
            "Flight search does not cover this trip's destination yet. "
            "Choose the arrival airport yourself."
        ),
        "trip_dates_past": "This trip's departure date has passed. Adjust the trip dates first.",
        "trip_dates_too_short": (
            "A round trip needs at least two trip days. Adjust the trip dates first."
        ),
        "trip_dates_mismatch": (
            "This search's dates no longer match the trip. Reload the trip's criteria."
        ),
        "flight_anchor_unavailable": "The trip has no dates yet, so a flight cannot be set",
        "offer_not_found": "This offer could not be found",
        "offer_return_leg_missing": "This offer has no return leg to bring into the trip",
        "offer_dates_mismatch": (
            "This offer departs on a different day than the trip. Adjust the trip dates first."
        ),
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
        "trip_limit_reached": "保存できる旅行は全会員共通で 20 件までです",
        "search_not_found": "検索が見つかりません",
        "hotspot_not_found": "観光スポットが見つかりません",
        "unsupported_theme": "このテーマは利用できません",
        "hotspot_theme_not_found": "テーマが見つかりません",
        "hotspot_intro_not_found": "この紹介文が見つかりません",
        "hotspot_intro_body_required": "紹介文が空か、長すぎます",
        "hotspot_theme_slug_exists": "このコードのテーマはすでにあります",
        "theme_months_not_applicable": "このテーマに月は設定できません",
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
        "trip_origin_required": "この旅行には出発空港がまだありません。先に選んでください。",
        "trip_destination_unsupported": (
            "この旅行の目的地はまだ航空券検索の対象外です。到着空港を自分で選んでください。"
        ),
        "trip_dates_past": "この旅行の出発日は過ぎています。先に旅行の日付を調整してください。",
        "trip_dates_too_short": (
            "往復航空券には 2 日以上の旅行日程が必要です。先に旅行の日付を調整してください。"
        ),
        "trip_dates_mismatch": (
            "この検索の日付は旅行の日付と一致しません。旅行の条件を再読み込みしてください。"
        ),
        "flight_anchor_unavailable": "この旅行にはまだ日付がないため、フライトを設定できません",
        "offer_not_found": "この料金が見つかりません",
        "offer_return_leg_missing": "この料金には旅行に取り込める復路がありません",
        "offer_dates_mismatch": (
            "この料金の出発日は旅行の日付と異なります。先に旅行の日付を調整してください。"
        ),
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
            "이 이메일은 관리자용으로 예약되어 있습니다. 호스트 관리자에게 계정 생성을 요청하세요"
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
        "trip_limit_reached": "모든 회원이 공유하는 저장 여행 한도 20개에 도달했습니다",
        "search_not_found": "검색을 찾을 수 없습니다",
        "hotspot_not_found": "명소를 찾을 수 없습니다",
        "unsupported_theme": "이 테마는 사용할 수 없습니다",
        "hotspot_theme_not_found": "테마를 찾을 수 없습니다",
        "hotspot_intro_not_found": "이 소개를 찾을 수 없습니다",
        "hotspot_intro_body_required": "소개 내용이 비었거나 너무 깁니다",
        "hotspot_theme_slug_exists": "이 코드의 테마가 이미 있습니다",
        "theme_months_not_applicable": "이 테마에는 월을 설정할 수 없습니다",
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
        "trip_origin_required": "이 여행에는 아직 출발 공항이 없습니다. 먼저 선택하세요.",
        "trip_destination_unsupported": (
            "이 여행의 목적지는 아직 항공권 검색 범위에 없습니다. 도착 공항을 직접 선택하세요."
        ),
        "trip_dates_past": "이 여행의 출발일이 지났습니다. 먼저 여행 날짜를 조정하세요.",
        "trip_dates_too_short": (
            "왕복 항공권에는 최소 2일의 여행 일정이 필요합니다. 먼저 여행 날짜를 조정하세요."
        ),
        "trip_dates_mismatch": (
            "이 검색의 날짜가 여행의 날짜와 다릅니다. 여행 조건을 다시 불러오세요."
        ),
        "flight_anchor_unavailable": "이 여행에는 아직 날짜가 없어 항공편을 설정할 수 없습니다",
        "offer_not_found": "이 요금을 찾을 수 없습니다",
        "offer_return_leg_missing": "이 요금에는 여행에 가져올 귀국편이 없습니다",
        "offer_dates_mismatch": (
            "이 요금의 출발일이 여행 날짜와 다릅니다. 먼저 여행 날짜를 조정하세요."
        ),
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
        "unsupported_theme": "目前沒有這個主題",
        "hotspot_theme_not_found": "找不到這個主題",
        "hotspot_intro_not_found": "找不到這筆介紹內容",
        "hotspot_intro_body_required": "介紹內容是空的或超過長度上限",
        "hotspot_theme_slug_exists": "已經有同名的主題代碼",
        "theme_months_not_applicable": "這個主題不適用月份",
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
        "trip_limit_reached": "已达所有会员共用的 20 条保存旅程上限",
        "search_not_found": "找不到这次搜索",
        "hotspot_not_found": "找不到这个景点",
        "unsupported_theme": "目前没有这个主题",
        "hotspot_theme_not_found": "找不到这个主题",
        "hotspot_intro_not_found": "找不到这条介绍内容",
        "hotspot_intro_body_required": "介绍内容是空的或超过长度上限",
        "hotspot_theme_slug_exists": "已经有同名的主题代码",
        "theme_months_not_applicable": "这个主题不适用月份",
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
        "trip_origin_required": "这趟旅程还没有出发机场，请先选择出发地",
        "trip_destination_unsupported": (
            "这趟旅程的目的地不在目前的机票搜索范围，请自行选择抵达机场"
        ),
        "trip_dates_past": "旅程的出发日已经过了，请先调整旅程日期",
        "trip_dates_too_short": "往返机票需要至少两天的旅程日期，请先调整旅程日期",
        "trip_dates_mismatch": "这次搜索的日期与旅程目前的日期不同，请重新载入旅程条件",
        "flight_anchor_unavailable": "旅程日期不完整，无法设置航班",
        "offer_not_found": "找不到这笔报价",
        "offer_return_leg_missing": "这笔报价没有回程航段，无法带入回程",
        "offer_dates_mismatch": "这笔报价的出发日与旅程日期不同，请先调整旅程日期",
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


def bind_request_locale(locale: str | None) -> Token[Locale]:
    """Make ``locale`` the active request locale; reset with :func:`reset_request_locale`."""

    return _request_locale.set(normalize_locale(locale))


def reset_request_locale(token: Token[Locale]) -> None:
    _request_locale.reset(token)


def active_locale() -> Locale:
    """The locale of the request being served, or the site default outside a request."""

    return _request_locale.get()


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
