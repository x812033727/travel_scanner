import { hydrateRoot } from "react-dom/client";
import { useEffect } from "react";
import { Page, type Props } from "./fixture";

const payload = document.getElementById("visible-props");
const container = document.getElementById("root");
if (!payload || !container) throw new Error("Missing fixture props");
const props: Props = JSON.parse(payload.textContent ?? "");
function ReadyPage() {
  useEffect(() => { document.documentElement.dataset.hydrated = "true"; }, []);
  return <Page {...props} />;
}
hydrateRoot(container, <ReadyPage />);
