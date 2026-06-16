/* ================================================
   Тема, бургер, flash, модалки
   ================================================ */

document.addEventListener("DOMContentLoaded", function () {
  // ===== THEME SWITCHER =====
  class ThemeSwitcher {
    constructor(selector = "#themeToggle") {
      this.el = document.querySelector(selector);
      this.key = "folio-theme";
      this._apply(localStorage.getItem(this.key) || "light");
      if (this.el) this.el.addEventListener("click", () => this.toggle());
    }
    _apply(theme) {
      if (theme === "dark") document.body.classList.add("dark-theme");
      else document.body.classList.remove("dark-theme");
      this._updateIcon();
    }
    _updateIcon() {
      if (!this.el) return;
      const isDark = document.body.classList.contains("dark-theme");
      this.el.setAttribute(
        "aria-label",
        isDark ? "Светлая тема" : "Тёмная тема",
      );
      this.el.innerHTML = isDark
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    }
    toggle() {
      const isDark = document.body.classList.toggle("dark-theme");
      localStorage.setItem(this.key, isDark ? "dark" : "light");
      this._updateIcon();
    }
  }
  window.themeSwitcher = new ThemeSwitcher();

  // ===== BURGER MENU =====
  const menuIcon = document.querySelector(".menu__icon");
  const menu = document.querySelector(".header__menu");
  const menuOverlay = document.getElementById("menu_overlay");

  function toggleMenu() {
    if (!menuIcon || !menu || !menuOverlay) return;
    const isOpen = menu.classList.toggle("active");
    menuIcon.classList.toggle("active", isOpen);
    menuOverlay.classList.toggle("active", isOpen);
    document.body.classList.toggle("menu-open", isOpen);
  }

  if (menuIcon)
    menuIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleMenu();
    });
  if (menuOverlay) menuOverlay.addEventListener("click", toggleMenu);
  document.querySelectorAll(".menu__list a").forEach((link) => {
    link.addEventListener("click", () => {
      if (menu && menu.classList.contains("active")) toggleMenu();
    });
  });
  window.addEventListener("resize", () => {
    if (window.innerWidth > 768 && menu && menu.classList.contains("active"))
      toggleMenu();
  });

  // ===== FLASH MESSAGES =====
  function autoCloseFlash() {
    document.querySelectorAll(".flash").forEach((flash) => {
      flash.addEventListener("click", () => {
        flash.style.animation = "flashOut 0.2s ease forwards";
        setTimeout(() => flash.remove(), 200);
      });
      setTimeout(() => {
        if (flash.parentNode) {
          flash.style.animation = "flashOut 0.3s ease forwards";
          setTimeout(() => flash.remove(), 300);
        }
      }, 4000);
    });
  }
  const style = document.createElement("style");
  style.textContent = `
    @keyframes flashOut {
      from { opacity: 1; transform: translateX(0); }
      to   { opacity: 0; transform: translateX(20px); }
    }
  `;
  document.head.appendChild(style);
  autoCloseFlash();

  // ===== MODALS =====
  let modalStack = [];
  function getActiveModal() {
    return document.querySelector(".modal__background.active");
  }

  window.openModal = function (name, data = {}) {
    if (!window.modals || !window.modals[name]) {
      console.error("Modal not found:", name);
      return;
    }
    const current = getActiveModal();
    if (current) {
      modalStack.push({ name: current.dataset.modal, html: current.outerHTML });
      current.remove();
    }
    const temp = document.createElement("div");
    temp.innerHTML = window.modals[name](data);
    const modal = temp.firstElementChild;
    modal.dataset.modal = name;
    document.body.appendChild(modal);
    requestAnimationFrame(() => modal.classList.add("active"));
    document.body.classList.add("modal-open");
    modal
      .querySelector(".modal__close")
      ?.addEventListener("click", window.closeModal);
    modal.addEventListener("click", (e) => {
      if (e.target === modal) window.closeModal();
    });
    document.addEventListener("keydown", _escHandler);
  };

  function _escHandler(e) {
    if (e.key === "Escape") window.closeModal();
  }

  window.closeModal = function () {
    const active = getActiveModal();
    if (active) active.remove();
    const prev = modalStack.pop();
    if (prev) {
      const temp = document.createElement("div");
      temp.innerHTML = prev.html;
      const modal = temp.firstElementChild;
      document.body.appendChild(modal);
    } else {
      document.body.classList.remove("modal-open");
      document.removeEventListener("keydown", _escHandler);
    }
  };

  document.addEventListener("click", (e) => {
    const opener = e.target.closest("[data-modal-open]");
    if (opener) {
      e.preventDefault();
      const name = opener.dataset.modalOpen;
      const data = opener.dataset;
      window.openModal(name, data);
    }
    const closer = e.target.closest("[data-modal-close]");
    if (closer) {
      e.preventDefault();
      window.closeModal();
    }
  });

  // ===== ГЛОБАЛЬНЫЕ УТИЛИТЫ =====
  window.folio = {
    ucfirst: (str) => (str ? str.charAt(0).toUpperCase() + str.slice(1) : ""),
    renderStars: (rating, max = 5) => {
      let html = '<span class="stars">';
      for (let i = 1; i <= max; i++) {
        html += `<span class="${i <= rating ? "" : "empty"}">★</span>`;
      }
      return html + "</span>";
    },
    plural: (n, forms) => {
      const mod10 = n % 10,
        mod100 = n % 100;
      if (mod10 === 1 && mod100 !== 11) return forms[0];
      if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20))
        return forms[1];
      return forms[2];
    },
  };
});
