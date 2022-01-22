import axios from './request.js'
import store from '@/store'

// let baseUrl = 'http://39.106.132.154:8000/api/v1'
const ip = 'http://39.106.132.154:8000'
// const ip = 'http://localhost:8000'
const baseUrl = `${ip}/api/v1`


export function getIP(){
  return ip
}

//获取搜索结果
export function getSearchResult(q, p) {
  return axios.get(`${baseUrl}/search?q=${q}&p=${p}`)
}
//根据输入的部分文本获取搜索建议
export function getSearchSuggest(someText) {
  return axios.get(`${baseUrl}/search/suggest?input=${someText}`)
}
//登录
export function login(email, password) {
  return axios.post(`${baseUrl}/jwt/create`, {
    "email": email,
    "password": password
  })
}
//注册
export function register(username, email, password, re_password) {
  return axios.post(`${baseUrl}/users/`, {
    "username": username,
    "email": email,
    "password": password,
    "re_password": re_password
  })
}
//获取用户资料
export function getUserProfile() {
  return axios.get(`${baseUrl}/users/me`)
}
//验证token是否失效
export function authorization(token) {
  return axios.post(`${baseUrl}/jwt/verify`,{
    "token": token,
  })
}
//通过刷新token进行刷新
export function refreshToken(refresh){
  return axios.post(`${baseUrl}/jwt/refresh`,{
    "refresh": refresh,
  })
}
//激活账号
export function activate(uid, token){
  return axios.post(`${baseUrl}/users/activation/`,{
    "uid": uid,
    "token": token
  })
}

