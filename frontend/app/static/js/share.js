let popup = document.getElementById("popup")
// console.log(popupid);

function openPopup(){
    popup.classList.add("open-popup");
}

function closePopup(){
    popup.classList.remove(".open-popup");
}





// const openModalButtons = document.querySelectorAll('[data-modal-target]')
// const closeModalButtoms = document.querySelectorAll('[data-close-button]')
// const overlay = document.getElementsById('overlay')

// openModalButtons.forEach(button => {
//     button.addEventListener('click', () => {
//         const modal = document.querySelector(button.dataset.modalTarget)
//         openModal(modal)
//     })
// })

// overlay.addEventListener('click', () => {
//     const modals = document.querySelectorAll('.modal.active')
//     modal.forEach(modal => {
//         closeModal(modal)
//     })
// })

// closeModalButtons.forEach(button => {
//     button.addEventListener('click', () => {
//         const modal = document.closest('.modal')
//         closeModal(modal)
//     })
// })

// function openModal(modal) {
//     if (modal == null) return
//     modal.classList.add('active')
//     overlay.classList.add('active')
// }

// function closeModal(modal) {
//     if (modal == null) return
//     modal.classList.remove('active')
//     overlay.classList.remove('active')
// }