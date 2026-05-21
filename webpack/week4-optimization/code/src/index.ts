import "./styles.css";
import _ from "lodash";

const appEl = document.getElementById("app");
if (!appEl) {
  throw new Error("#app not found");
}
const app: HTMLElement = appEl;

const values = _.range(1, 6000);
const shuffled = _.shuffle(values).slice(0, 10);

async function bootstrap(): Promise<void> {
  const { createReportText } = await import("./report");
  const panel = document.createElement("div");
  panel.className = "card";
  panel.innerHTML = `
    <h2>Week4 Optimization Demo</h2>
    <p>动态导入 + 分包 + 缓存策略演示</p>
    <pre>${createReportText(values.length, shuffled)}</pre>
  `;
  app.appendChild(panel);
}

bootstrap();
