<template>
	<div class="user-profile">
		<div v-show="leftShow" class="left"></div>
		<div class="center">
			<div class="user">
				<img class="avator" :src="avator" alt="" />
				<div class="username">{{ username }}</div>
				<div class="email">邮箱：{{ email }}</div>
				<div class="btns">
					<div
						class="btn1"
						:class="{ active: IsActive1 }"
						@mouseenter="IsActive1 = true"
						@mouseleave="IsActive1 = false"
						@click="resetemail"
					>
						重置邮箱
					</div>
					<div
						class="btn2"
						:class="{ active: IsActive2 }"
						@mouseenter="IsActive2 = true"
						@mouseleave="IsActive2 = false"
						@click="resetpassword"
					>
						重置密码
					</div>
				</div>
			</div>
			<div class="content">
				<img src="@/assets/userprofile.svg" alt="" />
			</div>
		</div>
		<div v-show="rightShow" class="right"></div>
	</div>
</template>
<script>
export default {
	data() {
		return {
			IsActive1: false,
			IsActive2: false,
			leftShow: false,
			rightShow: false,
		};
	},
	methods: {
		resetemail() {
			this.leftShow = !this.leftShow
			alert("别点了，不想写前端了...")
		},
		resetpassword() {
			this.rightShow = !this.rightShow
			alert("别点了，不想写前端了...")
		},
	},
};
</script>
<script setup>
import { onMounted } from "vue";
import { getIP } from "@/api/index.js";
import store from "@/store/index.js";

const avator = getIP() + store.state.UserProfile.avator || "";
const email = store.state.UserProfile.email;
const id = store.state.UserProfile.id;
const username = store.state.UserProfile.username;

onMounted(async () => {});
</script>
<style lang="less" scoped>
.user-profile {
	margin: 0.3rem 0.3rem 0rem;
	.center {
		.user {
			margin: auto;
			padding: 0.2rem 0.2rem 0.3rem 0.2rem;
			background-color: #fff;
			width: 4.5rem;
			border-radius: 0.2rem;
			box-shadow: 0.1rem 0.1rem 0.1rem #999;
			.avator {
				margin-left: 1.55rem;
				height: 1rem;
				width: 1rem;
				border-radius: 0.5rem;
			}
			.username {
				text-align: center;
				font-size: 0.2rem;
			}
			.email {
				margin-top: 0.3rem;
			}
			.btns {
				margin-top: 0.2rem;
				color: #999;
				.btn1 {
					display: block;
					margin-top: 0.1rem;
					cursor: pointer;
					height: 0.3rem;
					line-height: 0.3rem;
					width: 0.75rem;
					text-align: center;
					border-radius: 0.05rem;
				}
				.btn2 {
					margin-top: 0.1rem;
					cursor: pointer;
					height: 0.3rem;
					line-height: 0.3rem;
					width: 0.75rem;
					text-align: center;
					border-radius: 0.05rem;
				}
				.active {
					color: #111;
					background-color: #999;
				}
			}
		}
		.content {
			z-index: 20;
			img {
				margin: 0.1rem 2.25rem 0;
				z-index: 1000;
			}
		}
	}
}
.left {
	position: absolute;
	top: 0.3rem;
	left: 0.3rem;
	margin: auto;
	padding: 0.2rem 0.2rem 0.3rem 0.2rem;
	background-color: #fff;
	width: 4.5rem;
	height: 2.5rem;
	border-radius: 0.2rem;
	box-shadow: 0.1rem 0.1rem 0.1rem #999;
}
.right {
	position: absolute;
	top: 0.3rem;
	right: 0.3rem;
	margin: auto;
	padding: 0.2rem 0.2rem 0.3rem 0.2rem;
	background-color: #fff;
	width: 4.5rem;
	height: 2.5rem;
	border-radius: 0.2rem;
	box-shadow: 0.1rem 0.1rem 0.1rem #999;
}
</style>
