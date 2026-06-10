function modal() {
  const overlay = document.getElementById('cartOverlay')
  if (overlay) {
    overlay.classList.toggle('cart-overlay--open')
    document.body.classList.toggle('cart-open')
    return
  }
  const panel = document.querySelector('.modal.cart-panel') || document.querySelector('.modal')
  if (panel) {
    const wrap = panel.closest('.cart-overlay')
    if (wrap) {
      wrap.classList.toggle('cart-overlay--open')
      document.body.classList.toggle('cart-open')
      return
    }
    panel.classList.toggle('modalShow')
  }
}

window.modal = modal

function clearCartRow() {
  const row = document.querySelector('.cart-panel .row') || document.querySelector('.modal .row')
  if (row) row.classList.toggle('clear')
}

const menuBtn = document.querySelector('button.main')
if (menuBtn) {
  menuBtn.addEventListener('click', () => {
    const span = menuBtn.querySelector('span')
    const menu = document.querySelector('.main__menu')
    if (span) span.classList.toggle('show')
    if (menu) menu.classList.toggle('show')
    menuBtn.classList.toggle('show')
  })
}

const mobFiltBtn = document.querySelector('.mobFilt')
if (mobFiltBtn) {
  mobFiltBtn.addEventListener('click', () => {
    const filter = document.querySelector('.content .filter')
    if (filter) {
      filter.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
      const firstBtn = filter.querySelector('button')
      if (firstBtn) firstBtn.focus()
    }
  })
}

let filtbtn = document.querySelectorAll('.filter button')
let row = document.querySelectorAll('.slide .row')
let title = document.querySelectorAll('.slide .big__title')
let sbtn = document.querySelectorAll('.slide__btn')

filtbtn.forEach((i) => {
  i.addEventListener('click', () => {
    const activeBtn = document.querySelector('.filter button.active')
    if (activeBtn) activeBtn.classList.remove('active')
    i.classList.add('active')
    const link = i.getAttribute('data-id')

    row.forEach((rows) => {
      if (link === 'all') {
        rows.style.display = 'flex'
      } else if (rows.classList.contains(link)) {
        rows.style.display = 'flex'
      } else {
        rows.style.display = 'none'
      }
    })
    title.forEach((t) => {
      if (link === 'all') {
        t.style.display = 'block'
      } else if (t.classList.contains(link)) {
        t.style.display = 'block'
      } else {
        t.style.display = 'none'
      }
    })
    if (window.innerWidth <= 766) {
      sbtn.forEach((sb) => {
        if (link === 'all') {
          sb.style.display = 'block'
        } else if (sb.classList.contains(link)) {
          sb.style.display = 'block'
        } else {
          sb.style.display = 'none'
        }
      })
    }
  })
})

sbtn.forEach((btn) => {
  btn.addEventListener('click', () => {
    const b = btn.getAttribute('data-id')
    row.forEach((rows) => {
      if (rows.classList.contains(b)) {
        rows.classList.toggle('open')
      }
    })
  })
})

let mobBtn = document.querySelector('.mob__menu--btn')
let mobBtnAdd = document.querySelector('.mob__menu--btn.add')
if (mobBtn) {
  mobBtn.addEventListener('click', () => {
    const ul = document.querySelector('ul.point')
    if (ul) ul.classList.toggle('ulList')
  })
}
if (mobBtnAdd) {
  mobBtnAdd.addEventListener('click', () => {
    const ul = document.querySelector('ul.addition')
    if (ul) ul.classList.toggle('ulList')
  })
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const overlay = document.getElementById('cartOverlay')
    if (overlay && overlay.classList.contains('cart-overlay--open')) {
      overlay.classList.remove('cart-overlay--open')
      document.body.classList.remove('cart-open')
    }
  }
})
