const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { ModuleFederationPlugin } = require("webpack").container;

module.exports = {
  mode: "development",
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    publicPath: "http://localhost:3000/",
    clean: true
  },
  devServer: {
    port: 3000
  },
  plugins: [
    new ModuleFederationPlugin({
      name: "hostApp",
      remotes: {
        remoteApp: "remoteApp@http://localhost:3001/remoteEntry.js"
      }
    }),
    new HtmlWebpackPlugin({
      templateContent: "<!doctype html><html><body><div id='app'></div></body></html>"
    })
  ]
};
