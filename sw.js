// A.U.R.A Service Worker for Progressive Web App
const CACHE_NAME = 'aura-v1.0.0';
const STATIC_CACHE = 'aura-static-v1.0.0';
const DYNAMIC_CACHE = 'aura-dynamic-v1.0.0';

// Files to cache for offline functionality
const STATIC_FILES = [
  '/',
  '/manifest.json',
  '/static/css/',
  '/static/js/',
  '/favicon.ico'
];

// API endpoints to cache
const API_CACHE_PATTERNS = [
  '/gradio_api/',
  '/api/',
  '/static/'
];

// Install event - cache static files
self.addEventListener('install', (event) => {
  console.log('A.U.R.A Service Worker installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('Caching static files...');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('A.U.R.A Service Worker installed successfully');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('Service Worker installation failed:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('A.U.R.A Service Worker activating...');
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log('Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('A.U.R.A Service Worker activated');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Handle different types of requests
  if (url.pathname === '/' || url.pathname.startsWith('/gradio_api/')) {
    // Handle main app and API requests
    event.respondWith(
      caches.match(request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            console.log('Serving from cache:', request.url);
            return cachedResponse;
          }

          return fetch(request)
            .then((response) => {
              // Cache successful responses
              if (response.status === 200) {
                const responseClone = response.clone();
                caches.open(DYNAMIC_CACHE)
                  .then((cache) => {
                    cache.put(request, responseClone);
                  });
              }
              return response;
            })
            .catch(() => {
              // Return offline page for navigation requests
              if (request.mode === 'navigate') {
                return caches.match('/') || new Response(
                  `
                  <!DOCTYPE html>
                  <html>
                    <head>
                      <title>A.U.R.A - Offline</title>
                      <meta name="viewport" content="width=device-width, initial-scale=1">
                      <style>
                        body { 
                          font-family: 'Inter', sans-serif; 
                          background: linear-gradient(135deg, #F9F9F9 0%, #A7A7A7 30%, #646464 70%, #333333 100%);
                          color: #333333;
                          text-align: center;
                          padding: 50px;
                        }
                        .offline-container {
                          background: rgba(255, 255, 255, 0.95);
                          border-radius: 16px;
                          padding: 40px;
                          max-width: 500px;
                          margin: 0 auto;
                          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                        }
                        h1 { color: #E85002; }
                        .icon { font-size: 48px; margin-bottom: 20px; }
                      </style>
                    </head>
                    <body>
                      <div class="offline-container">
                        <div class="icon">🤖</div>
                        <h1>A.U.R.A - Offline</h1>
                        <p>You're currently offline. Some features may not be available.</p>
                        <p>Please check your internet connection and try again.</p>
                      </div>
                    </body>
                  </html>
                  `,
                  { headers: { 'Content-Type': 'text/html' } }
                );
              }
            });
        })
    );
  } else if (url.pathname.startsWith('/static/')) {
    // Handle static assets
    event.respondWith(
      caches.match(request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          return fetch(request);
        })
    );
  }
});

// Background sync for data processing
self.addEventListener('sync', (event) => {
  if (event.tag === 'aura-data-sync') {
    console.log('A.U.R.A background sync triggered');
    event.waitUntil(
      // Handle background data synchronization
      syncAuraData()
    );
  }
});

// Push notifications for A.U.R.A alerts
self.addEventListener('push', (event) => {
  console.log('A.U.R.A push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'A.U.R.A has new insights for you!',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 'aura-notification'
    },
    actions: [
      {
        action: 'open',
        title: 'Open A.U.R.A',
        icon: '/icons/icon-96x96.png'
      },
      {
        action: 'dismiss',
        title: 'Dismiss',
        icon: '/icons/icon-96x96.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('A.U.R.A Alert', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('A.U.R.A notification clicked');
  
  event.notification.close();

  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Helper function for background sync
async function syncAuraData() {
  try {
    console.log('Syncing A.U.R.A data in background...');
    // Implement background data synchronization logic here
    return Promise.resolve();
  } catch (error) {
    console.error('A.U.R.A background sync failed:', error);
    return Promise.reject(error);
  }
}
