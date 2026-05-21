async function mount() {
  const sayHi = (await import("remoteApp/SayHi")).default;
  const root = document.getElementById("app");
  root.innerHTML = `<h2>${sayHi("Host")}</h2>`;
}

mount();
