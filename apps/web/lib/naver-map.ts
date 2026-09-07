const DESTINATION_SEARCH_LABELS: Record<string, string> = {
  seoul: "서울",
  busan: "부산",
  jeju: "제주",
  daegu: "대구",
  gyeongju: "경주",
  jeonju: "전주",
};

export function naverMapSearchUrl(
  placeName: string,
  destinationId: string,
  fallbackCityName?: string,
): string {
  const city = DESTINATION_SEARCH_LABELS[destinationId] || fallbackCityName || destinationId;
  const query = [placeName.trim(), city.trim()].filter(Boolean).join(" ");
  return `https://map.naver.com/p/search/${encodeURIComponent(query)}`;
}
