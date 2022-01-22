<template>
	<div class="page-index">
		<div class="select-pages" v-if="SearchResult.totalNums != 0">
			<div
				v-if="SearchResult.page != 1"
				class="previous-page"
				:class="{ active: PActive }"
				@mouseenter="PActive = true"
				@mouseleave="PActive = false"
				@click="previous"
			>
				&lt
			</div>
			<!-- 这里active可以再总体或一个是否等于当前页码 -->
			<div
				class="page-item"
				:class="{ active: (IsActive && CurrentIndex == i) || (i == SearchResult.page) }"
				v-for="i in pagers"
				:key="i"
				@mouseenter="(IsActive = true), (CurrentIndex = i)"
				@mouseleave="(IsActive = false), (CurrentIndex = -1)"
				@click="jump(i)"
			>
				{{ i }}
			</div>
			<div
				v-if="SearchResult.page != SearchResult.pageNums"
				class="next-page"
				:class="{ active: NActive }"
				@mouseenter="NActive = true"
				@mouseleave="NActive = false"
				@click="next"
			>
				&gt
			</div>
		</div>
	</div>
</template>

<script>
import store from "@/store/index.js";
import { mapState, mapMutations } from "vuex";

export default {
	data() {
		return {
			IsActive: false,
			CurrentIndex: -1,
			PActive: false,
			NActive: false,
		};
	},
	computed: {
		...mapState(["SearchResult", "SearchValue"]),
		// 动态维护一个数组随页码以及页面总数变化而变化
		pagers() {
			console.log("SearchValue: ", this.SearchValue)
			const array = [];
			const perPages = 9;  // 显示多少页
			const pageCount = this.SearchResult.pageNums;
			let current = this.SearchResult.page;
			const _offset = (perPages - 1) / 2;

			const offset = {
				start: current - _offset,
				end: current + _offset,
			};
			//-1, 3
			if (offset.start < 1) {
				offset.end = offset.end + (1 - offset.start);
				offset.start = 1;
			}
			if (offset.end > pageCount) {
				offset.start = offset.start - (offset.end - pageCount);
				offset.end = pageCount;
			}
			if (offset.start < 1) offset.start = 1;

			this.showPrevMore = offset.start > 1;
			this.showNextMore = offset.end < pageCount;

			for (let i = offset.start; i <= offset.end; i++) {
				array.push(i);
			}
			return array;
		},
	},
	methods: {
		next() {
			this.$router.push({
				path: "/search",
				query: { q: this.SearchValue, p: this.SearchResult.page + 1 },
			});
		},
		previous() {
			this.$router.push({
				path: "/search",
				query: { q: this.SearchValue, p: this.SearchResult.page - 1 },
			});
		},
		jump(i) {
			// 因为在Searchboxdetail里面监听了路由的变化，所以这里一改变路由就可以直接跳转
			// 这里P也不用提交，因为跳转->被监听到->获取数据->提交
			if(this.SearchResult.page != i){
				// 不是当前页才跳转
				this.$router.push({
					path: "/search",
					query: { q: this.SearchValue, p: i },
				});
			}
		},
	},
};
</script>

<style lang="less" scoped>
.page-index {
	margin-top: 0.4rem;
	border-top: 1px solid #999;
	// background-color: #bbb;
	.select-pages {	
		margin: 0.4rem 0 0rem 1.5rem;
		padding-bottom: 1rem;
		width: 7rem;
		color: blue;
		display: flex;
		justify-content: left;
		align-items: center;
		.previous-page {
			margin-left: 0rem;
			height: 0.4rem;
			width: 0.4rem;
			background-color: #eee;
			border-radius: 0.1rem;
			box-shadow: 0.05rem 0.05rem 0.05rem #999;
			text-align: center;
			line-height: 0.4rem;
			cursor: pointer; 
		}
		.page-item {
			margin-left: 0.3rem;
			height: 0.4rem;
			width: 0.4rem;
			background-color: #eee;
			border-radius: 0.1rem;
			box-shadow: 0.05rem 0.05rem 0.05rem #999;
			text-align: center;
			line-height: 0.4rem;
			cursor: pointer; 
		}
		.next-page {
			margin-left: 0.3rem;
			height: 0.4rem;
			width: 0.4rem;
			background-color: #eee;
			border-radius: 0.1rem;
			box-shadow: 0.05rem 0.05rem 0.05rem #999;
			text-align: center;
			line-height: 0.4rem;
			cursor: pointer; 
		}
		.active {
			color: #fff;
			background-color: rgb(92, 92, 255);
		}
	}
}
</style>
