<template>
	<div></div>
</template>

<script setup>
import { activate } from "@/api/index.js";
import { useRouter, useRoute } from "vue-router";
import { ElLoading } from "element-plus";
const router = useRouter();
const route = useRoute();
const uid = route.query.uid;
const token = route.query.token;
const loading = ElLoading.service({
	lock: true,
	text: "拼命加载中...",
	background: "rgba(255,255,255,0.5)",
});
activate(uid, token)
	.then((res) => {
    loading.close()
		alert("激活成功...");
		router.push("/");
	})
	.catch((err) => {
		loading.close()
		alert("激活失败:" + err.response.data.detail);
		router.push("/");
	});
</script>
