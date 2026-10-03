import { fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { AdminBootstrap } from "@/lib/admin-operations";
import { adminOperationsCopy } from "@/lib/admin-operations-copy";
import { useModalSheet } from "@/lib/modal-sheet";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminShell } from "./admin-shell";

const location = vi.hoisted(() => ({ locale: "zh-TW", pathname: "/" }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) =>
    <a href={href} {...props}>{children}</a>,
  usePathname: () => location.pathname,
}));
vi.mock("next-intl", async () => {
  const actual = await vi.importActual<typeof import("next-intl")>("next-intl");
  const [en, ja, ko, zhCN, zhTW] = await Promise.all([
    import("../messages/en/admin.json"), import("../messages/ja/admin.json"),
    import("../messages/ko/admin.json"), import("../messages/zh-CN/admin.json"),
    import("../messages/zh-TW/admin.json"),
  ]);
  const catalogs: Record<string, typeof en.default> = {
    en: en.default, ja: ja.default, ko: ko.default, "zh-CN": zhCN.default, "zh-TW": zhTW.default,
  };
  const translate = (locale: string, namespace: "admin.navigation" | "admin.sitePages") =>
    actual.createTranslator({ locale, messages: { admin: catalogs[locale] }, namespace });
  const translators = new Map<string, ReturnType<typeof translate>>();
  return {
    ...actual,
    useLocale: () => location.locale,
    useTranslations: (namespace: "admin.navigation" | "admin.sitePages") => {
      const key = `${location.locale}:${namespace}`;
      if (!translators.has(key)) translators.set(key, translate(location.locale, namespace));
      return translators.get(key)!;
    },
  };
});
vi.mock("./language-switcher", () => ({ LanguageSwitcher: () => null }));

const copy = adminOperationsCopy("zh-TW");
const bootstrap: AdminBootstrap = {
  admin_roles: ["owner"],
  admin_capabilities: ["admin.access", "dashboard.read", "content.read"],
  navigation: [
    { key: "dashboard", href: "/admin", group: "overview" },
    { key: "hotspots", href: "/admin/hotspots", group: "content" },
  ],
  pending_counts: {},
  system_status: {},
  environment: "test",
  can_deploy: false,
  can_manage_database: false,
};

function AdditionalSheet({ open, onClose }: { open: boolean; onClose: () => void }) {
  const ref = useModalSheet<HTMLDivElement>(open, onClose);
  return open ? <div ref={ref} role="dialog" aria-label="Additional sheet">
    <button onClick={onClose}>Close additional sheet</button>
  </div> : null;
}

function Harness({ topOpen = false, onTopClose = () => {}, showShell = true, value = bootstrap }) {
  return <AdminOperationsProvider bootstrap={value}>
    {showShell && <AdminShell><button>Original keyboard focus</button></AdminShell>}
    <AdditionalSheet open={topOpen} onClose={onTopClose} />
  </AdminOperationsProvider>;
}

function openCommand() {
  const trigger = screen.getByRole("button", { name: copy.command });
  trigger.focus();
  fireEvent.click(trigger);
  return { trigger, dialog: screen.getByRole("dialog", { name: copy.command }) };
}

describe("AdminShell command dialog", () => {
  afterEach(() => {
    window.localStorage.clear(); document.body.style.overflow = "";
    location.locale = "zh-TW"; location.pathname = "/";
  });

  it.each([
    ["en", "AI News", "AI"], ["ja", "AI 自動ニュース", "ニュース"],
    ["ko", "AI 자동 뉴스", "뉴스"], ["zh-CN", "AI 自动新闻", "新闻"],
    ["zh-TW", "AI 自動新聞", "新聞"],
  ])("uses the %s news catalog for the heading, recent page and searchable command", async (locale, name, query) => {
    location.locale = locale; location.pathname = "/admin/news";
    const localizedCopy = adminOperationsCopy(locale);
    const { container } = render(<Harness value={{ ...bootstrap, navigation: [
      { key: "dashboard", href: "/admin", group: "overview" },
      { key: "news", href: "/admin/news", group: "content" },
    ] }} />);
    const breadcrumb = screen.getByRole("navigation", { name: "Breadcrumb" });
    expect(breadcrumb.querySelector('[aria-current="page"]')?.textContent).toBe(name);
    expect(container.querySelector(".admin-topbar-mobile-title")?.textContent).toBe(name);
    fireEvent.keyDown(window, { key: "k", metaKey: true });
    const dialog = screen.getByRole("dialog", { name: localizedCopy.command });
    const recent = (await within(dialog).findByRole("heading", { name: localizedCopy.recent })).closest("section")!;
    expect(within(recent).getByRole("link", { name: `${name}${localizedCopy.groups.content}` }).getAttribute("href")).toBe("/admin/news");
    fireEvent.change(within(dialog).getByRole("textbox"), { target: { value: query } });
    const links = within(dialog).getAllByRole("link");
    expect(links).toHaveLength(1);
    expect(links[0].textContent).toBe(`${name}${localizedCopy.groups.content}`);
    expect(links[0].getAttribute("href")).toBe("/admin/news");
  });

  it("focuses search, traps Tab and closes from document Escape with focus restored", () => {
    render(<Harness />);
    const { trigger, dialog } = openCommand();
    const input = within(dialog).getByRole("textbox");
    expect(document.activeElement).toBe(input);
    const links = within(dialog).getAllByRole("link");
    const last = links.at(-1)!;
    last.focus();
    fireEvent.keyDown(document, { key: "Tab" });
    expect(document.activeElement).toBe(input);
    fireEvent.keyDown(document, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(last);
    expect(document.body.style.overflow).toBe("hidden");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(document.activeElement).toBe(trigger);
    expect(document.body.style.overflow).toBe("");
  });

  it("returns to the actual keyboard opener after Ctrl+K", () => {
    render(<Harness />);
    const opener = screen.getByRole("button", { name: "Original keyboard focus" });
    opener.focus();
    fireEvent.keyDown(window, { key: "k", ctrlKey: true });
    expect(document.activeElement).toBe(within(screen.getByRole("dialog")).getByRole("textbox"));
    fireEvent.keyDown(document, { key: "Escape" });
    expect(document.activeElement).toBe(opener);
  });

  it("leaves Escape to an active IME or a handler that already consumed it", () => {
    render(<Harness />);
    openCommand();
    fireEvent.keyDown(document, { key: "Escape", isComposing: true });
    expect(screen.getByRole("dialog", { name: copy.command })).toBeTruthy();
    const handled = new KeyboardEvent("keydown", { key: "Escape", cancelable: true });
    handled.preventDefault();
    fireEvent(document, handled);
    expect(screen.getByRole("dialog", { name: copy.command })).toBeTruthy();
  });

  it("lets only the top sheet handle Tab and Escape, retaining the lower scroll lock", () => {
    const closeTop = vi.fn();
    const view = render(<Harness onTopClose={closeTop} />);
    const { dialog } = openCommand();
    const input = within(dialog).getByRole("textbox");
    view.rerender(<Harness topOpen onTopClose={closeTop} />);
    const topButton = screen.getByRole("button", { name: "Close additional sheet" });
    fireEvent.keyDown(document, { key: "Tab" });
    expect(document.activeElement).toBe(topButton);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(closeTop).toHaveBeenCalledOnce();
    expect(screen.getByRole("dialog", { name: copy.command })).toBe(dialog);
    view.rerender(<Harness onTopClose={closeTop} />);
    expect(document.activeElement).toBe(input);
    expect(document.body.style.overflow).toBe("hidden");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(document.body.style.overflow).toBe("");
  });

  it("keeps an independent sheet locked when the command shell unmounts first", () => {
    document.body.style.overflow = "clip";
    const view = render(<Harness />);
    openCommand();
    view.rerender(<Harness topOpen />);
    view.rerender(<Harness topOpen showShell={false} />);
    expect(document.body.style.overflow).toBe("hidden");
    view.rerender(<Harness showShell={false} />);
    expect(document.body.style.overflow).toBe("clip");
  });
});
