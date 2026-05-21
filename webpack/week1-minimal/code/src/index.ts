import "./styles.css";
import { createMessage } from "./esm-util";
import logoUrl from "./assets/logo.svg";
import getExtraText from "./extra";

const formatTitle = require("./commonjs-util.cjs") as (title: string) => string;

const root = document.createElement("div");
root.className = "card";

const title = document.createElement("h2");
title.className = "title";
title.textContent = formatTitle("week1 minimal webpack");

const content = document.createElement("p");
content.textContent = createMessage("Frontend Developer");

const image = document.createElement("img");
image.className = "preview-image";
image.src = logoUrl;
image.alt = "Week1 Logo";

root.appendChild(title);
root.appendChild(content);
root.appendChild(image);
document.body.appendChild(root);

console.log(getExtraText());
