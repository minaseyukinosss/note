const path = require("path");
const BuildReportPlugin = require("./plugins/build-report-plugin");

module.exports = (_, argv) => {
  const mode = argv.mode || "development";

  return {
    mode,
    entry: "./src/index.ts",
    output: {
      path: path.resolve(__dirname, "dist"),
      filename: "bundle.js",
      clean: true
    },
    resolve: {
      extensions: [".ts", ".tsx", ".js"]
    },
    module: {
      rules: [
        {
          test: /\.tsx?$/,
          exclude: /node_modules/,
          use: [
            {
              loader: path.resolve(__dirname, "loaders/banner-loader.js"),
              options: {
                banner: "Week2 Day1 Banner"
              }
            },
            "ts-loader"
          ]
        }
      ]
    },
    plugins: [new BuildReportPlugin()]
  };
};
