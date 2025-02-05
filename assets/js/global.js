console.log("Global.js connected")

document.addEventListener("DOMContentLoaded", function(){
    let GOOGLE_LINK = document.querySelector('a[title="Google"]')
    if (GOOGLE_LINK){
        GOOGLE_LINK.textContent = ''
        const img = document.createElement('img')
        img.classList.add('google-login-img')
        img.src = '/assets/logo/google.png'
        img.alt = 'Google Login'
        GOOGLE_LINK.appendChild(img)
    }
})