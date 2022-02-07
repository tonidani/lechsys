
// Register Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker
    .register('/service-worker.js')
    .then(function(registration) {

        return registration;
    })
    .catch(function(err) {

    });
}




let deferredPrompt;
const addBtn = document.querySelector('.add-button');
addBtn.style.display = 'none';



window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  addBtn.style.display = 'block';
  addBtn.addEventListener('click', (e) => {
    addBtn.style.display = 'none';
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {





        } else {



        }
        deferredPrompt = null;
      });
  });
});




window.addEventListener('online', function(e) {

}, false);


/*
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js').then(function(reg) {
    console.log('Service Worker Registered!', reg);

    askPermission()

    reg.pushManager.getSubscription().then(function(sub) {
      if (sub === null) {
        // Update UI to ask user to register for Push
        console.log('Not subscribed to push service!');
      } else {
        // We have a subscription, update the database
        console.log('Subscription object: ', sub);
      }
    });
  })
   .catch(function(err) {
    console.log('Service Worker registration failed: ', err);
  });
}

function subscribeUser() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready.then(function(reg) {

      reg.pushManager.subscribe({
        userVisibleOnly: true
      }).then(function(sub) {
        sendSubscriptionToBackEnd(sub)
      }).catch(function(e) {
        if (Notification.permission === 'denied') {
          console.warn('Permission for notifications was denied');
        } else {
          console.error('Unable to subscribe to push', e);
        }
      });
    })
  }
}



*/


"use strict";

const applicationServerPublicKey = 'BKqORuQMaGt4olIU-LEMquWWbowTq2_vmNd5mUp4R-YZz5NERsqooI2jNxt3XYVP2fUgkd-modY32sHcpcZDPR4';

"Authorization: vapid t=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJhdWQiOiJodHRwczovL3M0NDQ0NzEucHJvamVrdHN0dWRlbmNraS5wbCIsImV4cCI6IjE2NDEzODM2MDQiLCJzdWIiOiJtYWlsdG86bGVjaHN5c2JvdEBnbWFpbC5jb20ifQ.NdiZL5DZouqknoPMZLdVSGS9m6yhxyKL8nZWsU2KK9JPQGO8CBd60M_JfggeXWYqR7yua2JsN9Q-hSnSMYIO-g,k=BKqORuQMaGt4olIU-LEMquWWbowTq2_vmNd5mUp4R-YZz5NERsqooI2jNxt3XYVP2fUgkd-modY32sHcpcZDPR4";



const pushButton = document.querySelector('#pushBtn');
    let swRegistration = null;
let isSubscribed = false;
if ("serviceWorker" in navigator && "PushManager" in window) {


    navigator.serviceWorker.register("/service-worker.js").then(function (swReg) {



            swRegistration = swReg;
            initializeUI();
        })
        .catch(function (error) {

        });
} else {

    pushButton.textContent = "Push Not Supported";
}

function initializeUI() {
    if (pushButton != null){
    pushButton.addEventListener("click", function () {
        pushButton.disabled = true;
        if (isSubscribed) {

            unsubscribeUser();
        } else {
            subscribeUser();
        }
    });

    // Set the initial subscription value
    swRegistration.pushManager.getSubscription().then(function (subscription) {
        isSubscribed = !(subscription === null);

        updateSubscriptionOnServer(subscription);

        if (isSubscribed) {

        } else {

        }

        updateBtn();
    });
}
 }

function subscribeUser() {
    const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
    swRegistration.pushManager
        .subscribe({
            userVisibleOnly: true,
            applicationServerKey: applicationServerKey,
        })
        .then(function (subscription) {


            updateSubscriptionOnServer(subscription);

            isSubscribed = true;

            updateBtn();
        })
        .catch(function (err) {

            updateBtn();
        });
}

function unsubscribeUser() {
    swRegistration.pushManager
        .getSubscription()
        .then(function (subscription) {
            if (subscription) {
                fetch('/api/unsubscribe').then(function(response) {
                    if (!response.ok) {

                      throw new Error('Bad status code from server.');
                    }
                })

                return subscription.unsubscribe();
            }
        })
        .catch(function (error) {

        })
        .then(function () {
            updateSubscriptionOnServer(null);


            isSubscribed = false;

            updateBtn();
        });
}

function updateSubscriptionOnServer(subscription) {

    if (subscription) {


        sendSubscriptionToBackEnd(subscription)
    }
    /*
    else {
        subscriptionDetails.classList.add("is-invisible");
    }
    */
}

function updateBtn() {
    if (Notification.permission === "denied") {
        pushButton.textContent = "Push Messaging Blocked.";
        pushButton.disabled = true;
        updateSubscriptionOnServer(null);
        return;
    }

    if (isSubscribed) {
        pushButton.textContent = "Disable Push Messaging";
    } else {
        pushButton.textContent = "Enable Push Messaging";
    }

    pushButton.disabled = false;
}

function urlB64ToUint8Array(base64String) {
    const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, "+")
        .replace(/_/g, "/");

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}


function sendSubscriptionToBackEnd(subscription) {
  return fetch('/api/subscribe', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'vapid t=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJhdWQiOiJodHRwczovL3M0NDQ0NzEucHJvamVrdHN0dWRlbmNraS5wbCIsImV4cCI6IjE2NDEzODM2MDQiLCJzdWIiOiJtYWlsdG86bGVjaHN5c2JvdEBnbWFpbC5jb20ifQ.NdiZL5DZouqknoPMZLdVSGS9m6yhxyKL8nZWsU2KK9JPQGO8CBd60M_JfggeXWYqR7yua2JsN9Q-hSnSMYIO-g,k=BKqORuQMaGt4olIU-LEMquWWbowTq2_vmNd5mUp4R-YZz5NERsqooI2jNxt3XYVP2fUgkd-modY32sHcpcZDPR4'
    },
    body: JSON.stringify({
        subscription_info: JSON.stringify(subscription),
    }),
  })
  .then(function(response) {
    if (!response.ok) {

      throw new Error('Bad status code from server.');
    }

    return response.json();
  })
  .then(function(responseData) {
    if (!(responseData.data && responseData.data.success)) {

      //throw new Error('Bad response from server.');
    }
  });
}


function askPermission() {
  return new Promise(function(resolve, reject) {
    const permissionResult = Notification.requestPermission(function(result) {
      resolve(result);
    });

    if (permissionResult) {
      permissionResult.then(resolve, reject);

    }
  })
  .then(function(permissionResult) {
    if (permissionResult !== 'granted') {
      throw new Error('We weren\'t granted permission.');
    }
    else{
        subscribeUser()
    }
  });
}

