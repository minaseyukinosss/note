const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  mode: "production",
  entry: {
    home: "./src/home.ts",
    admin: "./src/admin.ts"
  },
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "js/[name].[contenthash:8].js",
    clean: true
  },
  resolve: {
    extensions: [".ts", ".tsx", ".js"]
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/
      }
    ]
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
