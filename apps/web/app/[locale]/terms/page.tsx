import { SiteInformationPage, siteInformationMetadata } from "@/components/site-information-page";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props) {
  return siteInformationMetadata("terms", (await params).locale);
}

export default async function Page({ params }: Props) {
  return <SiteInformationPage slug="terms" locale={(await params).locale} />;
}
