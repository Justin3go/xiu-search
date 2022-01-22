<template>
	<div class="login">
		<div class="welcome">欢迎回到XiuSearch这个大家庭~</div>
		<div class="container">
			<div class="pic">
				<img src="@/assets/login.svg" alt="" />
			</div>
			<div class="login-part">
				<div class="some-tips">在这里登录您的账号</div>
				<el-form
					ref="form"
					:model="form"
					:label-position="'top'"
					label-width="0.8rem"
					:rules="rules"
					class="demo-dynamic"
				>
					<el-form-item label="您的邮箱:" prop="userEmail">
						<el-autocomplete
							v-model="form.userEmail"
							:fetch-suggestions="querySearchEmail"
							:trigger-on-focus="false"
							placeholder="请输入您的邮箱"
							clearable
							type="email"
						>
						</el-autocomplete>
					</el-form-item>

					<el-form-item label="您的密码:" prop="userPassword">
						<el-input
							v-model="form.userPassword"
							placeholder="请输入您的密码"
							show-password
							clearable
						></el-input>
					</el-form-item>
					<div class="btn">
						<el-form-item>
							<el-button type="primary" @click="onSubmit('form')"
								>确认</el-button
							>
							<el-button>取消</el-button>
						</el-form-item>
						<el-form-item>
							<el-button @click="toregister()">注册</el-button>
						</el-form-item>
					</div>
				</el-form>
			</div>
		</div>
	</div>
</template>

<script>
import { login, getUserProfile } from "@/api/index.js";
import { ElLoading } from "element-plus";
export default {
	data() {
		return {
			form: {
				userEmail: "",
				userPassword: "",
			},
			rules: {
				userEmail: [
					{ required: true, message: "请输入邮箱", trigger: "blur" },
					{
						min: 6,
						max: 40,
						message: "长度在 6 到 40 个字符",
						trigger: "blur",
					},
					{
						required: true,
						type: "email",
						message: "请输入正确的邮箱格式",
						trigger: "blur",
					},
				],
				userPassword: [
					{ required: true, message: "请输入密码", trigger: "blur" },
					{
						min: 6,
						message: "密码长度至少为6",
						trigger: "blur",
					},
				],
			},
		};
	},
	methods: {
		onSubmit(formName) {
			this.$refs[formName].validate((valid) => {
				if (valid) {
					const loading = ElLoading.service({
						lock: true,
						text: "拼命加载中...",
						background: "rgba(255,255,255,0.5)",
					});
					login(this.form.userEmail, this.form.userPassword)
						.then(async (res) => {
							this.$store.commit("SetJwt", res.data);
							let info = await getUserProfile();
							console.log("info: ", info);
							this.$store.commit("SetUserProfile", info.data);
							loading.close()
							alert("登录成功!");
							this.$router.push("/");
						})
						.catch((err) => {
							loading.close()
							console.log(err.response.data);
							alert("登录失败，请检查您的账号及密码信息......");
						});
				} else {
					alert("提交失败!");
					return false;
				}
			});
		},
		toregister() {
			this.$router.push("/register");
		},
		// 邮箱自动填充后缀名
		querySearchEmail(queryString, callback) {
			const emailList = [
				{ value: "@qq.com" },
				{ value: "@163.com" },
				{ value: "@gmail.com" },
				{ value: "@foxmail.com" },
				{ value: "@sina.com" },
				{ value: "@126.com" },
				{ value: "@sohu.com" },
				{ value: "@yahoo.com.cn" },
				{ value: "@msn.com" },
				{ value: "@hotmail.com" },
				{ value: "@ask.com" },
			];
			let results = [];
			let queryList = [];
			emailList.map((item) => {
				queryList.push({ value: queryString.split("@")[0] + item.value });
			});
			results = queryString
				? queryList.filter(this.createFilter(queryString))
				: queryList;
			callback(results);
		},

		// 邮箱填写过滤
		createFilter(queryString) {
			return (item) => {
				return (
					item.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
				);
			};
		},
	},
};
</script>
<style lang="less" scoped>
.welcome {
	font-family: "Trebuchet MS", "Lucida Sans Unicode", "Lucida Grande",
		"Lucida Sans", Arial, sans-serif;
	font-style: italic;
	font-size: 0.8rem;
	margin-top: 0.5rem;
	text-align: center;
	font-weight: 900;
	color: rgb(20, 19, 68);
}
.container {
	margin-top: 0.4rem;
	display: flex;
	justify-content: space-around;
	align-items: center;
	img {
		height: 5rem;
		width: 5rem;
	}
	.login-part {
		background-color: #fff;
		padding: 0.5rem;
		width: 6.5rem;
		border-radius: 0.2rem;
		box-shadow: 0.1rem 0.1rem 0.1rem #999;
		.some-tips {
			font-size: 0.2rem;
			color: #ccc;
		}
		.el-form {
			/deep/ .el-autocomplete {
				width: 5.5rem;
				outline-style: none;
			}
			.btn {
				display: flex;
				justify-content: space-between;
				align-items: center;
			}
			.el-form-item {
				/deep/ .el-input {
					outline: none;
				}
			}
		}
	}
}
</style>
