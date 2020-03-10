/* globals fetch */

let currentTimerId

function q (selector) {
  return document.querySelector(selector)
}

function padZero (n) {
  return String(n).padStart(2, '0')
}

function updateTimer (timerStart) {
  const currentTime = new Date()
  const millis = currentTime - timerStart
  const hours = Math.floor(millis / 1000 / 60 / 60)
  const minutes = Math.floor(millis / 1000 / 60) % 60
  const seconds = Math.floor(millis / 1000) % 60
  q('#hours').textContent = padZero(hours)
  q('#minutes').textContent = padZero(minutes)
  q('#seconds').textContent = padZero(seconds)
  currentTimerId = setTimeout(() => updateTimer(timerStart), 1000)
}

function main () {
  checkForRunningTimer()
  setUpTimerForm()
  setUpStopButton()
}

function checkForRunningTimer () {
  fetch('/timer/')
    .then(res => res.json())
    .then(json => {
      if (json.status === 'ok' && json.data) {
        startTimer(json.data.started_at, json.data.client_name)
      } else {
        showTimerForm()
      }
    })
}

function showTimerForm () {
  q('#timer-not-running').classList.remove('dn')
  q('#timer-running').classList.add('dn')
}

function setUpTimerForm () {
  const form = q('#timer-form')
  form.addEventListener('submit', function (event) {
    event.preventDefault()

    fetch('/timer/start/', {
      method: 'POST',
      body: JSON.stringify({ clientId: q('#client').value })
    })
      .then(res => res.json())
      .then(json => {
        if (json.status === 'ok') {
          startTimer(json.data.started_at, json.data.client_name)
        }
      })
  })
}

function setUpStopButton () {
  const button = q('#stop-timer-button')
  button.addEventListener('click', (event) => {
    event.preventDefault()
    fetch('/timer/stop/', { method: 'POST' })
      .then(res => res.json())
      .then(json => {
        if (json.status === 'ok') {
          stopTimer()
          showTimerForm()
        }
      })
  })
}

function startTimer (startedAt, clientName) {
  // hide the not-running timer
  q('#timer-not-running').classList.add('dn')
  // show the running timer
  q('#timer-running').classList.remove('dn')
  // update the h, m, s
  updateTimer(new Date(startedAt))
  // update the client name
  q('#client-name').textContent = clientName
}

function stopTimer () {
  clearTimeout(currentTimerId)
}

document.addEventListener('DOMContentLoaded', function () {
  main()
})
