import { AdminNewsWorkspace } from "@/components/admin-news-workspace";
import { AdminNewsEditorial } from "@/components/admin-news-editorial";

export default function AdminNewsPage() {
  return <main className="admin-page"><AdminNewsWorkspace /><AdminNewsEditorial /></main>;
}
