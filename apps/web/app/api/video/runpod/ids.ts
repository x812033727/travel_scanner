// The broker's session ids are UUIDs; the forwarders check them so a stray path never reaches the API.
export const SESSION_ID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
