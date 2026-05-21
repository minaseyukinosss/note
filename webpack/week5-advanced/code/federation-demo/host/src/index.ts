async function mount(): Promise<void> {
  const sayHi = (await import("remoteApp/SayHi")).default;
  const root = document.getElementById("app");
  if (!root) {
    throw new Error("#app not found");
  }
  root.innerHTML = `<h2>${sayHi("Host")}</h2>`;
}

mount();
