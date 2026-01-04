function Exit()
{
    document.cookie = "hashkey=; path=/; max-age=0";
    showToast("Вы вышли из аккаунта","info");
    setTimeout(() => {
        window.location.href = "/";
    }, 1000);
}
function Back()
{
    window.location.href = "/";
}
function getCookie(name) 
{
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}
function setCookie(value) 
{
  document.cookie = `hashkey=${value}; path=/`;
}
function hasHashkeyCookie() 
{ 
    return document.cookie.split(';').map(c => c.trim()).some(c => c.startsWith('hashkey=')); 
}
function renderButtons(buttonConfigs) 
{
    buttonConfigs.forEach(cfg => {
        const container = document.getElementById(cfg.containerId);
        if (!container) return;

        container.innerHTML = "";

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = cfg.className || "";
        btn.textContent = cfg.text || "Кнопка";
        if (typeof cfg.onClick === "function")
        {
            btn.onclick = cfg.onClick;
        }
        container.appendChild(btn);
    });
}
function showToast(message, type = "error") 
{
    let container = document.querySelector(".toast-container");
    if (!container) {
        container = document.createElement("div");
        container.className = "toast-container";
        document.body.appendChild(container);
    }
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;

    const closeBtn = document.createElement("button");
    closeBtn.className = "close-btn";
    closeBtn.innerHTML = "&times;";
    closeBtn.onclick = () => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
    };
    toast.appendChild(closeBtn);

    container.appendChild(toast);
    setTimeout(() => toast.classList.add("show"), 0);
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
