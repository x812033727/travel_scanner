import { NextRequest } from "next/server";
import { callback } from "../../_shared";

type Context = { params: Promise<{ provider: string }> };

export async function GET(request: NextRequest, context: Context) {
  return callback(request, (await context.params).provider);
}

export async function POST(request: NextRequest, context: Context) {
  return callback(request, (await context.params).provider);
}
