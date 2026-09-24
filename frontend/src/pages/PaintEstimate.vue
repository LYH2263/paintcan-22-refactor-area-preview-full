<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const room_id = ref(1)
const preview_limit = ref(3)
const out = ref(null)
const run = async () => {
  out.value = await postJSON('/api/estimate', {
    room_id: room_id.value,
    preview_limit: preview_limit.value,
    persist: true,
  })
}
</script>
<template><div class="page"><h1>估漆工作台</h1>
<label>房间ID <input v-model.number="room_id" /></label>
<label>预览条数 <input v-model.number="preview_limit" /></label>
<button @click="run">估算</button>
<template v-if="out">
  <p>毛墙 {{ out.gross_m2 }} m² · 开洞合计 {{ out.openings_m2 }} m² · <strong>净 {{ out.net_m2 }} m²</strong></p>
  <p>{{ out.liters }} 升 · {{ out.coats }} 遍（覆盖率 {{ out.coverage }} m²/升）</p>
  <h2>开洞预览（{{ out.preview_count }}/{{ out.opening_count }} 条）</h2>
  <ul>
    <li v-for="o in out.openings_preview" :key="o.index">
      #{{ o.index + 1 }} {{ o.w }}×{{ o.h }} m · 扣除 {{ o.area_m2.toFixed(2) }} m²
    </li>
  </ul>
  <p v-if="out.preview_truncated" class="hint">仅展示前 {{ out.preview_count }} 条开洞；合计与净面积、升数仍按全量 {{ out.opening_count }} 条钉选。</p>
</template></div></template>
