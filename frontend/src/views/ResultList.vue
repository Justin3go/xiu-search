<template>
	<div class="result-list">
		<detail-nav></detail-nav>
		<some-tips></some-tips>
		<list></list>
		<related-search></related-search>
		<el-backtop />
		<page-index></page-index>
	</div>
</template>

<script>
import DetailNav from "@/components/ResultList/DetailNav.vue";
import SomeTips from "@/components/ResultList/SomeTips.vue";
import List from "@/components/ResultList/List.vue";
import RelatedSearch from "@/components/ResultList/RelatedSearch.vue";
import PageIndex from "@/components/ResultList/PageIndex.vue";

import { onMounted, onBeforeMount, reactive } from "vue";
import { useRoute } from "vue-router";
import { getSearchResult } from "@/api/index.js";

import store from "@/store/index.js";
export default {
	components: {
		DetailNav,
		SomeTips,
		List,
		RelatedSearch,
		PageIndex,
	},

	setup(props) {
		const route = useRoute();
		let state = reactive({
			hitList: [],
			page: 0,
			pageNums: 0,
			searchCostTime: 0,
			totalNums: 0,
		});
		onBeforeMount(async () => {
			// 直接放到SearchBoxDetail中执行，不然父子组件的执行顺序不对
			// let q = route.query.q;
			// let p = route.query.p;
			// let res = await getSearchResult(q, p);
			// console.log("getSearchResult: ", res.data);
			// store.commit("SetSearchResult", res.data);
			// // 注意这里，刷新或者进入这个界面也需要把搜索值提交上去
			// store.commit("SetSearchValue", q);
		});
		return {
			state,
		};
	},
};
</script>
<style lang="less" scoped>
hr {
	margin-top: 0.5rem;
}
</style>
