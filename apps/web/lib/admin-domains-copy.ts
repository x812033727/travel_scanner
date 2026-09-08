import en from "./admin-domains-messages/en.json";
import zhTW from "./admin-domains-messages/zh-TW.json";
import zhCN from "./admin-domains-messages/zh-CN.json";
import ja from "./admin-domains-messages/ja.json";
import ko from "./admin-domains-messages/ko.json";

export type AdminDomainsCopy = Record<keyof typeof en, string>;
const catalogs: Record<string, AdminDomainsCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };
export function adminDomainsCopy(locale: string): AdminDomainsCopy { return catalogs[locale] || en; }
