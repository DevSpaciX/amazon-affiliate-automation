<template>
  <v-container class="py-10" style="max-width: 1100px;">
    <!-- HERO -->
    <v-card class="glass" rounded="xl">
      <v-card-text class="pa-6 pa-md-8">
        <div class="d-flex flex-wrap align-start justify-space-between ga-4">
          <div>
            <div class="text-h5 section-title">Amazon Affiliate Automation</div>
            <div class="text-body-2 muted mt-1" style="max-width: 760px;">
              End-to-end demo: generate a tagged link → redirect buyer (logs click) → simulate checkout → revenue appears in table.
            </div>
          </div>

          <div class="d-flex align-center ga-2">
            <v-btn variant="tonal" rounded="xl" class="clickable" @click="loadAll" :loading="loadingAll">
              Refresh data
            </v-btn>
            <v-chip variant="outlined" class="muted" style="border-color: var(--stroke);">
              Mode: <b class="ml-1" style="color: var(--text);">{{ health?.mode ?? "…" }}</b>
            </v-chip>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <v-row class="mt-6">
      <!-- LEFT: Link flow -->
      <v-col cols="12" md="7">
        <v-card class="glass" rounded="xl">
          <v-card-text class="pa-6">
            <div class="d-flex align-center justify-space-between">
              <div>
                <div class="text-subtitle-1 section-title">1) Smart link generation</div>
                <div class="text-caption muted">This is clickable: “Generate link”, “Open redirect”, “Simulate buy”, “Copy”.</div>
              </div>
            </div>

            <v-text-field
              v-model="urlOrAsin"
              class="mt-4"
              label="Amazon URL or ASIN"
              variant="outlined"
              density="comfortable"
              hide-details
            />

            <div class="d-flex flex-wrap ga-2 mt-4">
              <v-btn color="primary" rounded="xl" size="large" :loading="loadingLink" @click="onGenerate">
                Generate link
              </v-btn>

              <v-btn variant="tonal" rounded="xl" class="clickable" @click="setExample('https://www.amazon.com/dp/B08N5WRWNW')">
                Use Echo Dot example
              </v-btn>

              <v-btn variant="tonal" rounded="xl" class="clickable" @click="setExample('https://www.amazon.com/dp/B09V3KXJPB')">
                Use Fire TV example
              </v-btn>
            </div>

            <v-divider class="my-6" />

            <!-- Link outputs -->
            <div v-if="link">
              <div class="text-caption muted">Generated outputs</div>

              <v-card class="mt-2" rounded="lg" style="background: rgba(255,255,255,.04); border: 1px solid var(--stroke);">
                <v-card-text class="py-4">
                  <div class="d-flex flex-wrap align-center justify-space-between ga-3">
                    <div>
                      <div class="text-caption muted">ASIN</div>
                      <div class="text-subtitle-1" style="font-weight: 800;">{{ link.asin }}</div>
                    </div>

                    <div class="d-flex align-center ga-2">
                      <v-btn variant="tonal" rounded="xl" class="clickable" @click="copy(link.asin)">
                        Copy ASIN
                      </v-btn>
                    </div>
                  </div>

                  <v-divider class="my-4" />

                  <div class="d-flex flex-wrap align-center justify-space-between ga-3">
                    <div style="min-width: 260px; max-width: 680px;">
                      <div class="text-caption muted">Affiliate URL (opens Amazon)</div>
                      <div class="text-body-2" style="word-break: break-all;">
                        {{ link.affiliate_url }}
                      </div>
                    </div>

                    <div class="d-flex align-center ga-2">
                      <v-btn color="secondary" variant="tonal" rounded="xl" class="clickable" :href="link.affiliate_url" target="_blank">
                        Open
                      </v-btn>
                      <v-btn variant="tonal" rounded="xl" class="clickable" @click="copy(link.affiliate_url)">
                        Copy
                      </v-btn>
                    </div>
                  </div>

                  <v-divider class="my-4" />

                  <div class="d-flex flex-wrap align-center justify-space-between ga-3">
                    <div style="min-width: 260px; max-width: 680px;">
                      <div class="text-caption muted">Redirect URL (logs click)</div>
                      <div class="text-body-2" style="word-break: break-all;">
                        {{ link.redirect_url }}
                        <span class="muted">?buyer=demo-buyer</span>
                      </div>
                    </div>

                    <div class="d-flex align-center ga-2">
                      <v-btn
                        color="success"
                        variant="tonal"
                        rounded="xl"
                        class="clickable"
                        :href="link.redirect_url + '?buyer=demo-buyer'"
                        target="_blank"
                      >
                        Open redirect
                      </v-btn>
                      <v-btn variant="tonal" rounded="xl" class="clickable" @click="copy(link.redirect_url)">
                        Copy
                      </v-btn>
                    </div>
                  </div>
                </v-card-text>
              </v-card>

              <!-- Simulate buy -->
              <div class="d-flex flex-wrap align-center ga-3 mt-5">
                <v-text-field
                  v-model.number="qty"
                  type="number"
                  min="1"
                  label="Quantity"
                  variant="outlined"
                  density="comfortable"
                  hide-details
                  style="max-width: 190px;"
                />
                <v-btn color="success" rounded="xl" size="large" :loading="loadingBuy" @click="onBuy">
                  Simulate buy
                </v-btn>

                <div class="text-caption muted">
                  Creates a transaction row using commission rates (mock verification).
                </div>
              </div>
            </div>

            <div v-else class="muted text-body-2">
              Click <b>Generate link</b> to unlock “Open redirect” and “Simulate buy”.
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- RIGHT: Rates + KPI -->
      <v-col cols="12" md="5">
        <v-card class="glass" rounded="xl">
          <v-card-text class="pa-6">
            <div>
              <div class="text-subtitle-1 section-title">2) Commission rates</div>
              <div class="text-caption muted">In mock mode this is fixed. In live mode: replace by report ingestion.</div>
            </div>

            <v-divider class="my-4" />

            <v-list density="comfortable" bg-color="transparent" class="pa-0">
              <v-list-item v-for="r in rates" :key="r.category" class="px-0">
                <v-list-item-title class="text-body-2">
                  <b>{{ r.category }}</b>
                </v-list-item-title>
                <template #append>
                  <v-chip variant="tonal" style="background: rgba(255,255,255,.06); border: 1px solid var(--stroke);">
                    {{ (r.rate * 100).toFixed(2) }}%
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>

            <v-divider class="my-6" />

            <div class="text-subtitle-1 section-title mb-3">3) Snapshot</div>
            <v-row>
              <v-col cols="6">
                <v-card rounded="lg" style="background: rgba(255,255,255,.04); border: 1px solid var(--stroke);">
                  <v-card-text>
                    <div class="text-caption muted">Transactions</div>
                    <div class="text-h6" style="font-weight: 900;">{{ txs.length }}</div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="6">
                <v-card rounded="lg" style="background: rgba(255,255,255,.04); border: 1px solid var(--stroke);">
                  <v-card-text>
                    <div class="text-caption muted">Total income</div>
                    <div class="text-h6" style="font-weight: 900;">${{ totalIncome }}</div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- TABLE -->
      <v-col cols="12" class="mt-2">
        <v-card class="glass" rounded="xl">
          <v-card-text class="pa-6">
            <div class="d-flex align-center justify-space-between">
              <div>
                <div class="text-subtitle-1 section-title">4) Accounting dashboard</div>
                <div class="text-caption muted">This table updates after “Simulate buy”.</div>
              </div>
              <v-btn variant="tonal" rounded="xl" class="clickable" :loading="loadingTx" @click="loadTx">
                Refresh table
              </v-btn>
            </div>

            <v-divider class="my-4" />

            <v-data-table
              :headers="headers"
              :items="txs"
              :items-per-page="10"
              density="comfortable"
              class="rounded-xl"
            >
              <template #item.item_price="{ item }">
                ${{ Number(item.item_price).toFixed(2) }}
              </template>
              <template #item.affiliate_income="{ item }">
                <b>${{ Number(item.affiliate_income).toFixed(2) }}</b>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snack.show" :timeout="1600">
      {{ snack.text }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { api } from "../api";

type LinkOut = { asin: string; affiliate_url: string; redirect_url: string };
type Rate = { category: string; rate: number };
type Tx = {
  transaction_id: string;
  product_name: string;
  quantity: number;
  item_price: number;
  affiliate_income: number;
};
type Health = { ok: boolean; mode: string };

const urlOrAsin = ref("https://www.amazon.com/dp/B08N5WRWNW");
const link = ref<LinkOut | null>(null);
const qty = ref(1);

const rates = ref<Rate[]>([]);
const txs = ref<Tx[]>([]);
const health = ref<Health | null>(null);

const loadingLink = ref(false);
const loadingBuy = ref(false);
const loadingTx = ref(false);
const loadingAll = ref(false);

const snack = ref({ show: false, text: "" });

const headers = [
  { title: "Transaction ID", key: "transaction_id" },
  { title: "Product Name", key: "product_name" },
  { title: "Quantity", key: "quantity" },
  { title: "Item Price", key: "item_price" },
  { title: "Affiliate Income", key: "affiliate_income" },
];

const totalIncome = computed(() => {
  const sum = txs.value.reduce((acc, t) => acc + (Number(t.affiliate_income) || 0), 0);
  return sum.toFixed(2);
});

function setExample(v: string) {
  urlOrAsin.value = v;
  snack.value = { show: true, text: "Example set ✅ (now click “Generate link”)" };
}

async function copy(text: string) {
  try {
    await navigator.clipboard.writeText(text);
    snack.value = { show: true, text: "Copied ✅" };
  } catch {
    snack.value = { show: true, text: "Copy failed (check browser permissions)" };
  }
}

async function onGenerate() {
  loadingLink.value = true;
  try {
    const { data } = await api.post("/api/links", { url_or_asin: urlOrAsin.value });
    link.value = data;
    snack.value = { show: true, text: "Link generated ✅" };
  } finally {
    loadingLink.value = false;
  }
}

async function onBuy() {
  if (!link.value) return;
  loadingBuy.value = true;
  try {
    const code = link.value.redirect_url.split("/").pop();
    await api.post("/api/simulate-buy", { link_code: code, buyer_id: "demo-buyer", quantity: qty.value });
    await loadTx();
    snack.value = { show: true, text: "Transaction created ✅" };
  } finally {
    loadingBuy.value = false;
  }
}

async function loadRates() {
  const { data } = await api.get("/api/commission-rates");
  rates.value = data;
}

async function loadTx() {
  loadingTx.value = true;
  try {
    const { data } = await api.get("/api/transactions");
    txs.value = data.items;
  } finally {
    loadingTx.value = false;
  }
}

async function loadHealth() {
  const { data } = await api.get("/api/health");
  health.value = data;
}

async function loadAll() {
  loadingAll.value = true;
  try {
    await Promise.all([loadHealth(), loadRates(), loadTx()]);
  } finally {
    loadingAll.value = false;
  }
}

onMounted(() => {
  void loadAll();
});
</script>
