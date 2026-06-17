// ─── Pixel Art: Windje de Meeuw ─────────────────────────────────────────────
// 28 × 36 sprite, 8px per pixel
// Palette
const C = {
  0: null,
  1: '#F4F4F4',   // white body
  2: '#0A0F1E',   // dark outline
  3: '#2563EB',   // blue wing
  4: '#FBBF24',   // gold compass
  5: '#F97316',   // orange beak/feet
  6: '#060B14',   // eye dark
  7: '#FFFFFF',   // eye highlight
  8: '#1D4ED8',   // navy scarf stripe
  9: '#BAE6FD',   // light blue scarf stripe
  10: '#92400E',  // compass inner detail
  11: '#60A5FA',  // wing mid-blue
};

// 28-wide × 36-tall
const SPRITE = [
  [0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,0,0,0,0,0,0],
  [0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0],
  [0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0],
  [0,0,0,0,2,1,1,1,6,6,1,1,1,1,1,1,1,6,6,1,1,1,1,2,0,0,0,0],
  [0,0,0,0,2,1,1,1,6,7,1,1,1,1,1,1,1,6,7,1,1,1,1,2,0,0,0,0],
  [0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0],
  [0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,5,5,5,2,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,2,1,1,1,1,1,1,1,1,1,5,5,5,5,5,2,0,0,0,0,0,0,0,0],
  [0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,5,5,5,2,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,2,2,1,1,1,1,1,1,1,1,1,2,2,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,2,8,9,8,9,8,9,8,9,8,9,2,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,2,2,1,8,9,8,9,8,9,8,9,8,9,1,2,2,0,0,0,0,0,0,0],
  [0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0],
  [0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0],
  [0,0,2,3,3,1,1,1,1,1,2,4,4,4,4,4,4,2,1,1,1,3,3,2,0,0,0,0],
  [0,2,3,3,3,1,1,1,1,2,4,4,4,4,4,4,4,4,2,1,1,3,3,3,2,0,0,0],
  [0,2,3,3,3,1,1,1,1,2,4,10,4,4,4,10,4,4,2,1,1,3,3,3,2,0,0,0],
  [0,2,3,3,3,1,1,1,1,2,4,4,4,10,4,4,4,4,2,1,1,3,3,3,2,0,0,0],
  [0,2,3,3,3,1,1,1,1,2,4,10,4,4,4,10,4,4,2,1,1,3,3,3,2,0,0,0],
  [0,0,2,3,3,1,1,1,1,1,2,4,4,4,4,4,4,2,1,1,1,3,3,2,0,0,0,0],
  [0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0],
  [0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0],
  [0,0,0,0,0,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,2,2,1,1,1,1,1,1,1,1,2,2,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,5,5,5,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,5,5,5,5,0,0,5,5,5,5,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,5,5,5,5,5,0,0,5,5,5,5,5,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,5,5,5,5,0,0,0,0,5,5,5,5,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
];

function drawWindje(canvas, scale = 8) {
  const ctx = canvas.getContext('2d');
  canvas.width  = SPRITE[0].length * scale;
  canvas.height = SPRITE.length    * scale;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.imageSmoothingEnabled = false;

  SPRITE.forEach((row, y) => {
    row.forEach((px, x) => {
      const color = C[px];
      if (!color) return;
      ctx.fillStyle = color;
      ctx.fillRect(x * scale, y * scale, scale, scale);
    });
  });
}

// ─── SPA Router ─────────────────────────────────────────────────────────────
const pages = {
  home:       renderHome,
  shop:       renderShop,
  games:      renderGames,
  stories:    renderStories,
  characters: renderCharacters,
};

function navigate(page) {
  document.querySelectorAll('.nav-link').forEach(l =>
    l.classList.toggle('active', l.dataset.page === page)
  );
  const main = document.getElementById('main');
  main.innerHTML = '';
  main.classList.remove('fade-in');
  void main.offsetWidth;
  main.classList.add('fade-in');
  (pages[page] || renderHome)(main);
}

// ─── HOME ────────────────────────────────────────────────────────────────────
function renderHome(el) {
  el.innerHTML = `
    <section class="hero">
      <div class="hero-bg">
        <div class="wave wave1"></div>
        <div class="wave wave2"></div>
        <div class="wave wave3"></div>
      </div>
      <div class="hero-content">
        <div class="hero-sprite-wrap">
          <canvas id="heroCanvas" class="pixel-hero"></canvas>
        </div>
        <div class="hero-text">
          <h1 class="hero-title">Windje<br><span class="accent">de Meeuw</span></h1>
          <p class="hero-sub">Een avontuurlijke zeemeeuw met een kompas en een droom.<br>
            Verken de zee, speel spelletjes en ontdek verhalen!</p>
          <div class="hero-btns">
            <button class="btn btn-primary" onclick="navigate('stories')">Lees verhalen</button>
            <button class="btn btn-outline" onclick="navigate('games')">Speel spelletjes</button>
          </div>
        </div>
      </div>
    </section>

    <section class="features">
      <h2 class="section-title">Ontdek de wereld van Windje</h2>
      <div class="feature-grid">
        <div class="feature-card" onclick="navigate('shop')">
          <div class="feature-icon">🛒</div>
          <h3>Shop</h3>
          <p>Windje-sleutelhangers, stickers, boeken en meer!</p>
        </div>
        <div class="feature-card" onclick="navigate('games')">
          <div class="feature-icon">🎮</div>
          <h3>Spelletjes</h3>
          <p>Speel mee met Windje in leuke zeeavonturen.</p>
        </div>
        <div class="feature-card" onclick="navigate('stories')">
          <div class="feature-icon">📖</div>
          <h3>Verhalen</h3>
          <p>Lees de spannende avonturen van Windje op zee.</p>
        </div>
        <div class="feature-card" onclick="navigate('characters')">
          <div class="feature-icon">🐦</div>
          <h3>Personages</h3>
          <p>Maak kennis met alle vrienden van Windje.</p>
        </div>
      </div>
    </section>

    <section class="about-strip">
      <div class="about-inner">
        <p>✦ Windje is de mascotte van <strong>Brug-Yachtcharter</strong> &nbsp;·&nbsp; Avontuur op het water ✦</p>
      </div>
    </section>
  `;

  const canvas = document.getElementById('heroCanvas');
  drawWindje(canvas, 9);
}

// ─── SHOP ────────────────────────────────────────────────────────────────────
const SHOP_ITEMS = [
  { name: 'Windje Sleutelhanger', price: '€4,99', emoji: '🔑',
    desc: 'De originele Windje foam sleutelhanger. Altijd bij je!' },
  { name: 'Windje Stickerset', price: '€2,99', emoji: '⭐',
    desc: '12 kleurrijke stickers van Windje en zijn vrienden.' },
  { name: 'Windje T-shirt', price: '€14,99', emoji: '👕',
    desc: 'Comfortabel shirt met Windje pixel art print.' },
  { name: 'Avonturenboek', price: '€9,99', emoji: '📚',
    desc: 'Het officiële Windje verhalenboek met 6 avonturen.' },
  { name: 'Windje Knuffel', price: '€19,99', emoji: '🧸',
    desc: 'Zachte pluchen zeemeeuw, 25 cm groot, met kompas.' },
  { name: 'Kleurplatenboek', price: '€3,99', emoji: '🎨',
    desc: '20 kleurplaten van Windje voor jonge kunstenaars.' },
  { name: 'Kompas Puzzel', price: '€7,99', emoji: '🧩',
    desc: '100-stukjes puzzel met Windje op de golven.' },
  { name: 'Windje Pet', price: '€11,99', emoji: '🧢',
    desc: 'Stoere pet met geborduurde Windje op de klep.' },
];

function renderShop(el) {
  el.innerHTML = `
    <div class="page-header ocean-header">
      <h1>Shop</h1>
      <p>Haal een stukje Windjes avontuur naar huis!</p>
    </div>
    <div class="shop-grid">
      ${SHOP_ITEMS.map(item => `
        <div class="shop-card">
          <div class="shop-emoji">${item.emoji}</div>
          <h3>${item.name}</h3>
          <p>${item.desc}</p>
          <div class="shop-footer">
            <span class="price">${item.price}</span>
            <button class="btn btn-primary btn-sm" onclick="addToCart('${item.name}')">Koop</button>
          </div>
        </div>
      `).join('')}
    </div>
    <div id="cart-msg" class="cart-toast" aria-live="polite"></div>
  `;
}

function addToCart(name) {
  const msg = document.getElementById('cart-msg');
  msg.textContent = `✓ "${name}" toegevoegd aan winkelwagen!`;
  msg.classList.add('show');
  setTimeout(() => msg.classList.remove('show'), 2600);
}

// ─── GAMES ───────────────────────────────────────────────────────────────────
function renderGames(el) {
  el.innerHTML = `
    <div class="page-header sky-header">
      <h1>Spelletjes</h1>
      <p>Speel mee met Windje in leuke zeeavonturen!</p>
    </div>

    <div class="games-grid">

      <div class="game-card featured">
        <div class="game-badge">Nu spelen!</div>
        <h2>Kompas Geheugenspel</h2>
        <p>Onthoud de windrichtingen die Windje aanwijst en herhaal ze in de juiste volgorde!</p>
        <div id="compass-game" class="compass-game-area">
          <div class="compass-btns">
            <button class="cbtn" id="cN" data-dir="N">N</button>
            <div class="cbtn-row">
              <button class="cbtn" id="cW" data-dir="W">W</button>
              <div class="compass-center">🧭</div>
              <button class="cbtn" id="cE" data-dir="E">O</button>
            </div>
            <button class="cbtn" id="cS" data-dir="S">Z</button>
          </div>
          <div class="game-status">
            <span id="game-status-text">Druk op Start om te beginnen!</span>
          </div>
          <div class="game-score">Score: <strong id="score">0</strong> &nbsp;|&nbsp; Record: <strong id="highscore">0</strong></div>
          <button class="btn btn-primary" id="start-btn" onclick="startCompassGame()">Start</button>
        </div>
      </div>

      <div class="game-card">
        <div class="game-badge coming">Binnenkort</div>
        <h2>Vissen met Windje</h2>
        <p>Gooi je hengel uit en vang zoveel mogelijk vis voordat de storm opkomt. Maar pas op voor de zeeschildpad!</p>
        <div class="game-preview">🎣 🐟 🐠 🐡 🦀</div>
      </div>

      <div class="game-card">
        <div class="game-badge coming">Binnenkort</div>
        <h2>Storm Navigator</h2>
        <p>Stuur Windje door de storm! Wijk uit voor bliksem en golven terwijl je de vuurtoren probeert te bereiken.</p>
        <div class="game-preview">⛵ ⚡ 🌊 🏠</div>
      </div>

      <div class="game-card">
        <div class="game-badge coming">Binnenkort</div>
        <h2>Windje's Woordzoeker</h2>
        <p>Zoek zeewoorden in het raster. Hoe meer woorden je vindt, hoe verder je met Windje kunt varen!</p>
        <div class="game-preview">🔤 🌊 🐚 ⚓</div>
      </div>

    </div>
  `;
  initCompassGame();
}

// ─── Simple Compass Memory Game ──────────────────────────────────────────────
let compassSeq = [], playerSeq = [], gameActive = false, hs = 0;

function initCompassGame() {
  ['N','W','E','S'].forEach(d => {
    const btn = document.getElementById('c' + d);
    if (btn) btn.addEventListener('click', () => playerHit(d));
  });
}

function startCompassGame() {
  compassSeq = []; playerSeq = []; gameActive = false;
  document.getElementById('score').textContent = '0';
  document.getElementById('start-btn').disabled = true;
  nextRound();
}

function nextRound() {
  playerSeq = [];
  const dirs = ['N','W','E','S'];
  compassSeq.push(dirs[Math.floor(Math.random() * 4)]);
  document.getElementById('game-status-text').textContent = 'Kijk goed…';
  playSequence(() => {
    document.getElementById('game-status-text').textContent = 'Jouw beurt! Herhaal de volgorde.';
    gameActive = true;
  });
}

function playSequence(cb) {
  let i = 0;
  function step() {
    if (i >= compassSeq.length) { setTimeout(cb, 400); return; }
    const d = compassSeq[i++];
    flashBtn(d, () => setTimeout(step, 300));
  }
  setTimeout(step, 500);
}

function flashBtn(d, cb) {
  const btn = document.getElementById('c' + d);
  if (!btn) return;
  btn.classList.add('flash');
  setTimeout(() => { btn.classList.remove('flash'); if (cb) cb(); }, 600);
}

function playerHit(d) {
  if (!gameActive) return;
  playerSeq.push(d);
  const idx = playerSeq.length - 1;
  if (playerSeq[idx] !== compassSeq[idx]) {
    gameOver(); return;
  }
  if (playerSeq.length === compassSeq.length) {
    gameActive = false;
    const s = compassSeq.length;
    document.getElementById('score').textContent = s;
    if (s > hs) { hs = s; document.getElementById('highscore').textContent = hs; }
    document.getElementById('game-status-text').textContent = '🎉 Goed gedaan! Volgende ronde…';
    setTimeout(nextRound, 1000);
  }
}

function gameOver() {
  gameActive = false;
  document.getElementById('game-status-text').textContent = '💥 Fout! Probeer opnieuw.';
  document.getElementById('start-btn').disabled = false;
  document.getElementById('start-btn').textContent = 'Opnieuw';
}

// ─── STORIES ─────────────────────────────────────────────────────────────────
const STORIES = [
  {
    title: "Windje's Eerste Vlucht",
    emoji: '🌅',
    tag: 'Avontuur',
    preview: "Op een stralende ochtend spreidde Windje voor het eerst zijn vleugels volledig uit. De wind rook naar zout en vrijheid…",
    full: `Op een stralende ochtend spreidde Windje voor het eerst zijn vleugels volledig uit. De wind rook naar zout en vrijheid. Kapitein Bram keek vanaf de kade toe terwijl de kleine meeuw steeds hoger steeg.

"Zo hoog had ik het niet verwacht!" piepte Windje verbaasd. Onder hem lag de hele haven: de boten, de vissersnetten, de vrolijke vlaggen die in de wind wapperden.

Zijn gouden kompas glom in het zonlicht. 'Noord', fluisterde het.

Windje volgde het kompas en vloog naar het puntje van de pier. Daar zat een oude zeehond.

"Welkom in de grote zee, kleine meeuw," grinnekte de zeehond. "Ik ben Siebert. Heb je al een avontuur gekozen?"

Windje dacht even na. Zijn ogen glommen. "Alle avonturen," zei hij vastberaden.

En zo begon het.`,
  },
  {
    title: "Het Verloren Kompas",
    emoji: '🧭',
    tag: 'Mysterie',
    preview: "Windje's gouden kompas was weg! Op het dek van de Blauwe Zeemeeuw lag alleen een veer en een krijtstreep…",
    full: `Windje's gouden kompas was weg! Op het dek van de Blauwe Zeemeeuw lag alleen een veer — een blauwe veer, van hemzelf — en een krijtstreep die naar het water wees.

"Wie steelt er nou een kompas?" mopperde Windje.

Zijn vriendin Marta, de vrolijke zeemeermin, dook naast de boot op. "Ik heb iets gezien," zei ze. "Een grote krab met goudgele scharen. Hij ging die richting op." Ze wees naar de rotsen.

Windje vloog er naatoe. Tussen de zeewieren en mosselen vond hij hem: Kees de Krab, druk bezig het kompas in zijn holletje te proppen.

"Kees! Dat is van mij!" riep Windje.

"Glanzend ding," bromde Kees. "Dacht dat het eten was."

Windje giechelde. Hij gaf Kees in ruil een stuk glinsterend zilverfolie. Iedereen blij.

Het kompas wees weer naar het noorden. Nieuw avontuur: gevonden.`,
  },
  {
    title: "Storm op de Zuiderzee",
    emoji: '⛈️',
    tag: 'Spanning',
    preview: "De wolken stapelden zich op als donkere bergen. Kapitein Bram riep iedereen aan dek. Maar Windje was verdwenen…",
    full: `De wolken stapelden zich op als donkere bergen. Kapitein Bram riep iedereen aan dek. Maar Windje was verdwenen.

De mast zwiepte. De golven werden steeds groter. "Windje!" schreeuwde Marta.

Boven in de mast, half verscholen achter een touwen knoop, zat Windje — ogen wijd open, vleugels stevig gevouwen.

"Ik ben niet bang!" riep hij, al klonk zijn stem een beetje bibberend.

Een bliksemflits verlichte de zee. En in dat licht zag Windje iets: een klein bootje, zonder schipper, dat recht op de rotsen af dreef.

Angst vergeten. Windje schoot de lucht in.

Met zijn sterkste vleugels vloog hij naar het bootje, greep het touw met zijn poten en trok uit alle macht. Centimeter voor centimeter keerde het bootje om.

Toen de storm ophield, klapten Bram, Marta en Siebert.

"Dapper," zei Bram simpel.

Windje straalde. Zijn kompas wees warm naar huis.`,
  },
  {
    title: "Windje en de Zeehond",
    emoji: '🦭',
    tag: 'Vriendschap',
    preview: "Siebert zat alleen op een rots en huilde zachtjes. Zijn vrienden waren vertrokken naar het zuiden, maar hij kon niet mee…",
    full: `Siebert zat alleen op een rots en huilde zachtjes. Zijn vrienden waren vertrokken naar het zuiden, maar hij had zijn enkel bezeerd en kon niet mee.

Windje hoorde hem en landde naast hem op de rots.

"Waarom zo verdrietig?"

"Ze zijn allemaal weg," snufte Siebert. "En ik zit hier vast."

Windje knikte serieus. "Dan blijf ik bij je."

"Maar jij kunt vliegen. Jij kunt overal heen."

"Overal heen is saai zonder een vriend om het mee te delen," zei Windje.

Ze zaten een hele dag samen op de rots. Windje vertelde verhalen over havens en verre kusten. Siebert vertelde over wat er leeft onder het wateroppervlak.

De volgende dag voelde Sieberts enkel beter. En hij was niet meer alleen.

"Vrienden zijn beter dan kompassen," concludeerde Windje die avond.

Zijn kompas piepte protestend. Windje lachte. "Maar kompassen zijn ook heel fijn."`,
  },
  {
    title: "De Schat van Schiermonnikoog",
    emoji: '💎',
    tag: 'Schatzoekers',
    preview: "Een oud vergeeld kaartje, gevonden in een fles. Een X op een eiland. Windje wist wat hem te doen stond…",
    full: `Een oud vergeeld kaartje, gevonden in een fles die ronddreef bij de boei. Een X op een eiland. Windje wist wat hem te doen stond.

"Schiermonnikoog," las Siebert. "Twee dagreizen varen."

De expeditie begon: Windje als gids in de lucht, Siebert zwemmend naast het bootje, Marta duikend als verkenner.

Op het eiland groeven ze bij de eeuwenoude vuurtoren. Drie treden van links, vijf van rechts, onder de steen.

Wat ze vonden was geen goud. Het was een doos vol tekeningen van kinderen — vroegere ontdekkers, net als zij.

Windje las de briefje erbij: "Voor de volgende avonturier. Voeg je tekening toe."

Windje pakte een krijtje en tekende zichzelf: kleine zeemeeuw, groot kompas, brede glimlach.

Hij stopte de doos terug.

"De echte schat," zei hij plechtig, "zijn de avonturen die je deelt."

Marta gooide een handvol schelpen omhoog als confetti. "Nou, Windje de Filosoof!"

Ze lachten de hele vaart naar huis.`,
  },
  {
    title: "Windje's Verjaardag Verrassing",
    emoji: '🎂',
    tag: 'Feest',
    preview: "Het was Windjes verjaardag, maar hij wist het zelf niet. Al zijn vrienden wisten het wel en hadden een plan…",
    full: `Het was Windjes verjaardag, maar hij wist het zelf niet. Al zijn vrienden wisten het wel en hadden een geheim plan.

Siebert hield hem bezig met een verzonnen schat in de baai. Marta versier de het jacht van Kapitein Bram. En Kees de Krab sleepte eigenhandig een schelp naar het dek als cadeau.

Toen Windje terugkwam van de mislukte schatzoeking — er was helemaal geen schat, dat begreep hij nu — stond het hele dek vol vlaggetjes en feestlichten.

"VERRASSING!"

Windje bleef stokstijf staan. Zijn bek viel open.

"Maar… hoe wisten jullie…?"

"Je kompas," zei Marta glunderend. "Elke dag op je verjaardag wijst het naar het zuiden. Dat heeft Bram ons verteld."

Windje keek naar zijn kompas. Het wees inderdaad zuiden. Hij had het nooit zo goed bekeken.

Hij knuffelde iedereen. Kees ook, hoewel dat een beetje prikkelde.

Het was zijn beste verjaardag ooit. En het zeilseizoen was nog maar net begonnen.`,
  },
];

let openStory = null;

function renderStories(el) {
  el.innerHTML = `
    <div class="page-header sand-header">
      <h1>Verhalen</h1>
      <p>Spannende avonturen van Windje op zee — lees ze allemaal!</p>
    </div>
    <div class="stories-grid">
      ${STORIES.map((s, i) => `
        <div class="story-card" onclick="openStoryModal(${i})">
          <div class="story-emoji">${s.emoji}</div>
          <div class="story-tag">${s.tag}</div>
          <h3>${s.title}</h3>
          <p>${s.preview}</p>
          <button class="btn btn-outline btn-sm">Lees verder →</button>
        </div>
      `).join('')}
    </div>
    <div id="story-modal" class="modal hidden" onclick="closeStoryModal(event)">
      <div class="modal-box">
        <button class="modal-close" onclick="closeStoryModal(null, true)">✕</button>
        <div id="modal-body"></div>
      </div>
    </div>
  `;
}

function openStoryModal(i) {
  const s = STORIES[i];
  document.getElementById('modal-body').innerHTML = `
    <div class="modal-emoji">${s.emoji}</div>
    <div class="story-tag">${s.tag}</div>
    <h2>${s.title}</h2>
    <div class="story-text">${s.full.split('\n').map(p => p.trim() ? `<p>${p}</p>` : '').join('')}</div>
  `;
  document.getElementById('story-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeStoryModal(e, force) {
  if (force || !e || e.target.id === 'story-modal') {
    document.getElementById('story-modal').classList.add('hidden');
    document.body.style.overflow = '';
  }
}

// ─── CHARACTERS ──────────────────────────────────────────────────────────────
const CHARS = [
  {
    name: 'Windje de Meeuw',
    role: 'Hoofdpersonage',
    emoji: '🐦',
    color: '#E0F2FE',
    border: '#3B82F6',
    traits: ['Dapper', 'Nieuwsgierig', 'Trouw'],
    bio: 'Windje is een jonge zeemeeuw met een magisch gouden kompas dat altijd de weg wijst. Hij houdt van avontuur, vriendschap en een goede storm. Zijn schattigste eigenschap? Hij gelooft altijd dat alles goed komt — en hij heeft nog nooit ongelijk gehad.',
  },
  {
    name: 'Kapitein Bram',
    role: 'De wijze zeeman',
    emoji: '⚓',
    color: '#FEF3C7',
    border: '#F59E0B',
    traits: ['Wijs', 'Grappig', 'Betrouwbaar'],
    bio: 'Kapitein Bram is de stoere maar goedhartige schipper van de Blauwe Zeemeeuw. Hij heeft Windje als kuiken gevonden en hem alles geleerd over de zee. Hij draagt altijd zijn versleten gele regenjack, ook als het geen regen regent.',
  },
  {
    name: 'Siebert de Zeehond',
    role: 'Beste vriend',
    emoji: '🦭',
    color: '#D1FAE5',
    border: '#10B981',
    traits: ['Loyaal', 'Grappig', 'Sterk'],
    bio: 'Siebert is Windjes dikste vriend. Hij kan niet vliegen maar hij zwemt sneller dan elk schip. Hij is een beetje clumsy op het land maar in het water is hij een ster. Hij houdt van haring en slechte moppen — bij voorkeur tegelijk.',
  },
  {
    name: 'Marta de Zeemeermin',
    role: 'Verkenner van de diepte',
    emoji: '🧜‍♀️',
    color: '#EDE9FE',
    border: '#8B5CF6',
    traits: ['Slim', 'Vrolijk', 'Mysterieus'],
    bio: 'Niemand kent de zee beter dan Marta. Ze weet waar de schatten liggen, waar de gevaarlijke stromen zijn en waar de lekkerste zeewieren groeien. Ze spreekt 12 talen — ook de taal van de walvissen.',
  },
  {
    name: 'Kees de Krab',
    role: 'De onverwachte held',
    emoji: '🦀',
    color: '#FEE2E2',
    border: '#EF4444',
    traits: ['Eigenwijs', 'Vindingrijk', 'Hart van goud'],
    bio: 'Kees beweert altijd dat hij nergens mee te maken wil hebben. En toch is hij er altijd bij als het erop aankomt. Hij verzamelt glanzende dingen en heeft een holletje vol schatten onder de grote rots bij de pier.',
  },
  {
    name: 'De Blauwe Zeemeeuw',
    role: 'Het schip',
    emoji: '⛵',
    color: '#DBEAFE',
    border: '#2563EB',
    traits: ['Snel', 'Sterk', 'Oud'],
    bio: "De Blauwe Zeemeeuw is Kapitein Brams trouwe boot. Ze kraakt een beetje en lekt hier en daar, maar ze heeft honderd stormen doorstaan. 's Avonds als de wind stil is, lijkt het alsof ze verhalen fluistert.",
  },
];

function renderCharacters(el) {
  el.innerHTML = `
    <div class="page-header purple-header">
      <h1>Personages</h1>
      <p>Maak kennis met alle vrienden van Windje!</p>
    </div>
    <div class="chars-grid">
      ${CHARS.map(ch => `
        <div class="char-card" style="--ch-bg:${ch.color};--ch-border:${ch.border}">
          <div class="char-emoji">${ch.emoji}</div>
          <div class="char-role">${ch.role}</div>
          <h3>${ch.name}</h3>
          <div class="char-traits">
            ${ch.traits.map(t => `<span class="trait">${t}</span>`).join('')}
          </div>
          <p>${ch.bio}</p>
        </div>
      `).join('')}
    </div>
  `;
}

// ─── Boot ────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-link').forEach(l =>
    l.addEventListener('click', () => navigate(l.dataset.page))
  );
  navigate('home');
});
