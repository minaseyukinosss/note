const { merge } = require("webpack-merge");
const common = require("./webpack.common");

module.exports = (env = {}) =>
  merge(common(env), {
    mode: "development",
    devtool: "eval-cheap-module-source-map",
    module: {
      rules: [
        {
          test: /\.css$/i,
          use: ["style-loader", "css-loader"]
        }
      ]
    },
    devServer: {
      port: 9003,
      hot: true,
      open: true
    }
  });
