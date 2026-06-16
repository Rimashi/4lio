/* ================================================
   взаимодействие с книгой
   ================================================ */

$(function () {
  function openModal(id) {
    $(id).addClass("active");
    $("body").addClass("modal-open");
  }
  function closeModal(id) {
    $(id).removeClass("active");
    $("body").removeClass("modal-open");
  }

  $(document).on("click", ".modal__close, .modal__close-btn", function () {
    $(this).closest(".modal__background").removeClass("active");
    $("body").removeClass("modal-open");
  });
  $(document).on("click", ".modal__background", function (e) {
    if (e.target === this) {
      $(this).removeClass("active");
      $("body").removeClass("modal-open");
    }
  });
  $(document).on("keydown", function (e) {
    if (e.key === "Escape") {
      $(".modal__background.active").removeClass("active");
      $("body").removeClass("modal-open");
    }
  });

  // Удалить книгу — открываем модалку, сабмит формы внутри модалки
  $("#btnDeleteBook").on("click", function () {
    openModal("#deleteBookModal");
  });

  // Кнопка "Да, удалить" в модалке уже является submit'ом формы,
  // поэтому отдельный обработчик не нужен.

  // Добавить в подборку — открываем модалку
  $("#btnAddToCollection").on("click", function () {
    openModal("#addToCollectionModal");
  });
  // Форма внутри модалки сама отправляется на сервер.

  // Показать форму рецензии (если она была скрыта на странице)
  // Но у нас теперь рецензия пишется на отдельной странице (write_review),
  // поэтому эта функциональность не используется. Оставляем для совместимости.
  // Можно удалить.
});
