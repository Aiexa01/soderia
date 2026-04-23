const CACHE_NAME = 'soderia-mobile-v1';
const ASSETS = [
  '/m/',
  '/static/css/mobile.css',
  '/static/images/icon-192.png',
  '/static/images/icon-512.png',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (e) => {
  // Only intercept /m/ routes and static assets
  if (e.request.url.includes('/m/') || e.request.url.includes('/static/')) {
    e.respondWith(
      fetch(e.request).catch(() => caches.match(e.request))
    );
  }
});
