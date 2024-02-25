import axios from 'axios'

let sessionToken = sessionStorage.getItem('sessionToken')
let commonHeader = {}
if (sessionToken) {
  commonHeader.token = sessionToken
}

const http = axios.create({
  baseURL: `/api/${process.env.VUE_APP_API_MONITOR_VER}`,
  timeout: 50 * 1000,
  headers: {
    common: commonHeader
  }
})

http.interceptors.request.use(
  (config) => {
    if (!config.params) config.params = {}
    // config.params._cache = Date.now()
    return config
  },
  (error) => {
    return Promise.reject(error);
  }
)

const userApi = axios.create({
  baseURL: `/api/${process.env.VUE_APP_API_MONITOR_VER}`,
  timeout: 50 * 1000,
  headers: {
    common: commonHeader
  }
})

userApi.interceptors.request.use(
  (config) => {
    if (!config.params) config.params = {}
    config.params._cache = Date.now()
    return config
  },
  (error) => {
    return Promise.reject(error);
  }
)

const aiApi = axios.create({
  baseURL: `/api/ai/${process.env.VUE_APP_API_MONITOR_VER}`,
  timeout: 50 * 1000,
  headers: {
    common: commonHeader
  }
})

aiApi.interceptors.request.use(
  (config) => {
    if (!config.params) config.params = {}
    config.params._cache = Date.now()
    return config
  },
  (error) => {
    return Promise.reject(error);
  }
)

export default {
  install(Vue) {
    Vue.prototype.$http = http
    Vue.prototype.$http_ai = aiApi
  }
}

export { http, userApi, aiApi }
