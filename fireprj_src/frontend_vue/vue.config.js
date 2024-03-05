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
        target: 'http://localhost:8081',
        ws: true,
        changeOrigin: true,
      }
    }
  }
}