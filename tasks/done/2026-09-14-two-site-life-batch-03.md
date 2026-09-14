---
id: 2026-09-14-two-site-life-batch-03
title: 兩站原創生活分享批次 03（20 篇）
status: done
priority: P2
area: docs
owner: codex-two-site-life
claimed_at: 2026-09-14T04:45:55Z
created_at: 2026-09-14T02:26:16Z
completed_at: 2026-09-14T05:43:32Z
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-500-error.json
  - apps/web/public/guides/wordpress-500-error
  - .codex/two-site-life/work/wordpress-500-error
  - apps/api/app/guides/content/wordpress-security-basics.json
  - apps/web/public/guides/wordpress-security-basics
  - .codex/two-site-life/work/wordpress-security-basics
  - apps/api/app/guides/content/wordpress-user-roles.json
  - apps/web/public/guides/wordpress-user-roles
  - .codex/two-site-life/work/wordpress-user-roles
  - apps/api/app/guides/content/wordpress-member-registration.json
  - apps/web/public/guides/wordpress-member-registration
  - .codex/two-site-life/work/wordpress-member-registration
  - apps/api/app/guides/content/wordpress-social-login.json
  - apps/web/public/guides/wordpress-social-login
  - .codex/two-site-life/work/wordpress-social-login
  - apps/api/app/guides/content/wordpress-multilingual-site.json
  - apps/web/public/guides/wordpress-multilingual-site
  - .codex/two-site-life/work/wordpress-multilingual-site
  - apps/api/app/guides/content/wordpress-plugin-theme-translation.json
  - apps/web/public/guides/wordpress-plugin-theme-translation
  - .codex/two-site-life/work/wordpress-plugin-theme-translation
  - apps/api/app/guides/content/wordpress-contact-forms.json
  - apps/web/public/guides/wordpress-contact-forms
  - .codex/two-site-life/work/wordpress-contact-forms
  - apps/api/app/guides/content/wordpress-smtp-delivery.json
  - apps/web/public/guides/wordpress-smtp-delivery
  - .codex/two-site-life/work/wordpress-smtp-delivery
  - apps/api/app/guides/content/wordpress-comment-spam.json
  - apps/web/public/guides/wordpress-comment-spam
  - .codex/two-site-life/work/wordpress-comment-spam
  - apps/api/app/guides/content/wordpress-table-of-contents.json
  - apps/web/public/guides/wordpress-table-of-contents
  - .codex/two-site-life/work/wordpress-table-of-contents
  - apps/api/app/guides/content/wordpress-map-form-embeds.json
  - apps/web/public/guides/wordpress-map-form-embeds
  - .codex/two-site-life/work/wordpress-map-form-embeds
  - apps/api/app/guides/content/wordpress-social-embeds.json
  - apps/web/public/guides/wordpress-social-embeds
  - .codex/two-site-life/work/wordpress-social-embeds
  - apps/api/app/guides/content/wordpress-chat-contact-buttons.json
  - apps/web/public/guides/wordpress-chat-contact-buttons
  - .codex/two-site-life/work/wordpress-chat-contact-buttons
  - apps/api/app/guides/content/wordpress-fonts-self-hosting.json
  - apps/web/public/guides/wordpress-fonts-self-hosting
  - .codex/two-site-life/work/wordpress-fonts-self-hosting
  - apps/api/app/guides/content/wordpress-ftp-file-management.json
  - apps/web/public/guides/wordpress-ftp-file-management
  - .codex/two-site-life/work/wordpress-ftp-file-management
  - apps/api/app/guides/content/astra-theme-customization.json
  - apps/web/public/guides/astra-theme-customization
  - .codex/two-site-life/work/astra-theme-customization
  - apps/api/app/guides/content/astra-portfolio-extensions.json
  - apps/web/public/guides/astra-portfolio-extensions
  - .codex/two-site-life/work/astra-portfolio-extensions
  - apps/api/app/guides/content/elementor-first-page.json
  - apps/web/public/guides/elementor-first-page
  - .codex/two-site-life/work/elementor-first-page
  - apps/api/app/guides/content/elementor-pro-theme-builder.json
  - apps/web/public/guides/elementor-pro-theme-builder
  - .codex/two-site-life/work/elementor-pro-theme-builder
---

# 兩站原創生活分享批次 03

## Why

依使用者核定的兩站標題盤點計畫，製作全部不重複主題。總表：`docs/content-research/two-site-life/catalogue.json`。

## Definition of done

- [x] 本批每篇都有原創正文、1600×900 封面、SVG 圖解、官方來源及查證日。
- [x] ingest、限定 slug lint、逐張圖片 QA 與相關測試通過。
- [x] 交付可匯入內容包；未執行正式站匯入、發布或部署。

## Steps

- [x] `wordpress-500-error` — WordPress 出現 500 錯誤：從記錄檔找原因。必寫：故障時間線、外掛與伺服器線索、回復驗證。
- [x] `wordpress-security-basics` — WordPress 安全維護：帳號、更新與防護外掛的分工。必寫：最小權限、更新與Wordfence、登入保護限制。
- [x] `wordpress-user-roles` — WordPress 會員與角色：誰能看、誰能改、誰能管理。必寫：角色與內容可見性、User Role Editor、選單與真正授權。
- [x] `wordpress-member-registration` — WordPress 會員註冊流程：表單、驗證與帳號復原。必寫：註冊登入介面、Ultimate Member與LoginPress、資料與復原。
- [x] `wordpress-social-login` — WordPress 社群登入：LINE、Google 與 Facebook 的串接檢查。必寫：應用程式設定、回呼網址、帳號綁定與退出。
- [x] `wordpress-multilingual-site` — WordPress 多語系網站：內容對照、網址與翻譯流程。必寫：Polylang與TranslatePress、語系網址、維護與切換。
- [x] `wordpress-plugin-theme-translation` — WordPress 主題外掛中文化：Loco Translate 與 Poedit 工作流。必寫：翻譯字串、檔案更新、覆寫與校對。
- [x] `wordpress-contact-forms` — WordPress 聯絡表單：欄位、垃圾訊息與送信驗收。必寫：Contact Form 7、個資最小化、提交到收信的驗證。
- [x] `wordpress-smtp-delivery` — WordPress 寄信失敗怎麼辦：SMTP、網域驗證與記錄。必寫：WP Mail SMTP、寄件網域驗證、Brevo錯誤排解。
- [x] `wordpress-comment-spam` — WordPress 垃圾留言怎麼處理：審核規則與 Akismet。必寫：垃圾留言、Akismet設定、誤擋與隱私。
- [x] `wordpress-table-of-contents` — WordPress 文章目錄：標題結構、錨點與手機閱讀。必寫：目錄生成、Easy Table of Contents、固定目錄驗收。
- [x] `wordpress-map-form-embeds` — WordPress 嵌入地圖與 Google 表單：寬度、隱私與可用性。必寫：嵌入方法、備援連結、手機與隱私。
- [x] `wordpress-social-embeds` — WordPress 社群嵌入：Instagram 與 Facebook 內容失效怎麼辦。必寫：嵌入支援限制、連線與授權、載入與替代連結。
- [x] `wordpress-chat-contact-buttons` — WordPress 即時聯絡按鈕：LINE、客服與舊 Messenger 外掛的替代。必寫：聯絡入口、產品支援現況、手機遮擋。
- [x] `wordpress-fonts-self-hosting` — WordPress 字型自己託管：檔案、授權與載入速度。必寫：字型授權、子集與格式、CSS引用及效能。
- [x] `wordpress-ftp-file-management` — WordPress 檔案傳輸：用 SFTP 管理網站檔案。必寫：安全連線、檔案權限、變更與還原。
- [x] `astra-theme-customization` — Astra 佈景主題怎麼設定：版型、導覽與付費功能的取捨。必寫：版型匯入、外觀客製、免費與Pro界線。
- [x] `astra-portfolio-extensions` — Astra 作品集與 Elementor 擴充：挑出真正需要的功能。必寫：作品集組織、擴充相容性、移除與效能。
- [x] `elementor-first-page` — Elementor 編輯頁面：用容器、間距與響應式建立版面。必寫：容器結構、背景圖片、手機調整。
- [x] `elementor-pro-theme-builder` — Elementor Pro 要用在哪：頁首頁尾、範本與授權選擇。必寫：方案查證、主題建構器、顯示條件。

## How to verify

`uv run python -m app.guides.pack_cli lint --kind life --slug <本批 slug> --render-dir <QA目錄>`

`uv run pytest tests/test_guides_content_pack.py -q`

`npm run check:tasks`

## Notes

來源原文只收標題與網址。不得將指派、通過 schema 或 AI 摘要視為完整文章。每篇 1,800–3,000 字並自行查證；協調者文件保存研究記錄。

2026-09-14：本批 20 篇及 40 張圖片完成本機驗收；ingest 與 lint 通過，內容包測試 9 passed / 5 skipped。詳見 docs/content-research/two-site-life/batch-03-review.md 與對應 audit、測試日誌。未發布。
