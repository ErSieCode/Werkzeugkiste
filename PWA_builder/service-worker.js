// ============================================
// SERVICE WORKER - Das Gehirn Ihrer PWA!
// ============================================
// Dieser Code läuft im Hintergrund, auch wenn die App geschlossen ist
// Er fängt ALLE Netzwerk-Anfragen ab und entscheidet was passiert

// ============================================
// SCHRITT 1: Cache-Namen definieren
// ============================================
// Versionierung ist WICHTIG! Bei jeder Änderung Version erhöhen
const CACHE_VERSION = 'v1';
const CACHE_NAME = `my-pwa-cache-${CACHE_VERSION}`;
const DATA_CACHE_NAME = `my-pwa-data-cache-${CACHE_VERSION}`;

// Was soll IMMER gecacht werden? (App Shell)
const STATIC_CACHE_URLS = [
  './',                    // Root
  './index.html',          // Hauptseite
  './manifest.json',       // Manifest
  './css/style.css',       // Styles
  './js/app.js',          // JavaScript
  './images/icon-192x192.png',  // Wichtige Icons
  './images/icon-512x512.png',
  // Offline-Fallback-Seite
  './offline.html'
];

// Welche Requests sollen NICHT gecacht werden?
const CACHE_BLACKLIST = [
  /analytics/,
  /google/,
  /facebook/,
  /stripe/  // Payment APIs niemals cachen!
];

// ============================================
// SCHRITT 2: INSTALL EVENT
// Wird NUR EINMAL ausgeführt, wenn SW installiert wird
// ============================================
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Install Event:', event);

  // Warte bis Installation fertig ist
  event.waitUntil(
    // Öffne Cache
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[ServiceWorker] Caching App Shell');

        // Füge alle URLs zum Cache hinzu
        // addAll() schlägt fehl wenn EINE URL nicht erreichbar ist!
        return cache.addAll(STATIC_CACHE_URLS);
      })
      .then(() => {
        console.log('[ServiceWorker] Install completed');

        // WICHTIG: skipWaiting() überspringt die Wartezeit
        // Normalerweise wartet ein neuer SW bis alle Tabs geschlossen sind
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[ServiceWorker] Install failed:', error);
      })
  );
});

// ============================================
// SCHRITT 3: ACTIVATE EVENT
// Wird ausgeführt wenn SW aktiviert wird
// Perfekt zum Aufräumen alter Caches!
// ============================================
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activate Event');

  // Liste der Caches die BEHALTEN werden sollen
  const cacheWhitelist = [CACHE_NAME, DATA_CACHE_NAME];

  event.waitUntil(
    // Hole alle Cache-Namen
    caches.keys()
      .then((cacheNames) => {
        // Lösche alle alten Caches
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (!cacheWhitelist.includes(cacheName)) {
              console.log('[ServiceWorker] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('[ServiceWorker] Claiming clients');

        // WICHTIG: clients.claim() übernimmt sofort alle offenen Tabs
        // Ohne das würde der alte SW weiter laufen bis Seite neu geladen wird
        return self.clients.claim();
      })
  );
});

// ============================================
// SCHRITT 4: FETCH EVENT - Das Herzstück!
// Wird bei JEDER Netzwerk-Anfrage ausgeführt
// ============================================
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  console.log('[ServiceWorker] Fetch:', request.url);

  // Ignoriere nicht-GET Requests
  if (request.method !== 'GET') {
    return;
  }

  // Prüfe Blacklist
  const isBlacklisted = CACHE_BLACKLIST.some(regex => regex.test(url.href));
  if (isBlacklisted) {
    console.log('[ServiceWorker] Blacklisted URL, skip caching');
    return;
  }

  // Unterscheide zwischen API-Calls und statischen Ressourcen
  if (url.pathname.startsWith('/api/')) {
    // API Calls: Network First, fallback auf Cache
    event.respondWith(networkFirstStrategy(request));
  } else {
    // Statische Ressourcen: Cache First, fallback auf Network
    event.respondWith(cacheFirstStrategy(request));
  }
});

// ============================================
// Cache-Strategien
// ============================================

// Strategie 1: Cache First (für statische Assets)
// Schnell, aber zeigt evtl. veraltete Inhalte
async function cacheFirstStrategy(request) {
  try {
    // Schaue zuerst im Cache
    const cachedResponse = await caches.match(request);

    if (cachedResponse) {
      console.log('[ServiceWorker] Found in cache:', request.url);

      // Aktualisiere Cache im Hintergrund (Stale While Revalidate)
      fetchAndCache(request);

      return cachedResponse;
    }

    // Nicht im Cache? Hole vom Netzwerk
    console.log('[ServiceWorker] Not in cache, fetching:', request.url);
    return await fetchAndCache(request);

  } catch (error) {
    console.error('[ServiceWorker] Fetch failed:', error);

    // Letzter Ausweg: Offline-Seite
    return await caches.match('./offline.html');
  }
}

// Strategie 2: Network First (für API/dynamische Inhalte)
// Immer frische Daten, aber langsamer
async function networkFirstStrategy(request) {
  try {
    // Versuche vom Netzwerk zu holen (mit Timeout!)
    const networkResponse = await fetchWithTimeout(request, 5000);

    // Erfolg? Cache es für später
    if (networkResponse && networkResponse.status === 200) {
      const cache = await caches.open(DATA_CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;

  } catch (error) {
    console.log('[ServiceWorker] Network failed, trying cache:', error);

    // Netzwerk failed? Versuche Cache
    const cachedResponse = await caches.match(request);

    if (cachedResponse) {
      console.log('[ServiceWorker] Found in cache:', request.url);
      return cachedResponse;
    }

    // Auch kein Cache? Fehler zurückgeben
    return new Response(
      JSON.stringify({ error: 'Offline' }),
      {
        status: 503,
        statusText: 'Service Unavailable',
        headers: new Headers({ 'Content-Type': 'application/json' })
      }
    );
  }
}

// Hilfsfunktion: Fetch mit Timeout
function fetchWithTimeout(request, timeout = 5000) {
  return Promise.race([
    fetch(request),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), timeout)
    )
  ]);
}

// Hilfsfunktion: Fetch und Cache
async function fetchAndCache(request) {
  const networkResponse = await fetch(request);

  // Nur erfolgreiche Responses cachen
  if (networkResponse && networkResponse.status === 200) {
    const cache = await caches.open(CACHE_NAME);
    cache.put(request, networkResponse.clone());
  }

  return networkResponse;
}

// ============================================
// SCHRITT 5: PUSH NOTIFICATIONS
// ============================================
self.addEventListener('push', (event) => {
  console.log('[ServiceWorker] Push received');

  let title = 'Neue Benachrichtigung';
  let options = {
    body: 'Sie haben eine neue Nachricht!',
    icon: './images/icon-192x192.png',
    badge: './images/badge-72x72.png',
    vibrate: [200, 100, 200], // Vibrationsmuster
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Öffnen',
        icon: './images/checkmark.png'
      },
      {
        action: 'close',
        title: 'Schließen',
        icon: './images/xmark.png'
      }
    ]
  };

  // Wenn Push-Daten vorhanden sind
  if (event.data) {
    const data = event.data.json();
    title = data.title || title;
    options.body = data.body || options.body;
  }

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification Click Handler
self.addEventListener('notificationclick', (event) => {
  console.log('[ServiceWorker] Notification click:', event.action);

  event.notification.close();

  if (event.action === 'explore') {
    // Öffne App
    event.waitUntil(
      clients.openWindow('/')
    );
  }
  // 'close' action = nur schließen
});

// ============================================
// SCHRITT 6: BACKGROUND SYNC (Offline-Aktionen)
// ============================================
self.addEventListener('sync', (event) => {
  console.log('[ServiceWorker] Background sync:', event.tag);

  if (event.tag === 'sync-data') {
    event.waitUntil(syncData());
  }
});

async function syncData() {
  try {
    // Hole gespeicherte offline Daten
    const cache = await caches.open('offline-data');
    const requests = await cache.keys();

    // Sende alle gespeicherten Requests
    for (const request of requests) {
      try {
        const response = await fetch(request.clone());

        if (response.ok) {
          // Erfolgreich? Lösche aus offline Cache
          await cache.delete(request);
        }
      } catch (error) {
        console.error('[ServiceWorker] Sync failed for:', request.url);
      }
    }
  } catch (error) {
    console.error('[ServiceWorker] Sync error:', error);
  }
}

// ============================================
// SCHRITT 7: MESSAGE HANDLING
// Kommunikation zwischen App und Service Worker
// ============================================
self.addEventListener('message', (event) => {
  console.log('[ServiceWorker] Message received:', event.data);

  if (event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then(cacheNames =>
        Promise.all(cacheNames.map(cache => caches.delete(cache)))
      )
    );
  }

  if (event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(CACHE_NAME).then(cache =>
        cache.addAll(event.data.urls)
      )
    );
  }
});

// ============================================
// BONUS: Performance Monitoring
// ============================================
self.addEventListener('fetch', (event) => {
  const startTime = performance.now();

  event.waitUntil(
    event.respondWith(
      fetch(event.request).then(response => {
        const endTime = performance.now();
        const duration = endTime - startTime;

        // Log langsame Requests
        if (duration > 1000) {
          console.warn(`[ServiceWorker] Slow request: ${event.request.url} took ${duration}ms`);
        }

        return response;
      })
    )
  );
});

// ============================================
// ERROR HANDLING
// ============================================
self.addEventListener('error', (error) => {
  console.error('[ServiceWorker] Error:', error);
});

self.addEventListener('unhandledrejection', (event) => {
  console.error('[ServiceWorker] Unhandled rejection:', event.reason);
});

// ============================================
// Utility Functions
// ============================================

// Prüfe ob Request cachebar ist
function isRequestCacheable(request) {
  const url = new URL(request.url);

  // Nur HTTPS oder localhost
  if (url.protocol !== 'https:' && url.hostname !== 'localhost') {
    return false;
  }

  // Nur GET requests
  if (request.method !== 'GET') {
    return false;
  }

  // Keine Auth/Session URLs
  if (url.pathname.includes('/auth/') || url.pathname.includes('/session/')) {
    return false;
  }

  return true;
}

// Cache Größe überwachen
async function getCacheSize() {
  const cacheNames = await caches.keys();
  let totalSize = 0;

  for (const name of cacheNames) {
    const cache = await caches.open(name);
    const requests = await cache.keys();

    for (const request of requests) {
      const response = await cache.match(request);
      if (response) {
        const blob = await response.blob();
        totalSize += blob.size;
      }
    }
  }

  return totalSize;
}

// Alte Cache Einträge löschen
async function cleanupCache(maxAgeMs = 7 * 24 * 60 * 60 * 1000) { // 7 Tage
  const cache = await caches.open(CACHE_NAME);
  const requests = await cache.keys();
  const now = Date.now();

  for (const request of requests) {
    const response = await cache.match(request);
    if (response) {
      const dateHeader = response.headers.get('date');
      if (dateHeader) {
        const responseDate = new Date(dateHeader).getTime();
        if (now - responseDate > maxAgeMs) {
          console.log('[ServiceWorker] Deleting old cache entry:', request.url);
          await cache.delete(request);
        }
      }
    }
  }
}