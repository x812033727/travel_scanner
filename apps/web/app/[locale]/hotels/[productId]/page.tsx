import { notFound } from "next/navigation";
import { SiteHeader } from "@/components/site-header";
import { HotelBookingPage } from "@/components/travel-services/hotel-booking-page";

export default async function HotelPage({ params }: {
  params: Promise<{ locale: string; productId: string }>;
}) {
  const { productId } = await params;
  if (!/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i.test(productId)) notFound();
  // This ordinary locale route must never import the public Stay22 SDK document.
  return <><SiteHeader /><HotelBookingPage productId={productId.toLowerCase()} /></>;
}
