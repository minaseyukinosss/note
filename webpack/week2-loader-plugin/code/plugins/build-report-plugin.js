const path = require("path");

class BuildReportPlugin {
  apply(compiler) {
    // 新增：编译开始时触发
    compiler.hooks.compile.tap("BuildReportPlugin", (compilation) => {
      console.log("[hook] compile: start");
    });

    compiler.hooks.emit.tap("BuildReportPlugin", (compilation) => {
      const assetCount = Object.keys(compilation.assets || {}).length;
      console.log(`[hook] emit: assetCount=${assetCount}`);
    });

    compiler.hooks.emit.tapAsync("BuildReportPlugin", (compilation, callback) => {
      console.log("[hook] emitAsync: start");
      setTimeout(() => {
        console.log("[hook] emitAsync: done");
        callback();
      }, 300);
    });
    
    compiler.hooks.emit.tapPromise("BuildReportPlugin", async (compilation) => {
      console.log("[hook] emitPromise: start");
      await new Promise((resolve) =>
        setTimeout(() => {
          console.log("[hook] emitPromise: done");
          resolve();
        }, 300)
      );
    });
    
    compiler.hooks.done.tap("BuildReportPlugin", (stats) => {
      const info = stats.toJson({
        all: false,
        assets: true,
        errors: true,
        warnings: true,
        timings: true
      });

      const hasErrors = stats.hasErrors();
      const outputPath = compiler.options.output.path || process.cwd();
      const lines = [];
      lines.push("=== Build Report ===");
      lines.push(`[hook] done: success=${!hasErrors}`);
      lines.push(`mode: ${compiler.options.mode}`);
      lines.push(`time: ${info.time}ms`);
      lines.push(`output: ${path.relative(process.cwd(), outputPath)}`);
      lines.push("");
      lines.push("assets:");

      for (const asset of info.assets || []) {
        lines.push(`- ${asset.name} (${asset.size} bytes)`);
      }

      if (info.errors && info.errors.length > 0) {
        lines.push("");
        lines.push(`errors: ${info.errors.length}`);
      }

      if (info.warnings && info.warnings.length > 0) {
        lines.push(`warnings: ${info.warnings.length}`);
      }

      // 直接输出到终端，便于观察 plugin 在生命周期中的执行结果。
      console.log(lines.join("\n"));
    });
  }
}

module.exports = BuildReportPlugin;
