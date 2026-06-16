/* ================================================
   история просмотров
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

  $("#btnClearHistory").on("click", function () {
    openModal("#clearHistoryModal");
  });

  // Форма внутри модалки сама отправляется на сервер.
});
