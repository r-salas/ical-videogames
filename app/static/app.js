/*
*
*   App
*
*/


function updateCalendarUrl() {
    const copyBtn = document.getElementById("copy-btn")
    const calendarLink = document.getElementById("calendar-link")
    const calendarForm = document.getElementById("calendar-form")

    const formData = new FormData(calendarForm)

    const region = formData.get("region")
    const platforms = formData.getAll("platform")
    const host = window.location.protocol + "//" + window.location.host

    if (!platforms.length) {
        calendarLink.value = ""
        copyBtn.disabled = true
    } else {
        let queryStringList = platforms.map(platform => "platform=" + platform)
        queryStringList.push("region=" + region)

        copyBtn.disabled = false
        calendarLink.value = host + "/calendar?" + queryStringList.join("&")
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const clipboard = new ClipboardJS("#copy-btn")
    const calendarForm = document.getElementById("calendar-form")

    updateCalendarUrl()

    calendarForm.addEventListener('change', function() {
        updateCalendarUrl()
    })
}, false)
