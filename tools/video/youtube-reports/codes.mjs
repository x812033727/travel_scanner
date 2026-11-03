// What the Reporting API's numeric dimension codes mean, copied from
// https://developers.google.com/youtube/reporting/v1/reports/dimensions (read 2026-11-02).
// A code not listed here is shown as itself, never guessed.

export const TRAFFIC_SOURCE_TYPE = {
  0: "Direct or unknown",
  1: "YouTube advertising",
  3: "Browse features",
  4: "YouTube channels",
  5: "YouTube search",
  7: "Suggested videos",
  8: "Other YouTube features",
  9: "External",
  11: "Video cards and annotations",
  14: "Playlists",
  17: "Notifications",
  18: "Playlist pages",
  19: "Programming from claimed content",
  20: "Interactive video endscreen",
  23: "Stories",
  24: "Shorts",
  25: "Product pages",
  26: "Hashtag pages",
  27: "Sound pages",
  28: "Live redirect",
  29: "Podcasts",
  30: "Remixed video",
  31: "Vertical live feed",
  32: "Related video (Shorts player)",
};

// What traffic_source_detail holds for a type, when the page says.
export const TRAFFIC_SOURCE_DETAIL = {
  1: "ad type",
  3: "browse feature",
  4: "channel id",
  5: "search term",
  7: "video id",
  8: "page type",
  9: "external page",
  17: "notification type",
  19: "video id",
  20: "video id",
  25: "product id",
  26: "hashtag",
  27: "video id",
  28: "channel id",
  30: "video id",
};

export const PLAYBACK_LOCATION_TYPE = {
  0: "Watch page or YouTube app",
  1: "Embedded on another site or app",
  2: "Channel page",
  5: "Other",
  7: "Home, subscriptions or another browse feature",
  8: "Search results page",
  10: "Shorts feed",
};

export const DEVICE_TYPE = {
  100: "Unknown",
  101: "Computer",
  102: "TV",
  103: "Game console",
  104: "Mobile phone",
  105: "Tablet",
};

export const OPERATING_SYSTEM = {
  1: "Other", 2: "Windows", 3: "Windows Mobile", 4: "Android", 5: "iOS", 6: "Symbian", 7: "Blackberry",
  9: "Macintosh", 10: "PlayStation", 11: "Bada", 12: "WebOS", 13: "Linux", 14: "Hiptop", 15: "MeeGo",
  16: "Wii", 17: "Xbox", 18: "PlayStation Vita", 19: "Smart TV", 20: "Nintendo 3DS", 21: "Chromecast",
  22: "Tizen", 23: "Firefox", 24: "RealMedia", 25: "KaiOS", 26: "Roku", 27: "Nintendo Switch",
  28: "Apple tvOS", 29: "Fire OS", 30: "ChromeOS", 31: "Vidaa", 32: "VegaOS",
};

export const CODED_COLUMNS = {
  traffic_source_type: TRAFFIC_SOURCE_TYPE,
  playback_location_type: PLAYBACK_LOCATION_TYPE,
  device_type: DEVICE_TYPE,
  operating_system: OPERATING_SYSTEM,
};

export function codeName(column, value) {
  const table = CODED_COLUMNS[column];
  if (!table || value === "" || value === undefined || value === null) return "";
  return table[Number(value)] ?? `code ${value}`;
}

/** ``result`` with a ``<column>_name`` column after every coded column it has. */
export function withNames(result) {
  const columns = [];
  const plan = [];
  result.columns.forEach((name, index) => {
    columns.push(name);
    plan.push([index, null]);
    if (CODED_COLUMNS[name]) {
      columns.push(`${name}_name`);
      plan.push([index, name]);
    }
  });
  const rows = result.rows.map((row) => plan.map(([index, coded]) => (coded ? codeName(coded, row[index]) : row[index])));
  return { ...result, columns, rows };
}
