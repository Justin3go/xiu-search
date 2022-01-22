<template>
	<div class="search-box">
		<div class="search">
			<input
				@focus="focusShow"
				@blur="blurShow"
				@keyup.enter="enterToSearch"
				class="input-box"
				type="text"
				placeholder="Search..."
				v-model="searchQuery"
			/>
			<router-link :to="{ path: '/search', query: { q: searchQuery, p: 1 } }">
				<svg class="icon" aria-hidden="true">
					<use xlink:href="#icon-sousuo"></use>
				</svg>
			</router-link>
		</div>
		<!-- {{searchedsuggests}} -->
		<div
			class="suggests"
			v-show="show && searchedsuggests.list.length != 0"
			@mouseenter="isMouseOnSerchBox = true"
			@mouseleave="isMouseOnSerchBox = false"
		>
			<div
				class="suggest-item"
				v-for="(item, index) in searchedsuggests.list"
				:key="index"
				@click="checkToSearch(item.value)"
			>
				<svg v-if="item.isHistory" class="icon" aria-hidden="true">
					<use xlink:href="#icon-lishixiao"></use>
				</svg>
				<svg v-else class="icon" aria-hidden="true">
					<use xlink:href="#icon-sousuo"></use>
				</svg>
				<div class="text">
					{{ item.value }}
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {
	onMounted,
	onUpdated,
	computed,
	reactive,
	ref,
	watch,
	watchEffect,
} from "vue";
import { useRouter } from "vue-router";
import store from "@/store/index.js";
import { getSearchSuggest } from "@/api/index.js";

export default {
	name: "search-box",
	data() {
		return {
			show: false,
			isMouseOnSerchBox: false,
		};
	},
	methods: {
		focusShow() {
			this.show = true;
		},
		blurShow() {
			// 这个if重点，没这个会造成建议选项无法点击，一点击就触发input焦点消失，然后这个建议的下拉选择项也跟着消失
			// 应该是如果点击区域不在search-box中才隐藏-->这里通过@mouseenter这个属性来判断
			if (!this.isMouseOnSerchBox) {
				this.show = false;
			} else {
				// 马上重置为false
				this.isMouseOnSerchBox = false;
			}
		},
	},
	components: {},
	setup(props) {
		const router = useRouter();
		const searchQuery = ref("");
		// 测试数据-->历史记录+搜索建议
		let historyList = JSON.parse(localStorage.getItem("historyList")) || [];

		let searchedsuggests = reactive({
			list: [],
		});
		watchEffect(async () => {
			let su = [];
			// 防止item为空tostring方法会报错
			if (historyList != []) {
				su = historyList.filter((item) => {
					return item.toString().indexOf(searchQuery.value) != -1;
				});
			}
			let suggests = [];
			// 如果历史记录大于n条就直接返回，否则就拼接请求的搜索建议
			if (su.length < 8) {
				// 获取搜索建议
				console.log("小于8条......");
				let res = await getSearchSuggest(searchQuery.value);
				console.log("res: ", res.data);
				//拼接并去前8条,同时区分是否是历史记录
				for (let i of su) {
					suggests.push({ isHistory: true, value: i });
				}
				console.log(8 - su.length);
				for (let j = 0; j < 8 - su.length; j++) {
					if (res.data.length <= j) {
						break;
					}
					suggests.push({ isHistory: false, value: res.data[j] });
				}
			} else {
				for (let i = 0; i < 8; i++) {
					suggests.push({ isHistory: true, value: su[i] });
				}
			}
			console.log("suggests: ", suggests);
			searchedsuggests.list = suggests;
		});

		function enterToSearch() {
			console.log("触发回车搜索事件......");
			store.commit("SetSearchValue", searchQuery.value);
			router.push({ path: "/search", query: { q: searchQuery.value, p: 1 } });
		}
		function checkToSearch(value) {
			// 从建议的选项中跳转
			console.log(value);
			store.commit("SetSearchValue", value);
			router.push({ path: "/search", query: { q: value, p: 1 } });
		}
		onUpdated(() => {
			console.log(searchQuery);
		});
		onMounted(() => {});
		return {
			searchedsuggests,
			searchQuery,
			enterToSearch,
			checkToSearch,
		};
	},
};
</script>

<style lang="less" scoped>
.search-box {
	background-color: #fff;
	width: 5rem;
	margin: auto;
	border-radius: 0.2rem;
	box-shadow: 0.05rem 0.05rem 0.1rem #666;
	.search {
		display: block;
		position: relative;
		left: 0;
		top: 0;
		width: 5rem;
		margin: auto;
		.input-box {
			width: 5rem;
			height: 0.4rem;
			padding: 0 0.5rem 0 0.2rem;
			color: #111;
			font-size: 0.2rem;
			border-radius: 0.2rem;
			border: 0;
			// box-shadow: 0.05rem 0.05rem 0.05rem #666;
			outline: none;
		}
		.icon {
			position: absolute;
			top: 0.05rem;
			right: 0.1rem;
			height: 0.3rem;
			width: 0.3rem;
			fill: #999;
		}
	}
	.suggests {
		padding-bottom: 0.15rem;
		margin: 0 0.1rem 0 0.1rem;
		border-top: #ccc 1px solid;
		.suggest-item {
			margin-top: 0.1rem;
			height: 0.3rem;
			padding-left: 0.1rem;
			cursor: pointer;
			display: flex;
			justify-content: left;
			align-items: center;
			.icon {
				height: 0.15rem;
				width: 0.15rem;
				fill: #999;
			}
			.text {
				width: 4.3rem;
				padding-left: 0.1rem;
				line-height: 0.3rem;
				overflow: hidden;
				text-overflow: ellipsis;
				display: -webkit-box;
				-webkit-box-orient: vertical;
				-webkit-line-clamp: 1;
				text-align: left;
			}
		}
	}
}
</style>
