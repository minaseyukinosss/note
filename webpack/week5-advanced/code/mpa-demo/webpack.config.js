const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  mode: "production",
  entry: {
    home: "./src/home.js",
    admin: "./src/admin.js"
  },
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "js/[name].[contenthash:8].js",
    clean: true
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./public/home.html",
      filename: "home.html",
      chunks: ["home"]
    }),
    new HtmlWebpackPlugin({
      template: "./public/admin.html",
      filename: "admin.html",
      chunks: ["admin"]
    })
  ]
};
