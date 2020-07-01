module.exports = {
  "configureWebpack": {
    "devServer": {
      "watchOptions": {
        "ignored": [
          "node_modules"
        ],
        "aggregateTimeout": 300,
        "poll": 1500
      },
      "public": "0.0.0.0",
      "proxy": {
        "/api": {
          "target": "http://localhost:8080",
        },
        "/admin": {
          "target": "http://localhost:8080",
        }
      },
    },
  },
  "pages": {
    "index": {
      "entry": 'src/main.js',
      "title": 'Open Acidification Control Center'
    }
  },
  "transpileDependencies": [
    "vuetify"
  ],
}