import type { NextRequest } from "next/server";
import { forward, type Context } from "./forward";

export function GET(request: NextRequest, context: Context) {
  return forward(request, context, "GET");
}

export function PUT(request: NextRequest, context: Context) {
  return forward(request, context, "PUT");
}

export function POST(request: NextRequest, context: Context) {
  return forward(request, context, "POST");
}
