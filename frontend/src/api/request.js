import axios from 'axios'
import store from '@/store'

axios.defaults.timeout = 10000;
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8;multipart/form-data';

// 添加请求拦截器，在请求头中加token
axios.interceptors.request.use(
  config => {
    console.log("store.state.Jwt: ", store.state.Jwt)
    if (store.state.Jwt != '') {
      console.log("将token添加进入请求头之中...")
      config.headers.Authorization = 'JWT ' + store.state.Jwt.access;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  });

export default axios;