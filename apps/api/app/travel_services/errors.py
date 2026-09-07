"""Stable errors for the reviewed travel-service catalog."""

SERVICE_ERRORS: dict[str, dict[str, str]] = {
    "en": {
        "service_unavailable": ("This service is not available."),
        "service_version_conflict": ("This record changed. Reload before editing."),
        "service_operation_conflict": (
            "This operation key was already used for another selection."
        ),
        "service_source_required": ("Provide official or authorized source evidence."),
        "service_identity_required": (
            "Verify exact map identity and source-backed coordinates first."
        ),
        "service_destination_mismatch": ("This option does not match the trip destination."),
        "service_area_required": ("Choose a verified stay area."),
        "service_airport_required": (
            "Confirm the airport, direction, flight number and passengers."
        ),
        "service_coverage_required": ("Verified country coverage is required."),
        "service_dates_required": ("Set valid trip dates and a same-day time window."),
        "service_time_conflict": (
            "This overlaps an existing item or is outside the verified time "
            "window. Choose another time."
        ),
        "service_capacity_exceeded": ("The passenger count exceeds the verified capacity."),
        "service_link_unavailable": (
            "The exact partner link could not be verified. Try again later."
        ),
        "service_csv_invalid": (
            "Invalid CSV fields or data. Fix the preview errors before importing."
        ),
        "service_offer_mismatch": (
            "The link is not a verified original URL for this brand and product."
        ),
        "service_brand_unavailable": (
            "Confirm this project's brand approval and Travelpayouts credentials first."
        ),
        "service_feed_unavailable": (
            "The official feed is unavailable; no sample data was substituted."
        ),
        "service_schedule_changed": ("Service selection changed. Recalculate affected routes."),
    },
    "ja": {
        "service_unavailable": ("このサービスは利用できません。"),
        "service_version_conflict": ("更新されています。再読み込みしてください。"),
        "service_operation_conflict": ("この操作キーは別の選択で使用済みです。"),
        "service_source_required": ("公式または許可された出典が必要です。"),
        "service_identity_required": ("正確な地図IDと出典付き座標を確認してください。"),
        "service_destination_mismatch": ("旅程の目的地と一致しません。"),
        "service_area_required": ("宿泊エリアの確認が必要です。"),
        "service_airport_required": ("空港、方向、便名、人数を確認してください。"),
        "service_coverage_required": ("対応国の確認が必要です。"),
        "service_dates_required": ("旅行日と同日内の有効な時間を指定してください。"),
        "service_time_conflict": ("既存の予定と重なるか、対応時間外です。時間を変更してください。"),
        "service_capacity_exceeded": ("確認済みの定員を超えています。"),
        "service_link_unavailable": (
            "正確な提携リンクを確認できません。後でもう一度お試しください。"
        ),
        "service_csv_invalid": ("CSVに不正な項目があります。修正してからインポートしてください。"),
        "service_offer_mismatch": ("このブランド・商品の元URLとして確認できません。"),
        "service_brand_unavailable": (
            "このプロジェクトのブランド承認と認証設定を確認してください。"
        ),
        "service_feed_unavailable": (
            "公式フィードを取得できません。サンプルへの置換は行いません。"
        ),
        "service_schedule_changed": ("サービスが変更されました。ルートを再計算してください。"),
    },
    "ko": {
        "service_unavailable": ("이 서비스를 이용할 수 없습니다."),
        "service_version_conflict": ("변경된 데이터입니다. 새로고침하세요."),
        "service_operation_conflict": ("이 작업 키는 다른 선택에 사용되었습니다."),
        "service_source_required": ("공식 또는 허가된 출처 증빙이 필요합니다."),
        "service_identity_required": ("정확한 지도 ID와 출처가 있는 좌표를 확인하세요."),
        "service_destination_mismatch": ("여행 목적지와 일치하지 않습니다."),
        "service_area_required": ("확인된 숙박 지역을 선택하세요."),
        "service_airport_required": ("공항, 방향, 항공편 번호, 인원을 확인하세요."),
        "service_coverage_required": ("사용 가능 국가를 확인해야 합니다."),
        "service_dates_required": ("여행 날짜와 같은 날의 유효한 시간을 지정하세요."),
        "service_time_conflict": (
            "기존 일정과 겹치거나 이용 가능 시간을 벗어났습니다. 다른 시간을 선택하세요."
        ),
        "service_capacity_exceeded": ("확인된 정원을 초과했습니다."),
        "service_link_unavailable": (
            "정확한 제휴 링크를 확인하지 못했습니다. 나중에 다시 시도하세요."
        ),
        "service_csv_invalid": (
            "CSV 필드 또는 데이터가 잘못되었습니다. 미리보기 오류를 수정하세요."
        ),
        "service_offer_mismatch": ("이 브랜드 및 상품의 원본 URL로 확인되지 않았습니다."),
        "service_brand_unavailable": ("이 프로젝트의 브랜드 승인과 인증 설정을 먼저 확인하세요."),
        "service_feed_unavailable": (
            "공식 피드를 사용할 수 없습니다. 샘플 데이터로 대체하지 않았습니다."
        ),
        "service_schedule_changed": ("서비스 선택이 변경되었습니다. 경로를 다시 계산하세요."),
    },
    "zh-TW": {
        "service_unavailable": ("目前無法使用此服務。"),
        "service_version_conflict": ("資料已更新，請重新載入後修改。"),
        "service_operation_conflict": ("這個操作識別已用於另一個選擇。"),
        "service_source_required": ("請提供官方或授權資料來源證明。"),
        "service_identity_required": ("請先核實精準地圖識別及具來源的座標。"),
        "service_destination_mismatch": ("此選項與旅程目的地不符。"),
        "service_area_required": ("請選擇已核實的住宿區域。"),
        "service_airport_required": ("請確認機場、方向、航班編號與人數。"),
        "service_coverage_required": ("需要已核實的國家覆蓋資料。"),
        "service_dates_required": ("請設定有效旅程日期與同一天內的時間。"),
        "service_time_conflict": ("此時段與既有項目衝突或超出已核實時段，請調整時間。"),
        "service_capacity_exceeded": ("人數超過已核實的載客上限。"),
        "service_link_unavailable": ("無法驗證精準合作連結，請稍後重試。"),
        "service_csv_invalid": ("CSV 欄位或資料有誤，請先修正預覽錯誤再匯入。"),
        "service_offer_mismatch": ("連結不是此品牌與商品的已核實原始網址。"),
        "service_brand_unavailable": ("請先確認此專案的品牌核准狀態與 Travelpayouts 憑證。"),
        "service_feed_unavailable": ("無法取得官方 feed，未使用範例資料替代。"),
        "service_schedule_changed": ("服務選擇已變更，請重算受影響路線。"),
    },
    "zh-CN": {
        "service_unavailable": ("目前无法使用此服务。"),
        "service_version_conflict": ("数据已更新，请重新加载后修改。"),
        "service_operation_conflict": ("这个操作标识已用于另一个选择。"),
        "service_source_required": ("请提供官方或授权数据来源证明。"),
        "service_identity_required": ("请先核实精确地图标识及有来源的坐标。"),
        "service_destination_mismatch": ("此选项与旅程目的地不符。"),
        "service_area_required": ("请选择已核实的住宿区域。"),
        "service_airport_required": ("请确认机场、方向、航班编号与人数。"),
        "service_coverage_required": ("需要已核实的国家覆盖数据。"),
        "service_dates_required": ("请设置有效旅程日期与同一天内的时间。"),
        "service_time_conflict": ("此时段与现有项目冲突或超出已核实时段，请调整时间。"),
        "service_capacity_exceeded": ("人数超过已核实的载客上限。"),
        "service_link_unavailable": ("无法验证精确合作链接，请稍后重试。"),
        "service_csv_invalid": ("CSV 字段或数据有误，请先修正预览错误再导入。"),
        "service_offer_mismatch": ("链接不是此品牌与商品的已核实原始网址。"),
        "service_brand_unavailable": ("请先确认此项目的品牌批准状态与 Travelpayouts 凭据。"),
        "service_feed_unavailable": ("无法获取官方 feed，未使用示例数据替代。"),
        "service_schedule_changed": ("服务选择已变更，请重算受影响路线。"),
    },
}
