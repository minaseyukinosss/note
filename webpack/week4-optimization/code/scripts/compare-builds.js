const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function runWithTime(command) {
  const start = Date.now();
  execSync(command, { stdio: "inherit" });
  return Date.now() - start;
}

function getDirSize(targetDir) {
  if (!fs.existsSync(targetDir)) return 0;

  const list = fs.readdirSync(targetDir);
  let total = 0;

  for (const name of list) {
    const absolute = path.join(targetDir, name);
    const stat = fs.statSync(absolute);
    if (stat.isDirectory()) {
      total += getDirSize(absolute);
    } else {
      total += stat.size;
    }
  }

  return total;
}

function formatKB(bytes) {
  return `${(bytes / 1024).toFixed(2)} KB`;
}

function main() {
  const root = path.resolve(__dirname, "..");
  const baseTime = runWithTime("npm run build:base");
  const optTime = runWithTime("npm run build:opt");

  const baseSize = getDirSize(path.join(root, "dist-base"));
  const optSize = getDirSize(path.join(root, "dist-optimized"));

  const report = `# Week4 构建对比报告

## 结果
- 基线构建时长: ${baseTime} ms
- 优化构建时长: ${optTime} ms
- 基线产物体积: ${formatKB(baseSize)}
- 优化产物体积: ${formatKB(optSize)}

## 结论
- 优化构建启用了 splitChunks / runtimeChunk / contenthash / filesystem cache。
- 在实际业务中应结合首屏请求数、缓存命中率与二次构建时长综合评估。
`;

  fs.writeFileSync(path.join(root, "build-comparison-report.md"), report, "utf8");
  console.log("\n对比报告已生成: build-comparison-report.md");
}

main();
