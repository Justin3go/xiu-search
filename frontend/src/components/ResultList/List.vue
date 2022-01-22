<template>
	<div class="list">
		<el-empty
			v-if="SearchResult.totalNums == 0"
			description="没有相关内容，试试其他关键词吧~"
			style="margin-top: 1.8rem"
		></el-empty>
		<div class="hit-list">
			<div
				class="hit-item"
				v-for="(item, i) in SearchResult.hitList"
				:key="i"
				:class="{ active: IsActive && current_index == i }"
				@mouseenter="(IsActive = true), (current_index = i)"
				@mouseleave="(IsActive = false), (current_index = -1)"
			>
				<a
					class="title"
					:href="item.page_url"
					target="_blank"
					v-html="item.title"
				></a>
				<div class="content" v-html="item.content"></div>
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
			current_index: -1, // 找到当前卡片，避免全部高亮
			loading: false,
			svg: `
        <path class="path" d="
          M 30 15
          L 28 17
          M 25.61 25.61
          A 15 15, 0, 0, 1, 15 30
          A 15 15, 0, 1, 1, 27.99 7.5
          L 15 15
        " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
      `,
		};
	},
	props: ["hitList"],
	updated() {
		console.log("SearchResult: ", this.SearchResult);
	},
	computed: {
		...mapState(["SearchResult"]),
	},
};
</script>

<style lang="less">
.list {
	min-height: 7rem;
	.hit-list {
		margin-left: 1.5rem;
		text-align: left;
		width: 8rem;
	}
	.hit-item {
		border-radius: 0.1rem;
		margin-top: 0.1rem;
		padding: 0.1rem 0.1rem 0.2rem 0.1rem;
		.title {
			font-size: 0.2rem;
			font-weight: 900;
		}
		.content {
			color: #666;
			overflow: hidden;
			text-overflow: ellipsis;
			display: -webkit-box;
			-webkit-box-orient: vertical;
			-webkit-line-clamp: 3;

			.highlight {
				color: rgb(255, 13, 13);
				font-weight: 400;
			}
		}
	}
	.active {
		box-shadow: 0.05rem 0.05rem 0.1rem #999;
		background-color: #eee;
		transition: all 0.8s;
	}
}
</style>
