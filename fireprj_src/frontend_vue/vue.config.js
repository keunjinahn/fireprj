module.exports = {
  assetsDir: 'static',
  publicPath: '/',
  transpileDependencies: [
    "vuetify"
  ],
  devServer: {
    host: 'localhost',
    proxy: {
      '^/api': {
        target: (process.env.LOCAL_SERVER === 'Y') ? 'http://localhost:8081' : 'http://118.128.43.7:50443',
        ws: true,
        changeOrigin: true,
      }
    }
  }
}