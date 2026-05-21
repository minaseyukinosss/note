const { merge } = require("webpack-merge");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const common = require("./webpack.common");

module.exports = (env = {}) =>
  merge(common(env), {
    mode: "production",
    devtool: "source-map",
    module: {
      rules: [
        {
          test: /\.css$/i,
          use: [MiniCssExtractPlugin.loader, "css-loader"]
        }
      ]
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: "[name].[contenthash:8].css"
      })
    ],
    optimization: {
      minimizer: [new TerserPlugin(), new CssMinimizerPlugin()]
    }
  });
