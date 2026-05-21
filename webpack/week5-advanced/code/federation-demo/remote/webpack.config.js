const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { ModuleFederationPlugin } = require("webpack").container;

module.exports = {
  mode: "development",
  entry: "./src/index.ts",
  output: {
    path: path.resolve(__dirname, "dist"),
    publicPath: "http://localhost:3001/",
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
  devServer: {
    port: 3001
  },
  plugins: [
    new ModuleFederationPlugin({
      name: "remoteApp",
      filename: "remoteEntry.js",
      exposes: {
        "./SayHi": "./src/say-hi.ts"
      }
    }),
    new HtmlWebpackPlugin({
      templateContent: "<!doctype html><html><body><div>remote app</div></body></html>"
    })
  ]
};
