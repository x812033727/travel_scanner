import { NextRequest } from "next/server";
import { forwardPairing } from "../forward";

export async function POST(request: NextRequest) {
  return forwardPairing(request, "pairings/poll");
}
