<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const room_id = ref(2)
const preview_limit = ref(2)
const out = ref(null)
const run = async () => {
  const body = { room_id: room_id.value, persist: true }
  if (preview_limit.value !== null && preview_limit.value !== '') body.preview_limit = Number(preview_limit.value)
  out.value = await postJSON('/api/estimate', body)
}
</script>
<template><div class="page"><h1>估漆工作台</h1>
<label>房间ID <input v-model.number="room_id" /></label>
<label>预览条数 <input v-model.number="preview_limit" type="number" min="0" /></label>
<button @click="run">估算</button>
<template v-if="out">
  <p>毛墙 {{ out.gross_m2 }} m² · 开洞扣除合计 {{ out.openings_m2 }} m² · 净 <strong>{{ out.net_m2 }}</strong> m² · {{ out.liters }} 升 · {{ out.coats }} 遍</p>
  <h2>开洞预览（共 {{ out.openings_count }} 条）</h2>
  <ul>
    <li v-for="o in out.openings_preview" :key="o.index">#{{ o.index + 1 }} {{ o.kind || '洞口' }} {{ o.w }}×{{ o.h }} 扣除 {{ o.area_m2.toFixed(2) }} m²</li>
  </ul>
  <p v-if="out.preview_truncated" class="hint">预览仅前 {{ out.openings_preview.length }} 条，合计与升数仍按全部 {{ out.openings_count }} 条开洞钉选。</p>
</template>
</div></template>
