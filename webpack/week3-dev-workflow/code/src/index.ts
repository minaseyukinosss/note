import "./styles.css";
import { getMessage } from "./message";

function render() {
  const app = document.getElementById("app");
  if (!app) return;

  app.innerHTML = "";
  const panel = document.createElement("section");
  panel.className = "panel";
  panel.innerHTML = `
    <h2>${process.env.APP_TITLE}</h2>
    <p>${getMessage()}</p>
    <p>当前时间：${new Date().toLocaleTimeString()}</p>
  `;
  app.appendChild(panel);
}

render();

if (module && module.hot) {
  module.hot.accept("./message", () => {
    render();
    console.log("message module updated via HMR");
  });
}
