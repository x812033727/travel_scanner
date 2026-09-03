"use client";

import { Soup } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { FoodsResponse } from "@/lib/foods";
import { FoodDishCard } from "@/components/food-dish-card";

export function FoodDishesSection({
  destinationId,
  countryCode,
}: {
  destinationId: string;
  countryCode: string | null;
}) {
  const t = useTranslations("foods");
  const [foods, setFoods] = useState<FoodsResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const cityParams = new URLSearchParams({ destination_id: destinationId, limit: "6" });
    api<FoodsResponse>(`/foods?${cityParams}`)
      .then((result) => {
        if (result.items.length > 0 || !countryCode) return result;
        const countryParams = new URLSearchParams({ country_code: countryCode, limit: "6" });
        return api<FoodsResponse>(`/foods?${countryParams}`);
      })
      .then(setFoods)
      .catch((reason: Error) => setError(reason.message));
  }, [countryCode, destinationId]);

  return (
    <section className="mt-10" aria-labelledby="food-dishes-title">
      <h2 id="food-dishes-title" className="flex items-center gap-2 text-xl font-bold">
        <Soup size={20} className="text-[var(--coral)]" />
        {t("fallbackDishes")}
      </h2>
      {error && (
        <div role="alert" className="mt-4 rounded-3xl bg-[var(--coral-soft)] p-6">
          {error}
        </div>
      )}
      {!error && !foods && (
        <div className="mt-4 rounded-3xl border border-[var(--line)] bg-white p-8 text-[var(--muted)]">
          {t("loading")}
        </div>
      )}
      {foods && (
        <div className="mt-4 grid gap-5 md:grid-cols-2">
          {foods.items.map((food) => (
            <FoodDishCard key={food.id} food={food} />
          ))}
        </div>
      )}
    </section>
  );
}
