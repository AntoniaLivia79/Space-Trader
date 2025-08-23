// Space Trader Game - View (UI and DOM manipulation)

function log(message) {
    const logEl = document.getElementById('gameLog');
    logEl.innerHTML += message + '<br>';
    logEl.scrollTop = logEl.scrollHeight;
}

function updateStatus() {
    const p = game.player;
    document.getElementById('status').innerHTML =
        `Captain: ${p.captain_name} | Ship: ${p.ship_name} | Age: ${p.age} | Credits: ${p.credits}`;
}

function setScreen(content) {
    document.getElementById('gameScreen').innerHTML = content;
}

function setMenu(options) {
    const menuEl = document.getElementById('menuOptions');
    menuEl.innerHTML = '';
    options.forEach((option, index) => {
        const button = document.createElement('button');
        button.innerHTML = `${option.text}`;
        button.onclick = option.action;
        menuEl.appendChild(button);
    });
}
