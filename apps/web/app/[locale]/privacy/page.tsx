import { SiteInformationPage, siteInformationMetadata } from "@/components/site-information-page";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props) {
  return siteInformationMetadata("privacy", (await params).locale);
}

export default async function Page({ params }: Props) {
  return <SiteInformationPage slug="privacy" locale={(await params).locale} />;
}
