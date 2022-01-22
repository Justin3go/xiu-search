<template>
	<div class="register">
		<div class="welcome">欢迎加入XiuSearch这个大家庭~</div>
		<div class="container">
			<div class="pic">
				<img src="@/assets/register.svg" alt="" />
			</div>
			<div class="register-part">
				<div class="some-tips">在这里注册您的账号</div>
				<el-form
					ref="form"
					:model="form"
					:label-position="'left'"
					label-width="1rem"
					:rules="rules"
				>
					<el-form-item label="用户名:" prop="userName">
						<el-input
							v-model="form.userName"
							placeholder="请输入您的用户名"
							clearable
						></el-input>
					</el-form-item>
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
					<el-form-item label="密码认证:" prop="userPassword2">
						<el-input
							v-model="form.userPassword2"
							placeholder="请再次输入您的密码"
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
							<el-button @click="gologin">登录</el-button>
						</el-form-item>
					</div>
				</el-form>
			</div>
		</div>
	</div>
</template>

<script>
import { register } from "@/api/index.js";
import { ElLoading } from "element-plus";
export default {
	data() {
		var validatePass2 = (rule, value, callback) => {
			if (value === "") {
				callback(new Error("请再次输入密码"));
			} else if (value !== this.form.userPassword) {
				callback(new Error("两次输入密码不一致!"));
			} else {
				callback();
			}
		};
		return {
			form: {
				userName: "",
				userEmail: "",
				userPassword: "",
				userPassword2: "",
			},

			rules: {
				userName: [
					{ required: true, message: "请输入用户名", trigger: "blur" },
				],
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
						message: "长度至少为6",
						trigger: "blur",
					},
				],
				// 这个两次密码应该一致
				userPassword2: [
					{ required: true, validator: validatePass2, trigger: "blur" },
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
					register(
						this.form.userName,
						this.form.userEmail,
						this.form.userPassword,
						this.form.userPassword2
					)
						.then((data) => {
							console.log(data);
							loading.close()
							alert("注册成功!");
							this.$router.push("/login");
						})
						.catch((err) => {
							loading.close()
							//TODO 这里简单的打印出来保证逻辑，后续在再优化显示
							let info = '请求错误'
							try{
								info = err.response.data
							}catch{
								info = '请求错误'
							}
							alert(JSON.stringify(info));
						});
				} else {
					alert("提交失败!");
					return false;
				}
			});
		},
		gologin() {
			this.$router.push("/login");
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
// #251AFF
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
	.register-part {
		background-color: #fff;
		padding: 0.5rem;
		width: 6.5rem;
		border-radius: 0.2rem;
		box-shadow: 0.1rem 0.1rem 0.1rem #999;
		.some-tips {
			font-size: 0.2rem;
			color: #ccc;
			margin-bottom: 0.15rem;
		}
		.el-form {
			/deep/ .el-autocomplete {
				width: 4.5rem;
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
