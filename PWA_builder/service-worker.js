// Inhalt aus der Variable "serviceWorkerCode" hier einfügen
const CACHE_NAME = 'pwa-guide-v1';
const API_CACHE = 'pwa-guide-api-v1';
const urlsToCache = [
    './',
    './index.html',
    './manifest.json',
    // Fügen Sie hier alle wichtigen Dateien hinzu
];

// Install Event
self.addEventListener('install', event => {
    console.log('[Service Worker] Installing...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[Service Worker] Caching app shell');
                return cache.addAll(urlsToCache);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate Event
self.addEventListener('activate', event => {
    console.log('[Service Worker] Activating...');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME && cacheName !== API_CACHE) {
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch Event
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response; // Aus dem Cache liefern
                }
                return fetch(event.request).then(networkResponse => {
                    // Gültige Antwort klonen und cachen
                    if (networkResponse && networkResponse.ok) {
                        const responseToCache = networkResponse.clone();
                        caches.open(CACHE_NAME).then(cache => {
                            cache.put(event.request, responseToCache);
                        });
                    }
                    return networkResponse;
                });
            }).catch(() => {
                // Offline Fallback
                return caches.match('./index.html');
            })
    );
});
